#!/usr/bin/env python3
"""
处理 CRAG Task 1 & 2 数据集

数据格式：每行一个 JSON 对象，包含：
- question: 问题
- answer: 答案
- search_results: 检索结果列表
"""
import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_html(html_content):
    """清理 HTML 内容，提取纯文本"""
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # 移除 script 和 style 标签
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text)
        return text
    except:
        # 如果 BeautifulSoup 失败，使用简单正则
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


def process_crag_data(input_file, output_dir, max_docs=100, max_questions=50):
    """
    处理 CRAG 数据
    
    Args:
        input_file: 输入的 jsonl 文件
        output_dir: 输出目录
        max_docs: 最大文档数量（用于 Demo）
        max_questions: 最大问题数量
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    documents = {}  # 使用 dict 去重
    questions = []
    
    print(f"处理文件: {input_file}")
    print(f"最大文档数: {max_docs}, 最大问题数: {max_questions}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if len(questions) >= max_questions:
                break
                
            try:
                data = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            
            # 提取问题 (CRAG 使用 'query' 字段)
            question = data.get('query', '') or data.get('question', '')
            if not question:
                continue
            
            # 提取答案
            answer = data.get('answer', '')
            
            # 提取检索结果作为文档
            search_results = data.get('search_results', [])
            expected_doc = None
            
            for idx, result in enumerate(search_results):
                page_url = result.get('page_url', '')
                page_name = result.get('page_name', '')
                page_result = result.get('page_result', '')  # HTML 内容
                page_snippet = result.get('page_snippet', '')
                
                if not page_url:
                    continue
                
                # 使用 URL hash 作为文档 ID
                doc_id = f"doc_{hash(page_url) % 100000}"
                
                # 清理内容：优先使用 snippet，否则清理 HTML
                if page_snippet and len(page_snippet) > 50:
                    content = page_snippet
                elif page_result:
                    content = clean_html(page_result)
                else:
                    continue
                
                if len(content) < 100:  # 跳过太短的内容
                    continue
                
                if doc_id not in documents and len(documents) < max_docs:
                    documents[doc_id] = {
                        'id': doc_id,
                        'source': page_url,
                        'title': page_name,
                        'content': content[:3000]  # 限制长度
                    }
                
                # 记录第一个相关文档
                if expected_doc is None and doc_id in documents:
                    expected_doc = doc_id
            
            if expected_doc:
                questions.append({
                    'question': question,
                    'answer': answer[:500] if answer else '',
                    'expected_doc': expected_doc
                })
            
            if line_num % 100 == 0:
                print(f"  已处理 {line_num} 行, 文档数: {len(documents)}, 问题数: {len(questions)}")
    
    # 保存文档
    docs_dir = output_dir / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    for doc_id, doc in documents.items():
        doc_file = docs_dir / f"{doc_id.replace('/', '_')}.txt"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {doc['title']}\n\n")
            f.write(f"Source: {doc['source']}\n\n")
            f.write(doc['content'])
    
    # 保存问题集
    questions_file = output_dir / 'questions.json'
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成!")
    print(f"  文档数: {len(documents)}")
    print(f"  问题数: {len(questions)}")
    print(f"  文档目录: {docs_dir}")
    print(f"  问题文件: {questions_file}")
    
    return documents, questions


if __name__ == '__main__':
    input_file = Path.home() / 'CodeFolder' / 'data' / 'crag_task_1_and_2_dev_v4.jsonl'
    output_dir = Path.home() / 'CodeFolder' / 'rag-demo' / 'backend' / 'data' / 'crag'
    
    # 先尝试安装 BeautifulSoup
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        import subprocess
        print("安装 beautifulsoup4...")
        subprocess.run(['pip', 'install', 'beautifulsoup4', '-q'], check=True)
        from bs4 import BeautifulSoup
    
    process_crag_data(input_file, output_dir, max_docs=100, max_questions=50)
