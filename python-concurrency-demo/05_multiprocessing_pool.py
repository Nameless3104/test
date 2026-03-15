#!/usr/bin/env python3
"""
进程池
======

知识点：
1. ProcessPoolExecutor 基本使用
2. Pool 类的使用
3. 进程池 vs 线程池的选择
4. 并行计算实战
"""

import multiprocessing
import concurrent.futures
import time
import os


# ============================================================
# 示例 1：ProcessPoolExecutor 基本使用
# ============================================================

def cpu_task(n: int) -> int:
    """
    CPU 密集型任务 - 计算 n 以内的素数个数
    
    Args:
        n: 计算范围
    
    Returns:
        素数个数
    """
    print(f"  [PID={os.getpid()}] 计算 1-{n} 的素数")
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    count = sum(1 for i in range(1, n + 1) if is_prime(i))
    return count


def demo_process_pool_executor():
    """演示 ProcessPoolExecutor"""
    print("=" * 60)
    print("示例 1：ProcessPoolExecutor")
    print("=" * 60)
    
    # 要计算的范围
    ranges = [10000, 20000, 30000, 40000]
    
    print(f"主进程 PID: {os.getpid()}")
    print(f"CPU 核心数: {multiprocessing.cpu_count()}")
    
    # 创建进程池
    # max_workers 默认等于 CPU 核心数
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # 提交任务
        futures = {executor.submit(cpu_task, n): n for n in ranges}
        
        # 获取结果
        for future in concurrent.futures.as_completed(futures):
            n = futures[future]
            count = future.result()
            print(f"  1-{n} 范围内有 {count} 个素数")


# ============================================================
# 示例 2：使用 multiprocessing.Pool
# ============================================================

def square(x: int) -> int:
    """计算平方"""
    time.sleep(0.1)  # 模拟计算时间
    return x * x


def demo_pool():
    """演示 multiprocessing.Pool"""
    print("\n" + "=" * 60)
    print("示例 2：multiprocessing.Pool")
    print("=" * 60)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # 创建进程池
    with multiprocessing.Pool(processes=4) as pool:
        
        # 方式 1：map() - 按顺序返回结果
        print("\n--- map() ---")
        results = pool.map(square, data)
        print(f"map 结果: {results}")
        
        # 方式 2：map_async() - 异步版本
        print("\n--- map_async() ---")
        async_result = pool.map_async(square, data)
        print("任务已提交，可以做其他事...")
        results = async_result.get()  # 阻塞等待结果
        print(f"map_async 结果: {results}")
        
        # 方式 3：imap() - 迭代器版本，按顺序返回
        print("\n--- imap() ---")
        for x, result in zip(data, pool.imap(square, data)):
            print(f"  {x}² = {result}")
        
        # 方式 4：imap_unordered() - 无序迭代器，按完成顺序返回
        print("\n--- imap_unordered() ---")
        for result in pool.imap_unordered(square, data):
            print(f"  结果: {result}")


# ============================================================
# 示例 3：apply 和 apply_async
# ============================================================

def process_task(name: str, value: int) -> str:
    """单个任务处理"""
    print(f"  [PID={os.getpid()}] 处理 {name}")
    time.sleep(0.5)
    return f"{name}: {value * 2}"


def demo_apply():
    """演示 apply 和 apply_async"""
    print("\n" + "=" * 60)
    print("示例 3：apply 和 apply_async")
    print("=" * 60)
    
    with multiprocessing.Pool(processes=2) as pool:
        
        # apply() - 同步执行单个任务（阻塞）
        print("\n--- apply() 同步执行 ---")
        result = pool.apply(process_task, args=("任务A", 10))
        print(f"结果: {result}")
        
        # apply_async() - 异步执行单个任务
        print("\n--- apply_async() 异步执行 ---")
        async_results = []
        for i in range(3):
            r = pool.apply_async(process_task, args=(f"任务{i}", i * 10))
            async_results.append(r)
        
        print("任务已提交，等待结果...")
        for i, r in enumerate(async_results):
            print(f"  结果 {i}: {r.get()}")


