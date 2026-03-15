# GraphRAG-Example 核心架构分析

> 项目地址: https://github.com/YiTangMJ/GraphRAG-Example
> 分析日期: 2026-03-13

## 项目概述

这是一个基于 **知识图谱 + 文档检索** 的 RAG 系统，使用 Vue 3 + Express 构建。

---

## 核心 RAG 实现流程

```
用户提问 → 关键词提取 → 双路检索 → 上下文构建 → LLM 回答
```

### 1. 关键词提取 (`textTokenizer.js`)

```javascript
// 中文：bigram 分词
// 英文：单词提取 + 停用词过滤
export function extractKeywords(text) {
  const tokens = tokenize(text)
  const filtered = tokens.filter(t => !CN_STOP_WORDS.has(t))
  return [...new Set(filtered)]  // 去重
}
```

**分词策略**：
- 中文：使用 bigram（双字分词），如 "知识图谱" → ["知识", "识图", "图谱"]
- 英文：提取单词，过滤停用词（the, a, is, etc.）
- 去重并保持顺序

### 2. 双路检索 (`ragRetriever.js`)

**主路：文档内容检索**
```javascript
// 通过关键词搜索导入的原始文档
fileResults = await searchFiles(graphId, keywords)
```

**辅路：图谱结构检索**
```javascript
// 1. 找到种子节点（关键词匹配实体标签/属性）
seedIds = findSeedNodes(graphStore, keywords)

// 2. BFS 扩展获取子图
subgraph = graphStore.bfsSubgraph(seedIds, bfsDepth, bfsMaxNodes)
```

**种子节点查找算法** (`graphService.js`):
```javascript
export function findSeedNodes(graphStore, keywords, maxSeeds = 10) {
  const scored = new Map()

  for (const keyword of keywords) {
    const lower = keyword.toLowerCase()
    for (const node of graphStore.nodes.values()) {
      const labelLower = node.label.toLowerCase()
      let score = scored.get(node.id) || 0

      // 完全匹配得分最高
      if (labelLower === lower) score += 10
      // 部分匹配次之
      else if (labelLower.includes(lower) || lower.includes(labelLower)) score += 5

      // 属性匹配
      for (const val of Object.values(node.properties)) {
        if (String(val).toLowerCase().includes(lower)) score += 2
      }

      if (score > 0) scored.set(node.id, score)
    }
  }

  // 按分数排序，返回前 maxSeeds 个
  return Array.from(scored.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, maxSeeds)
    .map(([id]) => id)
}
```

**BFS 子图提取** (`graphStore.js`):
```javascript
function bfsSubgraph(seedNodeIds, maxDepth = 2, maxNodes = 50) {
  const visited = new Set()
  const subEdges = new Set()
  let frontier = [...seedNodeIds]

  for (let depth = 0; depth <= maxDepth && frontier.length > 0; depth++) {
    const nextFrontier = []
    for (const nid of frontier) {
      if (visited.has(nid) || visited.size >= maxNodes) continue
      visited.add(nid)
      
      const adj = adjacency.value.get(nid)
      if (!adj) continue
      
      for (const eid of adj) {
        subEdges.add(eid)
        const edge = edges.value.get(eid)
        if (!edge) continue
        
        const neighbor = edge.source === nid ? edge.target : edge.source
        if (!visited.has(neighbor)) {
          nextFrontier.push(neighbor)
        }
      }
    }
    frontier = nextFrontier
  }

  // 返回子图节点和边
  return { nodes: subNodes, edges: subEdgeList }
}
```

### 3. 上下文构建

