#!/usr/bin/env python3
"""
下载 CRAG 数据集并准备用于 RAG Demo
"""
import json
import os
import requests

# 创建数据目录
data_dir = os.path.expanduser("~/CodeFolder/rag-demo/backend/data/crag")
os.makedirs(data_dir, exist_ok=True)

# CRAG 数据集 - 从 Hugging Face 下载
print("正在下载 CRAG 数据集...")

# 使用 Hugging Face datasets 的简化版本
dataset_url = "https://huggingface.co/datasets/Quivr/CRAG/resolve/main/crag_1.json"

try:
    response = requests.get(dataset_url, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"成功下载数据，条目数: {len(data) if isinstance(data, list) else 'N/A'}")
except Exception as e:
    print(f"下载失败: {e}")
    data = None

# 如果下载失败，创建模拟的 CRAG 格式数据
if not data:
    print("使用模拟 CRAG 数据...")
    
    # 创建模拟的问答对和文档
    mock_data = {
        "questions": [
            {
                "question": "What is Django and what is it used for?",
                "answer": "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.",
                "category": "technology"
            },
            {
                "question": "How does LangChain work?",
                "answer": "LangChain is a framework for developing applications powered by language models through composability.",
                "category": "technology"
            },
            {
                "question": "What is the purpose of vector databases in RAG?",
                "answer": "Vector databases store embeddings of documents to enable efficient similarity search for retrieval.",
                "category": "ai"
            },
            {
                "question": "What is Python used for?",
                "answer": "Python is a versatile programming language used for web development, data science, AI, automation, and more.",
                "category": "programming"
            },
            {
                "question": "What is the difference between SQL and NoSQL databases?",
                "answer": "SQL databases are relational with structured schemas, while NoSQL databases are non-relational with flexible schemas.",
                "category": "database"
            }
        ],
        "documents": [
            {
                "id": "doc_1",
                "content": """Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. 
Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. 
It's free and open source. Django was designed to help developers take applications from concept to completion as quickly as possible.
Django includes dozens of extras you can use to handle common web development tasks. Django takes security seriously and helps developers avoid many common security mistakes.
The framework includes protections against SQL injection, cross-site scripting, cross-site request forgery and clickjacking.""",
                "source": "django_documentation"
            },
            {
                "id": "doc_2",
                "content": """LangChain is a framework for developing applications powered by language models. 
It enables applications that are data-aware, connecting a language model to other sources of data, and agentic, allowing a language model to interact with its environment.
The main value propositions of LangChain are components and chains. Components are abstractions for working with language models, along with a collection of implementations for each abstraction.
Chains are structured assemblies of components for accomplishing specific higher-level tasks. LangChain makes it easy to swap out abstractions and implementations.
LangChain consists of several open-source libraries: langchain-core, langchain, langchain-community, and partner packages like langchain-openai.""",
                "source": "langchain_documentation"
            },
            {
                "id": "doc_3",
                "content": """Vector databases are designed to store and query high-dimensional vectors efficiently. 
In the context of RAG (Retrieval-Augmented Generation), vector databases store embeddings of documents.
These embeddings are numerical representations of text that capture semantic meaning.
When a user asks a question, the system converts the query into an embedding and searches the vector database for similar embeddings.
This allows the system to retrieve relevant documents that can be used to augment the language model's response.
Popular vector databases include Chroma, Pinecone, Weaviate, and Milvus. Chroma is a popular choice for local development and prototyping.""",
                "source": "rag_guide"
            },
            {
                "id": "doc_4",
                "content": """Python is a high-level, interpreted programming language known for its simplicity and readability. 
It was created by Guido van Rossum and first released in 1991. Python supports multiple programming paradigms, including procedural, object-oriented, and functional programming.
Python is widely used in various domains including web development (Django, Flask), data science (pandas, NumPy), machine learning (TensorFlow, PyTorch), 
automation and scripting, scientific computing, and more. Python's extensive standard library and vast ecosystem of third-party packages make it a versatile choice for developers.
The language emphasizes code readability with its use of significant whitespace.""",
                "source": "python_guide"
            },
            {
                "id": "doc_5",
                "content": """SQL (Structured Query Language) databases are relational databases that use structured schemas and tables to store data. 
They use SQL for defining and manipulating data. Examples include MySQL, PostgreSQL, and SQLite. SQL databases ensure ACID compliance (Atomicity, Consistency, Isolation, Durability).
NoSQL databases are non-relational databases that provide flexible schemas. They include document stores (MongoDB), key-value stores (Redis), wide-column stores (Cassandra), and graph databases (Neo4j).
NoSQL databases are often chosen for their scalability and flexibility with unstructured data. The choice between SQL and NoSQL depends on the specific requirements of the application,
including data structure, scalability needs, and consistency requirements.""",
                "source": "database_guide"
            },
            {
                "id": "doc_6",
                "content": """Retrieval-Augmented Generation (RAG) is a technique that enhances large language models by retrieving relevant information from external knowledge sources.
The RAG pipeline typically consists of three main components: indexing, retrieval, and generation.
During indexing, documents are processed, chunked, converted to embeddings, and stored in a vector database.
During retrieval, the user's query is converted to an embedding and similar documents are retrieved from the vector database.
During generation, the retrieved documents are combined with the user's query to create a context-rich prompt for the language model.
RAG helps reduce hallucinations and provides source attribution for generated responses.""",
                "source": "rag_overview"
            },
            {
                "id": "doc_7",
                "content": """Vue.js is a progressive JavaScript framework for building user interfaces. 
It is designed to be incrementally adoptable, meaning you can use it for a small part of your application or build a full single-page application.
Vue uses a virtual DOM for efficient rendering and provides reactive data binding. The framework is known for its gentle learning curve and excellent documentation.
Vue 3 introduced the Composition API, which provides a more flexible way to organize component logic. Vite is a modern build tool that provides fast development server startup
and optimized production builds. Vue and Vite work well together for modern frontend development.""",
                "source": "vue_documentation"
            },
            {
                "id": "doc_8",
                "content": """Embeddings are numerical representations of text, images, or other data that capture semantic meaning. 
In natural language processing, text embeddings convert words, sentences, or documents into vectors of floating-point numbers.
These vectors are designed such that similar texts have similar embeddings (small distance in vector space).
OpenAI provides text embedding models like text-embedding-ada-002 that can convert text into 1536-dimensional vectors.
Other embedding providers include Hugging Face, Cohere, and Google. The choice of embedding model affects the quality of retrieval in RAG systems.
Factors to consider include embedding dimension, supported languages, and performance on specific domains.""",
                "source": "embeddings_guide"
            }
        ]
    }
    data = mock_data

# 保存问题集（用于测试召回率）
questions_file = os.path.join(data_dir, "questions.json")
with open(questions_file, "w", encoding="utf-8") as f:
    json.dump(data.get("questions", data) if isinstance(data, dict) else [], f, ensure_ascii=False, indent=2)
print(f"问题集已保存: {questions_file}")

# 将文档保存为单独的文本文件
documents = data.get("documents", []) if isinstance(data, dict) else []
for i, doc in enumerate(documents):
    doc_file = os.path.join(data_dir, f"doc_{i+1}.txt")
    content = doc.get("content", str(doc)) if isinstance(doc, dict) else str(doc)
    with open(doc_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"文档已保存: {doc_file}")

print(f"\nCRAG 数据准备完成!")
print(f"- 文档数量: {len(documents)}")
print(f"- 问题数量: {len(data.get('questions', [])) if isinstance(data, dict) else 0}")
print(f"- 数据目录: {data_dir}")
