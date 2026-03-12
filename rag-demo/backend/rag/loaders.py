"""
文档加载模块

提供文档加载和分块功能，支持多种文档格式。
"""
import os
from typing import List
from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    PyPDFLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_documents(data_dir: str) -> List[Document]:
    """
    加载目录下的所有文档
    
    支持的文档格式:
    - .txt: 纯文本文件
    - .md: Markdown 文件
    - .pdf: PDF 文档
    - .csv: CSV 表格文件
    - .json: JSON 文件
    
    Args:
        data_dir: 文档目录路径
        
    Returns:
        List[Document]: 加载的文档列表
        
    Raises:
        ValueError: 当目录不存在时抛出
    """
    if not os.path.exists(data_dir):
        raise ValueError(f"数据目录不存在: {data_dir}")
    
    documents = []
    data_path = Path(data_dir)
    
    # 加载 .txt 文件
    txt_files = list(data_path.glob('**/*.txt'))
    for file_path in txt_files:
        try:
            loader = TextLoader(str(file_path), encoding='utf-8')
            documents.extend(loader.load())
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
    
    # 加载 .md 文件
    md_files = list(data_path.glob('**/*.md'))
    for file_path in md_files:
        try:
            loader = UnstructuredMarkdownLoader(str(file_path))
            documents.extend(loader.load())
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
    
    # 加载 .pdf 文件
    pdf_files = list(data_path.glob('**/*.pdf'))
    for file_path in pdf_files:
        try:
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
    
    # 加载 .csv 文件
    csv_files = list(data_path.glob('**/*.csv'))
    for file_path in csv_files:
        try:
            loader = CSVLoader(str(file_path), encoding='utf-8')
            documents.extend(loader.load())
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
    
    # 加载 .json 文件
    json_files = list(data_path.glob('**/*.json'))
    for file_path in json_files:
        try:
            loader = JSONLoader(
                str(file_path),
                jq_schema='.',  # 加载整个 JSON
                text_content=False
            )
            documents.extend(loader.load())
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
    
    print(f"成功加载 {len(documents)} 个文档")
    return documents


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    将文档分块
    
    使用递归字符文本分割器，按段落、句子、单词的优先级进行分割。
    
    Args:
        documents: 要分割的文档列表
        chunk_size: 每个块的最大字符数，默认 1000
        chunk_overlap: 相邻块之间的重叠字符数，默认 200
        
    Returns:
        List[Document]: 分割后的文档块列表
    """
    # 创建文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",  # 段落
            "\n",    # 行
            "。",    # 中文句号
            "！",    # 中文感叹号
            "？",    # 中文问号
            "。",    # 英文句号
            "!",     # 英文感叹号
            "?",     # 英文问号
            "；",    # 中文分号
            ";",     # 英文分号
            "，",    # 中文逗号
            ",",     # 英文逗号
            " ",     # 空格
            "",      # 字符
        ],
        is_separator_regex=False,
    )
    
    # 分割文档
    split_docs = text_splitter.split_documents(documents)
    
    print(f"文档分割完成: {len(documents)} 个文档 -> {len(split_docs)} 个块")
    return split_docs


def get_document_info(documents: List[Document]) -> dict:
    """
    获取文档信息统计
    
    Args:
        documents: 文档列表
        
    Returns:
        dict: 包含文档统计信息的字典
    """
    total_chars = sum(len(doc.page_content) for doc in documents)
    sources = set(doc.metadata.get('source', 'unknown') for doc in documents)
    
    return {
        'total_documents': len(documents),
        'total_characters': total_chars,
        'unique_sources': len(sources),
        'sources': list(sources),
    }
