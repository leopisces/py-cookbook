"""
Python 字符串

学习目标：
  - 字符串的创建与基本操作
  - 索引、切片、拼接
  - 常用方法: format, replace, split, join, strip, find, count
  - 编码与解码: encode, decode
  - 转义字符与原始字符串
"""

import re


def main():
    # ========== 1. 字符串的创建 ==========
    print("=== 1. 字符串的创建 ===")

    # 四种创建方式
    s1 = '单引号字符串'
    s2 = "双引号字符串"
    s3 = '''三个单引号
可以跨行
的字符串'''
    s4 = """三个双引号
也可以跨行
的字符串"""

    print(f"单引号: {s1}")
    print(f"双引号: {s2}")
    print(f"三单引号:\n{s3}")
    print(f"三双引号:\n{s4}")

    # 包含引号的字符串
    print(f"包含'单引号'的双引号字符串")
    print(f'包含"双引号"的单引号字符串')
    print(f"转义: 包含\"双引号\"和\'单引号\'")

    # ========== 2. 索引与切片 ==========
    print("\n=== 2. 索引与切片 ===")

    text = "Python编程"

    # 正向索引（从 0 开始）
    print(f"字符串: \"{text}\" (长度: {len(text)})")
    print(f"索引 0: '{text[0]}'")
    print(f"索引 1: '{text[1]}'")
    print(f"索引 6: '{text[6]}'")  # 中文字符

    # 反向索引（从 -1 开始）
    print(f"索引 -1: '{text[-1]}'")   # 最后一个字符
    print(f"索引 -3: '{text[-3]}'")

    # 切片 [start:stop:step]
    print(f"\n--- 切片操作 ---")
    print(f'text[0:6]   = "{text[0:6]}"')     # 取索引 0-5（左闭右开）
    print(f'text[:6]    = "{text[:6]}"')      # 从开头取到索引 5
    print(f'text[6:]    = "{text[6:]}"')      # 从索引 6 到末尾
    print(f'text[0:9:2] = "{text[0:9:2]}"')  # 步长为 2
    print(f'text[::-1]  = "{text[::-1]}"')   # 反向步长 → 反转字符串

    # ========== 3. 字符串拼接 ==========
    print("\n=== 3. 字符串拼接 ===")

    a, b = "Hello", "World"

    # 方式一: + 运算符
    result1 = a + " " + b
    print(f"+ 拼接: {result1}")

    # 方式二: f-string（推荐）
    name, age = "张三", 25
    result2 = f"我叫{name}，今年{age}岁"
    print(f"f-string: {result2}")

    # 方式三: format() 方法
    result3 = "我叫{}，今年{}岁".format(name, age)
    print(f"format(): {result3}")

    # 方式四: % 格式化（旧式）
    result4 = "我叫%s，今年%d岁" % (name, age)
    print(f"%格式化: {result4}")

    # 方式五: join() 方法
    words = ["Python", "is", "awesome"]
    result5 = " ".join(words)
    print(f"join(): {result5}")

    # ========== 4. 常用方法 ==========
    print("\n=== 4. 常用方法 ===")

    sample = "  Hello, Python World!  "

    print(f"原始字符串: \"{sample}\"")

    # 大小写转换
    print(f"upper(): \"{sample.upper()}\"")       # 全大写
    print(f"lower(): \"{sample.lower()}\"")        # 全小写
    print(f"title(): \"{sample.title()}\"")        # 首字母大写
    print(f"capitalize(): \"{sample.capitalize()}\"")  # 句首大写

    # 去空白
    print(f"strip(): \"{sample.strip()}\"")        # 两边去空白
    print(f"lstrip(): \"{sample.lstrip()}\"")      # 左边去空白
    print(f"rstrip(): \"{sample.rstrip()}\"")      # 右边去空白

    # 查找
    print(f"\n--- 查找与替换 ---")
    s = "hello world, hello python"
    print(f"字符串: \"{s}\"")
    print(f"find('hello'): {s.find('hello')}")     # 首次出现位置 → 0
    print(f"rfind('hello'): {s.rfind('hello')}")   # 最后一次出现 → 13
    print(f"index('world'): {s.index('world')}")   # 同 find 但找不到抛异常
    print(f"count('hello'): {s.count('hello')}")   # 出现次数 → 2
    print(f"startswith('hello'): {s.startswith('hello')}")  # 是否以...开头
    print(f"endswith('python'): {s.endswith('python')}")    # 是否以...结尾

    # 替换
    replaced = s.replace("hello", "你好")
    print(f"replace: \"{replaced}\"")

    # 分割
    csv_line = "apple,banana,orange,grape"
    parts = csv_line.split(",")
    print(f"split(','): {parts}")

    # ========== 5. 编码与解码 ==========
    print("\n=== 5. 编码与解码 (encode/decode) ===")

    text = "你好 Python"

    # 编码: str → bytes
    utf8_bytes = text.encode("utf-8")
    gbk_bytes = text.encode("gbk")

    print(f"原始字符串: \"{text}\"")
    print(f"UTF-8 编码: {utf8_bytes}")
    print(f"GBK 编码:   {gbk_bytes}")
    print(f"UTF-8 字节数: {len(utf8_bytes)}")
    print(f"GBK 字节数:   {len(gbk_bytes)}")

    # 解码: bytes → str
    decoded_utf8 = utf8_bytes.decode("utf-8")
    decoded_gbk = gbk_bytes.decode("gbk")
    print(f"UTF-8 解码: \"{decoded_utf8}\"")
    print(f"GBK 解码:   \"{decoded_gbk}\"")

    # ========== 6. 转义字符与原始字符串 ==========
    print("\n=== 6. 转义字符与原始字符串 ===")

    # 常见转义字符
    print("换行符:\\n → 新一行")          # \\n 是换行（这里展示的是字面量）
    print(f"实际换行: 第一行\n第二行")
    print(f"制表符: 列1\t列2\t列3")
    print(f"反斜杠: C:\\\\Users\\\\name")    # 两个反斜杠显示一个

    # 原始字符串（r-string）：不处理转义字符
    normal_path = "C:\\new_folder\\test.txt"
    raw_path = r"C:\new_folder\test.txt"
    print(f"普通字符串路径: {normal_path}")
    print(f"原始字符串路径: {raw_path}")

    # 原始字符串也适用于正则表达式
    text = "price: $100.00"
    # 不使用原始字符串，需要双反斜杠
    match1 = re.findall("\\$\\d+", text)
    # 使用原始字符串
    match2 = re.findall(r"\$\d+", text)
    print(f"正则匹配 (r-string): {match2}")


if __name__ == "__main__":
    main()
