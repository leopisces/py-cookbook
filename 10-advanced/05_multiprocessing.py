"""
多进程编程 (Multiprocessing)
==============================
Python 多进程: Process 创建(函数/类)、start/join、Queue 进程间通信、
Pipe 管道、Value/Array 共享状态、Pool 进程池(map/apply/apply_async)、
与 threading 多线程的 CPU 密集型任务性能对比。

multiprocessing 模块解决了 threading 受 GIL 限制无法利用多核的问题，
每个进程有独立的 Python 解释器和 GIL，真正实现并行计算。

参考: https://www.runoob.com/python3/python3-multiprocessing.html
"""

import multiprocessing
import os
import time
import threading
from multiprocessing import Process, Queue, Pipe, Value, Array, Pool


# ========== 多进程目标函数 (模块级别，供子进程导入) ==========

def _worker(name, count):
    """工作进程执行函数 - 模拟耗时任务"""
    pid = os.getpid()
    for i in range(count):
        print(f"  [进程 {name} PID={pid}] 第 {i+1} 次执行")
        time.sleep(0.1)


def _cpu_heavy(n):
    """纯 CPU 计算任务 - 计算 1 到 n 的累加和（无 I/O 操作）"""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def _square(n):
    """计算平方（供进程池使用）"""
    return n * n


def _sender(conn, messages):
    """Pipe 发送端进程"""
    for msg in messages:
        print(f"  [发送] → {msg}")
        conn.send(msg)
        time.sleep(0.1)
    conn.close()


def _receiver(conn):
    """Pipe 接收端进程"""
    while True:
        try:
            msg = conn.recv()
            print(f"  [接收] ← {msg}")
        except EOFError:
            print("  [接收] 管道已关闭，接收完毕")
            break


def _producer(q, items):
    """Queue 生产者进程 - 向队列放入数据"""
    for item in items:
        print(f"  [生产者] 放入: {item}")
        q.put(item)
        time.sleep(0.1)


def _consumer(q, name):
    """Queue 消费者进程 - 从队列取出数据"""
    while True:
        item = q.get()
        if item is None:  # 哨兵值，表示结束
            print(f"  [消费者-{name}] 收到结束信号，退出")
            break
        print(f"  [消费者-{name}] 取出: {item}")


def _increment_shared(val, arr, count):
    """操作共享内存的进程: 累加 Value，修改 Array"""
    for i in range(count):
        val.value += 1
        arr[i % len(arr)] = arr[i % len(arr)] + 1
        time.sleep(0.05)


# ========== 继承 Process 的自定义进程类 ==========

class _MyProcess(Process):
    """继承 multiprocessing.Process，重写 run() 方法"""

    def __init__(self, name, count):
        super().__init__()
        self._name = name
        self._count = count

    def run(self):
        """进程启动后自动调用，类似 threading.Thread.run()"""
        pid = os.getpid()
        for i in range(self._count):
            print(f"  [MyProcess {self._name} PID={pid}] 步骤 {i+1}")
            time.sleep(0.1)


# ========== 演示 1: Process 创建 - 函数方式 ==========
def demo_process_function():
    """使用 multiprocessing.Process(target=函数) 创建子进程"""
    print("=" * 50)
    print("演示 1: Process 创建 - 函数方式")
    print("=" * 50)

    print(f"  主进程 PID: {os.getpid()}")
    print("  创建并启动子进程 A 和 B...")

    p1 = Process(target=_worker, args=("A", 3))
    p2 = Process(target=_worker, args=("B", 3))

    p1.start()  # 启动子进程 A
    p2.start()  # 启动子进程 B

    print("  等待子进程结束...")
    p1.join()   # 主进程等待 p1 完成
    p2.join()   # 主进程等待 p2 完成
    print("  两个子进程都已执行完毕\n")


# ========== 演示 2: Process 创建 - 类方式 ==========
def demo_process_class():
    """继承 multiprocessing.Process 类来创建子进程"""
    print("=" * 50)
    print("演示 2: Process 创建 - 类方式")
    print("=" * 50)

    print(f"  主进程 PID: {os.getpid()}")
    print("  使用自定义 _MyProcess 类创建子进程...")

    p1 = _MyProcess("X", 3)
    p2 = _MyProcess("Y", 3)

    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("  类方式创建的子进程执行完毕\n")


# ========== 演示 3: 进程间通信 - Queue 和 Pipe ==========
def demo_queue_pipe():
    """multiprocessing.Queue 和 Pipe 实现进程间通信"""
    print("=" * 50)
    print("演示 3: 进程间通信 - Queue 和 Pipe")
    print("=" * 50)

    # --- 3a. Queue 生产者-消费者模式 ---
    print("--- 3a. Queue 队列通信 ---")
    print("  multiprocessing.Queue 底层使用管道+序列化，支持跨进程传递数据")
    print("  (对比 threading.Queue 只能在同一进程内线程间共享)\n")

    q = Queue()
    items = ["苹果", "香蕉", "橙子", "葡萄"]

    prod = Process(target=_producer, args=(q, items))
    cons1 = Process(target=_consumer, args=(q, "A"))
    cons2 = Process(target=_consumer, args=(q, "B"))

    cons1.start()
    cons2.start()
    prod.start()

    prod.join()          # 等待生产者完成
    q.put(None)          # 发送消费者 A 的结束信号
    q.put(None)          # 发送消费者 B 的结束信号
    cons1.join()
    cons2.join()
    print("  生产者-消费者全部结束\n")

    # --- 3b. Pipe 管道通信 ---
    print("--- 3b. Pipe 管道通信 ---")
    print("  Pipe 返回一对连接对象，支持双向通信（默认 duplex=True）\n")

    parent_conn, child_conn = Pipe()
    messages = ["消息1", "消息2", "消息3"]

    sender_p = Process(target=_sender, args=(parent_conn, messages))
    receiver_p = Process(target=_receiver, args=(child_conn,))

    receiver_p.start()
    sender_p.start()

    # 主进程关闭自己的连接副本，让子进程独占管道
    # 只有所有写端关闭后，接收端才能收到 EOFError
    parent_conn.close()
    child_conn.close()

    sender_p.join()
    receiver_p.join()
    print()


