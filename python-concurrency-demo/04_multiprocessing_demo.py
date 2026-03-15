#!/usr/bin/env python3
"""
多进程基础
==========

知识点：
1. 进程 vs 线程的区别
2. 创建进程
3. 进程间内存隔离
4. 绕过 GIL 实现真正的并行
"""

import multiprocessing
import threading
import time
import os


# ============================================================
# 示例 1：进程 vs 线程 - CPU 密集型任务
# ============================================================

def cpu_bound_task(count: int) -> int:
    """
    CPU 密集型任务 - 计算密集
    
    由于 GIL 的存在，多线程无法并行执行此任务
    但多进程可以真正并行（每个进程有自己的 GIL）
    """
    result = 0
    for i in range(count):
        result += i
    return result


def demo_thread_vs_process():
    """对比线程和进程在 CPU 密集型任务上的表现"""
    print("=" * 60)
    print("示例 1：线程 vs 进程 - CPU 密集型任务")
    print("=" * 60)
    
    count = 10_000_000
    num_workers = 4
    
    # 方式 1：多线程
    print("\n使用多线程:")
    start = time.time()
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=cpu_bound_task, args=(count,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    thread_time = time.time() - start
    print(f"  耗时: {thread_time:.2f}s")
    
    # 方式 2：多进程
    print("\n使用多进程:")
    start = time.time()
    processes = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=cpu_bound_task, args=(count,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    process_time = time.time() - start
    print(f"  耗时: {process_time:.2f}s")
    
    print(f"\n多进程比多线程快: {thread_time / process_time:.2f}x")
    print("原因：多进程绕过了 GIL，实现了真正的并行")


# ============================================================
# 示例 2：进程间内存隔离
# ============================================================

# 全局变量
shared_data = {"value": 0}


def modify_data_process():
    """在子进程中修改数据"""
    global shared_data
    print(f"  [子进程 PID={os.getpid()}] 修改前: {shared_data}")
    shared_data["value"] = 100
    print(f"  [子进程 PID={os.getpid()}] 修改后: {shared_data}")


def modify_data_thread():
    """在子线程中修改数据"""
    global shared_data
    print(f"  [子线程] 修改前: {shared_data}")
    shared_data["value"] = 100
    print(f"  [子线程] 修改后: {shared_data}")


def demo_memory_isolation():
    """演示进程间内存隔离"""
    print("\n" + "=" * 60)
    print("示例 2：进程间内存隔离")
    print("=" * 60)
    
    global shared_data
    
    # 测试线程 - 共享内存
    print("\n--- 线程（共享内存）---")
    shared_data = {"value": 0}
    print(f"[主线程] 初始值: {shared_data}")
    
    t = threading.Thread(target=modify_data_thread)
    t.start()
    t.join()
    
    print(f"[主线程] 子线程结束后: {shared_data}")
    print("结论：线程共享内存，修改对主线程可见")
    
    # 测试进程 - 内存隔离
    print("\n--- 进程（内存隔离）---")
    shared_data = {"value": 0}
    print(f"[主进程 PID={os.getpid()}] 初始值: {shared_data}")
    
    p = multiprocessing.Process(target=modify_data_process)
    p.start()
    p.join()
    
    print(f"[主进程 PID={os.getpid()}] 子进程结束后: {shared_data}")
    print("结论：进程内存隔离，子进程的修改不影响主进程")


# ============================================================
# 示例 3：创建进程的两种方式
# ============================================================

def simple_worker(name: str):
    """简单的工作函数"""
    print(f"  [进程 {name}, PID={os.getpid()}] 开始工作")
    time.sleep(0.5)
    print(f"  [进程 {name}, PID={os.getpid()}] 工作完成")


class WorkerProcess(multiprocessing.Process):
    """
    继承 Process 类创建自定义进程
    
    与线程类似，可以封装进程的状态和逻辑
    """
    
    def __init__(self, name: str):
        super().__init__()
        self.worker_name = name
        self.result = None
    
    def run(self):
        """进程启动时执行"""
        print(f"  [自定义进程 {self.worker_name}, PID={os.getpid()}] 开始")
        time.sleep(0.5)
        self.result = f"{self.worker_name} 的结果"
        print(f"  [自定义进程 {self.worker_name}, PID={os.getpid()}] 完成")


def demo_create_process():
    """演示创建进程的两种方式"""
    print("\n" + "=" * 60)
    print("示例 3：创建进程的两种方式")
    print("=" * 60)
    
    print(f"主进程 PID: {os.getpid()}")
    
    # 方式 1：使用 Process 类
    print("\n--- 方式 1：Process 类 ---")
    p1 = multiprocessing.Process(target=simple_worker, args=("P1",))
    p2 = multiprocessing.Process(target=simple_worker, args=("P2",))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    # 方式 2：继承 Process 类
    print("\n--- 方式 2：继承 Process 类 ---")
    p3 = WorkerProcess("P3")
    p4 = WorkerProcess("P4")
    
    p3.start()
    p4.start()
    
    p3.join()
    p4.join()
    
    # 注意：由于进程间内存隔离，无法直接访问子进程的属性
    # print(p3.result)  # 这里会是 None，因为 result 在子进程中设置


# ============================================================
# 示例 4：进程的生命周期
# ============================================================

def lifecycle_task():
    """演示进程生命周期"""
    print(f"  [子进程 PID={os.getpid()}] 开始执行")
    time.sleep(2)
    print(f"  [子进程 PID={os.getpid()}] 执行完毕")


def demo_process_lifecycle():
    """演示进程的生命周期和状态"""
    print("\n" + "=" * 60)
    print("示例 4：进程生命周期")
    print("=" * 60)
    
    p = multiprocessing.Process(target=lifecycle_task)
    
    print(f"创建后状态: is_alive={p.is_alive()}, pid={p.pid}")
    
    p.start()
    print(f"启动后状态: is_alive={p.is_alive()}, pid={p.pid}")
    
    time.sleep(0.5)
    print(f"运行中状态: is_alive={p.is_alive()}, pid={p.pid}")
    
    p.join()
    print(f"结束后状态: is_alive={p.is_alive()}, pid={p.pid}")
    print(f"退出码: {p.exitcode}")


# ============================================================
# 示例 5：守护进程
# ============================================================

def daemon_task():
    """守护进程任务"""
    print("  [守护进程] 开始")
    time.sleep(3)
    print("  [守护进程] 这句话可能不会打印（如果主进程先退出）")


def normal_task():
    """普通进程任务"""
    print("  [普通进程] 开始")
    time.sleep(1)
    print("  [普通进程] 完成")


def demo_daemon_process():
    """演示守护进程"""
    print("\n" + "=" * 60)
    print("示例 5：守护进程")
    print("=" * 60)
    
    # 守护进程：主进程退出时自动终止
    daemon = multiprocessing.Process(target=daemon_task)
    daemon.daemon = True  # 设置为守护进程
    
    # 普通进程：主进程会等待其完成
    normal = multiprocessing.Process(target=normal_task)
    normal.daemon = False  # 默认值
    
    daemon.start()
    normal.start()
    
    print("主进程等待普通进程完成...")
    normal.join()
    
    print("普通进程已完成，主进程即将退出")
    print("守护进程会随主进程一起终止（即使还没执行完）")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # 重要：Windows 上必须使用 if __name__ == "__main__"
    # 否则会无限递归创建进程
    
    # 对比线程和进程
    demo_thread_vs_process()
    
    # 内存隔离
    demo_memory_isolation()
    
    # 创建进程
    demo_create_process()
    
    # 进程生命周期
    demo_process_lifecycle()
    
    # 守护进程
    demo_daemon_process()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. 进程适合 CPU 密集型任务，绕过 GIL 实现真正并行")
    print("2. 进程间内存隔离，需要特殊机制通信")
    print("3. 进程创建开销比线程大")
    print("4. Windows 上必须使用 if __name__ == '__main__'")
    print("5. 守护进程随主进程一起终止")
    print("=" * 60)