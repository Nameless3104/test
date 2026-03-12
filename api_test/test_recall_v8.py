#!/usr/bin/env python3
"""
RAG 召回率测试 - 优化版 v8 (带重试机制)

优化目标：MRR 提升到 0.6 以上

策略：
1. 使用更好的 chunk 配置重建向量数据库
2. 添加重试机制避免中断
3. 使用查询扩展 + 重排序
"""
import os
import sys
import json
import time
import random
from pathlib import Path
from typing import List, Tuple

backend_dir = Path(__file__).parent.parent / "rag-demo" / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from langchain_openai import OpenAIEmbeddings

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
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY 未配置")
    
    kwargs = {"model": "text-embedding-ada-002", "openai_api_key": api_key}
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def load_vectorstore() -> Chroma:
    persist_dir = str(backend_dir / "vectordb")
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="crag_collection",
    )


def check_source_in_results(results: List, expected_doc: str) -> Tuple[bool, int]:
    for i, item in enumerate(results):
        if isinstance(item, tuple):
            doc = item[0]
        else:
            doc = item
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


def search_with_retry(vectorstore, question, k=10, max_retries=3, delay=1.0):
    """
    带重试机制的搜索
    """
    for attempt in range(max_retries):
        try:
            # 使用混合检索
            sim_results = vectorstore.similarity_search_with_score(question, k=k*2)
            mmr_results = vectorstore.max_marginal_relevance_search(
                question, k=k, fetch_k=k*3, lambda_mult=0.7
            )
            
            # 合并去重
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
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"    ⚠️ 重试 {attempt + 1}/{max_retries}: {e}")
                time.sleep(delay * (attempt + 1))
            else:
                raise e
    return []


def run_recall_test():
    print("=" * 60)
    print("RAG 召回率测试 - CRAG Task 1 & 2 (优化版 v8 - 重试机制)")
    print("=" * 60)
    
    test_questions = load_test_questions()
    print(f"\n共 {len(test_questions)} 个测试问题")
    
    vectorstore = load_vectorstore()
    print("✅ 向量数据库加载成功")
    
    all_results = []
    all_expected = []
    response_times = []
    errors = []
    
    print(f"\n开始测试（混合检索 + 重试机制）...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        start_time = time.time()
        try:
            results = search_with_retry(vectorstore, question, k=10)
            elapsed = time.time() - start_time
            response_times.append(elapsed)
            
            # 添加延迟避免限流
            time.sleep(0.3)
            
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
            print(f"  [{i}] ❌ 查询失败: {e}")
            continue
        
        all_results.append(results)
        all_expected.append(expected_doc)
        
        found, rank = check_source_in_results(results, expected_doc)
        status = "✅" if found else "❌"
        
        q_display = question[:50] + "..." if len(question) > 50 else question
        print(f"  [{i:2d}] {status} \"{q_display}\"")
        print(f"        期望: {expected_doc}, 排名: {rank if found else '未找到'}, 耗时: {elapsed:.3f}s")
    
    print("-" * 60)
    
    if errors:
        print(f"\n⚠️ 共 {len(errors)} 个查询失败")
    
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
        "total_questions": len(test_questions),
        "tested_questions": len(all_results),
        "errors": len(errors),
        "method": "hybrid_retry_v8"
    }


if __name__ == "__main__":
    result = run_recall_test()
    
    result_file = Path(__file__).parent / "recall_result_v8.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n结果已保存到: {result_file}")
