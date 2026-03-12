#!/usr/bin/env python3
"""
RAG 召回率测试 - 重排序优化版

优化策略：
1. 混合检索获取候选文档
2. 使用 cross-encoder 重排序
3. 提升正确答案的排名位置，优化 MRR
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
    
    # 使用更大的 embedding 模型
    kwargs = {"model": "text-embedding-3-large", "openai_api_key": api_key}
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def load_vectorstore() -> Chroma:
    persist_dir = backend_dir / "vectordb_large"
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name="crag_collection",
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


def hybrid_search_with_scores(vectorstore: Chroma, query: str, k: int = 20) -> List[Tuple]:
    """混合检索，返回带分数的结果"""
    # 1. 相似度检索 (带分数)
    sim_results = vectorstore.similarity_search_with_score(query, k=k)
    
    # 2. MMR 检索
    mmr_results = vectorstore.max_marginal_relevance_search(
        query, k=k//2, fetch_k=k*2, lambda_mult=0.7
    )
    
    # 3. 合并去重
    seen_sources = set()
    combined = []
    
    # 相似度结果带分数
    for doc, score in sim_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append((doc, score, "sim"))
    
    # MMR 结果给一个默认分数
    for doc in mmr_results:
        source = doc.metadata.get("source", "")
        if source not in seen_sources:
            seen_sources.add(source)
            combined.append((doc, 999, "mmr"))  # 999 表示无分数
    
    return combined[:k]


def rerank_with_llm(query: str, candidates: List[Tuple], top_k: int = 10) -> List:
    """
    使用 LLM 对候选文档进行重排序
    
    由于没有 cross-encoder，使用 LLM 来判断相关性
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    
    # 准备候选文档文本
    docs_text = []
    for i, (doc, score, source) in enumerate(candidates[:top_k*2]):
        content = doc.page_content[:500]  # 截取前500字符
        docs_text.append(f"[{i}] {content}")
    
    docs_block = "\n\n---\n\n".join(docs_text)
    
    # 使用 DeepSeek API
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0,
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个文档相关性评估专家。给定一个查询和多个候选文档，你需要：
1. 评估每个文档与查询的相关性（0-10分）
2. 返回最相关的文档索引列表，按相关性降序排列

只返回 JSON 格式：{{"rankings": [索引列表]}}
例如：{{"rankings": [2, 0, 5, 1, 3]}}"""),
        ("user", """查询：{query}

候选文档：
{docs}

请返回最相关的文档索引列表（最多{top_k}个）：""")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "query": query,
            "docs": docs_block,
            "top_k": top_k
        })
        
        import re
        match = re.search(r'\{[^}]+\}', response.content)
        if match:
            result = json.loads(match.group())
            rankings = result.get("rankings", [])
            
            # 按重排序结果重新排列
            reranked = []
            for idx in rankings[:top_k]:
                if 0 <= idx < len(candidates):
                    reranked.append(candidates[idx][0])
            
            # 如果重排序结果不足，补充原始排序
            seen = set()
            for doc in reranked:
                seen.add(doc.metadata.get("source", ""))
            
            for doc, score, source in candidates:
                if len(reranked) >= top_k:
                    break
                src = doc.metadata.get("source", "")
                if src not in seen:
                    reranked.append(doc)
                    seen.add(src)
            
            return reranked
    except Exception as e:
        print(f"    重排序失败: {e}")
    
    # 失败时返回原始排序
    return [doc for doc, _, _ in candidates[:top_k]]


def run_recall_test():
    print("=" * 60)
    print("RAG 召回率测试 - 重排序优化版")
    print("=" * 60)
    
    test_questions = load_test_questions()
    print(f"\n共 {len(test_questions)} 个测试问题")
    
    vectorstore = load_vectorstore()
    print("✅ 向量数据库加载成功 (text-embedding-3-large)")
    
    all_results = []
    all_expected = []
    response_times = []
    
    print("\n开始测试（混合检索 + LLM 重排序）...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        start_time = time.time()
        try:
            # 混合检索获取候选
            candidates = hybrid_search_with_scores(vectorstore, question, k=20)
            
            # LLM 重排序
            results = rerank_with_llm(question, candidates, top_k=10)
            
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
        print(f"  [{i:2d}] {status} \"{q_display}\" → 排名: {rank if found else '未找到'}, 耗时: {elapsed:.2f}s")
    
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
    print(f"  平均响应时间: {avg_time:.2f}s")
    
    print("=" * 60)
    
    return {
        "recall_at_1": recall_1,
        "recall_at_3": recall_3,
        "recall_at_5": recall_5,
        "recall_at_10": recall_10,
        "mrr": mrr,
        "avg_response_time_s": avg_time,
        "total_questions": len(test_questions),
        "tested_questions": len(all_results),
    }


if __name__ == "__main__":
    result = run_recall_test()
    
    result_file = Path(__file__).parent / "recall_result_rerank.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n结果已保存到: {result_file}")