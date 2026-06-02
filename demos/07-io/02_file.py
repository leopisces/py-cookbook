"""
文件操作 - Python 文件读写

学习目标：
  - open() 打开文件：读(r) / 写(w) / 追加(a) / 二进制(b)
  - with 语句自动关闭文件
  - read() / readline() / readlines() / write() / writelines()
  - 文件指针定位：seek() / tell()
  - 二进制文件读写
"""

import os
import tempfile


def main():
    # ========== 1. 写文件：write() / writelines() ==========
    print("=== 1. 写文件 ===")

    # 创建临时文件（演示用，脚本结束自动删除）
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    )
    filepath = tmp.name
    try:
        # 写入单行
        tmp.write("第一行：Hello Python\n")
        # writelines 写入多行（注意：不会自动加换行符）
        tmp.writelines(["第二行：文件操作\n", "第三行：这是最后一行\n"])
        tmp.close()

        # 查看文件内容
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"写入的文件内容:\n{content}")

    finally:
        os.unlink(filepath)  # 清理临时文件

    # ========== 2. 读取文件：read() / readline() / readlines() ==========
    print("=== 2. 读取文件的各种方式 ===")

    # 创建测试文件
    test_file = tempfile.mktemp(suffix=".txt")
    with open(test_file, "w", encoding="utf-8") as f:
        for i in range(1, 6):
            f.write(f"第{i}行：这是测试数据\n")

    try:
        # 方式一：read() 一次性读取全部内容
        print("--- read() 读取全部 ---")
        with open(test_file, "r", encoding="utf-8") as f:
            all_content = f.read()
        print(all_content)

        # 方式二：read(n) 读取指定字符数
        print("--- read(10) 读取前10个字符 ---")
        with open(test_file, "r", encoding="utf-8") as f:
            print(f.read(10))

        # 方式三：readline() 逐行读取
        print("--- readline() 逐行读取 ---")
        with open(test_file, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                print(f"  {line.strip()}")
                line = f.readline()

        # 方式四：readlines() 读取所有行到列表
        print("--- readlines() 返回列表 ---")
        with open(test_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"共 {len(lines)} 行，第一行: {lines[0].strip()}")

        # 方式五：直接迭代文件对象（最 Pythonic）
        print("--- 直接迭代文件对象 ---")
        with open(test_file, "r", encoding="utf-8") as f:
            for line in f:
                print(f"  {line.strip()}")

    finally:
        os.unlink(test_file)

    # ========== 3. 文件打开模式 ==========
    print("\n=== 3. 文件打开模式 ===")

    demo_file = tempfile.mktemp(suffix=".txt")

    # 'w' 模式：写入（覆盖已有内容）
    print("'w' 模式：覆盖写入")
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write("初始内容\n")
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write("覆盖后的内容\n")
    with open(demo_file, "r", encoding="utf-8") as f:
        print(f"  内容: {f.read().strip()}")

    # 'a' 模式：追加（在文件末尾添加）
    print("'a' 模式：追加写入")
    with open(demo_file, "a", encoding="utf-8") as f:
        f.write("追加的第一行\n")
        f.write("追加的第二行\n")
    with open(demo_file, "r", encoding="utf-8") as f:
        print(f"  内容:\n{f.read()}")

    # 'x' 模式：排他性创建（文件已存在则报错）
    print("'x' 模式：排他性创建")
    try:
        with open(demo_file, "x", encoding="utf-8") as f:
            f.write("这不会写入")
    except FileExistsError:
        print("  文件已存在，x 模式抛出 FileExistsError")

    os.unlink(demo_file)

    # ========== 4. 文件指针：seek() / tell() ==========
    print("\n=== 4. 文件指针：seek() / tell() ===")

    pointer_file = tempfile.mktemp(suffix=".txt")
    with open(pointer_file, "w", encoding="utf-8") as f:
        f.write("ABCDEFGHIJ")

    try:
        with open(pointer_file, "r", encoding="utf-8") as f:
            print(f"初始位置: tell() = {f.tell()}")
            print(f"读取3个字符: {f.read(3)}, tell() = {f.tell()}")

            # seek(offset, whence) 移动文件指针
            # whence: 0=开头, 1=当前位置, 2=末尾
            f.seek(0)  # 回到开头
            print(f"seek(0) 回到开头: tell() = {f.tell()}, read(1) = '{f.read(1)}'")

            f.seek(5)  # 跳到第5个字节
            print(f"seek(5): read(3) = '{f.read(3)}'")

            f.seek(0, 2)  # 跳到末尾
            print(f"seek(0, 2) 末尾: tell() = {f.tell()}")
    finally:
        os.unlink(pointer_file)

    # ========== 5. 二进制文件读写 ==========
    print("\n=== 5. 二进制文件读写 ===")

    bin_file = tempfile.mktemp(suffix=".bin")
    try:
        # 'wb' 模式：写入二进制数据
        data = bytes([0, 1, 2, 3, 255, 100, 200])
        with open(bin_file, "wb") as f:
            f.write(data)

        # 'rb' 模式：读取二进制数据
        with open(bin_file, "rb") as f:
            read_data = f.read()
        print(f"写入的二进制数据: {list(data)}")
        print(f"读取的二进制数据: {list(read_data)}")

        # 二进制文件的大小
        file_size = os.path.getsize(bin_file)
        print(f"文件大小: {file_size} 字节")

    finally:
        os.unlink(bin_file)

    # ========== 6. with 语句自动管理文件 ==========
    print("\n=== 6. with 语句的优势 ===")
    print("with open(...) as f:     # 自动关闭文件")
    print("    ...                  # 即使发生异常也会关闭")
    print("                         # 不需要手动 f.close()")

    # 对比：不用 with 需要手动关闭
    demo2 = tempfile.mktemp(suffix=".txt")
    f = open(demo2, "w", encoding="utf-8")
    f.write("手动管理文件")
    f.close()  # 必须手动关闭！
    os.unlink(demo2)
    print("已演示：使用 with 语句可以避免忘记关闭文件的问题")


if __name__ == "__main__":
    main()
