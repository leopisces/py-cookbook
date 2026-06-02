"""
Python warnings 模块 — 警告机制
================================
学习目标：
  - warnings.warn() 发出警告
  - 警告类别 (Warning/UserWarning/DeprecationWarning/RuntimeWarning等)
  - warnings.filterwarnings() 过滤警告
  - -W 命令行选项控制警告
  - 自定义警告类
  - 实际开发中的警告使用场景
"""

import warnings


# ========== 自定义警告类 ==========

class ConfigWarning(UserWarning):
    """配置相关警告"""
    pass


class DeprecatedAPIWarning(DeprecationWarning):
    """API 弃用警告"""
    pass


def old_api_function(data):
    """一个即将弃用的旧接口"""
    warnings.warn(
        "old_api_function() 将在 v2.0 中移除，请使用 new_api_function()",
        DeprecatedAPIWarning,
        stacklevel=2,
    )
    return data.upper()


def new_api_function(data):
    """新接口"""
    return data.upper()


def main():
    # ========== 1. 基本警告 — warnings.warn() ==========
    print("=" * 50)
    print("演示 1: 基本警告 — warnings.warn()")
    print("=" * 50)

    # 默认发出 UserWarning
    warnings.warn("这是一个用户警告", UserWarning)
    print("  警告发出后程序继续执行（不会中断）")

    # 警告 vs 异常的区别
    print("\n  警告 vs 异常:")
    print("  - 异常(Exception): 程序中断，必须处理")
    print("  - 警告(Warning): 程序继续运行，仅提醒开发者")

    # ========== 2. 警告类别 ==========
    print("\n" + "=" * 50)
    print("演示 2: 警告类别")
    print("=" * 50)

    categories = {
        "Warning":           "所有警告的基类",
        "UserWarning":       "用户代码发出的警告（默认类别）",
        "DeprecationWarning": "弃用警告（针对开发者，默认被过滤）",
        "RuntimeWarning":    "运行时警告",
        "SyntaxWarning":     "语法相关警告",
        "FutureWarning":     "未来行为变更警告（针对用户）",
        "PendingDeprecationWarning": "即将弃用警告",
    }

    for name, desc in categories.items():
        print(f"  {name:30s} → {desc}")

    # DeprecationWarning 默认被过滤（不会显示）
    print("\n--- DeprecationWarning 默认被过滤 ---")
    warnings.warn("这条弃用警告默认不会显示", DeprecationWarning)
    print("  上面发出了 DeprecationWarning，但默认被过滤了")

    # FutureWarning 默认会显示（面向最终用户）
    print("\n--- FutureWarning 默认会显示 ---")
    warnings.warn("这条未来警告默认会显示", FutureWarning)

    # ========== 3. 过滤警告 — filterwarnings() ==========
    print("\n" + "=" * 50)
    print("演示 3: 过滤警告 — filterwarnings()")
    print("=" * 50)

    # 过滤动作:
    # "default"  — 首次出现时显示（同位置仅显示一次）
    # "error"    — 将警告转为异常
    # "ignore"   — 忽略警告
    # "always"   — 每次出现都显示
    # "module"   — 同模块中首次出现时显示
    # "once"     — 全局仅显示一次

    # 忽略所有 UserWarning
    print("--- 忽略指定类别 ---")
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.warn("这条 UserWarning 被过滤了", UserWarning)
    print("  UserWarning 已被过滤，不会显示")

    # 恢复默认
    warnings.resetwarnings()
    warnings.warn("重置后 UserWarning 会恢复显示", UserWarning)

    # 按消息文本过滤
    print("\n--- 按消息文本过滤 ---")
    warnings.filterwarnings("ignore", message=".*deprecated.*")
    warnings.warn("deprecated 功能警告", UserWarning)  # 被过滤
    warnings.warn("普通警告", UserWarning)              # 正常显示
    warnings.resetwarnings()

    # 将警告转为异常
    print("\n--- 将警告转为异常 (action='error') ---")
    warnings.filterwarnings("error", category=UserWarning)
    try:
        warnings.warn("这条警告会被转为异常", UserWarning)
    except UserWarning as e:
        print(f"  捕获到警告转异常: {e}")
    warnings.resetwarnings()

    # ========== 4. stacklevel 参数 ==========
    print("\n" + "=" * 50)
    print("演示 4: stacklevel 参数")
    print("=" * 50)

    # stacklevel 控制警告指向的调用位置
    # stacklevel=1 → warn() 所在行（默认）
    # stacklevel=2 → 调用 warn() 的函数所在行（推荐）

    def inner_function():
        warnings.warn("stacklevel=1 指向此函数", UserWarning, stacklevel=1)
        warnings.warn("stacklevel=2 指向调用者", UserWarning, stacklevel=2)

    print("  stacklevel 控制警告的源代码指向位置:")
    inner_function()
    print("  推荐使用 stacklevel=2，让警告指向真正需要修改的地方")

    # ========== 5. 自定义警告类 ==========
    print("\n" + "=" * 50)
    print("演示 5: 自定义警告类")
    print("=" * 50)

    # 使用自定义警告类便于分类过滤
    warnings.warn("配置参数缺失，使用默认值", ConfigWarning)

    # 弃用 API 警告
    result = old_api_function("hello")
    print(f"  旧 API 结果: {result}")

    # ========== 6. 命令行 -W 选项 ==========
    print("\n" + "=" * 50)
    print("演示 6: 命令行 -W 选项")
    print("=" * 50)

    print("  Python 启动时可通过 -W 选项控制警告:")
    print("  python -W all      → 显示所有警告")
    print("  python -W ignore   → 忽略所有警告")
    print("  python -W error    → 所有警告转为异常")
    print("  python -W default  → 默认行为")
    print()
    print("  示例:")
    print("  python -W all 08-errors/04_warnings.py")
    print("  python -W ignore::DeprecationWarning 08-errors/04_warnings.py")

    # ========== 7. 实际开发中的使用场景 ==========
    print("\n" + "=" * 50)
    print("演示 7: 实际开发中的使用场景")
    print("=" * 50)

    print("  场景 1: API 弃用提醒")
    print("    使用 DeprecationWarning 提示旧接口即将移除")
    print("    开发阶段可见，生产环境默认过滤")
    print()
    print("  场景 2: 配置兼容性提醒")
    print("    使用 FutureWarning 提示行为将变更")
    print("    面向用户，默认显示")
    print()
    print("  场景 3: 类型不匹配提醒")
    print("    使用 UserWarning 提示参数类型不理想")
    print("    不中断程序，但提醒开发者检查")
    print()
    print("  最佳实践:")
    print("  - 始终使用 stacklevel=2 让警告指向调用者")
    print("  - 弃用用 DeprecationWarning，行为变更用 FutureWarning")
    print("  - 不要过度使用警告，只在确实需要提醒时使用")
    print("  - 测试时用 -W error 确保不忽略重要警告")


if __name__ == "__main__":
    main()

# ============================================================
# 相关主题:
#   - 08-errors/01_try_except.py  → 异常捕获基础
#   - 08-errors/02_custom_exceptions.py  → 自定义异常类
#   - 08-errors/03_exception_chaining.py → 异常链
# ============================================================