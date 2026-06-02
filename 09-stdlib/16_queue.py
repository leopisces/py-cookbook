#!/usr/bin/env python3
"""
queue模块 - Python标准库线程安全队列

涵盖内容:
  1. Queue - 先进先出 (FIFO) 队列
  2. LifoQueue - 后进先出 (LIFO) 栈
  3. PriorityQueue - 优先级队列
  4. 生产者-消费者模式
  5. 线程安全队列实战

参考: https://docs.python.org/zh-cn/3/library/queue.html
"""

import queue
import threading
import time
import random


# ============================================================
# 1. Queue (FIFO) - 先进先出队列
# ============================================================
print("=" * 60)
print("1. Queue (先进先出 FIFO)")
print("=" * 60)

# 创建队列 (maxsize=0 表示无限制)
q = queue.Queue(maxsize=5)
print(f"创建队列, 最大容量: {q.maxsize}, 当前大小: {q.qsize()}")

# put - 放入元素 (队列满时默认阻塞)
for i in range(5):
    q.put(f"任务-{i}")
    print(f"  put('任务-{i}') → 队列大小: {q.qsize()}")

print(f"\n队列是否满: {q.full()}")
print(f"队列是否空: {q.empty()}")

# get - 取出元素 (队列空时默认阻塞)
print("\n依次取出:")
try:
    while True:
        item = q.get_nowait()  # 非阻塞获取
        print(f"  get() → '{item}' 剩余: {q.qsize()}")
except queue.Empty:
    print("  队列已空!")

print(f"\n取完后是否空: {q.empty()}")

# ============================================================
# 2. LifoQueue (LIFO) - 后进先出队列 (栈)
# ============================================================
print("\n" + "=" * 60)
print("2. LifoQueue (后进先出 LIFO) - 栈行为")
print("=" * 60)

lq = queue.LifoQueue()

for item in ["A", "B", "C", "D"]:
    lq.put(item)

print("放入顺序: A → B → C → D")
print("取出顺序 (后进先出):", end=" ")
while not lq.empty():
    print(f"{lq.get()} ", end="")
print()

# ============================================================
# 3. PriorityQueue - 优先级队列
# ============================================================
print("\n" + "=" * 60)
print("3. PriorityQueue (优先级队列)")
print("=" * 60)

pq = queue.PriorityQueue()

# 优先级队列: 数字越小优先级越高
# 格式: (priority, data) 元组
tasks = [
    (3, "普通任务: 发送邮件"),
    (1, "紧急任务: 处理告警"),
    (4, "普通任务: 数据备份"),
    (2, "重要任务: 用户请求"),
    (5, "低优任务: 日志清理"),
]

print("任务列表 (优先级, 描述):")
for priority, desc in tasks:
    print(f"  优先级{priority}: {desc}")
    pq.put((priority, desc))

print(f"\n按优先级取出:")
while not pq.empty():
    priority, task = pq.get()
    print(f"  [优先级{priority}] {task}")

# 使用 dataclass 定义可排序任务 (Python 3.7+)
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedTask:
    """可排序的任务类"""
    priority: int
    item: Any = field(compare=False)


print(f"\n使用 @dataclass 定义优先级任务:")
pq2 = queue.PriorityQueue()
pq2.put(PrioritizedTask(3, "发送邮件"))
pq2.put(PrioritizedTask(1, "处理告警"))
pq2.put(PrioritizedTask(2, "用户请求"))

while not pq2.empty():
    task = pq2.get()
    print(f"  [优先级{task.priority}] {task.item}")

# ============================================================
# 4. 生产者-消费者模式
# ============================================================
print("\n" + "=" * 60)
print("4. 生产者-消费者模式")
print("=" * 60)


def producer(q, name, items):
    """生产者: 向队列中添加任务"""
    for item in items:
        time.sleep(random.uniform(0.01, 0.05))  # 模拟生产耗时
        q.put(item)
        print(f"  [{name}] 生产: {item}")
    q.put(None)  # 结束信号


