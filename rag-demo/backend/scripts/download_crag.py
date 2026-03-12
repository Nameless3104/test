#!/usr/bin/env python3
"""
下载 CRAG 数据集 - 使用直接 HTTP 请求
"""
import os
import json
import requests
from pathlib import Path

def download_crag():
    """下载 CRAG 数据集"""
    
    # 数据目录
    data_dir = Path.home() / "CodeFolder" / "rag-demo" / "backend" / "data" / "crag"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("正在下载 CRAG 数据集...")
    
    # CRAG 数据在 Hugging Face 上的位置
    # 格式: https://huggingface.co/datasets/Quivr/CRAG/resolve/main/crag_1.json
    base_url = "https://huggingface.co/datasets/Quivr/CRAG/resolve/main"
    
    all_data = []
    
    # 尝试下载多个文件
    for i in range(1, 4):  # crag_1.json, crag_2.json, crag_3.json
        url = f"{base_url}/crag_{i}.json"
        print(f"  尝试下载: {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                data = response.json()
                all_data.extend(data if isinstance(data, list) else [data])
                print(f"    ✅ 成功下载 crag_{i}.json")
            else:
                print(f"    ❌ 状态码: {response.status_code}")
        except Exception as e:
            print(f"    ❌ 下载失败: {e}")
    
    if all_data:
        # 保存合并的数据
        output_file = data_dir / "crag_raw.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 数据已保存到: {output_file}")
        print(f"   总条目数: {len(all_data)}")
        return all_data
    
    return None


def process_crag_data(raw_data):
    """处理 CRAG 数据，提取文档和问题"""
    
    data_dir = Path.home() / "CodeFolder" / "rag-demo" / "backend" / "data" / "crag"
    
    documents = []
    questions = []
    
    for item in raw_data:
        # 提取文档内容
        if "content" in item:
            doc_id = item.get("id", f"doc_{len(documents)}")
            doc_file = data_dir / f"{doc_id}.txt"
            with open(doc_file, "w", encoding="utf-8") as f:
                f.write(item["content"])
            documents.append({
                "id": doc_id,
                "source": str(doc_file.name)
            })
        
        # 提取问题
        if "question" in item:
            questions.append({
                "question": item["question"],
                "answer": item.get("answer", ""),
                "expected_doc": item.get("id", "")
            })
    
    # 保存问题集
    questions_file = data_dir / "questions.json"
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成:")
    print(f"  文档数: {len(documents)}")
    print(f"  问题数: {len(questions)}")
    
    return documents, questions


if __name__ == "__main__":
    raw_data = download_crag()
    
    if raw_data:
        process_crag_data(raw_data)
    else:
        print("\n❌ 下载失败，请检查网络连接或手动下载")
        print("\n手动下载方式:")
        print("1. 访问 https://huggingface.co/datasets/Quivr/CRAG")
        print("2. 下载数据文件")
        print("3. 放到 ~/CodeFolder/rag-demo/backend/data/crag/ 目录")
