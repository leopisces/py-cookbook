#!/usr/bin/env python3
"""
logging模块 - Python标准库日志系统

涵盖内容:
  1. 基本配置 (basicConfig)
  2. Logger / Handler / Formatter 架构
  3. 文件日志 (FileHandler)
  4. 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
  5. 实用日志配置模板

参考: https://docs.python.org/zh-cn/3/library/logging.html
"""

import logging
import os
import tempfile


# ============================================================
# 1. 基本日志配置
# ============================================================
print("=" * 60)
print("1. logging.basicConfig - 基本配置")
print("=" * 60)

# 基本日志输出 (默认输出到 stderr, 级别 WARNING)
print("=== 默认日志 (仅 WARNING 及以上) ===")
logging.warning("这是一个 WARNING 日志")
logging.error("这是一个 ERROR 日志")
logging.info("这条 INFO 不会显示 (因为默认级别是WARNING)")

# 配置日志格式和级别
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
print("\n=== 配置后日志 (所有级别, 含时间戳) ===")
logging.debug("这是 DEBUG 日志 - 调试信息")
logging.info("这是 INFO 日志  - 一般信息")
logging.warning("这是 WARNING 日志 - 警告")

# 注意: basicConfig 只生效一次, 已在上面调用, 后续设置无效
print("\n注意: basicConfig() 仅在首次调用时生效!")

# ============================================================
# 2. Logger / Handler / Formatter
# ============================================================
print("\n" + "=" * 60)
print("2. Logger / Handler / Formatter 架构")
print("=" * 60)

# 创建专门的 Logger (推荐方式, 而非直接用 root logger)
logger = logging.getLogger("MyApp")
logger.setLevel(logging.DEBUG)

# 防止日志向上传播到 root logger (避免重复输出)
logger.propagate = False

# Handler - 日志输出目标
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Formatter - 日志格式
formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)-8s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
console_handler.setFormatter(formatter)

# 将 Handler 添加到 Logger
logger.addHandler(console_handler)

# 测试各级别日志
print("自定义 Logger 输出:")
logger.debug("调试信息 - 变量 x = 42")
logger.info("用户登录成功")
logger.warning("磁盘空间不足 90%")
logger.error("数据库连接失败")
logger.critical("系统崩溃! 需要立即处理")

# ============================================================
# 3. 文件日志
# ============================================================
print("\n" + "=" * 60)
print("3. 文件日志 (FileHandler)")
print("=" * 60)

tmp_path = os.path.join(tempfile.gettempdir(), "py_cookbook_logging.log")

try:
    # 创建文件日志 Logger
    file_logger = logging.getLogger("FileLogger")
    file_logger.setLevel(logging.DEBUG)
    file_logger.propagate = False

    # FileHandler - 写入文件
    file_handler = logging.FileHandler(tmp_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
    )
    file_logger.addHandler(file_handler)

    # 写入日志
    file_logger.info("应用启动")
    file_logger.debug("加载配置文件")
    file_logger.warning("检测到低内存")
    file_logger.error("处理请求失败: /api/data")
    file_logger.info("应用关闭")

    # 确保写入磁盘
    for handler in file_logger.handlers:
        handler.flush()
        handler.close()

    # 读取并显示日志文件
    print(f"日志文件: {tmp_path}")
    print("内容:")
    with open(tmp_path, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"  {line.rstrip()}")

    # 文件大小
    size = os.path.getsize(tmp_path)
    print(f"\n文件大小: {size} 字节")

finally:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
        print(f"已删除日志文件")

# ============================================================
# 4. 日志级别详解
# ============================================================
print("\n" + "=" * 60)
print("4. 日志级别 (Level)")
print("=" * 60)

levels = [
    (logging.DEBUG, "DEBUG"),
    (logging.INFO, "INFO"),
    (logging.WARNING, "WARNING"),
    (logging.ERROR, "ERROR"),
    (logging.CRITICAL, "CRITICAL"),
]

