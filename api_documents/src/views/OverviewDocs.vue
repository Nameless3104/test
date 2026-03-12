<template>
  <div class="overview">
    <div class="section-intro">
      <h1>🏠 RAG Demo 项目概述</h1>
      <p>基于检索增强生成(RAG)的智能问答系统文档</p>
    </div>

    <div class="card">
      <h2>📋 项目简介</h2>
      <p>
        RAG Demo 是一个基于 LangChain 框架构建的智能问答系统，采用检索增强生成(Retrieval-Augmented Generation)技术，
        结合向量数据库和大型语言模型，实现对知识库的智能问答。
      </p>
    </div>

    <div class="card">
      <h2>🏗️ 技术架构</h2>
      <div class="tech-stack">
        <div class="tech-section">
          <h3>后端技术栈</h3>
          <ul>
            <li><strong>框架:</strong> Django 5.x + Django REST Framework</li>
            <li><strong>AI 框架:</strong> LangChain</li>
            <li><strong>向量数据库:</strong> ChromaDB</li>
            <li><strong>Embedding:</strong> OpenAI text-embedding-3-small</li>
            <li><strong>LLM:</strong> DeepSeek / OpenAI</li>
            <li><strong>数据库:</strong> SQLite (开发环境)</li>
          </ul>
        </div>
        <div class="tech-section">
          <h3>前端技术栈</h3>
          <ul>
            <li><strong>框架:</strong> Vue 3 (Composition API)</li>
            <li><strong>构建工具:</strong> Vite</li>
            <li><strong>样式:</strong> CSS3 + Scoped Styles</li>
            <li><strong>HTTP 客户端:</strong> Fetch API</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>📁 项目结构</h2>
      <pre><code>rag-demo/
├── backend/                    # 后端服务
│   ├── api/                   # API 应用
│   │   ├── views.py          # 视图函数
│   │   ├── urls.py           # URL 路由
│   │   └── serializers.py    # 序列化器
│   ├── rag/                   # RAG 核心模块
│   │   ├── loaders.py        # 文档加载器
│   │   ├── embeddings.py     # 向量化模块
│   │   ├── retriever.py      # 检索器
│   │   └── chain.py          # RAG 链
│   ├── rag_project/           # Django 项目配置
│   ├── data/                  # 知识库文档目录
│   └── vectordb/              # 向量数据库存储
│
└── frontend/                   # 前端应用
    ├── src/
    │   ├── views/             # 页面组件
    │   ├── components/        # UI 组件
    │   ├── api/               # API 调用
    │   └── App.vue            # 根组件
    └── vite.config.js         # Vite 配置</code></pre>
    </div>

    <div class="card">
      <h2>🚀 核心功能</h2>
      <div class="features-grid">
        <div class="feature-item">
          <span class="feature-icon">💬</span>
          <h4>智能问答</h4>
          <p>基于 RAG 技术的智能问答，支持上下文理解</p>
        </div>
        <div class="feature-item">
          <span class="feature-icon">📄</span>
          <h4>文档管理</h4>
          <p>支持多种文档格式上传和管理</p>
        </div>
        <div class="feature-item">
          <span class="feature-icon">🔍</span>
          <h4>混合检索</h4>
          <p>结合相似度检索和 MMR 检索，提升召回率</p>
        </div>
        <div class="feature-item">
          <span class="feature-icon">📊</span>
          <h4>来源追溯</h4>
          <p>展示回答的参考来源，增强可信度</p>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>📖 文档导航</h2>
      <div class="doc-nav">
        <div class="doc-item" @click="$emit('navigate', 'api')">
          <span class="doc-icon">🔌</span>
          <div>
            <h4>API 接口文档</h4>
            <p>后端 REST API 接口详细说明</p>
          </div>
        </div>
        <div class="doc-item" @click="$emit('navigate', 'components')">
          <span class="doc-icon">🧩</span>
          <div>
            <h4>前端组件文档</h4>
            <p>Vue 3 组件的 Props、Events、Slots</p>
          </div>
        </div>
        <div class="doc-item" @click="$emit('navigate', 'changelog')">
          <span class="doc-icon">📝</span>
          <div>
            <h4>改动记录</h4>
            <p>项目更新历史和 commit 记录</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.tech-section h3 {
  color: #6366f1;
  margin-bottom: 15px;
}

.tech-section ul {
  list-style: none;
}

.tech-section li {
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.feature-item {
  text-align: center;
  padding: 20px;
  background: #f9fafb;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 10px;
}

.feature-item h4 {
  color: #1a1a2e;
  margin-bottom: 8px;
}

.feature-item p {
  font-size: 14px;
  color: #6b7280;
}

.doc-nav {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.doc-item:hover {
  background: #e5e7eb;
  transform: translateX(5px);
}

.doc-icon {
  font-size: 28px;
}

.doc-item h4 {
  color: #1a1a2e;
  margin-bottom: 4px;
}

.doc-item p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}
</style>
