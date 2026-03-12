#!/usr/bin/env python3
"""
RAG 召回率测试 - 优化版 v11

策略：text-embedding-3-small + 查询重写 + 混合检索
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import List, Tuple

backend_dir = Path(__file__).parent.parent / "rag-demo" / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma


def load_test_questions():
    questions_file = backend_dir / "data" / "crag" / "questions.json"
    with open(questions_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_embeddings() -> OpenAIEmbeddings:
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    
    kwargs = {"model": "text-embedding-3-small", "openai_api_key": api_key}
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def get_llm():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    return ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.1,
    )


def load_vectorstore() -> Chroma:
    persist_dir = str(backend_dir / "vectordb_v3")
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="crag_collection_v3",
    )


def check_source_in_results(results: List, expected_doc: str) -> Tuple[bool, int]:
    for i, doc in enumerate(results):
        source = doc.metadata.get("source", "")
        doc_name = Path(source).stem
        if expected_doc == doc_name:
            return True, i + 1
    return False, 0


def calculate_recall_at_k(results_list: List[List], expected_docs: List[str], k: int) -> float:
    hits = 0
    for results, expected in zip(results_list, expected_docs):
        found, _ = check_source_in_results(results[:k], expected)
        if found:
            hits += 1
    return hits / len(expected_docs) if expected_docs else 0


def calculate_mrr(results_list: List[List], expected_docs: List[str]) -> float:
    reciprocal_ranks = []
    for results, expected in zip(results_list, expected_docs):
        found, rank = check_source_in_results(results, expected)
        if found:
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0)
    return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0


def rewrite_query(llm, question: str) -> str:
    """使用 LLM 重写查询"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract the most important keywords and entities for search.
Return ONLY the optimized search query, nothing else.
Focus on: names, dates, numbers, specific terms.

Examples:
Q: "what movie won the oscar best visual effects in 2016?"
A: "oscar best visual effects 2016 winner"

Q: "how many 3-point attempts did steve nash average per game?"
A: "steve nash 3-point attempts average per game"
"""),
        ("human", "{question}"),
    ])
    
    chain = prompt | llm
    try:
        result = chain.invoke({"question": question})
        return result.content.strip()
    except:
        return question


def hybrid_search(vectorstore, question, k=10):
    """混合检索"""
    sim_results = vectorstore.similarity_search_with_score(question, k=k*2)
    mmr_results = vectorstore.max_marginal_relevance_search(
        question, k=k, fetch_k=k*3, lambda_mult=0.7
    )
    
    seen_sources = set()
    combined = []
    
    for doc, score in sim_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append(doc)
    
    for doc in mmr_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append(doc)
    
    return combined[:k]


def run_recall_test():
    print("=" * 60)
    print("RAG 召回率测试 - CRAG Task 1 & 2 (v11 - 查询重写)")
    print("Embedding: text-embedding-3-small + DeepSeek 查询重写")
    print("=" * 60)
    
    test_questions = load_test_questions()
    print(f"\n共 {len(test_questions)} 个测试问题")
    
    vectorstore = load_vectorstore()
    print("✅ 向量数据库加载成功")
    
    llm = get_llm()
    print("✅ LLM 加载成功 (DeepSeek)")
    
    all_results = []
    all_expected = []
    response_times = []
    
    print(f"\n开始测试（查询重写 + 混合检索）...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        start_time = time.time()
        try:
            rewritten = rewrite_query(llm, question)
            results = hybrid_search(vectorstore, rewritten, k=10)
            elapsed = time.time() - start_time
            response_times.append(elapsed)
        except Exception as e:
            print(f"  [{i}] ❌ 查询失败: {e}")
            continue
        
        all_results.append(results)
        all_expected.append(expected_doc)
        
        found, rank = check_source_in_results(results, expected_doc)
        status = "✅" if found else "❌"
        
        q_display = question[:40] + "..." if len(question) > 40 else question
        rw_display = rewritten[:40] + "..." if len(rewritten) > 40 else rewritten
        print(f"  [{i:2d}] {status} \"{q_display}\"")
        print(f"        重写: \"{rw_display}\"")
        print(f"        期望: {expected_doc}, 排名: {rank if found else '未找到'}, 耗时: {elapsed:.3f}s")
    
    print("-" * 60)
    
    print("\n📊 召回率指标:")
    print("-" * 40)
    
    recall_1 = calculate_recall_at_k(all_results, all_expected, 1)
    recall_3 = calculate_recall_at_k(all_results, all_expected, 3)
    recall_5 = calculate_recall_at_k(all_results, all_expected, 5)
    recall_10 = calculate_recall_at_k(all_results, all_expected, 10)
    mrr = calculate_mrr(all_results, all_expected)
    avg_time = sum(response_times) / len(response_times) if response_times else 0
    
    print(f"  Recall@1:  {recall_1:.2%}")
    print(f"  Recall@3:  {recall_3:.2%}")
    print(f"  Recall@5:  {recall_5:.2%}")
    print(f"  Recall@10: {recall_10:.2%}")
    print(f"  MRR:       {mrr:.4f}")
    print(f"  平均响应时间: {avg_time*1000:.2f}ms")
    
    print("=" * 60)
    
    return {
        "recall_at_1": recall_1,
        "recall_at_3": recall_3,
        "recall_at_5": recall_5,
        "recall_at_10": recall_10,
        "mrr": mrr,
        "avg_response_time_ms": avg_time * 1000,
        "method": "text-embedding-3-small + query_rewrite"
    }


if __name__ == "__main__":
    result = run_recall_test()
    
    result_file = Path(__file__).parent / "recall_result_v11.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n结果已保存到: {result_file}")
