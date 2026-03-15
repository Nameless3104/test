#!/usr/bin/env python3
"""
进程间通信
==========

知识点：
1. Queue - 进程安全的队列
2. Pipe - 管道通信
3. Shared Memory - 共享内存
4. Manager - 管理共享对象
5. Value 和 Array - 共享值和数组
"""

import multiprocessing
import time
import os


# ============================================================
# 示例 1：Queue 进程队列
# ============================================================

def producer_queue(queue: multiprocessing.Queue, items: list):
    """
    生产者 - 向队列放入数据
    
    multiprocessing.Queue 是进程安全的
    与 threading.Queue 不同，它是为进程间通信设计的
    """
    print(f"[生产者 PID={os.getpid()}] 开始生产")
    for item in items:
        queue.put(item)  # 放入队列
        print(f"  生产: {item}")
        time.sleep(0.1)
    
    # 放入结束信号
    queue.put(None)
    print(f"[生产者] 结束")


def consumer_queue(queue: multiprocessing.Queue):
    """
    消费者 - 从队列获取数据
    """
    print(f"[消费者 PID={os.getpid()}] 开始消费")
    while True:
        item = queue.get()  # 从队列获取（阻塞）
        if item is None:
            break
        print(f"  消费: {item}")
        time.sleep(0.2)
    print(f"[消费者] 结束")


def demo_queue():
    """演示 Queue 进程间通信"""
    print("=" * 60)
    print("示例 1：Queue 进程队列")
    print("=" * 60)
    
    # 创建进程队列
    queue = multiprocessing.Queue()
    
    # 创建生产者和消费者进程
    p1 = multiprocessing.Process(target=producer_queue, args=(queue, [1, 2, 3, 4, 5]))
    p2 = multiprocessing.Process(target=consumer_queue, args=(queue,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("Queue 示例完成")


# ============================================================
# 示例 2：Pipe 管道
# ============================================================

def sender(conn):
    """
    发送端 - 通过管道发送数据
    
    Pipe() 返回两个连接对象，分别给两个进程使用
    """
    print(f"[发送端 PID={os.getpid()}] 发送数据")
    for i in range(5):
        conn.send(f"消息 {i}")  # 发送数据
        print(f"  发送: 消息 {i}")
        time.sleep(0.1)
    
    conn.send(None)  # 发送结束信号
    conn.close()  # 关闭连接
    print("[发送端] 结束")


def receiver(conn):
    """
    接收端 - 通过管道接收数据
    """
    print(f"[接收端 PID={os.getpid()}] 等待接收")
    while True:
        msg = conn.recv()  # 接收数据（阻塞）
        if msg is None:
            break
        print(f"  接收: {msg}")
    
    conn.close()
    print("[接收端] 结束")


def demo_pipe():
    """演示 Pipe 管道通信"""
    print("\n" + "=" * 60)
    print("示例 2：Pipe 管道")
    print("=" * 60)
    
    # Pipe() 返回两个连接对象
    # parent_conn, child_conn 可以双向通信
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # 创建进程
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,))
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("Pipe 示例完成")


# ============================================================
# 示例 3：共享内存 Value 和 Array
# ============================================================

def worker_value(shared_value, shared_array):
    """
    使用共享内存的进程
    
    Value: 共享单个值
    Array: 共享数组
    """
    print(f"[子进程 PID={os.getpid()}] 修改共享数据")
    
    # 修改共享值
    with shared_value.get_lock():  # 使用锁保护
        shared_value.value += 10
    
    # 修改共享数组
    for i in range(len(shared_array)):
        shared_array[i] *= 2
    
    print(f"  共享值: {shared_value.value}")
    print(f"  共享数组: {list(shared_array)}")


