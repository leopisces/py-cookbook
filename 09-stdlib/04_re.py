#!/usr/bin/env python3
"""
re模块 - Python标准库正则表达式

涵盖内容:
  1. match - 从开头匹配
  2. search - 搜索第一个匹配
  3. findall / finditer - 查找所有匹配
  4. sub / subn - 替换
  5. split - 分割字符串
  6. 分组、元字符、量词
  7. 贪婪与非贪婪匹配
  8. 常用正则模式 (邮箱/手机号/URL)

参考: https://www.runoob.com/python3/python3-reg-expressions.html
"""

import re


def print_match(m, title="匹配结果"):
    """格式化输出匹配信息"""
    if m:
        print(f"  [OK] {title}: '{m.group()}' (位置: {m.start()}-{m.end()})")
    else:
        print(f"  [XX] {title}: 无匹配")


# ============================================================
# 1. match - 从字符串开头匹配
# ============================================================
print("=" * 60)
print("1. match() - 从字符串开头匹配")
print("=" * 60)

print_match(re.match(r"Hello", "Hello World!"))
print_match(re.match(r"Hello", "Say Hello World!"))  # 不在开头,无匹配
print_match(re.match(r"\d+", "123abc"))          # 开头是数字,匹配

# ============================================================
# 2. search - 搜索第一个匹配
# ============================================================
print("\n" + "=" * 60)
print("2. search() - 搜索第一个匹配 (可以不在开头)")
print("=" * 60)

print_match(re.search(r"Hello", "Say Hello World!"))  # 中间位置也能匹配
print_match(re.search(r"\d+", "abc123def456"))         # 找到第一个数字序列

# ============================================================
# 3. findall / finditer - 查找所有匹配
# ============================================================
print("\n" + "=" * 60)
print("3. findall / finditer - 查找所有匹配")
print("=" * 60)

text = "Python 3.12, Python 3.11, Python 3.10"

# findall - 返回所有匹配的字符串列表
nums = re.findall(r"\d+\.\d+", text)
print(f"findall 数字版本: {nums}")

# findall 带分组 - 返回分组元组列表
result = re.findall(r"(Python) (\d+\.\d+)", text)
print(f"findall 分组: {result}")

# finditer - 返回迭代器 (Match对象), 适合大量匹配
print("finditer 遍历:")
for m in re.finditer(r"\d+\.?\d*", text):
    print(f"  位置{m.start()}-{m.end()}: '{m.group()}'")

# ============================================================
# 4. sub / subn - 替换
# ============================================================
print("\n" + "=" * 60)
print("4. sub / subn - 正则替换")
print("=" * 60)

text = "电话: 13812345678, 座机: 010-12345678"

# sub - 替换
masked = re.sub(r"\d{3}-\d{8}|\d{11}", "***", text)
print(f"屏蔽号码后: {masked}")

# 使用回调函数替换
def mask_phone(match):
    phone = match.group()
    return phone[:3] + "****" + phone[-4:]

masked2 = re.sub(r"\d{11}", mask_phone, text)
print(f"部分屏蔽: {masked2}")

# subn - 返回 (替换结果, 替换次数)
result, count = re.subn(r"\d", "X", "abc123def456")
print(f"subn结果: '{result}', 替换了{count}处")

# ============================================================
# 5. split - 分割字符串
# ============================================================
print("\n" + "=" * 60)
print("5. split() - 按正则分割字符串")
print("=" * 60)

text = "apple,  banana; orange:grape  |  mango"
# 按多种分隔符分割
parts = re.split(r"[,;:|]\s*", text)
print(f"原始: '{text}'")
print(f"分割: {parts}")

# split 保留分隔符 (用分组)
parts_with_delim = re.split(r"([,;:])", "a,b;c:d")
print(f"保留分隔符: {parts_with_delim}")

# ============================================================
# 6. 分组 (Group)
# ============================================================
print("\n" + "=" * 60)
print("6. 分组 (Group) - 提取子匹配")
print("=" * 60)

# 普通分组
m = re.match(r"(\w+)@(\w+)\.(\w+)", "user@example.com")
if m:
    print(f"完整匹配:   {m.group(0)}")
    print(f"用户名:     {m.group(1)}")
    print(f"域名:       {m.group(2)}")
    print(f"顶级域名:   {m.group(3)}")
    print(f"所有分组:   {m.groups()}")

