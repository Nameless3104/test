#!/usr/bin/env python3
"""
重建向量数据库 - 使用 CRAG 数据集
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
backend_dir = Path(__file__).parent.parent
env_file = backend_dir / '.env'
load_dotenv(env_file)

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_project.settings')
sys.path.insert(0, str(backend_dir))

import django
django.setup()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings


def main():
    # 配置 - 使用 CRAG 处理后的文档
    data_dir = backend_dir / "data" / "crag" / "docs"
    persist_dir = backend_dir / "vectordb"
    
    print(f"数据目录: {data_dir}")
    print(f"向量数据库目录: {persist_dir}")
    
    # 1. 加载文档
    print("\n1. 加载文档...")
    loader = DirectoryLoader(
        str(data_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"   加载了 {len(documents)} 个文档")
    
    # 2. 分块
    print("\n2. 文档分块...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"   分块后共 {len(split_docs)} 个文档块")
    
    # 3. 创建向量数据库
    print("\n3. 创建向量数据库...")
    
    # 清除旧的向量数据库
    import shutil
    if persist_dir.exists():
        shutil.rmtree(persist_dir)
        print(f"   已清除旧数据库")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_api_base=os.environ.get("OPENAI_BASE_URL")
    )
    print(f"   使用嵌入模型: text-embedding-ada-002")
    
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="crag_collection",
    )
    print(f"   向量数据库创建完成")
    
    # 4. 验证
    print("\n4. 验证向量数据库...")
    test_query = "Steve Nash basketball career"
    results = vectorstore.similarity_search(test_query, k=3)
    print(f"   测试查询: {test_query}")
    print(f"   返回 {len(results)} 个结果")
    for i, doc in enumerate(results):
        source = doc.metadata.get('source', 'unknown')
        content = doc.page_content[:100].replace('\n', ' ')
        print(f"   [{i+1}] {source}: {content}...")
    
    print("\n✅ 向量数据库重建完成!")
    print(f"   文档块数量: {len(split_docs)}")


if __name__ == "__main__":
    main()
