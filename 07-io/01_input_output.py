"""
输入输出 - Python 的数据输入与输出

学习目标：
  - print() 高级参数：sep / end / file / flush
  - 格式化输出：f-string / format() / % 格式化
  - input() 函数（演示原理，不阻塞执行）
"""

import sys
import io
import time


def main():
    # ========== 1. print() 的 sep 参数（分隔符） ==========
    print("=== 1. print() 的 sep 参数 ===")

    # 默认 sep=' '（空格分隔）
    print("苹果", "香蕉", "橘子")
    # 自定义分隔符
    print("苹果", "香蕉", "橘子", sep=", ")
    print("2026", "06", "02", sep="-")
    print("第一", "第二", "第三", sep=" -> ")
    # sep="" 可以无缝拼接
    print("Hello", "World", sep="")

    # ========== 2. print() 的 end 参数（行尾字符） ==========
    print("\n=== 2. print() 的 end 参数 ===")

    # 默认 end='\n'（换行）
    # end='' 不换行
    print("加载中", end="")
    print(".", end="")
    print(".", end="")
    print(".")  # 最后恢复换行

    # end 可以是任意字符串
    for i in range(1, 6):
        print(i, end=" → " if i < 5 else "\n")

    # ========== 3. print() 的 file 参数（输出到文件） ==========
    print("\n=== 3. print() 的 file 参数 ===")

    # 将输出重定向到字符串缓冲区
    buffer = io.StringIO()
    print("这行写入了 StringIO 缓冲区", file=buffer)

    # 默认输出到 sys.stdout
    print("这行正常输出到控制台")
    sys.stdout.write("sys.stdout.write 也能直接输出\n")

    # 读取缓冲区内容
    print(f"缓冲区内容: {buffer.getvalue().strip()}")
    buffer.close()

    # ========== 4. print() 的 flush 参数（立即刷新） ==========
    print("\n=== 4. print() 的 flush 参数 ===")
    print("flush=True 强制立即输出，不等待缓冲区填满")
    print("适用于实时日志、进度条等场景")
    # 演示（在脚本中效果不明显，但在长时间运行的程序中很有用）
    print("处理中", end="", flush=True)
    time.sleep(0.1)  # 模拟耗时操作
    print(".", end="", flush=True)
    time.sleep(0.1)
    print(".", end="", flush=True)
    time.sleep(0.1)
    print(" 完成!")

    # ========== 5. f-string 格式化输出（Python 3.6+） ==========
    print("\n=== 5. f-string 格式化输出 ===")

    name = "小明"
    age = 25
    score = 95.5678

    # 基本用法
    print(f"姓名: {name}, 年龄: {age}")

    # 表达式
    print(f"明年 {name} 就 {age + 1} 岁了")

    # 格式说明符：保留小数位
    print(f"成绩: {score:.2f}")

    # 宽度与对齐
    print(f"|{'左对齐':<10}|{'居中':^10}|{'右对齐':>10}|")

    # 数字格式化（千分位、百分比）
    price = 1234567
    rate = 0.8523
    print(f"价格: {price:,}")       # 千分位分隔
    print(f"比率: {rate:.2%}")      # 百分比
    print(f"二进制: {255:b}")       # 二进制
    print(f"十六进制: {255:#x}")    # 十六进制（带 0x 前缀）

    # ========== 6. str.format() 方法 ==========
    print("\n=== 6. str.format() 方法 ===")

    # 位置参数
    print("{} 今年 {} 岁".format("小红", 22))

    # 索引参数（可以重复使用）
    print("{0} 喜欢 {1}，{0} 也喜欢 {2}".format("小明", "打球", "编程"))

    # 关键字参数
    print("{name} 的成绩是 {score:.1f} 分".format(name="小刚", score=88.5))

    # 字典解包
    info = {"city": "北京", "temp": 26}
    print("城市: {city}, 温度: {temp}°C".format(**info))

    # ========== 7. % 格式化（旧式风格） ==========
    print("\n=== 7. %% 格式化（旧式风格） ===")

    # 基本占位符
    print("Hello, %s!" % "World")           # %s 字符串
    print("整数: %d" % 42)                  # %d 整数
    print("浮点数: %.2f" % 3.14159)         # %f 浮点数
    print("十六进制: %x" % 255)             # %x 十六进制

    # 多个值用元组
    print("%s 考了 %d 分" % ("小明", 95))

    # 注意：f-string 是现代 Python 推荐的方式

    # ========== 8. input() 函数（演示原理） ==========
    print("\n=== 8. input() 函数 ===")

    # input() 会阻塞程序等待用户输入，不适合自动化脚本
    # 这里演示其工作原理（不实际调用）
    print("input() 的基本用法（不实际执行）:")
    print('  name = input("请输入你的名字: ")')
    print("  input() 总是返回字符串类型")
    print("  如需数字，需要类型转换: int(input('年龄: '))")
    print()
    print("在自动化测试中，可以模拟输入:")

    # 模拟 input()：用 StringIO 替换 sys.stdin
    original_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO("Python学习者\n25\n")
        # 模拟的输入（自动读取，不会阻塞）
        fake_name = input("(模拟) 姓名: ")
        fake_age = input("(模拟) 年龄: ")
        print(f"模拟输入结果: 姓名={fake_name}, 年龄={fake_age}")
    finally:
        sys.stdin = original_stdin


if __name__ == "__main__":
    main()
