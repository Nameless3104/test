# RAG Demo - AI Knowledge Base

基于 LangChain 的 RAG (检索增强生成) 演示项目，用于求职展示。

## 技术栈

- **后端**: Django + Django REST Framework + LangChain
- **前端**: Vue 3 + Vite
- **向量数据库**: Chroma
- **LLM**: OpenAI API (可配置其他)

## 项目结构

```
rag-demo/
├── backend/                    # Django 后端
│   ├── rag_project/           # Django 项目配置
│   ├── api/                   # REST API
│   ├── rag/                   # LangChain RAG 模块
│   ├── data/                  # 原始文档
│   └── vectordb/              # 向量数据库
├── frontend/                   # Vue 前端
│   ├── src/                   # Vue 源码
│   └── package.json
└── README.md
```

## 快速开始

### 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat/` | POST | 发送问题，返回 RAG 回答 |
| `/api/documents/` | GET | 获取已索引文档列表 |
| `/api/documents/upload/` | POST | 上传新文档 |
| `/api/vectordb/rebuild/` | POST | 重建向量数据库 |

## 作者

AI 开发工程师求职展示项目
