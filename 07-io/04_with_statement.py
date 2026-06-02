"""
with 语句 - 上下文管理器

学习目标：
  - 上下文管理器协议：__enter__ / __exit__
  - 使用 contextlib.contextmanager 装饰器
  - 自定义上下文管理器
  - 嵌套 with 语句
  - 上下文管理器在资源管理中的应用
"""

from contextlib import contextmanager
import tempfile
import os
import time


def main():
    # ========== 1. __enter__ / __exit__ 协议 ==========
    print("=== 1. __enter__ / __exit__ 协议 ===")

    class Timer:
        """计时器上下文管理器：自动记录代码执行时间"""

        def __enter__(self):
            # with 进入时执行
            self.start = time.perf_counter()
            print("  [Timer 开始计时]")
            return self  # 返回值赋给 as 后的变量

        def __exit__(self, exc_type, exc_val, exc_tb):
            # with 退出时执行（正常或异常都会执行）
            elapsed = time.perf_counter() - self.start
            print(f"  [Timer 结束，耗时: {elapsed:.4f} 秒]")
            # 返回 False 让异常继续传播（默认行为）
            return False

        def elapsed_so_far(self):
            return time.perf_counter() - self.start

    with Timer() as timer:
        total = sum(range(1000000))
        print(f"  计算完成，sum = {total}")
        print(f"  已用时: {timer.elapsed_so_far():.4f} 秒")

    # ========== 2. 异常处理中的 __exit__ ==========
    print("\n=== 2. 异常处理中的 __exit__ ===")

    class SuppressError:
        """抑制特定异常的上下文管理器"""

        def __init__(self, exc_type_to_suppress):
            self.exc_type = exc_type_to_suppress

        def __enter__(self):
            print(f"  [进入上下文，将抑制 {self.exc_type.__name__}]")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                if issubclass(exc_type, self.exc_type):
                    print(f"  [已捕获并抑制异常: {exc_val}]")
                    return True  # 返回 True 表示异常已处理，不传播
                else:
                    print(f"  [其他异常: {exc_val}]")
            else:
                print("  [正常退出，无异常]")
            return False  # 返回 False 让异常继续传播

    print("情况1：正常退出")
    with SuppressError(ValueError):
        result = 1 + 1  # 正常执行

    print("\n情况2：捕获并抑制匹配的异常")
    with SuppressError(ValueError):
        # 这段代码会抛出 ValueError，但被 __exit__ 抑制
        int("not_a_number")
    print("  （异常已被抑制，程序继续执行）")

    print("\n情况3：不匹配的异常仍然会抛出（演示用 try 包裹）")
    try:
        with SuppressError(ValueError):
            1 / 0  # ZeroDivisionError 不在抑制范围内
    except ZeroDivisionError as e:
        print(f"  [未抑制的异常: {e}]")

    # ========== 3. contextlib.contextmanager 装饰器 ==========
    print("\n=== 3. contextlib.contextmanager 装饰器 ===")

    @contextmanager
    def temp_file(content="", suffix=".txt"):
        """使用 contextmanager 装饰器创建上下文管理器（更简洁）

        yield 之前 = __enter__ 逻辑
        yield 之后 = __exit__ 逻辑
        yield 的值 = as 变量的值
        """
        # __enter__ 部分
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        filepath = tmp.name
        tmp.write(content)
        tmp.close()
        print(f"  [创建临时文件: {filepath}]")

        try:
            yield filepath  # 返回给 as 变量
        finally:
            # __exit__ 部分（总是执行）
            if os.path.exists(filepath):
                os.unlink(filepath)
                print(f"  [清理临时文件: {filepath}]")

    with temp_file("Hello contextmanager!") as path:
        with open(path, "r", encoding="utf-8") as f:
            print(f"  文件内容: {f.read()}")

    # ========== 4. 嵌套 with 语句 ==========
    print("\n=== 4. 嵌套 with 语句 ===")

    # 方式一：多个 with 嵌套
    print("方式一：嵌套 with")
    tmp_dir = tempfile.mkdtemp(prefix="py_nested_")
    f1 = os.path.join(tmp_dir, "a.txt")
    f2 = os.path.join(tmp_dir, "b.txt")
    try:
        with open(f1, "w", encoding="utf-8") as file1:
            with open(f2, "w", encoding="utf-8") as file2:
                file1.write("文件A的内容\n")
                file2.write("文件B的内容\n")
                print("  同时打开了两个文件并写入")

        # 方式二：同一行写多个 with（Python 3.1+）
        print("方式二：同行多个 with")
        with open(f1, "r", encoding="utf-8") as r1, open(f2, "r", encoding="utf-8") as r2:
            print(f"  文件A: {r1.read().strip()}")
            print(f"  文件B: {r2.read().strip()}")
    finally:
        for f in [f1, f2]:
            if os.path.exists(f):
                os.unlink(f)
        os.rmdir(tmp_dir)

    # ========== 5. 自定义上下文管理器：事务模拟 ==========
    print("\n=== 5. 自定义上下文管理器：事务模拟 ===")

    class Transaction:
        """模拟数据库事务：自动提交或回滚"""

        def __init__(self, name):
            self.name = name
            self._operations = []

        def __enter__(self):
            print(f"  [事务 '{self.name}' 开始]")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self._commit()
                print(f"  [事务 '{self.name}' 已提交]")
            else:
                self._rollback()
                print(f"  [事务 '{self.name}' 已回滚，原因: {exc_val}]")
            return False

        def execute(self, sql):
            self._operations.append(sql)
            print(f"    执行: {sql}")

        def _commit(self):
            print(f"    提交了 {len(self._operations)} 条操作")

        def _rollback(self):
            print(f"    回滚了 {len(self._operations)} 条操作")

    # 正常提交
    print("正常事务：")
    with Transaction("create_user") as tx:
        tx.execute("INSERT INTO users VALUES (1, '张三')")
        tx.execute("INSERT INTO profiles VALUES (1, '管理员')")

    # 异常回滚
    print("\n异常导致回滚：")
    try:
        with Transaction("transfer_money") as tx:
            tx.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
            tx.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
            raise ValueError("余额不足")
    except ValueError:
        print("  （异常已被外层 try 捕获）")

    # ========== 6. 上下文管理器应用总结 ==========
    print("\n=== 6. 上下文管理器常见应用 ===")
    examples = [
        ("文件操作", "with open('file.txt') as f: ..."),
        ("线程锁", "with threading.Lock(): ..."),
        ("数据库连接", "with db.connect() as conn: ..."),
        ("网络请求", "with requests.Session() as s: ..."),
        ("临时目录", "with tempfile.TemporaryDirectory() as d: ..."),
        ("计时/性能测试", "with Timer() as t: ..."),
        ("重定向输出", "with redirect_stdout(buf): ..."),
    ]
    for app, code in examples:
        print(f"  {app}: {code}")


if __name__ == "__main__":
    main()
