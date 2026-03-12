#!/usr/bin/env python3
"""
RAG 召回率测试 - 分数分析版

分析相似度分数分布，找出重排序策略
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
    
    kwargs = {"model": "text-embedding-ada-002", "openai_api_key": api_key}
    if base_url:
        kwargs["openai_api_base"] = base_url
    
    return OpenAIEmbeddings(**kwargs)


def load_vectorstore() -> Chroma:
    persist_dir = backend_dir / "vectordb"
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name="crag_collection",
    )


def analyze_scores():
    print("=" * 60)
    print("RAG 分数分析 - 找出重排序策略")
    print("=" * 60)
    
    test_questions = load_test_questions()
    vectorstore = load_vectorstore()
    
    # 分析前 10 个问题的分数分布
    print("\n分析正确答案的分数分布...")
    print("-" * 60)
    
    correct_scores = []
    incorrect_scores = []
    rank_distributions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, '6-10': 0, 'not_found': 0}
    
    for i, test_case in enumerate(test_questions, 1):
        question = test_case["question"]
        expected_doc = test_case["expected_doc"]
        
        results = vectorstore.similarity_search_with_score(question, k=20)
        
        found = False
        for rank, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get("source", "")
            doc_name = Path(source).stem
            
            if expected_doc == doc_name:
                found = True
                correct_scores.append((rank, score))
                if rank <= 5:
                    rank_distributions[rank] += 1
                elif rank <= 10:
                    rank_distributions['6-10'] += 1
                break
            else:
                if rank <= 5:
                    incorrect_scores.append(score)
        
        if not found:
            rank_distributions['not_found'] += 1
    
    print("\n正确答案排名分布:")
    for k, v in rank_distributions.items():
        print(f"  排名 {k}: {v} 个")
    
    if correct_scores:
        print(f"\n正确答案的分数范围:")
        scores = [s for _, s in correct_scores]
        print(f"  最小: {min(scores):.4f}")
        print(f"  最大: {max(scores):.4f}")
        print(f"  平均: {sum(scores)/len(scores):.4f}")
    
    if incorrect_scores:
        print(f"\n前5名错误答案的分数范围:")
        print(f"  最小: {min(incorrect_scores):.4f}")
        print(f"  最大: {max(incorrect_scores):.4f}")
        print(f"  平均: {sum(incorrect_scores)/len(incorrect_scores):.4f}")
    
    # 分析：如果正确答案和错误答案分数接近，说明需要重排序
    print("\n" + "=" * 60)
    
    return correct_scores, incorrect_scores


if __name__ == "__main__":
    analyze_scores()
