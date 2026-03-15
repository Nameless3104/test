#!/usr/bin/env python3
"""
线程锁与同步
============

知识点：
1. Lock（互斥锁）的基本使用
2. RLock（可重入锁）
3. with 语句自动管理锁
4. 生产者-消费者模式
"""

import threading
import time
import random
from queue import Queue


# ============================================================
# 示例 1：使用 Lock 解决竞态条件
# ============================================================

# 共享资源
counter = 0
# 创建锁对象
lock = threading.Lock()


def increment_safe(name: str, times: int):
    """
    安全的计数器增加函数 - 使用锁保护共享资源
    
    Lock 的两个关键方法：
    - acquire(): 获取锁（如果锁已被占用，则阻塞等待）
    - release(): 释放锁
    """
    global counter
    for _ in range(times):
        # 方式 1：手动获取和释放锁
        lock.acquire()  # 获取锁
        try:
            counter += 1  # 临界区 - 同一时间只有一个线程能执行
        finally:
            lock.release()  # 释放锁（使用 finally 确保一定释放）


def increment_safe_with(name: str, times: int):
    """
    使用 with 语句管理锁（推荐方式）
    
    with 语句会自动调用 acquire() 和 release()
    即使发生异常也能正确释放锁
    """
    global counter
    for _ in range(times):
        with lock:  # 自动获取锁，退出时自动释放
            counter += 1


def demo_lock_solution():
    """演示使用锁解决竞态条件"""
    global counter
    counter = 0
    
    print("=" * 60)
    print("示例 1：使用 Lock 解决竞态条件")
    print("=" * 60)
    
    threads = []
    for i in range(10):
        # 使用安全的版本
        t = threading.Thread(
            target=increment_safe_with, 
            args=(f"T{i}", 1000)
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"期望结果: 10000")
    print(f"实际结果: {counter}")
    print(f"结果正确: {counter == 10000}")


# ============================================================
# 示例 2：RLock（可重入锁）
# ============================================================

class Counter:
    """
    使用 RLock 的计数器类
    
    RLock vs Lock:
    - Lock: 同一线程不能重复获取，会导致死锁
    - RLock: 同一线程可以多次获取，但必须释放相同次数
    
    RLock 适用场景：
    - 递归调用
    - 类的方法相互调用
    """
    
    def __init__(self):
        self.value = 0
        self._lock = threading.RLock()  # 使用 RLock
    
    def increment(self):
        """增加计数"""
        with self._lock:
            self.value += 1
    
    def increment_multiple(self, times: int):
        """多次增加 - 会递归获取锁"""
        with self._lock:  # 第一次获取锁
            for _ in range(times):
                self.increment()  # increment 内部会再次获取锁（RLock 允许）


def demo_rlock():
    """演示 RLock 的使用"""
    print("\n" + "=" * 60)
    print("示例 2：RLock（可重入锁）")
    print("=" * 60)
    
    counter = Counter()
    
    def worker():
        counter.increment_multiple(100)
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"最终计数: {counter.value}")
    print(f"RLock 允许同一线程多次获取锁")


# ============================================================
# 示例 3：生产者-消费者模式
# ============================================================

def producer(queue: Queue, name: str, count: int):
    """
    生产者 - 向队列中添加数据
    
    Queue 是线程安全的，内部已经使用了锁
    """
    for i in range(count):
        item = f"{name}-商品{i}"
        queue.put(item)  # 线程安全的操作
        print(f"[生产者 {name}] 生产了: {item}")
        time.sleep(random.random() * 0.1)  # 模拟生产时间
    
    # 发送结束信号
    queue.put(None)
    print(f"[生产者 {name}] 结束")


