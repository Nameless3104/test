#!/usr/bin/env python3
"""
API 功能测试

测试 RAG Demo 的 REST API 接口
"""
import requests
import json
from typing import Dict, Any

# API 基础地址
API_BASE_URL = "http://localhost:8000/api"


def test_health():
    """测试服务健康状态"""
    print("\n[测试] 服务健康检查")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            print("  ✅ 服务运行正常")
            return True
        else:
            print(f"  ❌ 服务异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ❌ 无法连接到服务，请确保后端已启动")
        return False
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_chat_endpoint():
    """测试聊天接口"""
    print("\n[测试] 聊天接口 /api/chat/")
    
    test_questions = [
        "What is Django?",
        "What is RAG?",
        "How does LangChain work?",
    ]
    
    for question in test_questions:
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/",
                json={"question": question},
                timeout=30,
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")[:100]
                print(f"  ✅ Q: \"{question[:30]}...\"")
                print(f"     A: {answer}...")
            else:
                print(f"  ❌ 请求失败: {response.status_code}")
                print(f"     响应: {response.text[:200]}")
        except Exception as e:
            print(f"  ❌ 测试失败: {e}")
    
    return True


def test_documents_endpoint():
    """测试文档列表接口"""
    print("\n[测试] 文档列表接口 /api/documents/")
    
    try:
        response = requests.get(f"{API_BASE_URL}/documents/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get("documents", [])
            print(f"  ✅ 获取文档列表成功，共 {len(docs)} 个文档")
            for doc in docs[:5]:
                print(f"     - {doc}")
            return True
        else:
            print(f"  ❌ 请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def run_api_tests():
    """运行所有 API 测试"""
    print("=" * 60)
    print("RAG Demo API 功能测试")
    print("=" * 60)
    print(f"API 地址: {API_BASE_URL}")
    
    results = {
        "health": test_health(),
        "chat": test_chat_endpoint(),
        "documents": test_documents_endpoint(),
    }
    
    print("\n" + "=" * 60)
    print("测试摘要:")
    print("-" * 40)
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(results.values())
    print("=" * 60)
    print(f"总体结果: {'✅ 全部通过' if all_passed else '❌ 存在失败'}")
    
    return results


if __name__ == "__main__":
    run_api_tests()
