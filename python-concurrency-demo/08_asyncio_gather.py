#!/usr/bin/env python3
"""
并发执行多个协程
================

知识点：
1. asyncio.gather() - 并发执行多个协程
2. asyncio.wait() - 更灵活的等待方式
3. asyncio.as_completed() - 按完成顺序获取结果
4. asyncio.TaskGroup - Python 3.11+ 任务组
"""

import asyncio
import time
import random


# ============================================================
# 示例 1：asyncio.gather() 基本使用
# ============================================================

async def fetch_data(name: str, delay: float) -> str:
    """
    模拟异步获取数据
    
    Args:
        name: 数据名称
        delay: 模拟网络延迟
    
    Returns:
        获取的数据
    """
    print(f"  [{name}] 开始获取，预计 {delay:.1f}s")
    await asyncio.sleep(delay)  # 模拟网络请求
    print(f"  [{name}] 获取完成")
    return f"{name} 的数据"


async def demo_gather():
    """演示 asyncio.gather()"""
    print("=" * 60)
    print("示例 1：asyncio.gather() 并发执行")
    print("=" * 60)
    
    start = time.time()
    
    # gather() 并发执行多个协程
    # 返回结果列表，顺序与传入顺序一致
    results = await asyncio.gather(
        fetch_data("API-1", 1.0),
        fetch_data("API-2", 0.5),
        fetch_data("API-3", 0.8),
        fetch_data("API-4", 0.3),
    )
    
    elapsed = time.time() - start
    print(f"\n总耗时: {elapsed:.2f}s")
    print(f"结果: {results}")
    print("注意：总耗时 ≈ 最长的任务时间，而不是所有任务时间之和")


# ============================================================
# 示例 2：gather() 异常处理
# ============================================================

async def may_fail(name: str, fail: bool):
    """可能失败的任务"""
    await asyncio.sleep(0.5)
    if fail:
        raise ValueError(f"{name} 失败了！")
    return f"{name} 成功"


async def demo_gather_exception():
    """演示 gather() 异常处理"""
    print("\n" + "=" * 60)
    print("示例 2：gather() 异常处理")
    print("=" * 60)
    
    # 默认：第一个异常会传播，其他任务继续执行但结果丢失
    print("\n--- 默认行为（return_exceptions=False）---")
    try:
        results = await asyncio.gather(
            may_fail("任务A", False),
            may_fail("任务B", True),   # 这个会失败
            may_fail("任务C", False),
        )
    except ValueError as e:
        print(f"捕获异常: {e}")
    
    # return_exceptions=True：异常作为结果返回，不抛出
    print("\n--- return_exceptions=True ---")
    results = await asyncio.gather(
        may_fail("任务A", False),
        may_fail("任务B", True),   # 这个会失败
        may_fail("任务C", False),
        return_exceptions=True,    # 异常作为结果返回
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  任务{i+1}: 失败 - {result}")
        else:
            print(f"  任务{i+1}: 成功 - {result}")


# ============================================================
# 示例 3：asyncio.wait() 更灵活的等待
# ============================================================

async def demo_wait():
    """演示 asyncio.wait()"""
    print("\n" + "=" * 60)
    print("示例 3：asyncio.wait() 灵活等待")
    print("=" * 60)
    
    # 创建任务
    tasks = [
        asyncio.create_task(fetch_data(f"任务{i}", random.uniform(0.3, 1.0)))
        for i in range(5)
    ]
    
    # wait() 返回两个集合：已完成 和 未完成
    # return_when 参数：
    # - ALL_COMPLETED: 等待所有完成（默认）
    # - FIRST_COMPLETED: 第一个完成就返回
    # - FIRST_EXCEPTION: 第一个异常就返回
    
    print("\n--- 等待第一个完成 ---")
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"已完成: {len(done)} 个")
    print(f"未完成: {len(pending)} 个")
    
    # 获取已完成任务的结果
    for task in done:
        print(f"  结果: {task.result()}")
    
    # 取消未完成的任务
    for task in pending:
        task.cancel()
    
    print("已取消未完成的任务")


