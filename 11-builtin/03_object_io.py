"""
内置函数 — 输入输出与执行相关 (I/O / Execution / Other)
==========================================================
演示与代码执行、文件操作、作用域相关的 Python 内置函数：
eval, exec, compile, open, globals, locals
以及内置函数的实用组合案例。

参考: https://www.runoob.com/python3/python3-built-in-functions.html
"""

import tempfile
import os


# ========== 演示 1: 输入输出与执行相关函数 ==========
def demo_io_exec_functions():
    """eval / exec / open / compile / globals / locals"""
    print("=" * 50)
    print("演示 1: 输入输出与执行相关函数")
    print("=" * 50)

    # --- eval(): 执行表达式字符串并返回值 ---
    print("--- eval() ---")
    print(f"  eval('2 + 3 * 4')  = {eval('2 + 3 * 4')}")
    print(f"  eval('[1,2,3]')    = {eval('[1,2,3]')}")
    x_val = 10
    print(f"  eval('x_val * 2')   = {eval('x_val * 2')}")
    # 安全: 可以限制可用命名空间
    print(f"  eval('min([1,2,3])', {{'min': min}}) = {eval('min([1,2,3])', {'min': min})}")

    # --- exec(): 执行代码块（无返回值） ---
    print("\n--- exec() ---")
    code = """
result = 0
for i in range(1, 6):
    result += i
"""
    local_ns = {}
    exec(code, {}, local_ns)
    print(f"  exec('1到5求和') → result = {local_ns['result']}")

    # --- open(): 文件操作 ---
    print("\n--- open() ---")
    fd, tmp_path = tempfile.mkstemp(suffix=".txt", prefix="builtin_demo_")
    os.close(fd)
    # 写入
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("Hello, Python!\n内置函数演示。\n")
    # 读取
    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  文件内容: {content.strip().split(chr(10))}")
    os.unlink(tmp_path)

    # --- compile(): 编译代码为可执行对象 ---
    print("\n--- compile() ---")
    compiled = compile("a + b", "<test>", "eval")
    result = eval(compiled, {"a": 3, "b": 4})
    print(f"  compile + eval: 3 + 4 = {result}")

    # --- globals() / locals(): 查看当前作用域变量 ---
    print("\n--- globals() / locals() ---")
    test_var = "I am local"
    print(f"  'test_var' in locals(): {'test_var' in locals()}")
    print(f"  '__name__' in globals(): {'__name__' in globals()}")
    print()


# ========== 演示 2: 实用组合案例 ==========
def demo_practical_combos():
    """展示几个内置函数组合使用的实用案例"""
    print("=" * 50)
    print("演示 2: 实用组合案例")
    print("=" * 50)

    # 案例1: 学生成绩统计
    print("--- 案例1: 成绩统计 ---")
    students = [
        {"name": "张三", "score": 85},
        {"name": "李四", "score": 92},
        {"name": "王五", "score": 78},
        {"name": "赵六", "score": 95},
        {"name": "钱七", "score": 60},
    ]
    # 平均分
    avg = sum(s["score"] for s in students) / len(students)
    print(f"  平均分: {avg:.1f}")
    # 最高分和最低分
    best = max(students, key=lambda s: s["score"])
    worst = min(students, key=lambda s: s["score"])
    print(f"  最高分: {best['name']} ({best['score']})")
    print(f"  最低分: {worst['name']} ({worst['score']})")
    # 及格人数
    passed = sum(1 for s in students if s["score"] >= 60)
    print(f"  及格人数: {passed}/{len(students)}")
    # 按分数排序
    ranked = sorted(students, key=lambda s: s["score"], reverse=True)
    names_ranked = [s["name"] for s in ranked]
    print(f"  排名: {names_ranked}")

    # 案例2: 字符串处理组合
    print("\n--- 案例2: 字符串处理 ---")
    text = "  Hello, Python World! 123  "
    # strip + filter + map 组合
    chars = list(filter(str.isalpha, text.strip()))
    print(f"  提取字母: {chars}")
    # 转换为大写并去重
    upper_unique = sorted(set(ch.upper() for ch in chars))
    print(f"  大写去重排序: {''.join(upper_unique)}")

    # 案例3: 数据验证
    print("\n--- 案例3: 数据验证 ---")
    values = [1, 2, "3", None, 5, "abc"]
    # 过滤并转换为整数
    ints = []
    for v in values:
        if isinstance(v, (int, str)):
            try:
                ints.append(int(v))
            except (ValueError, TypeError):
                pass
    print(f"  有效整数: {ints}")
    print(f"  总和: {sum(ints)}")
    print(f"  全部为正? {all(n > 0 for n in ints)}")

    # 案例4: 动态对象操作
    print("\n--- 案例4: 动态对象操作 ---")

    class Config:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def __repr__(self):
            attrs = [f"{k}={v!r}" for k, v in vars(self).items()]
            return f"Config({', '.join(attrs)})"

    cfg = Config(host="localhost", port=8080, debug=True)
    print(f"  配置: {cfg}")
    print(f"  属性列表: {list(vars(cfg).keys())}")
    for attr_name in sorted(dir(cfg)):
        if not attr_name.startswith("_"):
            val = getattr(cfg, attr_name)
            print(f"    cfg.{attr_name} = {val}")

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_io_exec_functions()
    demo_practical_combos()
    print("\n=== 所有内置函数演示完成! ===")