# ============================================================
# 示例 4：并行计算实战 - 蒙特卡洛计算 π
# ============================================================

import random


def monte_carlo_pi(points: int) -> int:
    """
    蒙特卡洛方法计算 π
    
    在单位正方形内随机撒点，统计落在 1/4 圆内的比例
    π ≈ 4 * (圆内点数 / 总点数)
    """
    inside = 0
    for _ in range(points):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside += 1
    return inside


def demo_parallel_pi():
    """并行计算 π"""
    print("\n" + "=" * 60)
    print("示例 4：并行计算 π（蒙特卡洛方法）")
    print("=" * 60)
    
    total_points = 10_000_000
    num_processes = 4
    points_per_process = total_points // num_processes
    
    print(f"总点数: {total_points:,}")
    print(f"进程数: {num_processes}")
    
    # 串行计算
    print("\n--- 串行计算 ---")
    start = time.time()
    inside = monte_carlo_pi(total_points)
    pi_estimate = 4 * inside / total_points
    serial_time = time.time() - start
    print(f"π ≈ {pi_estimate:.6f}")
    print(f"耗时: {serial_time:.2f}s")
    
    # 并行计算
    print("\n--- 并行计算 ---")
    start = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(monte_carlo_pi, [points_per_process] * num_processes)
        total_inside = sum(results)
        pi_estimate = 4 * total_inside / total_points
    parallel_time = time.time() - start
    print(f"π ≈ {pi_estimate:.6f}")
    print(f"耗时: {parallel_time:.2f}s")
    
    print(f"\n加速比: {serial_time / parallel_time:.2f}x")


# ============================================================
# 示例 5：进程池 vs 线程池对比
# ============================================================

def io_bound_task(duration: float) -> float:
    """I/O 密集型任务"""
    time.sleep(duration)
    return duration


def cpu_bound_task(n: int) -> int:
    """CPU 密集型任务"""
    return sum(i * i for i in range(n))


def compare_pools():
    """对比进程池和线程池"""
    print("\n" + "=" * 60)
    print("示例 5：进程池 vs 线程池对比")
    print("=" * 60)
    
    # I/O 密集型任务
    print("\n--- I/O 密集型任务 ---")
    io_tasks = [0.5] * 8
    
    # 线程池
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(io_bound_task, io_tasks))
    thread_time = time.time() - start
    print(f"线程池耗时: {thread_time:.2f}s")
    
    # 进程池
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(io_bound_task, io_tasks))
    process_time = time.time() - start
    print(f"进程池耗时: {process_time:.2f}s")
    
    print("结论：I/O 密集型任务，线程池更高效（进程创建开销大）")
    
    # CPU 密集型任务
    print("\n--- CPU 密集型任务 ---")
    cpu_tasks = [500000] * 4
    
    # 线程池
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, cpu_tasks))
    thread_time = time.time() - start
    print(f"线程池耗时: {thread_time:.2f}s")
    
    # 进程池
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, cpu_tasks))
    process_time = time.time() - start
    print(f"进程池耗时: {process_time:.2f}s")
    
    print("结论：CPU 密集型任务，进程池更高效（绕过 GIL）")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # ProcessPoolExecutor
    demo_process_pool_executor()
    
    # multiprocessing.Pool
    demo_pool()
    
    # apply 和 apply_async
    demo_apply()
    
    # 并行计算 π
    demo_parallel_pi()
    
    # 进程池 vs 线程池
    compare_pools()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. ProcessPoolExecutor 和 Pool 都可以创建进程池")
    print("2. ProcessPoolExecutor API 与 ThreadPoolExecutor 一致")
    print("3. Pool 提供更多方法：map, imap, apply 等")
    print("4. CPU 密集型任务用进程池，I/O 密集型用线程池")
    print("5. 进程数通常设为 CPU 核心数")
    print("=" * 60)