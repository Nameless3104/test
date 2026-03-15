#!/usr/bin/env python3
"""
混合使用示例
============

知识点：
1. 线程 + 异步混合
2. 进程 + 异步混合
3. 实际应用场景
4. 最佳实践
"""

import asyncio
import threading
import multiprocessing
import concurrent.futures
import time
import random
import queue


# ============================================================
# 示例 1：在异步中调用阻塞函数
# ============================================================

def blocking_network_request(url: str) -> dict:
    """
    模拟阻塞的网络请求
    
    例如：使用 requests 库
    """
    print(f"  [线程 {threading.current_thread().name}] 请求 {url}")
    time.sleep(random.uniform(0.2, 0.5))  # 模拟阻塞
    return {"url": url, "status": 200}


async def demo_async_with_blocking():
    """演示在异步中调用阻塞函数"""
    print("=" * 60)
    print("示例 1：在异步中调用阻塞函数")
    print("=" * 60)
    
    urls = [
        "https://api.example.com/1",
        "https://api.example.com/2",
        "https://api.example.com/3",
    ]
    
    # 方式 1：使用 asyncio.to_thread()（Python 3.9+）
    print("\n--- 方式 1：asyncio.to_thread() ---")
    start = time.time()
    results = await asyncio.gather(*[
        asyncio.to_thread(blocking_network_request, url)
        for url in urls
    ])
    print(f"耗时: {time.time() - start:.2f}s")
    
    # 方式 2：使用 run_in_executor()
    print("\n--- 方式 2：run_in_executor() ---")
    loop = asyncio.get_event_loop()
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = await asyncio.gather(*[
            loop.run_in_executor(pool, blocking_network_request, url)
            for url in urls
        ])
    
    print(f"耗时: {time.time() - start:.2f}s")


# ============================================================
# 示例 2：在异步中运行 CPU 密集型任务
# ============================================================

def cpu_intensive_task(n: int) -> int:
    """CPU 密集型任务"""
    print(f"  [进程 PID={multiprocessing.current_process().pid}] 计算 {n}")
    return sum(i * i for i in range(n))


async def demo_async_with_process():
    """演示在异步中运行 CPU 密集型任务"""
    print("\n" + "=" * 60)
    print("示例 2：在异步中运行 CPU 密集型任务")
    print("=" * 60)
    
    tasks = [500_000, 500_000, 500_000, 500_000]
    
    # 使用 ProcessPoolExecutor
    print("\n使用 ProcessPoolExecutor:")
    start = time.time()
    
    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        results = await asyncio.gather(*[
            loop.run_in_executor(pool, cpu_intensive_task, n)
            for n in tasks
        ])
    
    print(f"耗时: {time.time() - start:.2f}s")
    print(f"结果数量: {len(results)}")


# ============================================================
# 示例 3：异步生产者-消费者（线程间通信）
# ============================================================

async def async_producer(queue: asyncio.Queue, count: int):
    """异步生产者"""
    for i in range(count):
        item = f"商品-{i}"
        await queue.put(item)
        print(f"  [生产者] 生产: {item}")
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    # 发送结束信号
    await queue.put(None)
    print("  [生产者] 结束")


async def async_consumer(queue: asyncio.Queue, name: str):
    """异步消费者"""
    while True:
        item = await queue.get()
        if item is None:
            # 放回结束信号，让其他消费者也能收到
            await queue.put(None)
            break
        
        print(f"  [消费者 {name}] 消费: {item}")
        await asyncio.sleep(random.uniform(0.2, 0.4))
    
    print(f"  [消费者 {name}] 结束")


async def demo_async_queue():
    """演示异步队列"""
    print("\n" + "=" * 60)
    print("示例 3：异步生产者-消费者")
    print("=" * 60)
    
    # asyncio.Queue 是异步安全的
    queue = asyncio.Queue(maxsize=10)
    
    # 启动生产者和消费者
    await asyncio.gather(
        async_producer(queue, 10),
        async_consumer(queue, "A"),
        async_consumer(queue, "B"),
    )


# ============================================================
# 示例 4：混合线程和异步
# ============================================================