def demo_shared_memory():
    """演示共享内存 Value 和 Array"""
    print("\n" + "=" * 60)
    print("示例 3：共享内存 Value 和 Array")
    print("=" * 60)
    
    # 创建共享值
    # 'i' 表示整数类型，'d' 表示浮点数
    shared_value = multiprocessing.Value('i', 0)
    
    # 创建共享数组
    # 'i' 表示整数类型
    shared_array = multiprocessing.Array('i', [1, 2, 3, 4, 5])
    
    print(f"初始值: {shared_value.value}")
    print(f"初始数组: {list(shared_array)}")
    
    # 创建多个进程
    processes = [
        multiprocessing.Process(target=worker_value, args=(shared_value, shared_array))
        for _ in range(3)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"\n最终值: {shared_value.value}")
    print(f"最终数组: {list(shared_array)}")


# ============================================================
# 示例 4：Manager 管理共享对象
# ============================================================

def worker_manager(shared_dict, shared_list, name):
    """
    使用 Manager 创建的共享对象
    
    Manager 支持更多数据类型：dict, list, Queue, Lock 等
    比 Value/Array 更灵活，但性能稍低
    """
    print(f"[{name} PID={os.getpid()}] 操作共享数据")
    
    # 修改共享字典
    shared_dict[name] = os.getpid()
    
    # 修改共享列表
    shared_list.append(name)
    
    time.sleep(0.1)


def demo_manager():
    """演示 Manager 管理共享对象"""
    print("\n" + "=" * 60)
    print("示例 4：Manager 管理共享对象")
    print("=" * 60)
    
    # 创建 Manager
    with multiprocessing.Manager() as manager:
        # 创建共享字典和列表
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        # 创建进程
        processes = [
            multiprocessing.Process(
                target=worker_manager, 
                args=(shared_dict, shared_list, f"进程{i}")
            )
            for i in range(3)
        ]
        
        for p in processes:
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"\n共享字典: {dict(shared_dict)}")
        print(f"共享列表: {list(shared_list)}")


# ============================================================
# 示例 5：进程间同步
# ============================================================

def worker_with_lock(lock, counter, name):
    """
    使用锁进行进程间同步
    """
    for _ in range(1000):
        with lock:  # 获取锁
            counter.value += 1
    
    print(f"[{name}] 完成")


def demo_process_lock():
    """演示进程间锁"""
    print("\n" + "=" * 60)
    print("示例 5：进程间同步（锁）")
    print("=" * 60)
    
    # 创建锁和共享计数器
    lock = multiprocessing.Lock()
    counter = multiprocessing.Value('i', 0)
    
    # 创建进程
    processes = [
        multiprocessing.Process(
            target=worker_with_lock, 
            args=(lock, counter, f"进程{i}")
        )
        for i in range(5)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"最终计数: {counter.value} (期望: 5000)")


# ============================================================
# 示例 6：对比不同通信方式
# ============================================================

def demo_comparison():
    """对比不同进程间通信方式"""
    print("\n" + "=" * 60)
    print("示例 6：进程间通信方式对比")
    print("=" * 60)
    
    print("""
┌──────────────┬─────────────────────────────────────────────┐
│ 方式         │ 特点                                        │
├──────────────┼─────────────────────────────────────────────┤
│ Queue        │ 进程安全队列，适合生产者-消费者模式          │
│ Pipe         │ 双向管道，适合两个进程间的点对点通信         │
│ Value/Array  │ 共享内存，性能高，适合简单数据类型           │
│ Manager      │ 支持多种数据类型，灵活但性能较低             │
│ Lock         │ 进程间同步，保护共享资源                     │
└──────────────┴─────────────────────────────────────────────┘
""")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    # Queue
    demo_queue()
    
    # Pipe
    demo_pipe()
    
    # 共享内存
    demo_shared_memory()
    
    # Manager
    demo_manager()
    
    # 进程间锁
    demo_process_lock()
    
    # 对比
    demo_comparison()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. Queue 适合生产者-消费者模式")
    print("2. Pipe 适合两个进程间的双向通信")
    print("3. Value/Array 共享内存性能最高")
    print("4. Manager 支持更多数据类型，但性能较低")
    print("5. 进程间也需要锁来保护共享资源")
    print("=" * 60)