#!/usr/bin/env python3
"""
subprocess模块 - Python标准库子进程管理

涵盖内容:
  1. run - 运行命令并等待完成 (推荐)
  2. 捕获标准输出和标准错误
  3. Popen - 高级进程控制
  4. 管道 (pipe) 与进程间通信
  5. 返回码检查

[!]  安全提醒: 永远不要将用户输入直接传递给 shell=True

参考: https://docs.python.org/zh-cn/3/library/subprocess.html
"""

import subprocess
import sys
import os


def print_result(result, label="命令结果"):
    """格式化输出 subprocess 结果"""
    print(f"=== {label} ===")
    print(f"  返回码: {result.returncode}")
    print(f"  参数:   {result.args}")
    if result.stdout:
        print(f"  stdout: {result.stdout.strip()}")
    if result.stderr:
        print(f"  stderr: {result.stderr.strip()}")


# ============================================================
# 1. 基本命令执行
# ============================================================
print("=" * 60)
print("1. subprocess.run() - 运行命令")
print("=" * 60)

# Windows 和 Unix 命令不同, 用 Python 命令 (跨平台)
python_cmd = sys.executable

# 方式1: 字符串列表 (推荐, 安全)
print("运行: python --version")
result1 = subprocess.run(
    [python_cmd, "--version"],
    capture_output=True,
    text=True,
)
print_result(result1, "python --version")

# 方式2: shell=True (仅用于简单/已知命令, 有安全风险!)
print("\n方式: shell=True (echo 演示):")
result2 = subprocess.run(
    "echo Hello from subprocess!",
    shell=True,
    capture_output=True,
    text=True,
)
print_result(result2, "echo")

# ============================================================
# 2. 捕获标准输出与标准错误
# ============================================================
print("\n" + "=" * 60)
print("2. 捕获 stdout 和 stderr")
print("=" * 60)

# 执行 Python 代码并捕获输出
print("执行: print('Hello stdout'); print('Error msg', file=stderr)")
code = "import sys; print('Hello stdout'); print('Error msg', file=sys.stderr)"
result3 = subprocess.run(
    [python_cmd, "-c", code],
    capture_output=True,
    text=True,
)
print_result(result3, "捕获stdout和stderr")

