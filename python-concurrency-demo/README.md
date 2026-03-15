# Python 并发编程学习 Demo

## 目录结构

```
python-concurrency-demo/
├── README.md                    # 本文件
├── 01_threading_demo.py         # 线程基础示例
├── 02_threading_lock.py         # 线程锁与同步
├── 03_threading_pool.py         # 线程池
├── 04_multiprocessing_demo.py   # 多进程基础
├── 05_multiprocessing_pool.py   # 进程池
├── 06_process_communication.py  # 进程间通信
├── 07_asyncio_demo.py           # 异步编程基础
├── 08_asyncio_gather.py         # 并发执行多个协程
├── 09_asyncio_with_sync.py      # 异步与同步对比
├── 10_mixed_demo.py             # 混合使用示例
└── requirements.txt             # 依赖（可选）
```

## 核心概念对比

| 概念 | 适用场景 | 特点 |
|------|----------|------|
| **Thread（线程）** | I/O 密集型任务 | 共享内存，轻量级，受 GIL 限制 |
| **Process（进程）** | CPU 密集型任务 | 独立内存，重量级，绕过 GIL |
| **Asyncio（协程）** | I/O 密集型任务 | 单线程，协作式调度，最高效 |

## GIL（全局解释器锁）

Python 的 GIL 使得同一时刻只有一个线程执行 Python 字节码。

- **线程**：适合网络请求、文件读写等 I/O 操作（I/O 时会释放 GIL）
- **进程**：适合计算密集型任务（多进程绕过 GIL）
- **协程**：适合大量 I/O 操作（单线程切换，无锁问题）

## 运行方式

```bash
# 运行单个示例
python 01_threading_demo.py

# 运行所有示例
for f in *.py; do echo "=== $f ===" && python "$f"; done
```
