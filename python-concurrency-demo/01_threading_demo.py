#!/usr/bin/env python3
"""
线程基础示例
============

知识点：
1. 创建线程的两种方式
2. 线程的启动和等待
3. 线程共享全局变量
"""

import threading
import time


# ============================================================
# 示例 1：使用 threading.Thread 创建线程
# ============================================================

def worker(name: str, count: int):
    """
    工作函数 - 线程执行的任务
    
    Args:
        name: 线程名称
        count: 执行次数
    """
    print(f"[{name}] 线程开始执行")
    
    for i in range(count):
        # time.sleep 模拟 I/O 操作（如网络请求、文件读写）
        # I/O 操作期间，线程会释放 GIL，其他线程可以执行
        time.sleep(0.1)
        print(f"[{name}] 正在执行第 {i + 1} 次任务")
    
    print(f"[{name}] 线程执行完毕")


def demo_basic_threading():
    """演示基本的线程创建和启动"""
    print("=" * 60)
    print("示例 1：基本线程创建")
    print("=" * 60)
    
    # 创建两个线程
    # target: 线程要执行的函数
    # args: 传递给函数的参数（元组形式）
    thread1 = threading.Thread(target=worker, args=("线程A", 3))
    thread2 = threading.Thread(target=worker, args=("线程B", 3))
    
    print("主线程：启动两个子线程")
    
    # start() 启动线程
    # 注意：不要调用 run()，那会在当前线程同步执行
    thread1.start()
    thread2.start()
    
    print("主线程：等待子线程完成...")
    
    # join() 等待线程结束
    # 如果不调用 join()，主线程会继续执行，可能在线程结束前退出
    thread1.join()
    thread2.join()
    
    print("主线程：所有子线程已完成")


# ============================================================
# 示例 2：继承 Thread 类创建线程
# ============================================================

class WorkerThread(threading.Thread):
    """
    通过继承 Thread 类创建自定义线程
    
    优点：
    - 可以封装线程的状态和逻辑
    - 更面向对象
    """
    
    def __init__(self, name: str, count: int):
        # 调用父类构造函数
        super().__init__()
        self.name = name
        self.count = count
        self.result = None  # 存储线程执行结果
    
    def run(self):
        """
        重写 run 方法
        线程启动时（调用 start()）会自动调用此方法
        """
        print(f"[{self.name}] 自定义线程开始")
        
        total = 0
        for i in range(self.count):
            time.sleep(0.1)
            total += i
            print(f"[{self.name}] 计算中: {i + 1}/{self.count}")
        
        self.result = total
        print(f"[{self.name}] 完成，结果: {self.result}")


def demo_custom_thread():
    """演示自定义线程类"""
    print("\n" + "=" * 60)
    print("示例 2：自定义线程类")
    print("=" * 60)
    
    # 创建自定义线程实例
    t1 = WorkerThread("自定义线程A", 3)
    t2 = WorkerThread("自定义线程B", 3)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    # 可以访问线程的属性
    print(f"主线程：获取结果 - t1={t1.result}, t2={t2.result}")


# ============================================================
# 示例 3：线程共享全局变量（潜在问题）
# ============================================================

# 全局变量 - 所有线程共享
counter = 0


def increment_unsafe(name: str, times: int):
    """
    不安全的计数器增加函数
    
    问题：counter += 1 不是原子操作
    实际上包含三步：
    1. 读取 counter 的值
    2. 加 1
    3. 写回 counter
    
    多线程同时执行时，可能发生竞态条件（Race Condition）
    """
    global counter
    for _ in range(times):
        # 模拟一些处理时间，增加竞态条件发生的概率
        temp = counter  # 1. 读取
        time.sleep(0.0001)  # 模拟上下文切换
        counter = temp + 1  # 2. 计算 + 3. 写回


def demo_race_condition():
    """演示竞态条件"""
    print("\n" + "=" * 60)
    print("示例 3：竞态条件演示（不安全）")
    print("=" * 60)
    
    global counter
    counter = 0
    
    # 创建 10 个线程，每个增加 1000 次
    # 期望结果：10000
    threads = []
    for i in range(10):
        t = threading.Thread(target=increment_unsafe, args=(f"T{i}", 1000))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"期望结果: 10000")
    print(f"实际结果: {counter}")
    print(f"差异: {10000 - counter}（由于竞态条件丢失的计数）")


# ============================================================
# 示例 4：获取当前线程信息
# ============================================================

def show_thread_info():
    """显示当前线程信息"""
    print("\n" + "=" * 60)
    print("示例 4：线程信息")
    print("=" * 60)
    
    # 获取当前线程对象
    current = threading.current_thread()
    print(f"当前线程: {current.name}")
    print(f"线程 ID: {current.ident}")
    print(f"是否存活: {current.is_alive()}")
    
    # 获取所有活跃线程
    print(f"\n当前活跃线程数: {threading.active_count()}")
    print("所有线程:")
    for thread in threading.enumerate():
        print(f"  - {thread.name} (ID: {thread.ident})")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # 演示基本线程
    demo_basic_threading()
    
    # 演示自定义线程类
    demo_custom_thread()
    
    # 演示竞态条件
    demo_race_condition()
    
    # 显示线程信息
    show_thread_info()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. 线程适合 I/O 密集型任务（网络、文件等）")
    print("2. 线程共享内存，需要注意竞态条件")
    print("3. 使用 Lock 可以避免竞态条件（见下一个示例）")
    print("4. Python 的 GIL 限制了线程的并行计算能力")
    print("=" * 60)
