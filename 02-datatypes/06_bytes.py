"""
Python bytes 与 bytearray

学习目标：
  - bytes：不可变的字节序列
  - bytearray：可变的字节序列
  - 创建与基本操作
  - 与 str 的相互转换（编码与解码）
  - 十六进制表示
  - 字节序 (endianness) 概念
"""

def main():
    # ========== 1. bytes 的创建 ==========
    print("=== 1. bytes 的创建 ===")

    # 多种创建方式
    b1 = b"hello"                           # 字面量（仅 ASCII 字符）
    b2 = bytes([72, 101, 108, 108, 111])    # 从整数列表
    b3 = bytes("你好", encoding="utf-8")     # 从字符串编码
    b4 = bytes(5)                           # 创建 5 个零字节

    print(f"字面量: {b1}")
    print(f"从整数列表: {b2}")
    print(f"从字符串编码: {b3}")
    print(f"零字节: {b4}")

    # ========== 2. bytes 的基本操作 ==========
    print("\n=== 2. bytes 的基本操作 ===")

    data = b"ABCDEFG"
    print(f"字节序列: {data}")

    # 索引（返回 int，不是 bytes）
    print(f"data[0] = {data[0]} (整数，不是字节)")
    print(f"data[0] 的字符: '{chr(data[0])}'")

    # 切片（返回 bytes）
    print(f"data[:3] = {data[:3]}")

    # 遍历
    print("遍历:", end=" ")
    for byte in data:
        print(f"{byte}({chr(byte)})", end=" ")
    print()

    # 其他操作
    print(f"长度: len(data) = {len(data)}")
    print(f"in 检查: b'C' in data = {b'C' in data}")
    print(f"连接: data + b'XYZ' = {data + b'XYZ'}")
    print(f"重复: data[:2] * 3 = {data[:2] * 3}")

    # bytes 是不可变的
    # data[0] = 90  # TypeError: 'bytes' object does not support item assignment

    # ========== 3. bytearray 可变字节序列 ==========
    print("\n=== 3. bytearray 可变字节序列 ===")

    # 创建
    ba = bytearray(b"hello")
    print(f"初始: {ba}")

    # 修改（bytearray 是可变的！）
    ba[0] = ord("H")                        # 修改第一个字节
    ba.append(33)                           # 追加字节 (33 = '!')
    ba.extend(b" world")                    # 扩展
    print(f"修改后: {ba}")

    # 转为字符串
    text = ba.decode("ascii")
    print(f"解码: '{text}'")

    # 插入与删除
    ba2 = bytearray(b"ABCD")
    ba2.insert(2, ord("X"))                 # 在索引2插入
    print(f"insert: {ba2}")
    ba2.pop(2)                              # 删除索引2
    print(f"pop: {ba2}")

    # ========== 4. 字符串与字节的互转 ==========
    print("\n=== 4. 字符串与字节的互转 ===")

    original = "Python编程很有趣"

    # 编码: str → bytes
    utf8_bytes = original.encode("utf-8")
    gbk_bytes = original.encode("gbk")

    print(f"原始字符串: '{original}' ({len(original)} 个字符)")
    print(f"UTF-8 字节: {utf8_bytes} ({len(utf8_bytes)} 字节)")
    print(f"GBK 字节:   {gbk_bytes} ({len(gbk_bytes)} 字节)")

    # 解码: bytes → str
    decoded_utf8 = utf8_bytes.decode("utf-8")
    decoded_gbk = gbk_bytes.decode("gbk")
    print(f"UTF-8 解码: '{decoded_utf8}'")
    print(f"GBK 解码:   '{decoded_gbk}'")

    # 编码错误处理
    text_with_emoji = "Hello ✨"
    try:
        ascii_bytes = text_with_emoji.encode("ascii")
    except UnicodeEncodeError:
        print(f"\n编码错误处理:")
        # ignore — 忽略无法编码的字符
        print(f"ignore: '{text_with_emoji.encode('ascii', errors='ignore')}'")
        # replace — 替换为 ?
        print(f"replace: '{text_with_emoji.encode('ascii', errors='replace')}'")
        # xmlcharrefreplace — XML 实体引用
        print(f"xmlcharrefreplace: '{text_with_emoji.encode('ascii', errors='xmlcharrefreplace')}'")

    # ========== 5. 十六进制表示 ==========
    print("\n=== 5. 十六进制表示 ===")

    data = b"\x48\x65\x6c\x6c\x6f"         # 相当于 b"Hello"
    print(f"十六进制字节: {data}")
    print(f"字符串表示: {data.decode('ascii')}")

    # hex() 方法 — 查看十六进制
    print(f"\nhex() 方法:")
    print(f"b'Hello'.hex() = {b'Hello'.hex()}")
    print(f"b'Hello'.hex(' ') = {b'Hello'.hex(' ')}")     # 空格分隔
    print(f"b'Hello'.hex(':') = {b'Hello'.hex(':')}")     # 冒号分隔

    # bytes.fromhex() — 从十六进制创建
    hex_str = "48656c6c6f"
    bytes_from_hex = bytes.fromhex(hex_str)
    print(f"\nfromhex('{hex_str}') = {bytes_from_hex}")
    print(f"解码: {bytes_from_hex.decode('ascii')}")

    # 显示文件签名（magic bytes）
    png_signature = b"\x89PNG\r\n\x1a\n"
    print(f"\nPNG 文件签名 (hex): {png_signature.hex(' ')}")

    # ========== 6. 进制转换与内存视图 ==========
    print("\n=== 6. 进制转换与内存视图 ===")

    # int → bytes
    num = 2025
    num_bytes = num.to_bytes(2, byteorder="big")       # 2字节大端序
    num_bytes_le = num.to_bytes(2, byteorder="little") # 2字节小端序
    print(f"{num} → 大端序: {num_bytes.hex(' ')}, 小端序: {num_bytes_le.hex(' ')}")

    # bytes → int
    restored = int.from_bytes(num_bytes, byteorder="big")
    print(f"大端序还原: {restored}")

    # 大端序 vs 小端序
    val = 0x1234
    big = val.to_bytes(2, "big")
    little = val.to_bytes(2, "little")
    print(f"\n0x1234: 大端={big.hex(' ')}, 小端={little.hex(' ')}")
    print("大端序: 高位字节在前（人类习惯）")
    print("小端序: 低位字节在前（CPU常用）")

    # memoryview — 零拷贝查看字节数据
    data = b"abcdefgh"
    mv = memoryview(data)
    print(f"\nmemoryview: {mv.tobytes()}")
    print(f"mv[0:4].tobytes() = {mv[0:4].tobytes()}")


if __name__ == "__main__":
    main()