```javascript
function formatCombinedContext(fileResults, subgraph) {
  const lines = []

  // ── 文档内容（主要依据）────────────────────────────
  if (fileResults.length > 0) {
    lines.push('=== 原始文档内容（主要参考依据）===')
    for (const file of fileResults) {
      lines.push(`【文件: ${file.fileName}】`)
      if (file.fullContent) {
        lines.push(file.fullContent.trim())
      } else {
        for (const snippet of (file.snippets || [])) {
          lines.push(snippet.trim())
          lines.push('...')
        }
      }
    }
  }

  // ── 图谱结构（辅助参考）────────────────────────────
  if (subgraph.nodes.length > 0) {
    lines.push('=== 知识图谱结构（辅助参考）===')
    lines.push('【实体】')
    for (const node of subgraph.nodes) {
      let desc = `- ${node.label}`
      if (node.type && node.type !== 'entity') {
        desc += ` (${node.type})`
      }
      lines.push(desc)
    }

    if (subgraph.edges.length > 0) {
      lines.push('【关系】')
      for (const edge of subgraph.edges) {
        lines.push(`- ${src} --[${rel}]--> ${tgt}`)
      }
    }
  }

  return lines.join('\n')
}
```

### 4. LLM 调用 (`llmApiService.js`)

```javascript
export function buildRAGMessages(contextText, userQuery) {
  return [
    {
      role: 'system',
      content: `你是一个智能文档问答助手。请根据提供的参考资料回答用户的问题。

回答规则：
1. 以"原始文档内容"为核心依据，优先引用文档中的原文进行回答
2. "知识图谱结构"仅作为辅助参考，帮助理解实体之间的关系
3. 回答应准确、详细，尽量基于文档原文，可以适当引用关键语句
4. 如果文档中没有相关信息，请诚实说明

${contextText}`
    },
    {
      role: 'user',
      content: userQuery
    }
  ]
}
```

---

## 知识图谱构建

### LLM 实体关系提取 (`llmExtractor.js`)

```javascript
export async function extractWithLLM(text, settings) {
  const systemPrompt = `你是一个知识图谱构建专家。请从以下文本中提取实体和关系。

要求：
1. 提取文本中的关键实体（人物、组织、地点、概念、技术、事件等）
2. 提取实体之间的关系
3. 以 JSON 格式返回，格式如下：
{
  "nodes": [{"label": "实体名", "type": "实体类型"}],
  "edges": [{"source": "实体1", "target": "实体2", "label": "关系"}]
}
4. 只返回 JSON，不要其他文字`

  const messages = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: truncated }
  ]

  const raw = await callLLM(settings, messages)
  return parseExtractionResult(raw)
}
```

**JSON 解析容错处理**：
- 支持 markdown 代码块提取
- 中文标点转换（，→ , ：→ :）
- 尾随逗号修复
- 多种字段名兼容（nodes/entities, edges/relations/links）

### 图谱存储 (`graphStore.js`)

**数据结构**：
```javascript
const nodes = ref(new Map())        // nodeId -> node
const edges = ref(new Map())        // edgeId -> edge
const labelIndex = ref(new Map())   // normalizedLabel -> nodeId
const adjacency = ref(new Map())    // nodeId -> Set<edgeId>
```

**节点添加（自动去重）**：
```javascript
function addNode(node) {
  const normalized = normalizeLabel(node.label)
  
  // 如果已存在同名节点，合并属性
  if (labelIndex.value.has(normalized)) {
    const existing = nodes.value.get(labelIndex.value.get(normalized))
    existing.properties = { ...existing.properties, ...node.properties }
    return existing.id
  }
  
  // 创建新节点
  const id = generateId('n')
  nodes.value.set(id, newNode)
  labelIndex.value.set(normalized, id)
  adjacency.value.set(id, new Set())
  return id
}
```

---

## 架构图