def consumer(queue: Queue, name: str):
    """
    消费者 - 从队列中获取数据
    
    queue.get() 会阻塞直到有数据
    """
    while True:
        # get() 会阻塞等待，直到队列有数据
        item = queue.get()
        
        if item is None:  # 收到结束信号
            print(f"[消费者 {name}] 收到结束信号，退出")
            break
        
        print(f"[消费者 {name}] 消费了: {item}")
        time.sleep(random.random() * 0.2)  # 模拟消费时间
        
        # task_done() 通知队列任务完成（配合 join() 使用）
        queue.task_done()


def demo_producer_consumer():
    """演示生产者-消费者模式"""
    print("\n" + "=" * 60)
    print("示例 3：生产者-消费者模式")
    print("=" * 60)
    
    # 创建共享队列
    # Queue 内部已经实现了线程安全
    shared_queue = Queue()
    
    # 创建生产者和消费者线程
    producers = [
        threading.Thread(target=producer, args=(shared_queue, "P1", 5)),
        threading.Thread(target=producer, args=(shared_queue, "P2", 5)),
    ]
    
    consumers = [
        threading.Thread(target=consumer, args=(shared_queue, "C1")),
        threading.Thread(target=consumer, args=(shared_queue, "C2")),
    ]
    
    # 启动所有线程
    for t in producers + consumers:
        t.start()
    
    # 等待生产者完成
    for t in producers:
        t.join()
    
    # 发送结束信号给消费者（每个消费者一个）
    for _ in consumers:
        shared_queue.put(None)
    
    # 等待消费者完成
    for t in consumers:
        t.join()
    
    print("所有生产者和消费者已完成")


# ============================================================
# 示例 4：Condition（条件变量）
# ============================================================

class BoundedBuffer:
    """
    有界缓冲区 - 使用 Condition 实现生产者-消费者
    
    Condition 提供了更灵活的等待/通知机制：
    - wait(): 释放锁并等待通知
    - notify(): 通知一个等待的线程
    - notify_all(): 通知所有等待的线程
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()
    
    def put(self, item):
        """添加元素到缓冲区"""
        with self.condition:
            # 缓冲区满时等待
            while len(self.buffer) >= self.capacity:
                print(f"  [缓冲区] 已满，等待消费...")
                self.condition.wait()  # 释放锁并等待
            
            self.buffer.append(item)
            print(f"  [缓冲区] 添加: {item}，当前大小: {len(self.buffer)}")
            
            # 通知等待的消费者
            self.condition.notify()
    
    def get(self):
        """从缓冲区获取元素"""
        with self.condition:
            # 缓冲区空时等待
            while len(self.buffer) == 0:
                print(f"  [缓冲区] 为空，等待生产...")
                self.condition.wait()
            
            item = self.buffer.pop(0)
            print(f"  [缓冲区] 取出: {item}，当前大小: {len(self.buffer)}")
            
            # 通知等待的生产者
            self.condition.notify()
            
            return item


def demo_condition():
    """演示 Condition 的使用"""
    print("\n" + "=" * 60)
    print("示例 4：Condition 条件变量")
    print("=" * 60)
    
    buffer = BoundedBuffer(capacity=3)
    
    def producer_task():
        for i in range(5):
            buffer.put(f"商品{i}")
            time.sleep(0.1)
    
    def consumer_task():
        for _ in range(5):
            buffer.get()
            time.sleep(0.2)
    
    p = threading.Thread(target=producer_task)
    c = threading.Thread(target=consumer_task)
    
    p.start()
    c.start()
    
    p.join()
    c.join()
    
    print("Condition 示例完成")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # 演示 Lock 解决竞态条件
    demo_lock_solution()
    
    # 演示 RLock
    demo_rlock()
    
    # 演示生产者-消费者
    demo_producer_consumer()
    
    # 演示 Condition
    demo_condition()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. Lock 用于保护共享资源，避免竞态条件")
    print("2. 推荐使用 with 语句自动管理锁")
    print("3. RLock 允许同一线程多次获取锁（递归场景）")
    print("4. Queue 是线程安全的，适合生产者-消费者模式")
    print("5. Condition 提供更灵活的等待/通知机制")
    print("=" * 60)