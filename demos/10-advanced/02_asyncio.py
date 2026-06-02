"""
异步编程 (Asyncio)
=====================
Python asyncio: async/await 定义协程、asyncio.run()、asyncio.create_task()、
asyncio.gather()、异步 HTTP 请求概念、异步文件操作概念。

参考: https://www.runoob.com/python3/python3-asyncio.html
"""

import asyncio
import time
import tempfile
import os


# ========== 演示 1: async/await 基本用法 ==========
async def demo_async_await():
    """async/await 定义和运行协程"""
    print("=" * 50)
    print("演示 1: async/await 基本用法")
    print("=" * 50)

    async def greet(name):
        """这是一个协程函数（coroutine function）"""
        print(f"  你好，{name}！")
        await asyncio.sleep(0.1)  # 模拟异步等待
        print(f"  再见，{name}！")
        return f"已处理: {name}"

    # 调用协程函数返回的是一个协程对象（coroutine object）
    coro = greet("小明")
    print(f"  协程对象: {coro}")

    # 运行协程并获取结果
    result = await coro
    print(f"  返回结果: {result}")

    print()


# ========== 演示 2: asyncio.run() 运行协程 ==========
def demo_asyncio_run():
    """asyncio.run() 是运行异步程序的入口"""
    print("=" * 50)
    print("演示 2: asyncio.run() 顶层入口")
    print("=" * 50)

    async def fetch_data(item, delay):
        """模拟异步获取数据"""
        print(f"  开始获取 {item}...")
        await asyncio.sleep(delay)  # 模拟 I/O 等待
        print(f"  完成获取 {item}")
        return f"数据-{item}"

    async def main():
        """主协程: 所有异步逻辑的起点"""
        print("  程序开始")
        result = await fetch_data("用户信息", 0.1)
        print(f"  获取到: {result}")
        print("  程序结束")

    asyncio.run(main())
    print()


# ========== 演示 3: asyncio.create_task() 并发任务 ==========
async def demo_create_task():
    """asyncio.create_task() 创建并发运行的 Task"""
    print("=" * 50)
    print("演示 3: create_task() 创建并发任务")
    print("=" * 50)

    async def download(name, duration):
        """模拟下载任务"""
        print(f"  [开始] 下载 {name}")
        await asyncio.sleep(duration)
        print(f"  [完成] 下载 {name}")
        return f"{name} 下载完毕"

    async def main():
        start = time.time()

        # 串行执行（一个接一个）
        print("--- 串行执行 ---")
        await download("A", 0.1)
        await download("B", 0.1)
        await download("C", 0.1)
        serial_time = time.time() - start

        # 并行执行（使用 create_task）
        start = time.time()
        print("\n--- 并行执行 (create_task) ---")
        task1 = asyncio.create_task(download("X", 0.1))
        task2 = asyncio.create_task(download("Y", 0.1))
        task3 = asyncio.create_task(download("Z", 0.1))

        # 等待所有任务完成
        result1 = await task1
        result2 = await task2
        result3 = await task3

        parallel_time = time.time() - start

        print(f"\n  串行耗时: {serial_time:.3f}s")
        print(f"  并行耗时: {parallel_time:.3f}s")
        print(f"  结果: {result1}, {result2}, {result3}")


# ========== 演示 4: asyncio.gather() 批量运行 ==========
async def demo_gather():
    """asyncio.gather() 同时运行多个协程并收集结果"""
    print("\n" + "=" * 50)
    print("演示 4: asyncio.gather() 批量并发")
    print("=" * 50)

    async def process(n):
        """模拟处理任务"""
        await asyncio.sleep(n * 0.05)
        return n * n

    async def main():
        # gather 接收多个协程，并发执行，返回结果列表（保持传入顺序）
        print("  同时启动 5 个任务...")
        results = await asyncio.gather(
            process(1),
            process(2),
            process(3),
            process(4),
            process(5),
        )
        print(f"  gather 结果: {results}")

        # gather 设置 return_exceptions=True 时异常不会抛出
        async def might_fail():
            await asyncio.sleep(0.05)
            raise ValueError("模拟出错")

        results2 = await asyncio.gather(
            process(1),
            might_fail(),
            process(3),
            return_exceptions=True,  # 异常作为结果返回而不是抛出
        )
        print(f"  含异常的结果: {results2}")


