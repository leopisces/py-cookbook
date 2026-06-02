#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
csv模块 - Python标准库CSV文件读写

涵盖内容:
  1. reader - 读取CSV文件
  2. writer - 写入CSV文件
  3. DictReader - 字典方式读取
  4. DictWriter - 字典方式写入
  5. CSV格式选项与方言

参考: https://www.runoob.com/python3/python3-csv.html
"""

import csv
import os
import tempfile


# ============================================================
# 准备工作: 创建临时CSV文件用于演示
# ============================================================
print("=" * 60)
print("准备工作: 创建示例CSV文件")
print("=" * 60)

# 写入示例数据
tmp_path = os.path.join(tempfile.gettempdir(), "py_cookbook_demo.csv")

sample_data = [
    ["姓名", "年龄", "城市", "职业"],
    ["张三", "25", "北京", "工程师"],
    ["李四", "30", "上海", "设计师"],
    ["王五", "28", "广州", "产品经理"],
    ["赵六", "35", "深圳", "架构师"],
]

try:
    with open(tmp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    print(f"示例文件已创建: {tmp_path}")
    print(f"共 {len(sample_data)} 行数据 (含表头)")

except Exception as e:
    print(f"文件创建失败: {e}")
    tmp_path = None


# ============================================================
# 1. csv.reader - 读取CSV
# ============================================================
if tmp_path and os.path.exists(tmp_path):
    print("\n" + "=" * 60)
    print("1. csv.reader - 逐行读取CSV")
    print("=" * 60)

    with open(tmp_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # reader 是迭代器
        for i, row in enumerate(reader):
            print(f"  第{i + 1}行: {row}")

    # 跳过表头读取
    print("\n跳过表头:")
    with open(tmp_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 读取表头
        print(f"  表头: {headers}")
        print(f"  数据行:")
        for row in reader:
            print(f"    {row}")


# ============================================================
# 2. csv.writer - 写入CSV
# ============================================================
print("\n" + "=" * 60)
print("2. csv.writer - 写入CSV数据")
print("=" * 60)

tmp_path2 = os.path.join(tempfile.gettempdir(), "py_cookbook_write.csv")

try:
    # writerow - 逐行写入
    with open(tmp_path2, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "商品", "价格", "库存"])  # 表头
        writer.writerow([1, "笔记本电脑", 5999.00, 50])
        writer.writerow([2, "机械键盘", 399.00, 200])
        writer.writerow([3, "显示器", 1499.00, 80])

    # 验证写入结果
    with open(tmp_path2, 'r', encoding='utf-8') as f:
        print(f"写入结果 (文件: {tmp_path2}):")
        for line in f:
            print(f"  {line.rstrip()}")

    # writerows - 批量写入多行
    with open(tmp_path2, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        more_data = [
            [4, "鼠标", 99.00, 500],
            [5, "耳机", 299.00, 150],
        ]
        writer.writerows(more_data)

    print(f"\n追加后:")
    with open(tmp_path2, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"  {line.rstrip()}")
    os.unlink(tmp_path2)
finally:
    if os.path.exists(tmp_path2):
        os.unlink(tmp_path2)


# ============================================================
# 3. DictReader - 字典方式读取
# ============================================================
if tmp_path and os.path.exists(tmp_path):
    print("\n" + "=" * 60)
    print("3. DictReader - 字典方式读取CSV")
    print("=" * 60)

    with open(tmp_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"表头字段: {reader.fieldnames}")
        print(f"\n数据行 (字典格式):")
        for row in reader:
            print(f"  {row['姓名']}, {row['年龄']}岁, {row['城市']}, {row['职业']}")


# ============================================================
# 4. DictWriter - 字典方式写入
# ============================================================
print("\n" + "=" * 60)
print("4. DictWriter - 字典方式写入CSV")
print("=" * 60)

tmp_path3 = os.path.join(tempfile.gettempdir(), "py_cookbook_dict.csv")

try:
    fieldnames = ["name", "score", "grade"]
    students = [
        {"name": "Alice", "score": 92, "grade": "A"},
        {"name": "Bob", "score": 78, "grade": "B"},
        {"name": "Charlie", "score": 65, "grade": "C"},
    ]

    with open(tmp_path3, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()           # 写入表头
        writer.writerows(students)     # 批量写入

    # 验证
    with open(tmp_path3, 'r', encoding='utf-8') as f:
        print("写入结果:")
        for line in f:
            print(f"  {line.rstrip()}")

    # DictWriter 还可以在 __init__ 时指定 extrasaction
    # extrasaction='ignore' → 忽略字典中多余的键
    os.unlink(tmp_path3)
finally:
    if os.path.exists(tmp_path3):
        os.unlink(tmp_path3)


# ============================================================
# 5. CSV格式选项
# ============================================================
print("\n" + "=" * 60)
print("5. CSV格式选项与方言")
print("=" * 60)

# 自定义格式: 分号分隔 + 单引号包围
tmp_path4 = os.path.join(tempfile.gettempdir(), "py_cookbook_custom.csv")

try:
    print("使用分号分隔符 + 单引号包围:")
    with open(tmp_path4, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';', quotechar="'", quoting=csv.QUOTE_ALL)
        writer.writerow(["张三", "北京", "工程师"])
        writer.writerow(["李四", "上海, 浦东", "设计师"])  # 字段含逗号

    with open(tmp_path4, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"  {line.rstrip()}")

    # 用相同参数读取
    with open(tmp_path4, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';', quotechar="'")
        for row in reader:
            print(f"  解析: {row}")

    os.unlink(tmp_path4)
finally:
    if os.path.exists(tmp_path4):
        os.unlink(tmp_path4)

# 常用 quoting 常量说明
print("\nquoting 常量说明:")
print("  csv.QUOTE_MINIMAL  - 仅在必要时加引号 (默认)")
print("  csv.QUOTE_ALL      - 所有字段都加引号")
print("  csv.QUOTE_NONNUMERIC - 非数字字段加引号")
print("  csv.QUOTE_NONE     - 不加引号 (需指定 escapechar)")

# dialect - 预设格式
print("\n注册和使用方言:")
csv.register_dialect('mydialect', delimiter='|', quoting=csv.QUOTE_MINIMAL)
tmp_path5 = os.path.join(tempfile.gettempdir(), "py_cookbook_dialect.csv")

try:
    with open(tmp_path5, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='mydialect')
        writer.writerow(["A", "B", "C"])
        writer.writerow(["1", "2", "3"])

    with open(tmp_path5, 'r', encoding='utf-8') as f:
        print(f"管道分隔符格式:")
        for line in f:
            print(f"  {line.rstrip()}")
    os.unlink(tmp_path5)
finally:
    if os.path.exists(tmp_path5):
        os.unlink(tmp_path5)

# ============================================================
# 清理临时文件
# ============================================================
if tmp_path and os.path.exists(tmp_path):
    os.unlink(tmp_path)
    print(f"\n已清理临时文件: {tmp_path}")
