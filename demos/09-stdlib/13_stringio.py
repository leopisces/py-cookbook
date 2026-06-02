#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
io.StringIO / io.BytesIO - Python标准库内存缓冲区

涵盖内容:
  1. StringIO - 内存文本缓冲区 (类似文件对象)
  2. StringIO 的读写与定位
  3. BytesIO - 内存二进制缓冲区
  4. BytesIO 的读写与定位
  5. 与真实文件接口的一致性 (鸭子类型)

参考: https://docs.python.org/zh-cn/3/library/io.html
"""

from io import StringIO, BytesIO
import os
import tempfile


# ============================================================
# 1. StringIO - 文本缓冲区基本操作
# ============================================================
print("=" * 60)
print("1. StringIO - 内存文本缓冲区")
print("=" * 60)

# 创建并写入
buffer = StringIO()
print(f"创建空 StringIO: 位置={buffer.tell()}")

# write - 写入文本
buffer.write("第一行: Hello World\n")
buffer.write("第二行: Python 学习\n")
buffer.write("第三行: StringIO 演示\n")
print(f"写入3行后: 位置={buffer.tell()}")

# 查看内容
buffer.seek(0)  # 回到开头
print(f"\n缓冲区内容:")
print(buffer.read())

# ============================================================
# 2. StringIO 读写操作详解
# ============================================================
print("\n" + "=" * 60)
print("2. StringIO 详细操作")
print("=" * 60)

# 用初始值创建
sio = StringIO("Line1\nLine2\nLine3\nLine4\nLine5\n")
print(f"初始内容字符数: {len(sio.read())}")

# seek - 定位
sio.seek(0)
print(f"\n逐行读取:")
for i, line in enumerate(sio, 1):
    if line.strip():
        print(f"  第{i}行: {line.rstrip()}")

# tell - 当前位置
sio.seek(0)
sio.readline()
print(f"\n读完第一行后位置: {sio.tell()}")

# 写入后读取
sio = StringIO()
sio.write("ABCDEFGHIJ")
print(f"\n写入10个字符, 位置: {sio.tell()}")

# 从中间读取
sio.seek(3)
print(f"seek(3) 后读取: '{sio.read(3)}'")

# truncate - 截断
sio.seek(5)
sio.truncate()  # 从当前位置截断
sio.seek(0)
print(f"truncate(5) 后: '{sio.read()}'")

# getvalue - 获取全部内容 (不改变位置)
sio2 = StringIO("Hello Python")
print(f"\ngetvalue() 不改变位置: '{sio2.getvalue()}'")
print(f"  位置仍为: {sio2.tell()}")

# ============================================================
# 3. BytesIO - 二进制缓冲区
# ============================================================
print("\n" + "=" * 60)
print("3. BytesIO - 内存二进制缓冲区")
print("=" * 60)

# 创建 BytesIO
bio = BytesIO()
print(f"创建空 BytesIO")

# 写入二进制数据
bio.write(b"Hello, World!")           # 字符串 → 字节
bio.write(bytes([0, 1, 2, 255]))      # 字节序列
bio.write((12345).to_bytes(4, 'big')) # 整数 → 字节

print(f"写入后大小: {bio.tell()} 字节")

# 读取全部
bio.seek(0)
all_data = bio.read()
print(f"全部数据 ({len(all_data)}字节): {all_data}")
print(f"  hex: {all_data.hex()}")

# 结构化读写
print(f"\n结构化读写:")
bio2 = BytesIO()

# 模拟写入 4 个 32位整数
import struct
for n in [42, 100, 255, 9999]:
    bio2.write(struct.pack('>I', n))  # 大端序 4字节无符号整数

bio2.seek(0)
print(f"写入4个整数, 共 {bio2.getbuffer().nbytes} 字节")

# 逐个读取
bio2.seek(0)
values = []
while chunk := bio2.read(4):
    if len(chunk) == 4:
        values.append(struct.unpack('>I', chunk)[0])
print(f"读出整数: {values}")

# ============================================================
# 4. 与文件接口一致 - 鸭子类型
# ============================================================
print("\n" + "=" * 60)
print("4. 与文件接口一致 (鸭子类型)")
print("=" * 60)


def process_text_stream(stream):
    """统一处理文件或 StringIO (鸭子类型)"""
    stream.seek(0)
    lines = stream.readlines()
    word_count = sum(len(line.split()) for line in lines)
    return len(lines), word_count


# 使用真实文件
tmp_path = os.path.join(tempfile.gettempdir(), "py_cookbook_io_test.txt")
try:
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write("Hello World\n")
        f.write("Python 是一门很棒的语言\n")
        f.write("StringIO 非常实用\n")

    with open(tmp_path, 'r', encoding='utf-8') as f:
        line_count, words = process_text_stream(f)
        print(f"从文件读取: {line_count}行, {words}个词")

    os.unlink(tmp_path)
except Exception as e:
    print(f"文件操作失败: {e}")

# 使用 StringIO (相同的函数!)
sio = StringIO(
    "Hello World\n"
    "Python 是一门很棒的语言\n"
    "StringIO 非常实用\n"
)
line_count, words = process_text_stream(sio)
print(f"从 StringIO 读取: {line_count}行, {words}个词")

print(f"\n结论: 相同接口, 一个用文件, 一个用内存 → 鸭子类型!")

# ============================================================
# 5. 实用场景
# ============================================================
print("\n" + "=" * 60)
print("5. 实用场景演示")
print("=" * 60)

# 场景1: 构建CSV内容 (不写磁盘)
print("场景1 - 动态构建CSV:")
csv_buffer = StringIO()
csv_buffer.write("姓名,年龄,城市\n")
csv_buffer.write("张三,25,北京\n")
csv_buffer.write("李四,30,上海\n")
csv_buffer.write("王五,28,广州\n")

csv_buffer.seek(0)
print(csv_buffer.read().rstrip())

# 场景2: 捕获 print 输出
print("\n场景2 - 捕获 print 输出:")
output = StringIO()
print("这条消息会被捕获到 StringIO", file=output)
print("而不是显示在终端", file=output)
captured = output.getvalue()
print(f"捕获到的内容:\n{captured}")

# 场景3: BytesIO 用于图片/数据中间处理
print("场景3 - BytesIO 模拟二进制数据处理:")
img_buffer = BytesIO()
# 模拟写入图像头部 (PNG magic bytes + 一些数据)
img_buffer.write(b'\x89PNG\r\n\x1a\n')  # PNG 文件头
img_buffer.write(b'IMAGEDATA' * 3)      # 模拟像素数据

img_buffer.seek(0)
header = img_buffer.read(8)
print(f"  文件头: {header}")
is_png = header == b'\x89PNG\r\n\x1a\n'
print(f"  是PNG吗: {is_png} (仅演示, 实际需精确匹配)")
print(f"  总大小: {img_buffer.getbuffer().nbytes} 字节")

# 场景4: 重定向 stdout (演示后恢复)
import sys
print("\n场景4 - 临时重定向 stdout:")
old_stdout = sys.stdout
try:
    capture = StringIO()
    sys.stdout = capture
    print("这条被重定向了!")
    print("所有 print 都进入 StringIO")
    sys.stdout = old_stdout  # 恢复
    print(f"捕获内容: '{capture.getvalue().strip()}'")
finally:
    sys.stdout = old_stdout  # 确保恢复

print("\n总结: StringIO/BytesIO 用于需要在内存中操作类文件数据的场景")
print("  典型用例: 测试/日志捕获/中间格式化/HTTP响应构建")
