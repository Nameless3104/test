"""
检索器模块

提供向量数据库创建和检索功能，使用 Chroma 作为向量存储。
"""
import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever

try:
    from langchain_chroma import Chroma
    HAS_CHROMA = True
except ImportError:
    try:
        from langchain_community.vectorstores import Chroma
        HAS_CHROMA = True
    except ImportError:
        HAS_CHROMA = False


def create_vectorstore(
    documents: List[Document],
    embeddings: Embeddings,
    persist_directory: str,
    collection_name: str = "rag_collection"
) -> Chroma:
    """
    创建向量数据库
    
    将文档嵌入并存储到 Chroma 向量数据库中。
    
    Args:
        documents: 要存储的文档列表
        embeddings: 嵌入模型实例
        persist_directory: 向量数据库持久化目录
        collection_name: 集合名称，默认 "rag_collection"
        
    Returns:
        Chroma: 创建的向量数据库实例
        
    Raises:
        ValueError: 当 Chroma 不可用时抛出
    """
    if not HAS_CHROMA:
        raise ValueError(
            "Chroma 向量数据库不可用。"
            "请安装: pip install chromadb"
        )
    
    # 确保目录存在
    os.makedirs(persist_directory, exist_ok=True)
    
    print(f"创建向量数据库: {persist_directory}")
    print(f"文档数量: {len(documents)}")
    
    # 创建向量数据库
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
    
    # Chroma 会自动持久化，无需调用 persist()
    print("向量数据库创建完成")
    
    return vectorstore


def load_vectorstore(
    persist_directory: str,
    embeddings: Embeddings,
    collection_name: str = "rag_collection"
) -> Chroma:
    """
    加载已有的向量数据库
    
    Args:
        persist_directory: 向量数据库持久化目录
        embeddings: 嵌入模型实例
        collection_name: 集合名称，默认 "rag_collection"
        
    Returns:
        Chroma: 加载的向量数据库实例
        
    Raises:
        ValueError: 当目录不存在或 Chroma 不可用时抛出
    """
    if not HAS_CHROMA:
        raise ValueError(
            "Chroma 向量数据库不可用。"
            "请安装: pip install chromadb"
        )
    
    # 确保路径是字符串
    persist_directory = str(persist_directory)
    
    if not os.path.exists(persist_directory):
        raise ValueError(f"向量数据库目录不存在: {persist_directory}")
    
    print(f"加载向量数据库: {persist_directory}")
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name,
    )
    
    print("向量数据库加载完成")
    
    return vectorstore


def get_retriever(
    vectorstore: Chroma,
    search_type: str = "similarity",
    search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    """
    获取检索器
    
    Args:
        vectorstore: 向量数据库实例
        search_type: 搜索类型，可选值:
            - "similarity": 返回最相似的文档 (默认)
            - "mmr": 最大边际相关性，平衡相关性和多样性
            - "similarity_score_threshold": 只返回相似度高于阈值的文档
        search_kwargs: 搜索参数，根据 search_type 不同:
            - similarity: {"k": 4} 返回前4个最相似的文档
            - mmr: {"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
            - similarity_score_threshold: {"k": 4, "score_threshold": 0.8}
        
    Returns:
        BaseRetriever: 检索器实例
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}  # 默认返回前4个结果
    
    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs,
    )
    
    print(f"创建检索器: search_type={search_type}, kwargs={search_kwargs}")
    
    return retriever


def similarity_search(
    vectorstore: Chroma,
    query: str,
    k: int = 4
) -> List[Document]:
    """
    相似度搜索
    
    直接在向量数据库中搜索相似文档，不使用检索器。
    
    Args:
        vectorstore: 向量数据库实例
        query: 查询文本
        k: 返回的文档数量
        
    Returns:
        List[Document]: 相似文档列表
    """
    results = vectorstore.similarity_search(query, k=k)
    return results


def similarity_search_with_score(
    vectorstore: Chroma,
    query: str,
    k: int = 4
) -> List[tuple]:
    """
    带分数的相似度搜索
    
    Args:
        vectorstore: 向量数据库实例
        query: 查询文本
        k: 返回的文档数量
        
    Returns:
        List[tuple]: (Document, score) 元组列表，score 越小越相似
    """
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results


def hybrid_search(
    vectorstore: Chroma,
    query: str,
    k: int = 10
) -> List[Document]:
    """
    混合检索：结合相似度检索和 MMR 检索
    
    这是优化后的检索策略，在 CRAG 数据集上 Recall@3 达到 60%。
    
    Args:
        vectorstore: 向量数据库实例
        query: 查询文本
        k: 返回的文档数量
        
    Returns:
        List[Document]: 合并后的文档列表
    """
    from pathlib import Path
    
    # 1. 相似度检索 (带分数)
    sim_results = vectorstore.similarity_search_with_score(query, k=k*2)
    
    # 2. MMR 检索
    mmr_results = vectorstore.max_marginal_relevance_search(
        query, k=k, fetch_k=k*3, lambda_mult=0.7
    )
    
    # 3. 合并结果，去重（保留相似度检索的分数排序）
    seen_sources = set()
    combined = []
    
    # 先添加相似度检索结果
    for doc, score in sim_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append(doc)
    
    # 再添加 MMR 结果
    for doc in mmr_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append(doc)
    
    return combined[:k]
