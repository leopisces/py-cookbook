"""
多线程编程 (Threading)
==========================
Python 多线程: Thread 创建(函数/类)、start/join、daemon 线程、Lock/RLock、
Event 线程间通信、ThreadPoolExecutor 线程池、GIL 简述。

参考: https://www.runoob.com/python3/python3-multithreading.html
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor


# ========== 演示 1: Thread 创建 - 函数方式 ==========
def demo_thread_function():
    """使用 threading.Thread(target=函数) 创建线程"""
    print("=" * 50)
    print("演示 1: 用函数创建线程")
    print("=" * 50)

    def worker(name, count):
        """线程执行的工作函数"""
        for i in range(count):
            print(f"  [线程 {name}] 第 {i+1} 次执行")
            time.sleep(0.1)

    # 创建线程，target 指定要执行的函数，args 传递参数
    t1 = threading.Thread(target=worker, args=("A", 3))
    t2 = threading.Thread(target=worker, args=("B", 3))

    print("启动线程...")
    t1.start()  # 启动线程 A
    t2.start()  # 启动线程 B

    print("等待线程结束...")
    t1.join()   # 主线程等待 t1 完成
    t2.join()   # 主线程等待 t2 完成
    print("两个线程都已执行完毕\n")


# ========== 演示 2: Thread 创建 - 类方式 ==========
def demo_thread_class():
    """继承 threading.Thread 类来创建线程"""
    print("=" * 50)
    print("演示 2: 用类创建线程")
    print("=" * 50)

    class MyThread(threading.Thread):
        """自定义线程类，必须重写 run() 方法"""

        def __init__(self, name, count):
            super().__init__()  # 必须调用父类的 __init__
            self.name = name
            self.count = count

        def run(self):
            """线程启动后自动调用此方法"""
            for i in range(self.count):
                print(f"  [MyThread {self.name}] 执行步骤 {i+1}")
                time.sleep(0.1)

    # 创建自定义线程实例
    t1 = MyThread("X", 3)
    t2 = MyThread("Y", 3)

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("类方式创建的线程执行完毕\n")


# ========== 演示 3: Daemon 守护线程 ==========
def demo_daemon():
    """
    守护线程: 当主线程结束时，守护线程会被强制终止。
    非守护线程: 主线程会等待其完成后再退出。
    """
    print("=" * 50)
    print("演示 3: Daemon 守护线程")
    print("=" * 50)

    def daemon_worker():
        """守护线程 - 会被主线程结束而强制终止"""
        for i in range(5):
            print(f"  [守护线程] 第 {i+1} 次运行")
            time.sleep(0.15)

    def non_daemon_worker():
        """非守护线程 - 主线程会等待它完成"""
        for i in range(3):
            print(f"  [普通线程] 第 {i+1} 次运行")
            time.sleep(0.1)

    d = threading.Thread(target=daemon_worker, daemon=True)   # 设为守护线程
    n = threading.Thread(target=non_daemon_worker)            # 普通线程

    d.start()
    n.start()

    print("主线程继续执行其他工作...")
    time.sleep(0.2)  # 主线程做些事情
    print("主线程即将结束...")
    # 注意: 守护线程 d 可能还没执行完就被终止了
    # 普通线程 n 会继续执行直到完成
    n.join()  # 显式等待普通线程结束
    print("普通线程已结束。注意守护线程可能提前终止。\n")


# ========== 演示 4: Lock / RLock 线程锁 ==========
def demo_locks():
    """Lock 互斥锁 和 RLock 可重入锁"""
    print("=" * 50)
    print("演示 4: Lock / RLock 线程锁")
    print("=" * 50)

    # --- Lock: 基本互斥锁 ---
    print("--- 4a. Lock 互斥锁 ---")

    counter = 0
    lock = threading.Lock()

    def increment():
        nonlocal counter
        for _ in range(100):
            # 使用 with 语句自动获取/释放锁（推荐方式）
            with lock:
                current = counter
                # 模拟计算时间（不加锁会出现竞态条件）
                time.sleep(0.001)
                counter = current + 1

    threads = [threading.Thread(target=increment) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  加锁后计数结果: {counter} (期望: 500)")

    # --- 竞态条件演示（不加锁会出错）---
    counter2 = 0

    def increment_unsafe():
        nonlocal counter2
        for _ in range(100):
            current = counter2
            time.sleep(0.001)
            counter2 = current + 1

    threads2 = [threading.Thread(target=increment_unsafe) for _ in range(5)]
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()
    print(f"  不加锁计数结果: {counter2} (可能不是 500，出现了竞态条件)")

    # --- RLock: 可重入锁 ---
    print("\n--- 4b. RLock 可重入锁 ---")
    # RLock 允许同一线程多次获取锁（Lock 会死锁）
    rlock = threading.RLock()

    def recursive_func(level):
        """递归函数，同一线程多次获取同一个 RLock"""
        rlock.acquire()
        try:
            if level > 0:
                print(f"    RLock 重入，层级: {level}")
                recursive_func(level - 1)
        finally:
            rlock.release()

    recursive_func(3)
    print("   RLock 递归获取/释放成功，不会死锁\n")


# ========== 演示 5: Event 线程间通信 ==========
def demo_event():
    """使用 Event 实现线程间的信号通信"""
    print("=" * 50)
    print("演示 5: Event 线程间通信")
    print("=" * 50)

    event = threading.Event()  # 创建事件对象

    def waiter():
        """等待事件触发"""
        print("  [等待线程] 等待事件触发...")
        event.wait()  # 阻塞直到 event.set() 被调用
        print("  [等待线程] 收到事件，开始执行工作！")

    def setter():
        """延迟后触发事件"""
        print("  [触发线程] 准备工作中...")
        time.sleep(0.3)
        print("  [触发线程] 触发事件！")
        event.set()  # 设置事件，唤醒所有等待的线程

    w = threading.Thread(target=waiter)
    s = threading.Thread(target=setter)

    w.start()
    s.start()
    w.join()
    s.join()
    print()

    # Event 的 clear() 方法可以重置事件状态
    print("  Event 重置演示:")
    event.clear()  # 重置事件
    result = event.wait(timeout=0.1)  # 带超时的等待
    print(f"  event.wait(timeout=0.1) 返回: {result} (超时返回 False)\n")


# ========== 演示 6: ThreadPoolExecutor 线程池 ==========
def demo_thread_pool():
    """使用 concurrent.futures.ThreadPoolExecutor 管理线程池"""
    print("=" * 50)
    print("演示 6: ThreadPoolExecutor 线程池")
    print("=" * 50)

    def square(n):
        """计算平方"""
        time.sleep(0.05)
        return n * n

    # 使用上下文管理器自动管理线程池生命周期
    with ThreadPoolExecutor(max_workers=3) as executor:
        # --- submit 方式: 逐个提交任务 ---
        print("--- submit 提交任务 ---")
        futures = []
        for i in range(1, 6):
            future = executor.submit(square, i)
            futures.append(future)
            print(f"  提交任务: square({i})")

        # 获取结果
        for i, future in enumerate(futures, 1):
            result = future.result()  # 阻塞直到任务完成
            print(f"  square({i}) = {result}")

        # --- map 方式: 批量提交任务 ---
        print("\n--- map 批量提交 ---")
        numbers = [6, 7, 8, 9, 10]
        results = executor.map(square, numbers)
        # map 返回迭代器，保持输入顺序
        for num, res in zip(numbers, results):
            print(f"  square({num}) = {res}")

    print()


# ========== 演示 7: GIL 简述 ==========
def demo_gil():
    """GIL (Global Interpreter Lock) 全局解释器锁简介"""
    print("=" * 50)
    print("演示 7: GIL (全局解释器锁) 简介")
    print("=" * 50)

    explanation = """
    GIL (Global Interpreter Lock) 是 CPython 解释器的一个机制:
    
    1. 同一时刻只有一个线程在执行 Python 字节码
    2. 多线程在 CPU 密集型任务上无法利用多核优势
    3. I/O 密集型任务（网络请求、文件读写）仍可受益于多线程
    4. 解决方案:
       - CPU 密集型 → 使用 multiprocessing 多进程
       - I/O 密集型 → 使用 threading 多线程或 asyncio 异步
       - 使用 C 扩展可以释放 GIL
    
    简单验证: 下面的 CPU 计算用多线程反而比单线程慢
    """
    print(explanation)

    # 演示: CPU 密集型任务
    import time

    def cpu_intensive():
        """纯 CPU 计算（无 I/O 操作）"""
        total = 0
        for i in range(5_000_000):
            total += i
        return total

    # 单线程
    start = time.time()
    cpu_intensive()
    single_time = time.time() - start

    # 多线程 (实际上会更慢，因为 GIL 竞争)
    start = time.time()
    t1 = threading.Thread(target=cpu_intensive)
    t2 = threading.Thread(target=cpu_intensive)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    multi_time = time.time() - start

    print(f"  单线程耗时: {single_time:.3f} 秒")
    print(f"  双线程耗时: {multi_time:.3f} 秒")
    print(f"  说明: 双线程反而更慢(约2倍)，这就是 GIL 的影响")
    print(f"  结论: CPU密集型用 multiprocessing，I/O密集型用 threading\n")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_thread_function()
    demo_thread_class()
    demo_daemon()
    demo_locks()
    demo_event()
    demo_thread_pool()
    demo_gil()
    print("\n=== 所有多线程演示完成! ===")