# ============================================================
# 示例 4：asyncio.as_completed() 按完成顺序
# ============================================================

async def demo_as_completed():
    """演示 asyncio.as_completed()"""
    print("\n" + "=" * 60)
    print("示例 4：as_completed() 按完成顺序获取")
    print("=" * 60)
    
    tasks = [
        asyncio.create_task(fetch_data(f"任务{i}", random.uniform(0.3, 1.0)))
        for i in range(5)
    ]
    
    print("按完成顺序获取结果:")
    
    # as_completed() 返回一个迭代器，按完成顺序产生 future
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  完成: {result}")


# ============================================================
# 示例 5：asyncio.TaskGroup (Python 3.11+)
# ============================================================

async def demo_task_group():
    """演示 TaskGroup（Python 3.11+）"""
    print("\n" + "=" * 60)
    print("示例 5：TaskGroup 任务组 (Python 3.11+)")
    print("=" * 60)
    
    results = []
    
    async def worker(name: str):
        result = await fetch_data(name, random.uniform(0.3, 0.8))
        results.append(result)
    
    # TaskGroup 会自动管理任务
    # 如果任何任务失败，会取消其他任务
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(worker(f"任务{i}"))
    
    print(f"\n所有任务完成: {results}")


# ============================================================
# 示例 6：超时控制
# ============================================================

async def demo_timeout():
    """演示超时控制"""
    print("\n" + "=" * 60)
    print("示例 6：超时控制")
    print("=" * 60)
    
    # 方式 1：asyncio.wait_for()
    print("\n--- wait_for() 超时 ---")
    try:
        result = await asyncio.wait_for(
            fetch_data("慢任务", 5.0),
            timeout=1.0
        )
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("任务超时！")
    
    # 方式 2：asyncio.timeout() 上下文管理器 (Python 3.11+)
    print("\n--- timeout() 上下文管理器 ---")
    try:
        async with asyncio.timeout(1.0):
            await fetch_data("另一个慢任务", 5.0)
    except asyncio.TimeoutError:
        print("任务超时！")


# ============================================================
# 示例 7：实际应用 - 并发请求多个 API
# ============================================================

async def fetch_url(url: str) -> dict:
    """
    模拟异步 HTTP 请求
    
    在实际应用中，可以使用 aiohttp 库
    """
    print(f"  请求: {url}")
    await asyncio.sleep(random.uniform(0.2, 0.8))  # 模拟网络延迟
    return {"url": url, "status": 200, "data": f"来自 {url} 的数据"}


async def demo_concurrent_requests():
    """演示并发请求多个 API"""
    print("\n" + "=" * 60)
    print("示例 7：并发请求多个 API")
    print("=" * 60)
    
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/likes",
    ]
    
    start = time.time()
    
    # 并发请求所有 API
    results = await asyncio.gather(*[
        fetch_url(url) for url in urls
    ])
    
    elapsed = time.time() - start
    
    print(f"\n请求完成，耗时: {elapsed:.2f}s")
    for result in results:
        print(f"  {result['url']}: {result['status']}")


# ============================================================
# 主程序
# ============================================================

async def main():
    """主协程"""
    # gather 基本使用
    await demo_gather()
    
    # gather 异常处理
    await demo_gather_exception()
    
    # wait 灵活等待
    await demo_wait()
    
    # as_completed 按完成顺序
    await demo_as_completed()
    
    # TaskGroup
    await demo_task_group()
    
    # 超时控制
    await demo_timeout()
    
    # 并发请求
    await demo_concurrent_requests()


if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. gather() 并发执行多个协程，结果按传入顺序返回")
    print("2. return_exceptions=True 可以捕获异常而不抛出")
    print("3. wait() 更灵活，可以等待第一个完成或全部完成")
    print("4. as_completed() 按完成顺序获取结果")
    print("5. TaskGroup (Python 3.11+) 自动管理任务组")
    print("6. wait_for() 和 timeout() 用于超时控制")
    print("=" * 60)