# ========== 演示 4: 共享状态 - Value / Array ==========
def demo_shared_state():
    """multiprocessing.Value 和 Array 实现进程间共享内存"""
    print("=" * 50)
    print("演示 4: 共享状态 - Value / Array")
    print("=" * 50)

    print("  Value: 单个共享值（支持 int/float 等类型）")
    print("  Array: 共享数组（类似 ctypes 数组）")
    print("  注意: 进程间不共享全局变量，必须使用这些机制来共享数据\n")

    # Value('i', 0) → 类型 'i' 表示 C 的 int，初始值 0
    shared_val = Value('i', 0)
    # Array('i', [0, 0, 0]) → 包含 3 个 int 的共享数组
    shared_arr = Array('i', [0, 0, 0])

    print(f"  初始状态 - Value: {shared_val.value}, Array: {shared_arr[:]}\n")

    procs = []
    for pid in range(3):
        p = Process(target=_increment_shared, args=(shared_val, shared_arr, 3))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()

    print(f"\n  最终状态 - Value: {shared_val.value} (期望: 3进程 × 3次 = 9)")
    print(f"  Array: {shared_arr[:]} (每个元素被3个进程各加3次)")
    print()


# ========== 演示 5: 进程池 Pool ==========
def demo_pool():
    """multiprocessing.Pool 进程池: map/apply/apply_async"""
    print("=" * 50)
    print("演示 5: 进程池 Pool")
    print("=" * 50)

    print("  Pool 管理固定数量的工作进程，自动分配任务\n")

    # 创建包含 3 个工作进程的进程池
    with Pool(processes=3) as pool:
        # --- 5a. pool.map: 并行 map，保持输入顺序 ---
        print("--- 5a. pool.map 并行映射 ---")
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        results = pool.map(_square, numbers)
        print(f"  输入: {numbers}")
        print(f"  输出: {results}")
        print("  map 将任务分配到3个进程，结果保持输入顺序\n")

        # --- 5b. pool.apply: 同步调用（阻塞） ---
        print("--- 5b. pool.apply 同步调用 ---")
        result = pool.apply(_square, (10,))
        print(f"  apply(_square, (10,)) = {result}")
        print("  apply 会阻塞主进程，等待任务完成\n")

        # --- 5c. pool.apply_async: 异步调用（非阻塞） ---
        print("--- 5c. pool.apply_async 异步调用 ---")
        async_results = [pool.apply_async(_square, (i,)) for i in range(11, 15)]
        print("  提交了4个异步任务，主进程可以继续做其他事情...")
        time.sleep(0.3)  # 模拟主进程做其他工作
        print(f"  结果: {[r.get() for r in async_results]}")
        print("  使用 get() 获取异步结果时会阻塞等待\n")

    print()


# ========== 演示 6: 与 threading 对比 - CPU 密集型任务 ==========
def demo_vs_threading():
    """CPU 密集型任务: 多进程 vs 多线程 vs 单线程性能对比"""
    print("=" * 50)
    print("演示 6: 与 threading 对比 - CPU 密集型任务")
    print("=" * 50)

    N = 3_000_000  # 计算量（足够展示性能差异）

    # --- 单线程顺序执行 ---
    start = time.time()
    _cpu_heavy(N)
    _cpu_heavy(N)
    seq_time = time.time() - start

    # --- threading 多线程（受 GIL 限制，反而更慢） ---
    start = time.time()
    t1 = threading.Thread(target=_cpu_heavy, args=(N,))
    t2 = threading.Thread(target=_cpu_heavy, args=(N,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    thread_time = time.time() - start

    # --- multiprocessing 多进程（利用多核，真正并行） ---
    start = time.time()
    p1 = Process(target=_cpu_heavy, args=(N,))
    p2 = Process(target=_cpu_heavy, args=(N,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    proc_time = time.time() - start

    print(f"  任务: 每个执行 _cpu_heavy({N:,}) 两次")
    print(f"  CPU 核心数: {multiprocessing.cpu_count()}")
    print()
    label1 = "单线程顺序".ljust(16)
    label2 = "threading 双线程".ljust(16)
    label3 = "multiprocessing 双进程".ljust(16)
    print(f"  {label1} {seq_time:.3f} 秒  (基准)")
    print(f"  {label2} {thread_time:.3f} 秒  (GIL 导致线程切换开销)")
    print(f"  {label3} {proc_time:.3f} 秒  (真正并行)")
    print()
    print("  结论:")
    print("  - CPU 密集型任务 → 使用 multiprocessing（利用多核加速）")
    print("  - I/O 密集型任务 → 使用 threading 或 asyncio（GIL 影响小）")
    print("  - 多进程开销: 需序列化数据、启动进程，任务太小可能得不偿失\n")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_process_function()
    demo_process_class()
    demo_queue_pipe()
    demo_shared_state()
    demo_pool()
    demo_vs_threading()
    print("\n=== 所有多进程演示完成! ===")

# ============================================================
# 相关主题:
#   - 10-advanced/01_threading.py  → GIL对比与线程/进程选择
# ============================================================