class AsyncWorker:
    """
    在线程中运行异步代码
    
    适用场景：需要在后台持续运行的异步任务
    """
    
    def __init__(self):
        self.queue = queue.Queue()  # 线程安全的队列
        self.loop = None
        self.thread = None
    
    def start(self):
        """启动工作线程"""
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
    
    def _run_loop(self):
        """运行事件循环"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # 运行事件循环
        self.loop.run_forever()
    
    async def process_task(self, task_data):
        """处理任务"""
        print(f"  [异步工作线程] 处理: {task_data}")
        await asyncio.sleep(0.5)
        return f"处理完成: {task_data}"
    
    def submit_task(self, task_data):
        """提交任务（线程安全）"""
        if self.loop:
            # 在事件循环中调度协程
            future = asyncio.run_coroutine_threadsafe(
                self.process_task(task_data),
                self.loop
            )
            return future
    
    def stop(self):
        """停止工作线程"""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)


def demo_thread_with_async():
    """演示线程中运行异步代码"""
    print("\n" + "=" * 60)
    print("示例 4：线程中运行异步代码")
    print("=" * 60)
    
    worker = AsyncWorker()
    worker.start()
    
    # 等待事件循环启动
    time.sleep(0.5)
    
    # 提交任务
    print("提交任务...")
    futures = []
    for i in range(3):
        future = worker.submit_task(f"任务-{i}")
        futures.append(future)
    
    # 等待结果
    print("等待结果...")
    for future in futures:
        result = future.result(timeout=5)  # 阻塞等待结果
        print(f"  结果: {result}")
    
    worker.stop()
    print("工作线程已停止")


# ============================================================
# 示例 5：实际应用 - 异步 Web 爬虫
# ============================================================

async def fetch_page(session, url: str) -> tuple:
    """
    模拟异步获取网页
    
    实际应用中可以使用 aiohttp:
    async with session.get(url) as response:
        return await response.text()
    """
    print(f"  获取: {url}")
    await asyncio.sleep(random.uniform(0.1, 0.3))  # 模拟网络延迟
    return (url, f"<html>{url}</html>")


async def crawl_website(base_url: str, pages: int) -> list:
    """爬取网站多个页面"""
    urls = [f"{base_url}/page/{i}" for i in range(pages)]
    
    # 并发获取所有页面
    results = await asyncio.gather(*[
        fetch_page(None, url) for url in urls
    ])
    
    return results


async def demo_web_crawler():
    """演示异步 Web 爬虫"""
    print("\n" + "=" * 60)
    print("示例 5：异步 Web 爬虫")
    print("=" * 60)
    
    start = time.time()
    
    # 并发爬取多个网站
    results = await asyncio.gather(*[
        crawl_website(f"https://site{i}.example.com", 5)
        for i in range(3)
    ])
    
    elapsed = time.time() - start
    total_pages = sum(len(r) for r in results)
    
    print(f"\n爬取完成:")
    print(f"  总页面数: {total_pages}")
    print(f"  总耗时: {elapsed:.2f}s")
    print(f"  平均每页: {elapsed/total_pages*1000:.1f}ms")


# ============================================================
# 示例 6：最佳实践总结
# ============================================================

def demo_best_practices():
    """最佳实践总结"""
    print("\n" + "=" * 60)
    print("示例 6：最佳实践总结")
    print("=" * 60)
    
    print("""
┌─────────────────────────────────────────────────────────────┐
│                    Python 并发最佳实践                       │
├─────────────────────────────────────────────────────────────┤
│ 任务类型        │ 推荐方案                                  │
├────────────────┼────────────────────────────────────────────┤
│ I/O 密集型      │ asyncio（首选）或 线程池                  │
│ CPU 密集型      │ 多进程（ProcessPoolExecutor）             │
│ 混合型          │ asyncio + to_thread/run_in_executor      │
│ 简单脚本        │ 同步代码                                  │
├────────────────┴────────────────────────────────────────────┤
│ 常见陷阱：                                                   │
│ 1. 不要在异步代码中使用 time.sleep()                        │
│ 2. 不要忘记 await 协程                                      │
│ 3. CPU 密集型任务不要用 asyncio                             │
│ 4. 共享资源需要加锁                                         │
│ 5. Windows 多进程需要 if __name__ == "__main__"            │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# 主程序
# ============================================================

async def main():
    """主协程"""
    # 异步 + 阻塞函数
    await demo_async_with_blocking()
    
    # 异步 + CPU 任务
    await demo_async_with_process()
    
    # 异步队列
    await demo_async_queue()
    
    # Web 爬虫示例
    await demo_web_crawler()
    
    # 最佳实践
    demo_best_practices()


if __name__ == "__main__":
    # 线程中运行异步
    demo_thread_with_async()
    
    # 运行主协程
    asyncio.run(main())
    
    print("\n" + "=" * 60)
    print("恭喜！你已完成 Python 并发编程学习！")
    print("=" * 60)
    print("""
核心知识点回顾：

1. 线程 (threading)
   - 适合 I/O 密集型任务
   - 共享内存，需要锁
   - 受 GIL 限制

2. 进程 (multiprocessing)
   - 适合 CPU 密集型任务
   - 内存隔离，需要 IPC
   - 绕过 GIL

3. 异步 (asyncio)
   - 适合大量 I/O 操作
   - 单线程，协作式调度
   - 最高效的并发方式

4. 混合使用
   - to_thread(): 异步中运行阻塞代码
   - run_in_executor(): 异步中使用线程/进程池
   - asyncio.Queue: 异步生产者-消费者
""")