```
┌─────────────────────────────────────────────────────────┐
│                      前端 (Vue 3)                        │
├─────────────────────────────────────────────────────────┤
│  用户提问                                                │
│      ↓                                                  │
│  ┌─────────────────┐                                    │
│  │ extractKeywords │ ← textTokenizer.js                 │
│  └────────┬────────┘                                    │
│           ↓                                             │
│  ┌─────────────────────────────────────┐                │
│  │        retrieveContext              │                │
│  │  ┌─────────────┐ ┌───────────────┐  │                │
│  │  │ 文档检索    │ │ 图谱检索      │  │                │
│  │  │ (主路)      │ │ (辅路)        │  │                │
│  │  │ searchFiles │ │ BFS Subgraph  │  │                │
│  │  └─────────────┘ └───────────────┘  │                │
│  └─────────────────┬───────────────────┘                │
│                    ↓                                    │
│  ┌─────────────────────────────────────┐                │
│  │ formatCombinedContext               │                │
│  │ 文档内容 + 图谱结构 → Prompt        │                │
│  └─────────────────┬───────────────────┘                │
│                    ↓                                    │
│  ┌─────────────────────────────────────┐                │
│  │ callLLM (OpenAI 兼容 API)           │                │
│  └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                   后端 (Express)                         │
├─────────────────────────────────────────────────────────┤
│  /api/graphs/*   图谱 CRUD                              │
│  /api/messages/* 聊天历史                               │
│  /api/files/*    文档存储 + 关键词搜索                  │
│                                                         │
│  数据库: SQLite (sql.js)                                │
└─────────────────────────────────────────────────────────┘
```

---

## 关键设计特点

| 特点 | 说明 |
|------|------|
| **双路检索** | 文档内容为主，图谱结构为辅 |
| **BFS 子图** | 从种子节点扩展，限制深度和节点数 |
| **LLM 提取** | 用大模型从非结构化文本抽取三元组 |
| **OpenAI 兼容** | 支持 DeepSeek、Kimi、Qwen 等多种 API |
| **前端可视化** | D3.js 力导向图，支持多种布局 |

---

## 与传统 RAG 的区别

| 传统 RAG | GraphRAG |
|----------|----------|
| 向量相似度检索 | 关键词匹配 + BFS 图遍历 |
| 文本分块 | 实体关系三元组 |
| 无结构知识 | 结构化知识图谱 |
| 单一检索 | 双路检索（文档+图谱） |

---

## 可借鉴的优化点

### 1. 关键词提取优化
当前使用简单的 bigram 分词，可以考虑：
- 使用 jieba 等中文分词库
- 添加 TF-IDF 权重
- 结合实体识别（NER）

### 2. 图谱检索优化
- 添加实体类型权重
- 考虑边的权重（关系强度）
- 支持多跳推理路径

### 3. 向量化增强
- 添加向量检索作为第三路
- 实体和关系也可以向量化
- 支持语义相似度匹配

### 4. 上下文优化
- 动态调整文档和图谱的比例
- 根据问题类型选择检索策略
- 添加重排序（rerank）步骤

---

## 文件结构

```
GraphRAG-Example/
├── src/
│   ├── services/
│   │   ├── ragRetriever.js      # RAG 检索核心
│   │   ├── llmExtractor.js      # LLM 实体关系提取
│   │   ├── llmApiService.js     # LLM API 调用
│   │   └── graphService.js      # 图谱服务
│   ├── composables/
│   │   └── useRagQuery.js       # RAG 查询组合函数
│   ├── stores/
│   │   └── graphStore.js        # 图谱状态管理
│   └── utils/
│       └── textTokenizer.js     # 文本分词
└── server/
    ├── routes/                   # API 路由
    └── db.js                     # 数据库操作
```

---

## 总结

这个项目是一个轻量级的 GraphRAG 实现，核心特点：

1. **双路检索策略**：文档内容为主，图谱结构为辅
2. **BFS 子图提取**：从关键词匹配的种子节点扩展
3. **LLM 驱动的知识抽取**：用大模型从非结构化文本提取实体关系
4. **前端可视化**：D3.js 实现图谱可视化

适合作为 GraphRAG 的入门学习项目，理解知识图谱增强检索的核心概念。