# RAG Demo 后端

基于 Django + LangChain 的 RAG (检索增强生成) 后端服务。

## 项目结构

```
backend/
├── rag_project/          # Django 项目配置
│   ├── settings.py       # 项目设置
│   ├── urls.py           # URL 路由
│   ├── wsgi.py           # WSGI 入口
│   └── asgi.py           # ASGI 入口
├── api/                  # API 应用
│   ├── views.py          # API 视图
│   ├── urls.py           # API 路由
│   ├── models.py         # 数据模型
│   └── serializers.py    # 序列化器
├── rag/                  # RAG 核心模块
│   ├── loaders.py        # 文档加载
│   ├── embeddings.py     # 向量化
│   ├── retriever.py      # 检索器
│   └── chain.py          # RAG 链
├── data/                 # 文档目录
├── vectordb/             # 向量数据库
├── manage.py             # Django 管理脚本
└── requirements.txt      # 依赖列表
```

## 快速开始

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量 (可选)

创建 `.env` 文件：

```env
# OpenAI API Key (可选，用于 LLM)
OPENAI_API_KEY=your-api-key-here

# LLM 模型名称
LLM_MODEL_NAME=gpt-3.5-turbo

# Embedding 模型名称 (默认使用 HuggingFace 免费模型)
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

### 4. 运行数据库迁移

```bash
python manage.py migrate
```

### 5. 启动服务器

```bash
python manage.py runserver
```

服务器将在 http://localhost:8000 启动。

## API 接口

### POST /api/chat/

聊天问答接口

**请求:**
```json
{
  "question": "什么是 RAG?"
}
```

**响应:**
```json
{
  "answer": "RAG 是检索增强生成技术...",
  "sources": [
    {
      "content": "RAG (Retrieval-Augmented Generation) 是一种...",
      "source": "sample.txt"
    }
  ]
}
```

### GET /api/documents/

获取文档列表

**响应:**
```json
{
  "documents": [
    {
      "name": "sample.txt",
      "size": 1024
    }
  ]
}
```

### POST /api/documents/upload/

上传文档

**请求:** multipart/form-data
- file: 文档文件

**响应:**
```json
{
  "message": "上传成功",
  "filename": "document.txt",
  "size": 2048
}
```

### POST /api/vectordb/rebuild/

重建向量数据库

**响应:**
```json
{
  "message": "向量数据库重建成功",
  "document_count": 5,
  "chunk_count": 20
}
```

## 使用说明

1. 上传文档到 `data/` 目录或通过 API 上传
2. 调用 `/api/vectordb/rebuild/` 构建向量索引
3. 使用 `/api/chat/` 进行问答

## 注意事项

- 默认使用 HuggingFace 的免费 Embedding 模型，无需 API key
- 如需使用 OpenAI LLM，请设置 `OPENAI_API_KEY` 环境变量
- 首次运行时会自动下载 Embedding 模型（约 90MB）
