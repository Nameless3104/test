#!/usr/bin/env python3
"""
重建向量数据库 - 最佳配置版

基于之前的测试结果：
- chunk_size=300, overlap=80 效果最好 (Recall@3=42%)
- 继续优化：增加检索数量 + 使用更好的查询处理
"""
import os
import sys
import re
import shutil
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).parent.parent
env_file = backend_dir / '.env'
load_dotenv(env_file)

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


def clean_text(text: str) -> str:
    """清理文本"""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def main():
    data_dir = backend_dir / "data" / "crag" / "docs"
    persist_dir = backend_dir / "vectordb"
    
    print(f"数据目录: {data_dir}")
    
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
    
    # 清理
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    
    # 2. 分块 - 最佳配置
    print("\n2. 文档分块（最佳配置: chunk=300, overlap=80）...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", ", ", " ", ""],
    )
    split_docs = text_splitter.split_documents(documents)
    
    # 过滤太短的块
    split_docs = [d for d in split_docs if len(d.page_content) > 50]
    print(f"   分块后共 {len(split_docs)} 个文档块")
    
    # 3. 创建向量数据库
    print("\n3. 创建向量数据库...")
    
    if persist_dir.exists():
        shutil.rmtree(persist_dir)
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_api_base=os.environ.get("OPENAI_BASE_URL")
    )
    
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="crag_collection",
    )
    
    print(f"   向量数据库创建完成")
    print(f"   文档块数量: {len(split_docs)}")
    print("\n✅ 完成!")


if __name__ == "__main__":
    main()
