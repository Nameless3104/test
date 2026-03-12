"""
RAG Chain Module - RAG 问答链

这个模块负责创建和管理 RAG 问答链，将检索器和 LLM 结合起来。
使用 LangChain 新版 API，直接调用 LLM 和 Retriever。
"""

from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def create_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
):
    """
    创建 LLM 实例

    Args:
        model_name: 模型名称，如果为 None 则从 settings 获取
        temperature: 温度参数 (0-1)
        api_key: API Key，如果为 None 则从 settings 获取
        base_url: Base URL，如果为 None 则从 settings 获取

    Returns:
        LLM 实例
    """
    from django.conf import settings
    
    # 优先使用 DeepSeek API
    if api_key is None:
        api_key = settings.DEEPSEEK_API_KEY or settings.OPENAI_API_KEY
    if base_url is None:
        base_url = settings.DEEPSEEK_BASE_URL if settings.DEEPSEEK_API_KEY else settings.OPENAI_BASE_URL
    if model_name is None:
        model_name = settings.LLM_MODEL_NAME
    
    if not api_key:
        raise ValueError(
            "API Key 未配置。请在 .env 文件中设置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY"
        )
    
    # DeepSeek 使用 OpenAI 兼容接口
    # 注意：deepseek-reasoner 不支持 temperature 参数
    if model_name == 'deepseek-reasoner':
        kwargs = {
            "model": model_name,
            "openai_api_key": api_key,
        }
    else:
        kwargs = {
            "model": model_name,
            "temperature": temperature,
            "openai_api_key": api_key,
        }
    
    # 如果配置了 base_url，则使用自定义的 base_url
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return ChatOpenAI(**kwargs)


def format_docs(docs: List[Document]) -> str:
    """将文档列表格式化为字符串"""
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(
    retriever: BaseRetriever,
    llm=None,
) -> Any:
    """
    创建 RAG 问答链

    Args:
        retriever: 检索器
        llm: LLM 实例 (可选，默认从 settings 配置创建)

    Returns:
        RAG 链实例 (Runnable)
    """
    if llm is None:
        llm = create_llm()

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个有用的AI助手。请根据以下上下文回答用户的问题。
如果你不知道答案，请说"我不知道"，不要编造答案。

上下文:
{context}

请用中文回答问题。"""),
        ("human", "{question}"),
    ])

    # 创建 RAG 链 (使用 LCEL - LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(
    chain: Any,
    question: str,
    retriever: BaseRetriever = None
) -> Dict[str, Any]:
    """
    执行问答

    Args:
        chain: RAG 链
        question: 用户问题
        retriever: 检索器 (用于获取来源文档)

    Returns:
        包含答案和来源的字典
    """
    try:
        # 获取答案
        answer = chain.invoke(question)
        
        # 获取来源文档
        sources = []
        if retriever:
            docs = retriever.invoke(question)
            for doc in docs:
                if isinstance(doc, Document):
                    sources.append({
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "source": doc.metadata.get("source", "Unknown")
                    })

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }


def format_response(result: Dict[str, Any]) -> str:
    """
    格式化响应结果

    Args:
        result: 问答结果

    Returns:
        格式化的字符串
    """
    output = f"Answer: {result['answer']}\n\n"

    if result['sources']:
        output += "Sources:\n"
        for i, source in enumerate(result['sources'], 1):
            output += f"{i}. {source['source']}\n"

    return output
