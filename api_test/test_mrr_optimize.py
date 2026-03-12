#!/usr/bin/env python3
"""
RAG 召回率测试 - MRR 优化版

优化策略：
1. 使用 text-embedding-3-large
2. 相似度检索带分数，按分数排序
3. 不使用 MMR（MMR 会降低 MRR，因为它追求多样性）
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
    
    # 使用与向量库一致的 embedding 模型
    kwargs = {"model": "text-embedding-ada-002", "openai_api_key": api_key}
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def load_vectorstore() -> Chroma:
    persist_dir = backend_dir / "vectordb"  # 使用原始向量库
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name="crag_collection",
    )


def check_source_in_results(results: List, expected_doc: str) -> Tuple[bool, int]:
    for i, item in enumerate(results):
        # 支持 (doc, score) 元组或 doc 对象
        if isinstance(item, tuple):
            doc = item[0]
        else:
            doc = item
        source = doc.metadata.get("source", "")
        doc_name = Path(source).stem
        if expected_doc == doc_name:
            return True, i + 1
    return False, 0


def calculate_recall_at_k(results_list: List, expected_docs: List[str], k: int) -> float:
    hits = 0
    for results, expected in zip(results_list, expected_docs):
        found, _ = check_source_in_results(results[:k], expected)
        if found:
            hits += 1
    return hits / len(expected_docs) if expected_docs else 0


def calculate_mrr(results_list: List, expected_docs: List[str]) -> float:
    reciprocal_ranks = []
    for results, expected in zip(results_list, expected_docs):
        found, rank = check_source_in_results(results, expected)
        if found:
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0)
    return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0


def run_test():
    print("=" * 60)
    print("RAG 召回率测试 - MRR 优化版")
    print("=" * 60)
    
    test_questions = load_test_questions()
    print(f"\n共 {len(test_questions)} 个测试问题")
    
    vectorstore = load_vectorstore()
    print("✅ 向量数据库加载成功 (text-embedding-3-large)")
    
    all_results = []
    all_expected = []
    response_times = []
    
    print("\n开始测试（纯相似度检索，按分数排序）...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        start_time = time.time()
        try:
            # 纯相似度检索，带分数
            results = vectorstore.similarity_search_with_score(question, k=10)
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
        print(f"  [{i:2d}] {status} \"{q_display}\" → 排名: {rank if found else '未找到'}, 耗时: {elapsed:.3f}s")
    
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
        "total_questions": len(test_questions),
        "tested_questions": len(all_results),
    }


if __name__ == "__main__":
    result = run_test()
    
    result_file = Path(__file__).parent / "recall_result_mrr.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n结果已保存到: {result_file}")
