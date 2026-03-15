#!/usr/bin/env python3
"""
异步与同步对比
==============

知识点：
1. 同步代码 vs 异步代码的性能对比
2. 何时使用异步
3. 异步的陷阱
4. 混合同步和异步代码
"""

import asyncio
import time
import threading
import concurrent.futures


# ============================================================
# 示例 1：I/O 密集型任务对比
# ============================================================

def sync_io_task(name: str, duration: float) -> str:
    """同步 I/O 任务"""
    print(f"  [{name}] 开始")
    time.sleep(duration)  # 阻塞
    print(f"  [{name}] 完成")
    return f"{name} 结果"


async def async_io_task(name: str, duration: float) -> str:
    """异步 I/O 任务"""
    print(f"  [{name}] 开始")
    await asyncio.sleep(duration)  # 非阻塞
    print(f"  [{name}] 完成")
    return f"{name} 结果"


def demo_sync_io():
    """同步执行 I/O 任务"""
    print("=" * 60)
    print("示例 1：I/O 密集型任务对比")
    print("=" * 60)
    
    # 同步执行
    print("\n--- 同步执行（阻塞）---")
    start = time.time()
    results = []
    for i in range(5):
        result = sync_io_task(f"任务{i}", 0.5)
        results.append(result)
    sync_time = time.time() - start
    print(f"耗时: {sync_time:.2f}s")


async def demo_async_io():
    """异步执行 I/O 任务"""
    # 异步执行
    print("\n--- 异步执行（非阻塞）---")
    start = time.time()
    results = await asyncio.gather(*[
        async_io_task(f"任务{i}", 0.5) for i in range(5)
    ])
    async_time = time.time() - start
    print(f"耗时: {async_time:.2f}s")


# ============================================================
# 示例 2：CPU 密集型任务 - 异步不适用
# ============================================================

async def cpu_task(name: str, n: int) -> int:
    """
    CPU 密集型任务
    
    注意：异步不适合 CPU 密集型任务！
    因为 CPU 计算会阻塞事件循环
    """
    print(f"  [{name}] 开始计算")
    # 这是 CPU 密集型操作，会阻塞事件循环
    result = sum(i * i for i in range(n))
    print(f"  [{name}] 计算完成")
    return result


async def demo_cpu_bound():
    """演示异步不适合 CPU 密集型任务"""
    print("\n" + "=" * 60)
    print("示例 2：CPU 密集型任务 - 异步不适用")
    print("=" * 60)
    
    print("\n异步执行 CPU 密集型任务:")
    start = time.time()
    
    # 即使使用 gather，CPU 任务也是顺序执行的
    # 因为计算过程阻塞了事件循环
    results = await asyncio.gather(*[
        cpu_task(f"任务{i}", 1_000_000) for i in range(3)
    ])
    
    elapsed = time.time() - start
    print(f"耗时: {elapsed:.2f}s")
    print("注意：CPU 任务阻塞了事件循环，无法并发执行")
    print("解决方案：使用 asyncio.to_thread() 或 ProcessPoolExecutor")


# ============================================================
# 示例 3：在异步中运行同步代码
# ============================================================

def blocking_io(name: str) -> str:
    """
    阻塞的 I/O 操作
    
    例如：requests 库、文件操作等
    """
    print(f"  [{name}] 执行阻塞操作")
    time.sleep(0.5)
    return f"{name} 完成"


async def demo_to_thread():
    """演示 asyncio.to_thread() 在线程中运行同步代码"""
    print("\n" + "=" * 60)
    print("示例 3：asyncio.to_thread() 运行同步代码")
    print("=" * 60)
    
    print("\n使用 to_thread() 在线程池中运行阻塞代码:")
    start = time.time()
    
    # to_thread() 在单独的线程中运行同步函数
    results = await asyncio.gather(*[
        asyncio.to_thread(blocking_io, f"任务{i}")
        for i in range(5)
    ])
    
    elapsed = time.time() - start
    print(f"耗时: {elapsed:.2f}s")
    print("to_thread() 将阻塞操作放到线程池，不阻塞事件循环")


# ============================================================
# 示例 4：在异步中运行 CPU 密集型任务
# ============================================================

def cpu_bound_task(n: int) -> int:
    """CPU 密集型任务"""
    return sum(i * i for i in range(n))


