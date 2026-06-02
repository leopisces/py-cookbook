"""
OS 模块 - 操作系统接口与文件系统操作

学习目标：
  - os.path 路径操作（join/split/exists/isfile/isdir 等）
  - os 目录操作（mkdir/rmdir/listdir/getcwd/chdir）
  - os.environ 环境变量操作
  - shutil 高级文件操作（copy/move/rmtree）
"""

import os
import shutil
import tempfile


def main():
    # ========== 1. os.path 路径操作 ==========
    print("=== 1. os.path 路径操作 ===")

    # 路径拼接（跨平台兼容）
    path = os.path.join("home", "user", "documents", "file.txt")
    print(f"os.path.join: {path}")

    # 路径拆分
    print(f"os.path.split:      {os.path.split(path)}")
    print(f"os.path.dirname:    {os.path.dirname(path)}")
    print(f"os.path.basename:   {os.path.basename(path)}")

    # 扩展名操作
    print(f"os.path.splitext:   {os.path.splitext(path)}")

    # 路径判断
    current_file = os.path.abspath(__file__)
    print(f"\n当前文件: {current_file}")
    print(f"  存在:           {os.path.exists(current_file)}")
    print(f"  是文件:         {os.path.isfile(current_file)}")
    print(f"  是目录:         {os.path.isdir(os.path.dirname(current_file))}")
    print(f"  是绝对路径:     {os.path.isabs(current_file)}")

    # 路径转换
    print(f"\nos.path.abspath('.'):    {os.path.abspath('.')}")
    print(f"os.path.relpath:         {os.path.relpath(current_file, os.path.dirname(os.path.dirname(current_file)))}")
    print(f"os.path.normpath:        {os.path.normpath('a/b/../c//d')}")  # 规范化路径

    # 获取文件信息
    file_stat = os.stat(current_file)
    print(f"\n文件大小: {file_stat.st_size} 字节")
    print(f"文件大小(可读): {file_stat.st_size / 1024:.1f} KB")

    # ========== 2. os 目录操作 ==========
    print("\n=== 2. os 目录操作 ===")

    # 获取当前工作目录
    cwd = os.getcwd()
    print(f"当前工作目录: {cwd}")

    # 列出目录内容（前10项）
    entries = os.listdir(cwd)
    print(f"目录下共 {len(entries)} 项（前5项）:")
    for entry in entries[:5]:
        full_path = os.path.join(cwd, entry)
        type_mark = "[目录]" if os.path.isdir(full_path) else "[文件]"
        print(f"  {type_mark} {entry}")

    # 临时目录创建与删除演示
    tmp_dir = tempfile.mkdtemp(prefix="py_os_demo_")
    try:
        print(f"\n创建临时目录: {tmp_dir}")

        # 创建子目录
        sub_dir = os.path.join(tmp_dir, "subdir")
        os.mkdir(sub_dir)
        print(f"创建子目录: {sub_dir}")

        # 创建嵌套目录（os.makedirs 会创建所有中间目录）
        nested = os.path.join(tmp_dir, "a", "b", "c")
        os.makedirs(nested, exist_ok=True)
        print(f"创建嵌套目录: {nested}")

        # 创建文件
        test_file = os.path.join(tmp_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hello OS Module")
        print(f"创建文件: {test_file}")

        # 遍历目录树
        print("\n目录树结构:")
        for root, dirs, files in os.walk(tmp_dir):
            level = root.replace(tmp_dir, "").count(os.sep)
            indent = "  " * level
            print(f"{indent}{os.path.basename(root)}/")
            for file in files:
                print(f"{indent}  - {file}")

    finally:
        # 清理：递归删除整个临时目录
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # ========== 3. os.environ 环境变量 ==========
    print("\n=== 3. os.environ 环境变量 ===")

    # 读取环境变量
    print(f"HOME/USERPROFILE: {os.environ.get('HOME', os.environ.get('USERPROFILE', 'N/A'))}")
    print(f"PATH (前80字符): {os.environ.get('PATH', 'N/A')[:80]}...")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', '(未设置)')}")

    # os.environ 是字典样式的对象
    print(f"\n环境变量总数: {len(os.environ)}")
    # 列出前5个环境变量
    env_items = list(os.environ.items())[:5]
    for key, value in env_items:
        print(f"  {key} = {value}")

    # 操作系统的分隔符
    print(f"\nos.sep (路径分隔符):  {os.sep!r}")
    print(f"os.linesep (行分隔符):  {os.linesep!r}")
    print(f"os.pathsep (路径列表分隔符): {os.pathsep!r}")

    # ========== 4. shutil 高级文件操作 ==========
    print("\n=== 4. shutil 文件复制与移动 ===")

    shutil_dir = tempfile.mkdtemp(prefix="py_shutil_")
    try:
        # 创建源文件
        src = os.path.join(shutil_dir, "source.txt")
        with open(src, "w", encoding="utf-8") as f:
            f.write("这是源文件内容\n第二行\n第三行")

        # shutil.copy() 复制文件（内容 + 权限）
        dst = os.path.join(shutil_dir, "copy.txt")
        shutil.copy(src, dst)
        print(f"复制文件: {src} -> {dst}")

        # shutil.copy2() 复制文件（内容 + 权限 + 元数据）
        dst2 = os.path.join(shutil_dir, "copy2.txt")
        shutil.copy2(src, dst2)
        print(f"复制文件(含元数据): {src} -> {dst2}")

        # shutil.copytree() 复制整个目录
        src_dir = os.path.join(shutil_dir, "src_dir")
        os.mkdir(src_dir)
        with open(os.path.join(src_dir, "data.txt"), "w") as f:
            f.write("子目录中的文件")
        dst_dir = os.path.join(shutil_dir, "dst_dir")
        shutil.copytree(src_dir, dst_dir)
        print(f"复制目录: {src_dir} -> {dst_dir}")
        print(f"  目标目录内容: {os.listdir(dst_dir)}")

        # shutil.move() 移动文件/目录
        move_src = os.path.join(shutil_dir, "to_move.txt")
        with open(move_src, "w") as f:
            f.write("将被移动")
        move_dst = os.path.join(shutil_dir, "moved.txt")
        shutil.move(move_src, move_dst)
        print(f"移动文件: {move_src} -> {move_dst}")
        print(f"  原位置仍存在: {os.path.exists(move_src)}")
        print(f"  新位置已存在: {os.path.exists(move_dst)}")

        # 磁盘使用情况
        try:
            usage = shutil.disk_usage(shutil_dir)
            print(f"\n磁盘空间 (GB):")
            print(f"  总容量: {usage.total / (1024**3):.1f}")
            print(f"  已使用: {usage.used / (1024**3):.1f}")
            print(f"  可用:   {usage.free / (1024**3):.1f}")
        except Exception:
            print("\n磁盘使用情况: (当前系统不支持)")

    finally:
        shutil.rmtree(shutil_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
