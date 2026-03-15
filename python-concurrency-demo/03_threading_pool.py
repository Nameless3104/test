#!/usr/bin/env python3
"""
线程池
======

知识点：
1. ThreadPoolExecutor 基本使用
2. submit() 提交单个任务
3. map() 批量提交任务
4. as_completed() 获取完成的任务
5. Future 对象
"""

import concurrent.futures
import time
import random


# ============================================================
# 示例 1：ThreadPoolExecutor 基本使用
# ============================================================

def task(name: str, duration: float) -> str:
    """
    模拟一个耗时任务
    
    Args:
        name: 任务名称
        duration: 执行时长
    
    Returns:
        任务结果
    """
    print(f"[{name}] 开始执行，预计耗时 {duration:.1f}s")
    time.sleep(duration)  # 模拟耗时操作
    print(f"[{name}] 执行完毕")
    return f"{name} 的结果"


def demo_basic_pool():
    """演示线程池基本使用"""
    print("=" * 60)
    print("示例 1：ThreadPoolExecutor 基本使用")
    print("=" * 60)
    
    # 创建线程池
    # max_workers: 最大线程数
    # with 语句确保线程池正确关闭
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        
        # 方式 1：submit() 提交单个任务
        # 返回 Future 对象，代表一个尚未完成的操作
        future1 = executor.submit(task, "任务A", 1.0)
        future2 = executor.submit(task, "任务B", 0.5)
        future3 = executor.submit(task, "任务C", 0.8)
        
        # Future 对象的方法：
        # - result(): 获取结果（会阻塞直到任务完成）
        # - done(): 检查是否完成
        # - cancel(): 尝试取消任务
        # - exception(): 获取异常
        
        print(f"\n任务A 是否完成: {future1.done()}")
        
        # 获取结果（会阻塞）
        result1 = future1.result()
        result2 = future2.result()
        result3 = future3.result()
        
        print(f"\n结果: {result1}, {result2}, {result3}")
        print(f"任务A 是否完成: {future1.done()}")


# ============================================================
# 示例 2：使用 map() 批量提交任务
# ============================================================

def process_item(item: int) -> int:
    """处理单个数据项"""
    print(f"  处理项目 {item}")
    time.sleep(random.random() * 0.5)
    return item * item  # 返回平方


def demo_map():
    """演示使用 map() 批量处理"""
    print("\n" + "=" * 60)
    print("示例 2：使用 map() 批量提交任务")
    print("=" * 60)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # map() 返回结果的迭代器
        # 注意：结果顺序与输入顺序一致（即使任务完成顺序不同）
        results = executor.map(process_item, data)
        
        print("结果（按输入顺序）:")
        for item, result in zip(data, results):
            print(f"  {item}² = {result}")


# ============================================================
# 示例 3：使用 as_completed() 获取完成的任务
# ============================================================

def fetch_url(url: str) -> tuple:
    """模拟获取 URL 内容"""
    duration = random.random() * 2
    time.sleep(duration)
    return (url, f"内容-{url}", duration)


def demo_as_completed():
    """演示 as_completed() - 按完成顺序获取结果"""
    print("\n" + "=" * 60)
    print("示例 3：as_completed() 按完成顺序获取结果")
    print("=" * 60)
    
    urls = [
        "https://api.example.com/1",
        "https://api.example.com/2",
        "https://api.example.com/3",
        "https://api.example.com/4",
        "https://api.example.com/5",
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 使用字典保存 future 和 URL 的对应关系
        future_to_url = {
            executor.submit(fetch_url, url): url 
            for url in urls
        }
        
        print("按完成顺序获取结果:")
        
        # as_completed() 返回一个迭代器，按完成顺序产生 future
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result_url, content, duration = future.result()
                print(f"  完成: {result_url} (耗时 {duration:.2f}s)")
            except Exception as e:
                print(f"  失败: {url}, 错误: {e}")


# ============================================================
# 示例 4：异常处理
# ============================================================

def may_fail(x: int) -> int:
    """可能失败的任务"""
    if x == 3:
        raise ValueError(f"项目 {x} 处理失败！")
    time.sleep(0.5)
    return x * 10


def demo_exception_handling():
    """演示异常处理"""
    print("\n" + "=" * 60)
    print("示例 4：异常处理")
    print("=" * 60)
    
    items = [1, 2, 3, 4, 5]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(may_fail, x): x for x in items}
        
        for future in concurrent.futures.as_completed(futures):
            x = futures[future]
            try:
                result = future.result()  # 获取结果，如果有异常会在这里抛出
                print(f"  项目 {x} 成功: {result}")
            except ValueError as e:
                print(f"  项目 {x} 失败: {e}")
            except Exception as e:
                print(f"  项目 {x} 未知错误: {e}")


# ============================================================
# 示例 5：超时控制
# ============================================================

def slow_task(name: str) -> str:
    """慢任务"""
    print(f"  [{name}] 开始...")
    time.sleep(3)
    return f"{name} 完成"


def demo_timeout():
    """演示超时控制"""
    print("\n" + "=" * 60)
    print("示例 5：超时控制")
    print("=" * 60)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(slow_task, "慢任务")
        
        try:
            # result(timeout) 设置超时时间
            # 如果超时，抛出 TimeoutError
            result = future.result(timeout=1.0)
            print(f"结果: {result}")
        except TimeoutError:
            print("任务超时！")
            # 注意：超时后任务仍在后台运行
            # 可以调用 cancel() 尝试取消（如果还没开始）
            print(f"任务是否取消: {future.cancel()}")


# ============================================================
# 示例 6：回调函数
# ============================================================

def callback_task(x: int) -> int:
    """带回调的任务"""
    time.sleep(0.5)
    return x * 2


def on_complete(future):
    """任务完成时的回调函数"""
    try:
        result = future.result()
        print(f"  [回调] 任务完成，结果: {result}")
    except Exception as e:
        print(f"  [回调] 任务失败: {e}")


def demo_callback():
    """演示回调函数"""
    print("\n" + "=" * 60)
    print("示例 6：回调函数")
    print("=" * 60)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for i in range(3):
            future = executor.submit(callback_task, i)
            # 添加完成回调
            # 回调会在任务完成后立即调用（在同一个线程中）
            future.add_done_callback(on_complete)
            futures.append(future)
        
        # 等待所有任务完成
        concurrent.futures.wait(futures)


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # 基本使用
    demo_basic_pool()
    
    # map 批量处理
    demo_map()
    
    # as_completed 按完成顺序
    demo_as_completed()
    
    # 异常处理
    demo_exception_handling()
    
    # 超时控制
    demo_timeout()
    
    # 回调函数
    demo_callback()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. ThreadPoolExecutor 管理线程池，避免频繁创建销毁线程")
    print("2. submit() 提交单个任务，返回 Future 对象")
    print("3. map() 批量提交，结果顺序与输入一致")
    print("4. as_completed() 按完成顺序获取结果")
    print("5. Future.result() 可以设置超时