async def demo_cpu_in_async():
    """演示在异步中运行 CPU 密集型任务"""
    print("\n" + "=" * 60)
    print("示例 4：在异步中运行 CPU 密集型任务")
    print("=" * 60)
    
    # 使用 ProcessPoolExecutor
    print("\n使用 ProcessPoolExecutor:")
    start = time.time()
    
    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ProcessPoolExecutor() as pool:
        results = await asyncio.gather(*[
            loop.run_in_executor(pool, cpu_bound_task, 1_000_000)
            for _ in range(4)
        ])
    
    elapsed = time.time() - start
    print(f"耗时: {elapsed:.2f}s")
    print("ProcessPoolExecutor 绕过 GIL，实现真正的并行")


# ============================================================
# 示例 5：异步的陷阱
# ============================================================

async def trap_demo():
    """演示异步编程的常见陷阱"""
    print("\n" + "=" * 60)
    print("示例 5：异步编程的陷阱")
    print("=" * 60)
    
    # 陷阱 1：忘记 await
    print("\n--- 陷阱 1：忘记 await ---")
    
    async def my_coro():
        await asyncio.sleep(0.1)
        return "结果"
    
    # 错误：没有 await，只是创建了协程对象
    coro = my_coro()
    print(f"没有 await: {coro}")  # 打印协程对象，不是结果
    
    # 正确：使用 await
    result = await coro
    print(f"使用 await: {result}")
    
    # 陷阱 2：在同步函数中调用异步函数
    print("\n--- 陷阱 2：在同步函数中调用异步函数 ---")
    
    def sync_function():
        # 错误：不能在同步函数中直接 await
        # result = await my_coro()  # SyntaxError!
        
        # 解决方案：使用 asyncio.run()（会创建新的事件循环）
        # 或 asyncio.run_coroutine_threadsafe()
        pass
    
    # 陷阱 3：阻塞事件循环
    print("\n--- 陷阱 3：阻塞事件循环 ---")
    
    async def bad_practice():
        # 错误：使用 time.sleep() 会阻塞整个事件循环
        # time.sleep(1)  # 所有协程都会被阻塞
        
        # 正确：使用 asyncio.sleep()
        await asyncio.sleep(1)  # 只暂停当前协程
    
    print("不要在异步代码中使用 time.sleep()、requests 等")


# ============================================================
# 示例 6：何时使用异步
# ============================================================

def demo_when_to_use():
    """演示何时使用异步"""
    print("\n" + "=" * 60)
    print("示例 6：何时使用异步")
    print("=" * 60)
    
    print("""
┌─────────────────────┬─────────────────────────────────────┐
│ 场景                │ 推荐方案                            │
├─────────────────────┼─────────────────────────────────────┤
│ 网络请求（大量）    │ ✅ asyncio + aiohttp                │
│ 数据库查询（大量）  │ ✅ asyncio + asyncpg/aiomysql       │
│ 文件 I/O            │ ✅ asyncio + aiofiles               │
│ CPU 密集型计算      │ ❌ 使用多进程                       │
│ 简单脚本            │ ❌ 同步代码更简单                   │
│ 需要精确控制顺序    │ ⚠️  同步代码更直观                  │
└─────────────────────┴─────────────────────────────────────┘

异步的优势：
1. 高并发：单线程处理大量连接
2. 低开销：没有线程切换开销
3. 简洁：代码比回调更易读

异步的劣势：
1. 学习曲线：需要理解事件循环
2. 生态限制：需要异步库支持
3. 调试困难：堆栈跟踪更复杂
""")


# ============================================================
# 主程序
# ============================================================

async def main():
    """主协程"""
    # I/O 对比
    demo_sync_io()
    await demo_async_io()
    
    # CPU 密集型
    await demo_cpu_bound()
    
    # to_thread
    await demo_to_thread()
    
    # CPU in async
    await demo_cpu_in_async()
    
    # 陷阱
    await trap_demo()
    
    # 何时使用
    demo_when_to_use()


if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. 异步适合 I/O 密集型任务，不适合 CPU 密集型")
    print("2. time.sleep() 会阻塞事件循环，用 asyncio.sleep()")
    print("3. to_thread() 在线程中运行同步代码")
    print("4. ProcessPoolExecutor 用于 CPU 密集型任务")
    print("5. 不要忘记 await，否则协程不会执行")
    print("=" * 60)