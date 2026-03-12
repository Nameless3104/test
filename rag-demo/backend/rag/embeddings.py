"""
向量化模块

提供文本嵌入(Embedding)功能，使用 OpenAI 嵌入模型。
注意：DeepSeek 不提供 embedding API，所以 embedding 必须使用 OpenAI。
"""
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


def get_embeddings(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> Embeddings:
    """
    获取 OpenAI 嵌入模型
    
    注意：DeepSeek 不提供 embedding API，所以必须使用 OpenAI 的 embedding 服务。
    推荐使用 text-embedding-3-small 模型，效果更好。
    
    Args:
        model_name: 模型名称，默认 'text-embedding-3-small'
        api_key: OpenAI API Key，如果为 None 则从 Django settings 获取
        base_url: OpenAI Base URL，如果为 None 则从 Django settings 获取
        
    Returns:
        Embeddings: 嵌入模型实例
    """
    # 从 Django settings 获取配置
    from django.conf import settings
    
    # Embedding 必须使用 OpenAI (DeepSeek 不支持)
    if api_key is None:
        api_key = settings.OPENAI_API_KEY
    if base_url is None:
        base_url = settings.OPENAI_BASE_URL
    if model_name is None:
        model_name = settings.EMBEDDING_MODEL_NAME
    
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY 未配置。DeepSeek 不提供 embedding API，"
            "请在 .env 文件中设置 OPENAI_API_KEY 用于 embedding 功能"
        )
    
    print(f"使用 OpenAI 嵌入模型: {model_name}")
    
    kwargs = {
        "model": model_name,
        "openai_api_key": api_key,
    }
    
    # 如果配置了 base_url，则使用自定义的 base_url
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def get_embedding_dimension(embeddings: Embeddings) -> int:
    """
    获取嵌入向量的维度
    
    Args:
        embeddings: 嵌入模型实例
        
    Returns:
        int: 嵌入向量的维度
    """
    # 通过嵌入一个简单的文本来获取维度
    test_embedding = embeddings.embed_query("test")
    return len(test_embedding)