# 合并 stderr 到 stdout
print("\n合并 stderr 到 stdout (stderr=subprocess.STDOUT):")
result4 = subprocess.run(
    [python_cmd, "-c", code],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
print(f"合并后 stdout: {result4.stdout.strip()}")

# ============================================================
# 3. 返回码检查
# ============================================================
print("\n" + "=" * 60)
print("3. 返回码检查 (returncode)")
print("=" * 60)

# check=True - 非零返回码时抛出 CalledProcessError
print("成功命令 (check=True):")
try:
    subprocess.run(
        [python_cmd, "-c", "print('success')"],
        check=True,
        capture_output=True,
        text=True,
    )
    print("  [OK] 命令执行成功")
except subprocess.CalledProcessError as e:
    print(f"  [XX] 命令失败: {e}")

print("\n失败命令 (check=True):")
try:
    subprocess.run(
        [python_cmd, "-c", "import sys; sys.exit(1)"],
        check=True,
        capture_output=True,
        text=True,
    )
    print("  [OK] 命令执行成功")
except subprocess.CalledProcessError as e:
    print(f"  [XX] CalledProcessError: 返回码={e.returncode}")

# 手动检查返回码
print("\n手动检查返回码:")
result5 = subprocess.run(
    [python_cmd, "-c", "import sys; sys.exit(42)"],
    capture_output=True,
    text=True,
)
print(f"  返回码: {result5.returncode}")
if result5.returncode == 0:
    print("  状态: 成功")
else:
    print(f"  状态: 失败 (退出码 {result5.returncode})")

# ============================================================
# 4. timeout - 超时控制
# ============================================================
print("\n" + "=" * 60)
print("4. timeout - 超时控制")
print("=" * 60)

print("执行 sleep 0.5 秒, timeout=2:")
try:
    result6 = subprocess.run(
        [python_cmd, "-c", "import time; time.sleep(0.5); print('done')"],
        capture_output=True,
        text=True,
        timeout=2,  # 2秒超时
    )
    print(f"  [OK] 完成: {result6.stdout.strip()}")
except subprocess.TimeoutExpired:
    print("  [XX] 命令超时")

print("\n超时演示 (timeout=0.1):")
try:
    subprocess.run(
        [python_cmd, "-c", "import time; time.sleep(5)"],
        capture_output=True,
        text=True,
        timeout=0.1,
    )
except subprocess.TimeoutExpired as e:
    print(f"  [XX] TimeoutExpired: {e}")

# ============================================================
# 5. Popen - 高级进程控制
# ============================================================
print("\n" + "=" * 60)
print("5. Popen - 非阻塞进程控制")
print("=" * 60)

# Popen - 启动进程但不等它完成
print("Popen 示例: 执行 sleep 并检查状态")
proc = subprocess.Popen(
    [python_cmd, "-c", "import time; time.sleep(0.5); print('Child done')"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

print(f"  进程 PID: {proc.pid}")
print(f"  是否完成: {proc.poll()}")  # None = 仍在运行

# 等待完成
stdout, stderr = proc.communicate(timeout=5)
print(f"  完成后的返回码: {proc.returncode}")
print(f"  stdout: {stdout.strip()}")
if stderr:
    print(f"  stderr: {stderr.strip()}")

# ============================================================
# 6. 管道 - 进程间通信
# ============================================================
print("\n" + "=" * 60)
print("6. 管道 (Pipe) - 进程间通信")
print("=" * 60)

# 模拟: echo "hello world" | python -c "print(input().upper())"
# Windows 和 Unix 方式不同, 使用 Popen 管道
print("管道示例: 大写转换")
p1 = subprocess.Popen(
    [python_cmd, "-c", "print('hello world from pipe')"],
    stdout=subprocess.PIPE,
    text=True,
)
p2 = subprocess.Popen(
    [python_cmd, "-c", "import sys; print(sys.stdin.read().upper())"],
    stdin=p1.stdout,
    stdout=subprocess.PIPE,
    text=True,
)

# 关闭 p1 的 stdout (这样 p2 才能收到 EOF)
if p1.stdout:
    p1.stdout.close()

output, _ = p2.communicate()
print(f"  管道输出: {output.strip()}")

# input 参数 - 直接传递输入
print("\n使用 input 参数传递数据:")
result7 = subprocess.run(
    [python_cmd, "-c", "import sys; data=sys.stdin.read(); print(f'Received: {data.strip().upper()}')"],
    input="hello from input parameter",
    capture_output=True,
    text=True,
    encoding="utf-8",
)
print(f"  {result7.stdout.strip()}")

# ============================================================
# 7. 环境变量
# ============================================================
print("\n" + "=" * 60)
print("7. 环境变量操作")
print("=" * 60)

# 传递自定义环境变量
my_env = {**os.environ, "MY_VAR": "hello_from_subprocess"}
result8 = subprocess.run(
    [python_cmd, "-c", "import os; print(os.environ.get('MY_VAR', 'NOT SET'))"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    env=my_env,
)
print(f"自定义环境变量: {result8.stdout.strip() if result8.stdout else '(empty)'}")

# ============================================================
# 安全提示
# ============================================================
print("\n" + "=" * 60)
print("8. [!]  安全提示")
print("=" * 60)

print("""
[XX] 危险 (shell注入):
  user_input = "user_file; rm -rf /"
  subprocess.run(f"cat {user_input}", shell=True)  # 会删除所有文件!

[OK] 安全 (使用列表参数):
  user_input = "user_file; rm -rf /"
  subprocess.run(["cat", user_input])  # 把整个输入当文件名, 安全!

[OK] 最佳实践:
  1. 优先使用参数列表 (非字符串), 避免 shell=True
  2. 如果必须 shell=True, 确保输入已经过严格过滤
  3. 使用 shlex.quote() 来安全转义参数
  4. 用 check=True 检测命令失败
  5. 用 timeout 防止命令无限挂起
""")
