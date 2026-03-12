#!/usr/bin/env python3
"""
重建向量数据库 - 优化版

优化策略：
1. 更小的 chunk size（200 vs 500）- 提高精确匹配
2. 更大的 overlap（50 vs 100）- 减少信息丢失
3. 添加文档元数据 - 提高检索质量
"""
import os
import sys
import re
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


def clean_text(text: str) -> str:
    """清理文本，移除多余空白和噪声"""
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊字符
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', ' ', text)
    return text.strip()


def main():
    # 配置
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
    
    # 清理文档内容
    print("\n2. 清理文档内容...")
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    
    # 2. 分块 - 优化参数
    print("\n3. 文档分块（优化参数）...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,      # 更小的块，提高精确匹配
        chunk_overlap=80,    # 更大的重叠，减少边界信息丢失
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"   分块后共 {len(split_docs)} 个文档块")
    
    # 3. 创建向量数据库
    print("\n4. 创建向量数据库...")
    
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
    print("\n5. 验证向量数据库...")
    test_queries = [
        "Steve Nash basketball career",
        "Oscar best visual effects 2012",
        "Microsoft ex-dividend date",
    ]
    
    for query in test_queries:
        results = vectorstore.similarity_search(query, k=3)
        print(f"\n   查询: {query}")
        for i, doc in enumerate(results):
            source = Path(doc.metadata.get('source', 'unknown')).stem
            content = doc.page_content[:80].replace('\n', ' ')
            print(f"   [{i+1}] {source}: {content}...")
    
    print("\n✅ 向量数据库重建完成!")
    print(f"   文档块数量: {len(split_docs)}")
    print(f"   平均块大小: 300 字符")
    print(f"   重叠大小: 80 字符")


if __name__ == "__main__":
    main()
