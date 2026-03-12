#!/usr/bin/env python3
"""
重建向量数据库 - 最终优化版

策略：
1. 极细粒度分块 (chunk_size=150)
2. 保留完整句子
3. 添加更多文档元数据
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
    
    # 2. 分块 - 极细粒度
    print("\n2. 文档分块（极细粒度）...")
    
    # 使用多种分块策略
    splitters = [
        RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=30,
            separators=["\n\n", "\n", ". ", ", ", " ", ""],
        ),
        RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""],
        ),
    ]
    
    all_splits = []
    for splitter in splitters:
        splits = splitter.split_documents(documents)
        all_splits.extend(splits)
    
    # 去重（基于内容）
    seen = set()
    unique_splits = []
    for doc in all_splits:
        content_hash = hash(doc.page_content)
        if content_hash not in seen and len(doc.page_content) > 30:
            seen.add(content_hash)
            unique_splits.append(doc)
    
    print(f"   分块后共 {len(unique_splits)} 个文档块")
    
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
        documents=unique_splits,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="crag_collection",
    )
    
    # 4. 验证
    print("\n4. 验证...")
    test_queries = [
        "Steve Nash 3-point attempts average",
        "Oscar best visual effects 2012",
        "Microsoft ex-dividend date 2024",
    ]
    
    for query in test_queries:
        results = vectorstore.similarity_search_with_score(query, k=5)
        print(f"\n   查询: {query}")
        for i, (doc, score) in enumerate(results[:3]):
            source = Path(doc.metadata.get('source', 'unknown')).stem
            content = doc.page_content[:50].replace('\n', ' ')
            print(f"   [{i+1}] {source} (score: {score:.4f}): {content}...")
    
    print("\n✅ 向量数据库重建完成!")
    print(f"   文档块数量: {len(unique_splits)}")


if __name__ == "__main__":
    main()