def consumer(q, name):
    """消费者: 从队列中取出任务处理"""
    while True:
        item = q.get()
        if item is None:  # 收到结束信号
            q.put(None)   # 传递给其他消费者
            print(f"  [{name}] 收到结束信号, 退出")
            break
        time.sleep(random.uniform(0.02, 0.08))  # 模拟消费耗时
        print(f"  [{name}] 消费: {item}")
        q.task_done()  # 标记任务完成


# 创建队列和线程
task_queue = queue.Queue()

# 示例任务
sample_items = [f"任务-{i}" for i in range(1, 9)]

# 启动生产者
prod_thread = threading.Thread(
    target=producer,
    args=(task_queue, "生产者", sample_items),
)
prod_thread.start()

# 启动消费者
cons1 = threading.Thread(target=consumer, args=(task_queue, "消费者A"))
cons2 = threading.Thread(target=consumer, args=(task_queue, "消费者B"))
cons1.start()
cons2.start()

# 等待所有线程完成
prod_thread.join()
cons1.join()
cons2.join()

print(f"\n所有任务处理完成! 队列最终大小: {task_queue.qsize()}")

# ============================================================
# 5. 队列的高级特性
# ============================================================
print("\n" + "=" * 60)
print("5. 队列高级特性")
print("=" * 60)

# put 和 get 的阻塞/超时
demo_q = queue.Queue(maxsize=2)
print("测试 put/get 的阻塞与超时:")

# 填满队列
demo_q.put("A")
demo_q.put("B")
print(f"  队列已满 (2/2): full={demo_q.full()}")

# put 非阻塞 - 队列满时抛异常
try:
    demo_q.put("C", block=False)
except queue.Full:
    print("  put(block=False) → queue.Full 异常 (正确)")

# put 带超时
try:
    demo_q.put("C", timeout=0.1)
except queue.Full:
    print("  put(timeout=0.1) → queue.Full 超时 (正确)")

# 清空并再测试 get
demo_q.get()
demo_q.get()

# get 非阻塞 - 队列空时抛异常
try:
    demo_q.get(block=False)
except queue.Empty:
    print("  get(block=False) → queue.Empty 异常 (正确)")

# join - 等待所有任务完成
print(f"\njoin() 演示 - 等待所有 task_done():")
join_q = queue.Queue()
for i in range(3):
    join_q.put(f"Task-{i}")


def worker():
    """模拟工作线程"""
    while True:
        try:
            item = join_q.get(timeout=0.1)
            time.sleep(0.02)
            join_q.task_done()
            # 如果队列空了就退出
            if join_q.empty():
                break
        except queue.Empty:
            break


# 启动工作线程
t = threading.Thread(target=worker)
t.start()
t.join()

try:
    join_q.join()  # 阻塞直到所有 task_done() 被调用
    print("  所有任务已处理完毕 (join 返回)")
except Exception as e:
    print(f"  异常: {e}")

# ============================================================
# 6. 实际应用场景
# ============================================================
print("\n" + "=" * 60)
print("6. 实际应用场景")
print("=" * 60)

print("""
queue 模块典型应用:
  1. 生产者-消费者: 多线程爬虫, 下载队列管理
  2. 任务调度:    优先级队列处理紧急任务
  3. 线程池:      任务队列 + 工作线程 (类似 concurrent.futures)
  4. 消息缓冲:    日志/消息的异步处理
  5. 流量控制:    有界队列限制并发任务数

Python 版本选择:
  - queue.Queue    → 线程安全, 用于 threading
  - multiprocessing.Queue → 进程安全, 用于 multiprocessing
  - asyncio.Queue  → 协程安全, 用于 asyncio (Python 3.7+)
  - collections.deque → 高性能双端队列 (非线程安全)

线程安全说明:
  - queue.Queue 内部使用 threading.Lock
  - 所有操作 (put/get/empty/full) 都是原子操作
  - 不需要额外加锁
  - 适用场景: 线程间通信, 任务分发
""")
