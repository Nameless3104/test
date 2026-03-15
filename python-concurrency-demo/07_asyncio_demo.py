#!/usr/bin/env python3
"""
异步编程基础 (asyncio)
====================

知识点：
1. async/await 语法
2. 协程的概念
3. 事件循环
4. async with 和 async for
"""

import asyncio
import time


# ============================================================
# 示例 1：第一个协程
# ============================================================

async def hello():
    """
    异步函数（协程）
    
    使用 async def 定义的函数是协程函数
    调用协程函数返回协程对象，不会立即执行
    """
    print("Hello")
    # await 暂停当前协程，等待其他操作完成
    # asyncio.sleep 是异步的 sleep，不会阻塞线程
    await asyncio.sleep(1)
    print("World")


async def demo_first_coroutine():
    """演示第一个协程"""
    print("=" * 60)
    print("示例 1：第一个协程")
    print("=" * 60)
    
    # 调用协程函数返回协程对象
    coro = hello()
    print(f"协程对象: {coro}")
    
    # 使用 await 执行协程
    await hello()


# ============================================================
# 示例 2：协程 vs 普通函数
# ============================================================

def sync_task(name: str, duration: float):
    """同步函数 - 会阻塞"""
    print(f"  [{name}] 开始")
    time.sleep(duration)  # 阻塞整个线程
    print(f"  [{name}] 结束")


async def async_task(name: str, duration: float):
    """异步函数 - 不阻塞"""
    print(f"  [{name}] 开始")
    await asyncio.sleep(duration)  # 不阻塞，允许其他协程执行
    print(f"  [{name}] 结束")


async def demo_sync_vs_async():
    """对比同步和异步"""
    print("\n" + "=" * 60)
    print("示例 2：同步 vs 异步")
    print("=" * 60)
    
    # 同步执行
    print("\n--- 同步执行（阻塞）---")
    start = time.time()
    sync_task("A", 0.5)
    sync_task("B", 0.5)
    sync_task("C", 0.5)
    print(f"总耗时: {time.time() - start:.2f}s")
    print("同步执行：任务依次执行，总时间 = 所有任务时间之和")
    
    # 异步执行
    print("\n--- 异步执行（非阻塞）---")
    start = time.time()
    # 并发执行多个协程
    await asyncio.gather(
        async_task("A", 0.5),
        async_task("B", 0.5),
        async_task("C", 0.5),
    )
    print(f"总耗时: {time.time() - start:.2f}s")
    print("异步执行：任务并发执行，总时间 ≈ 最长任务时间")


# ============================================================
# 示例 3：事件循环
# ============================================================

async def simple_task(name: str):
    """简单任务"""
    print(f"  [{name}] 执行中...")
    await asyncio.sleep(0.1)
    return f"{name} 的结果"


def demo_event_loop():
    """演示事件循环"""
    print("\n" + "=" * 60)
    print("示例 3：事件循环")
    print("=" * 60)
    
    print("""
事件循环是 asyncio 的核心：
┌─────────────────────────────────────────────────────────┐
│                    事件循环 (Event Loop)                 │
├─────────────────────────────────────────────────────────┤
│  1. 管理所有协程的执行                                   │
│  2. 当协程 await 时，切换到其他就绪的协程                 │
│  3. 当 await 的操作完成时，恢复协程执行                   │
│  4. 单线程，协作式调度                                   │
└─────────────────────────────────────────────────────────┘

运行协程的方式：
1. asyncio.run(coro)        - Python 3.7+，推荐方式
2. loop.run_until_complete() - 低级 API
""")
    
    # 方式 1：asyncio.run()（推荐）
    print("--- 方式 1：asyncio.run() ---")
    result = asyncio.run(simple_task("任务A"))
    print(f"结果: {result}")


# ============================================================
# 示例 4：async with 异步上下文管理器
# ============================================================

class AsyncTimer:
    """
    异步上下文管理器
    
    实现 __aenter__ 和 __aexit__ 方法
    """
    
    async def __aenter__(self):
        print("  进入上下文")
        self.start = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        print(f"  退出上下文，耗时: {elapsed:.2f}s")
        return False  # 不抑制异常


async def demo_async_with():
    """演示 async with"""
    print("\n" + "=" * 60)
    print("示例 4：async with 异步上下文管理器")
    print("=" * 60)
    
    async with AsyncTimer() as timer:
        print("  执行一些异步操作...")
        await asyncio.sleep(0.5)
        print("  操作完成")


# ============================================================
# 示例 5：async for 异步迭代器
# ============================================================

class AsyncCounter:
    """
    异步迭代器
    
    实现 __aiter__ 和 __anext__ 方法
    """
    
    def __init__(self, count: int):
        self.count = count
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.count:
            raise StopAsyncIteration
        
        self.current += 1
        await asyncio.sleep(0.1)  # 模拟异步操作
        return self.current


async def demo_async_for():
    """演示 async for"""
    print("\n" + "=" * 60)
    print("示例 5：async for 异步迭代器")
    print("=" * 60)
    
    print("异步迭代:")
    async for num in AsyncCounter(5):
        print(f"  数字: {num}")


# ============================================================
# 示例 6：创建任务
# ============================================================

async def background_task(name: str, duration: float):
    """后台任务"""
    print(f"  [{name}] 开始")
    await asyncio.sleep(duration)
    print(f"  [{name}] 完成")
    return f"{name} 的结果"


async def demo_create_task():
    """演示创建任务"""
    print("\n" + "=" * 60)
    print("示例 6：创建任务 (asyncio.create_task)")
    print("=" * 60)
    
    # create_task() 将协程包装成 Task 对象，立即调度执行
    task1 = asyncio.create_task(background_task("任务A", 1.0))
    task2 = asyncio.create_task(background_task("任务B", 0.5))
    
    print("任务已创建，可以做其他事...")
    await asyncio.sleep(0.2)
    print("其他事做完了，等待任务完成...")
    
    # 等待任务完成
    result1 = await task1
    result2 = await task2
    
    print(f"结果: {result1}, {result2}")


# ============================================================
# 示例 7：协程的状态
# ============================================================

async def state_demo():
    """演示协程状态"""
    print("\n" + "=" * 60)
    print("示例 7：协程/任务的状态")
    print("=" * 60)
    
    async def pending_task():
        await asyncio.sleep(1)
        return "完成"
    
    # 创建任务
    task = asyncio.create_task(pending_task())
    
    print(f"创建后: done={task.done()}, cancelled={task.cancelled()}")
    
    # 等待一小段时间
    await asyncio.sleep(0.1)
    print(f"执行中: done={task.done()}, cancelled={task.cancelled()}")
    
    # 等待完成
    result = await task
    print(f"完成后: done={task.done()}, cancelled={task.cancelled()}")
    print(f"结果: {result}")


# ============================================================
# 主程序
# ============================================================

async def main():
    """主协程"""
    # 第一个协程
    await demo_first_coroutine()
    
    # 同步 vs 异步
    await demo_sync_vs_async()
    
    # async with
    await demo_async_with()
    
    # async for
    await demo_async_for()
    
    # 创建任务
    await demo_create_task()
    
    # 协程状态
    await state_demo()


if __name__ == "__main__":
    # 演示事件循环（同步方式）
    demo_event_loop()
    
    # 运行主协程
    asyncio.run(main())
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. async def 定义协程函数，await 执行协程")
    print("2. 协程是单线程的，通过协作式调度实现并发")
    print("3. asyncio.run() 是运行协程的推荐方式")
    print("4. create_task() 创建任务，立即调度执行")
    print("5. async with 和 async for 支持异步上下文和迭代")
    print("=" * 60)