# ========== 演示 5: 异步 HTTP 请求概念 ==========
async def demo_async_http():
    """演示异步 HTTP 请求的 API 模式（不实际发送请求）"""
    print("\n" + "=" * 50)
    print("演示 5: 异步 HTTP 请求概念")
    print("=" * 50)

    # 模拟异步 HTTP 客户端的 API 模式
    # 真实场景使用 aiohttp 库: pip install aiohttp
    # 这里仅演示 API 调用模式

    async def async_get(url):
        """模拟异步 HTTP GET 请求"""
        print(f"  GET {url} ...")
        await asyncio.sleep(0.05)  # 模拟网络延迟
        return f"200 OK: {url}"

    async def async_post(url, data):
        """模拟异步 HTTP POST 请求"""
        print(f"  POST {url} data={data} ...")
        await asyncio.sleep(0.05)  # 模拟网络延迟
        return f"201 Created: {url}"

    async def main():
        # 并发发送多个请求（真实场景中这是核心优势）
        responses = await asyncio.gather(
            async_get("https://api.example.com/users"),
            async_get("https://api.example.com/posts"),
            async_post("https://api.example.com/login", {"user": "admin"}),
        )
        for resp in responses:
            print(f"  响应: {resp}")

    # 这里 demo_async_http 自身也是 async，可以直接 await
    await main()


# ========== 演示 6: 异步文件操作概念 ==========
async def demo_async_file():
    """演示异步文件操作的概念"""
    print("\n" + "=" * 50)
    print("演示 6: 异步文件操作概念")
    print("=" * 50)

    # 标准库的 open/read/write 是同步的
    # 异步文件操作需要使用 aiofiles 库: pip install aiofiles
    # 这里演示如何用 asyncio 包装同步文件操作

    async def write_file(filename, content):
        """模拟异步文件写入（实际使用 run_in_executor 包装同步操作）"""
        print(f"  写入文件: {filename}")
        # 使用线程池运行同步 I/O，避免阻塞事件循环
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,  # 使用默认的 ThreadPoolExecutor
            lambda: open(filename, "w", encoding="utf-8").write(content),
        )
        print(f"  写入完成: {filename}")

    async def read_file(filename):
        """模拟异步文件读取"""
        print(f"  读取文件: {filename}")
        loop = asyncio.get_running_loop()

        def _read():
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()

        content = await loop.run_in_executor(None, _read)
        print(f"  读取内容: {content.strip()}")
        return content

    # 创建临时文件进行演示
    fd, tmp_path = tempfile.mkstemp(suffix=".txt", prefix="async_demo_")

    try:
        # 写入
        await write_file(tmp_path, "Hello from asyncio!\n异步编程很强大。\n")

        # 读取
        await read_file(tmp_path)
    finally:
        os.close(fd)
        os.unlink(tmp_path)  # 删除临时文件

    print()

    # 对比: 同步方式与异步方式
    print("--- 同步 vs 异步文件操作 ---")
    print("  同步: 读写时阻塞整个线程")
    print("  异步: 使用 run_in_executor 将阻塞操作放到线程池")
    print("  真实项目: 用 aiofiles 库 (pip install aiofiles)")
    print("    import aiofiles")
    print('    async with aiofiles.open("file.txt", "r") as f:')
    print("        content = await f.read()")


# ========== 演示 7: 异步超时与取消 ==========
async def demo_timeout_cancel():
    """asyncio.wait_for() 超时和 task.cancel() 取消"""
    print("\n" + "=" * 50)
    print("演示 7: 异步超时与取消")
    print("=" * 50)

    async def slow_task(name, delay):
        """一个耗时较长的任务"""
        print(f"  {name}: 开始执行 (预计 {delay}s)")
        try:
            await asyncio.sleep(delay)
            print(f"  {name}: 正常完成")
            return f"{name} 结果"
        except asyncio.CancelledError:
            print(f"  {name}: 被取消了！")
            raise  # 重新抛出以传播取消

    async def main():
        # --- wait_for: 设置超时 ---
        print("--- wait_for 超时 ---")
        try:
            result = await asyncio.wait_for(slow_task("慢任务", 1.0), timeout=0.15)
            print(f"  结果: {result}")
        except asyncio.TimeoutError:
            print("  超时！任务被取消")

        # --- 手动取消任务 ---
        print("\n--- 手动取消任务 ---")
        task = asyncio.create_task(slow_task("可取消任务", 0.5))
        await asyncio.sleep(0.1)  # 让任务先跑一会儿
        task.cancel()  # 请求取消
        try:
            await task
        except asyncio.CancelledError:
            print("  任务已被手动取消")


# ========== 主程序入口 ==========
async def main_all():
    """运行所有演示"""
    await demo_async_await()
    await demo_create_task()
    await demo_gather()
    await demo_async_http()
    await demo_async_file()
    await demo_timeout_cancel()


if __name__ == "__main__":
    # demo_asyncio_run 是同步函数，先运行
    demo_asyncio_run()
    # 其余演示是异步的，用 asyncio.run 运行
    asyncio.run(main_all())
    print("\n=== 所有异步编程演示完成! ===")
