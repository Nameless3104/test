#!/usr/bin/env python3
"""
RAG 召回率测试 - 优化版 v10 (查询扩展 + 重排序)

优化目标：MRR 提升到 0.6 以上

策略：
1. 查询扩展：生成多个相关查询
2. 合并多个查询的结果
3. 使用相似度分数进行重排序
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import List, Tuple, Dict

backend_dir = Path(__file__).parent.parent / "rag-demo" / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

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


def expand_query(question: str) -> List[str]:
    """
    查询扩展：生成多个相关查询
    """
    # 简单的查询扩展策略
    queries = [question]
    
    # 提取关键词
    words = question.lower().split()
    
    # 移除常见停用词
    stop_words = {'what', 'which', 'how', 'many', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'did', 'does', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # 创建关键词查询
    if keywords:
        keyword_query = ' '.join(keywords[:5])
        if keyword_query != question.lower():
            queries.append(keyword_query)
    
    return queries


def search_with_expansion(vectorstore, question, k=10):
    """
    使用查询扩展的搜索
    """
    queries = expand_query(question)
    
    # 收集所有结果和分数
    doc_scores: Dict[str, Tuple] = {}  # source -> (doc, min_score)
    
    for query in queries:
        try:
            results = vectorstore.similarity_search_with_score(query, k=k*2)
            for doc, score in results:
                source = doc.metadata.get("source", "")
                if source not in doc_scores or score < doc_scores[source][1]:
                    doc_scores[source] = (doc, score)
        except Exception as e:
            print(f"    ⚠️ 查询扩展失败: {e}")
    
    # 按分数排序
    sorted_results = sorted(doc_scores.values(), key=lambda x: x[1])
    
    return [doc for doc, score in sorted_results[:k]]


def run_recall_test():
    print("=" * 60)
    print("RAG 召回率测试 - CRAG Task 1 & 2 (v10 - 查询扩展)")
    print("=" * 60)
    
    test_questions = load_test_questions()
    print(f"\n共 {len(test_questions)} 个测试问题")
    
    vectorstore = load_vectorstore()
    print("✅ 向量数据库加载成功")
    
    all_results = []
    all_expected = []
    response_times = []
    errors = []
    
    print(f"\n开始测试（查询扩展 + 重排序）...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        start_time = time.time()
        try:
            results = search_with_expansion(vectorstore, question, k=10)
            elapsed = time.time() - start_time
            response_times.append(elapsed)
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
        "method": "query_expansion_v10"
    }


if __name__ == "__main__":
    result = run_recall_test()
    
    result_file = Path(__file__).parent / "recall_result_v10.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n结果已保存到: {result_file}")
