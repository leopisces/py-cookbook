#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
random模块 - Python标准库随机数生成

涵盖内容:
  1. 基础随机 (random, randint, uniform)
  2. 序列随机选择 (choice, choices, sample)
  3. 序列随机打乱 (shuffle)
  4. 随机种子 (seed) 与可复现随机
  5. 实用示例: 随机密码生成

参考: https://www.runoob.com/python3/python3-random.html
"""

import random
import string


# ============================================================
# 1. 基础随机函数
# ============================================================
print("=" * 60)
print("1. 基础随机函数")
print("=" * 60)

# random() - [0.0, 1.0) 之间的浮点数
print(f"random()  [0.0, 1.0) 浮点数:  {random.random():.4f}")

# uniform(a, b) - [a, b] 之间的浮点数
print(f"uniform(10, 20)              :  {random.uniform(10, 20):.4f}")

# randint(a, b) - [a, b] 之间的整数 (包含两端)
print(f"randint(1, 100) 1-100间整数   :  {random.randint(1, 100)}")

# randrange(start, stop, step) - 指定范围的随机整数
print(f"randrange(0, 100, 2) 偶数     :  {random.randrange(0, 100, 2)}")

# ============================================================
# 2. 序列随机选择
# ============================================================
print("\n" + "=" * 60)
print("2. 序列随机选择")
print("=" * 60)

colors = ["红", "橙", "黄", "绿", "青", "蓝", "紫"]
print(f"颜色列表: {colors}")

# choice(seq) - 随机返回一个元素
print(f"choice()  随机选一个: {random.choice(colors)}")

# choices(seq, k=n) - 有放回随机选 n 个
print(f"choices(k=5) 选5个(可重复): {random.choices(colors, k=5)}")

# choices(seq, weights=...) - 带权重的随机选择
weights = [1, 1, 1, 1, 1, 1, 10]  # 紫色权重高
print(f"choices(k=5, 紫色权重10):  {random.choices(colors, weights=weights, k=5)}")

# sample(seq, k=n) - 无放回随机选 n 个 (不重复)
print(f"sample(k=4)  选4个(不重复): {random.sample(colors, k=4)}")

# ============================================================
# 3. 序列随机打乱
# ============================================================
print("\n" + "=" * 60)
print("3. shuffle() 原地打乱列表")
print("=" * 60)

deck = list(range(1, 14))  # 1-13 代表扑克牌
print(f"原始顺序: {deck}")
random.shuffle(deck)
print(f"打乱后:   {deck}")

# ============================================================
# 4. 随机种子 - 可复现的"随机"
# ============================================================
print("\n" + "=" * 60)
print("4. seed() 随机种子 - 让随机可复现")
print("=" * 60)

for trial in range(2):
    random.seed(42)  # 固定种子
    nums = [random.randint(1, 100) for _ in range(5)]
    print(f"第{trial + 1}次 seed(42) 生成的5个数: {nums}")

print("说明: 相同种子 → 相同随机序列, 便于调试和测试复现")

# ============================================================
# 5. 实用示例: 随机密码生成
# ============================================================
print("\n" + "=" * 60)
print("5. 实用示例: 生成随机密码")
print("=" * 60)


def generate_password(length=12):
    """生成包含大小写字母、数字、特殊字符的随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    # 确保至少包含每类字符至少一个
    password = [
        random.choice(string.ascii_lowercase),  # 至少一个小写
        random.choice(string.ascii_uppercase),  # 至少一个大写
        random.choice(string.digits),           # 至少一个数字
        random.choice("!@#$%^&*"),              # 至少一个特殊字符
    ]
    # 剩余位随机填补
    password += random.choices(chars, k=length - 4)
    random.shuffle(password)  # 打乱顺序
    return ''.join(password)


# 生成 5 个示例密码
print("生成的随机密码示例:")
for i in range(5):
    print(f"  密码{i + 1}: {generate_password(16)}")

# ============================================================
# 其他实用函数
# ============================================================
print("\n" + "=" * 60)
print("其他实用函数")
print("=" * 60)

# getrandbits(k) - 生成 k 位随机整数
print(f"getrandbits(8)  8位随机数  (0-255):  {random.getrandbits(8)}")
print(f"getrandbits(32) 32位随机数:          {random.getrandbits(32)}")

# betavariate / gauss / triangular 等分布函数
print(f"gauss(0, 1)     高斯分布(均值0,标准差1): {random.gauss(0, 1):.4f}")
print(f"triangular(0, 10, 5) 三角分布(0-10,模5): {random.triangular(0, 10, 5):.4f}")

# random.SystemRandom - 加密级随机 (不可复现,用于安全场景)
print("\n说明: 需要加密级随机时, 使用 secrets 模块而非 random 模块.")
print("      示例: import secrets; secrets.token_hex(16)")