# 命名分组
m = re.match(r"(?P<name>\w+)@(?P<domain>\w+)\.(?P<tld>\w+)", "user@example.com")
if m:
    print(f"\n命名分组:")
    print(f"  name:   {m.group('name')}")
    print(f"  domain: {m.group('domain')}")
    print(f"  tld:    {m.group('tld')}")
    print(f"  groupdict: {m.groupdict()}")

# 非捕获分组 (?:...)
m = re.match(r"(?:\w+)@(\w+)\.(\w+)", "user@example.com")
if m:
    print(f"\n非捕获分组 (不捕获用户名): groups()={m.groups()}")

# ============================================================
# 7. 贪婪 vs 非贪婪
# ============================================================
print("\n" + "=" * 60)
print("7. 贪婪匹配 vs 非贪婪匹配")
print("=" * 60)

html = "<h1>标题</h1><p>段落</p>"

# 贪婪匹配 - 尽可能多地匹配
greedy = re.findall(r"<.*>", html)
print(f"贪婪匹配 .*  : {greedy}")

# 非贪婪匹配 - 尽可能少地匹配
non_greedy = re.findall(r"<.*?>", html)
print(f"非贪婪匹配 .*?: {non_greedy}")

# 量词对比表
print("\n量词对比:")
tests = ["a", "ab", "abb", "abbb", "ac"]
for t in tests:
    r1 = re.match(r"ab+", t)   # 贪婪一个或多个
    r2 = re.match(r"ab+?", t)  # 非贪婪
    r3 = re.match(r"ab*", t)   # 零个或多个
    r4 = re.match(r"ab?", t)   # 零个或一个
    print(f"  '{t}': +={bool(r1)}, +?={bool(r2)}, *={bool(r3)}, ?={bool(r4)}")

# ============================================================
# 8. 常用正则模式
# ============================================================
print("\n" + "=" * 60)
print("8. 常用正则模式")
print("=" * 60)


def test_pattern(pattern, test_cases, description):
    """测试正则模式"""
    print(f"\n{description}: {pattern}")
    for case in test_cases:
        result = "[OK] 匹配" if re.fullmatch(pattern, case) else "[XX] 不匹配"
        print(f"  {case:<30} → {result}")


# 邮箱验证
test_pattern(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    ["user@example.com", "test.user@mail.co.uk", "invalid@com", "@no-user.com", "no@.com"],
    "邮箱格式"
)

# 中国手机号
test_pattern(
    r"^1[3-9]\d{9}$",
    ["13812345678", "15900001111", "12345678901", "1381234567", "138123456789"],
    "中国手机号"
)

# IPv4 地址
ip_pattern = r"^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$"
test_pattern(
    ip_pattern,
    ["192.168.1.1", "255.255.255.0", "256.1.1.1", "192.168.1"],
    "IPv4地址"
)

# URL 匹配
print("\nURL提取:")
url_text = "访问 https://www.example.com 和 http://test.org/path?q=1"
urls = re.findall(r"https?://[^\s]+", url_text)
for u in urls:
    print(f"  找到URL: {u}")

# 中文字符匹配
print("\n中文字符匹配:")
cn_text = "Hello世界Python你好123"
cn_chars = re.findall(r"[\u4e00-\u9fff]+", cn_text)
print(f"  原文: '{cn_text}'")
print(f"  中文: {cn_chars}")

# ============================================================
# 常用元字符速查
# ============================================================
print("\n" + "=" * 60)
print("9. 常用元字符速查")
print("=" * 60)

patterns = {
    r"\d": "任意数字 [0-9]",
    r"\D": "任意非数字",
    r"\w": "单词字符 [a-zA-Z0-9_]",
    r"\W": "非单词字符",
    r"\s": "空白字符 (空格/制表/换行)",
    r"\S": "非空白字符",
    r".": "任意字符 (除换行外)",
    r"^": "字符串开头",
    r"$": "字符串结尾",
    r"[abc]": "字符集, 匹配 a/b/c",
    r"[^abc]": "排除字符集",
    r"a|b": "或, 匹配 a 或 b",
}

for p, desc in patterns.items():
    print(f"  {p:>10}  → {desc}")

print("\n常用模式标志 (flags):")
print("  re.I  = 忽略大小写")
print("  re.M  = 多行模式 (^$匹配每行)")
print("  re.S  = 点号匹配换行符")
print("  re.A  = ASCII模式")