print(f"{'级别':<10} {'数值':<6} {'说明'}")
print("-" * 50)
explanations = {
    "DEBUG": "详细的调试信息, 仅开发时使用",
    "INFO": "确认程序正常运行的信息",
    "WARNING": "表明有潜在问题, 程序仍可运行",
    "ERROR": "严重问题, 某功能无法正常运行",
    "CRITICAL": "致命错误, 程序可能无法继续运行",
}
for level_num, level_name in levels:
    print(f"{level_name:<10} {level_num:<6} {explanations[level_name]}")

# 动态设置级别
print("\n动态调整日志级别演示:")
demo_logger = logging.getLogger("LevelDemo")
demo_logger.setLevel(logging.WARNING)
demo_logger.propagate = False
dh = logging.StreamHandler()
dh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
demo_logger.addHandler(dh)

print("setLevel(WARNING):")
demo_logger.debug("不会被看到")
demo_logger.info("也不会被看到")
demo_logger.warning("这个会显示")

print("\nsetLevel(DEBUG):")
demo_logger.setLevel(logging.DEBUG)
demo_logger.debug("现在可以看到 DEBUG 了")
demo_logger.info("INFO 也可以显示了")

# 防止后续干扰, 移除 handler
demo_logger.removeHandler(dh)

# ============================================================
# 5. 实用日志配置模板
# ============================================================
print("\n" + "=" * 60)
print("5. 实用日志配置模板")
print("=" * 60)


def setup_logger(name, log_file=None, console_level=logging.INFO,
                 file_level=logging.DEBUG):
    """
    创建配置好的 Logger 实例

    Args:
        name: Logger 名称 (通常用 __name__)
        log_file: 日志文件路径 (None = 不写文件)
        console_level: 控制台日志级别
        file_level: 文件日志级别

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # 控制台 Handler
    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(logging.Formatter(
        "[%(levelname)-7s] %(name)s - %(message)s"
    ))
    logger.addHandler(console)

    # 文件 Handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-7s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(file_handler)

    return logger


# 使用模板
print("使用配置模板:")

# 示例1: 仅控制台日志
app_logger = setup_logger("App")
app_logger.info("应用启动 (仅控制台)")

# 示例2: 同时写控制台和文件
tmp_path2 = os.path.join(tempfile.gettempdir(), "py_cookbook_app.log")
try:
    full_logger = setup_logger("FullApp", log_file=tmp_path2)
    full_logger.debug("这条 DEBUG 只写文件")
    full_logger.info("这条 INFO 写文件并显示在控制台")
    full_logger.warning("这条 WARNING 也是如此")

    # 关闭文件 handler 以释放文件句柄
    for handler in full_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()

    # 查看文件日志
    print(f"\n文件日志 ({tmp_path2}):")
    if os.path.exists(tmp_path2):
        with open(tmp_path2, 'r', encoding='utf-8') as f:
            for line in f:
                print(f"  {line.rstrip()}")
        os.unlink(tmp_path2)
finally:
    if os.path.exists(tmp_path2):
        os.unlink(tmp_path2)

# ============================================================
# 日志最佳实践
# ============================================================
print("\n" + "=" * 60)
print("6. 日志最佳实践")
print("=" * 60)

print("""
[OK] 最佳实践:
  1. 使用 `logger = logging.getLogger(__name__)` 创建 Logger
  2. 不要用 root logger (logging.info 等函数)
  3. 用合适的级别: DEBUG 开发, INFO 生产, WARNING 关注
  4. 写有用的信息: 包含关键变量值, 不要写无意义日志
  5. 异常日志用 logger.exception() 自动附加堆栈
  6. 生产环境配置: 文件日志 + 日志轮转 (RotatingFileHandler)
  7. 不要用 print() 代替日志!

[XX] 常见错误:
  - 在循环中大量写 DEBUG 日志
  - 日志中包含敏感信息 (密码/密钥/Token)
  - 多次调用 basicConfig
  - 忘记设置 encoding='utf-8' (中文乱码)
""")

# 异常日志示例
print("异常日志示例 (logger.exception):")
err_logger = logging.getLogger("ErrorDemo")
err_logger.propagate = False
eh = logging.StreamHandler()
eh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
err_logger.addHandler(eh)

try:
    result = 1 / 0
except ZeroDivisionError:
    err_logger.exception("计算错误 (自动附加完整堆栈):")
