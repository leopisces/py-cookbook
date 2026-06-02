"""
pip 与包管理 — Python 包的安装、管理与发布
=============================================
学习目标：
  - pip 基本命令 (install/uninstall/list/show/search)
  - requirements.txt 与依赖管理
  - 虚拟环境 (venv) 的创建与使用
  - pip 配置与镜像源
  - 包的发布概念 (setup.py / pyproject.toml)
  - 开发中的依赖管理最佳实践
"""

import subprocess
import sys
import os


def main():
    # ========== 1. pip 基本命令 ==========
    print("=" * 50)
    print("演示 1: pip 基本命令")
    print("=" * 50)

    # 查看已安装的包
    print("--- pip list ---")
    result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=columns"],
                           capture_output=True, text=True, timeout=30)
    lines = result.stdout.strip().split("\n")
    # 只显示前 10 行（包含表头）
    for line in lines[:10]:
        print(f"  {line}")
    if len(lines) > 10:
        print(f"  ... 共 {len(lines) - 2} 个已安装包")

    # 查看某个包的详细信息
    print("\n--- pip show ---")
    result = subprocess.run([sys.executable, "-m", "pip", "show", "pip"],
                           capture_output=True, text=True, timeout=15)
    print(f"  {result.stdout.strip()}")

    # 常用命令总结
    print("\n--- pip 常用命令速查 ---")
    commands = {
        "pip install <包名>":      "安装包",
        "pip install <包名>==版本": "安装指定版本",
        "pip uninstall <包名>":    "卸载包",
        "pip list":                "列出已安装的包",
        "pip show <包名>":         "查看包的详细信息",
        "pip freeze":              "导出依赖列表（格式: 包名==版本）",
        "pip check":               "检查依赖冲突",
        "pip install -r file.txt": "从文件批量安装依赖",
        "pip install --upgrade <包名>": "升级包",
        "pip config list":         "查看 pip 配置",
    }
    for cmd, desc in commands.items():
        print(f"  {cmd:38s} → {desc}")

    # ========== 2. requirements.txt ==========
    print("\n" + "=" * 50)
    print("演示 2: requirements.txt 与依赖管理")
    print("=" * 50)

    print("  requirements.txt 格式:")
    print("  ─────────────────────────────────")
    print("  # 基本格式")
    print("  numpy>=1.20")
    print("  pandas==1.4.0")
    print("  requests>=2.28,<3.0  # 范围约束")
    print("  flask                # 不指定版本（最新）")
    print()
    print("  # 开发依赖（注释说明）")
    print("  pytest>=7.0          # 测试框架")
    print("  ruff>=0.1            # 代码检查")
    print()
    print("  生成命令:")
    print("  pip freeze > requirements.txt   → 导出当前环境所有依赖")
    print("  pip install -r requirements.txt → 从文件安装所有依赖")

    # 实际演示 pip freeze
    print("\n--- pip freeze (仅显示前5行) ---")
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                           capture_output=True, text=True, timeout=15)
    freeze_lines = result.stdout.strip().split("\n")
    for line in freeze_lines[:5]:
        print(f"  {line}")
    if len(freeze_lines) > 5:
        print(f"  ... 共 {len(freeze_lines)} 个依赖")

    # ========== 3. 虚拟环境 (venv) ==========
    print("\n" + "=" * 50)
    print("演示 3: 虚拟环境 (venv)")
    print("=" * 50)

    print("  虚拟环境的作用:")
    print("  - 隔离项目依赖（避免全局污染）")
    print("  - 不同项目使用不同版本的包")
    print("  - 便于部署和复现环境")
    print()

    print("  venv 使用步骤:")
    print("  ─────────────────────────────────")
    print("  # 1. 创建虚拟环境")
    print("  python -m venv myenv")
    print()
    print("  # 2. 激活虚拟环境")
    print("  # Windows:")
    print("  myenv\\Scripts\\activate")
    print("  # macOS/Linux:")
    print("  source myenv/bin/activate")
    print()
    print("  # 3. 安装依赖（在虚拟环境中）")
    print("  pip install -r requirements.txt")
    print()
    print("  # 4. 退出虚拟环境")
    print("  deactivate")

    print()
    print("  其他虚拟环境工具:")
    print("  - conda: Anaconda/Miniconda 的环境管理（适合科学计算）")
    print("  - virtualenv: venv 的增强版（更灵活）")
    print("  - poetry: 现代依赖管理工具（pyproject.toml 风格）")
    print("  - pipenv: Pip + venv 的结合体")

    # ========== 4. pip 配置与镜像源 ==========
    print("\n" + "=" * 50)
    print("演示 4: pip 配置与镜像源")
    print("=" * 50)

    print("  国内常用镜像源:")
    mirrors = {
        "清华大学":  "https://pypi.tuna.tsinghua.edu.cn/simple",
        "阿里云":    "https://mirrors.aliyun.com/pypi/simple",
        "豆瓣":      "https://pypi.doubanio.com/simple",
        "腾讯云":    "https://mirrors.cloud.tencent.com/pypi/simple",
        "华为云":    "https://repo.huaweicloud.com/repository/pypi/simple",
    }
    for name, url in mirrors.items():
        print(f"  {name:10s}: {url}")

    print()
    print("  临时使用镜像:")
    print("  pip install <包名> -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print()
    print("  永久配置（pip config）:")
    print("  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple")
    print("  pip config list  # 查看当前配置")

    # 查看当前 pip 配置
    print("\n--- 当前 pip 配置 ---")
    result = subprocess.run([sys.executable, "-m", "pip", "config", "list"],
                           capture_output=True, text=True, timeout=15)
    config_output = result.stdout.strip()
    if config_output:
        print(f"  {config_output}")
    else:
        print("  (无自定义配置，使用默认源)")

    # ========== 5. 包的发布概念 ==========
    print("\n" + "=" * 50)
    print("演示 5: 包的发布概念")
    print("=" * 50)

    print("  发布到 PyPI 的基本步骤:")
    print("  ─────────────────────────────────")
    print("  1. 项目结构:")
    print("     my_package/")
    print("     ├── pyproject.toml  # 现代项目配置（推荐）")
    print("     ├── src/")
    print("     │   └── my_package/")
    print("     │       ├── __init__.py")
    print("     │       └── core.py")
    print("     └── tests/")
    print()
    print("  2. pyproject.toml 最小配置:")
    print("     [project]")
    print("     name = 'my-package'")
    print("     version = '0.1.0'")
    print("     description = 'My awesome package'")
    print("     requires-python = '>=3.10'")
    print()
    print("  3. 构建与发布:")
    print("     pip install build twine")
    print("     python -m build             # 构建 wheel 和 sdist")
    print("     twine upload dist/*         # 上传到 PyPI")
    print()
    print("  注意: 实际发布需要 PyPI 账号和 API token")

    # ========== 6. 开发最佳实践 ==========
    print("\n" + "=" * 50)
    print("演示 6: 依赖管理最佳实践")
    print("=" * 50)

    print("  最佳实践:")
    print("  ─────────────────────────────────")
    practices = [
        "1. 每个项目使用独立虚拟环境",
        "2. 用 requirements.txt 固定生产依赖版本",
        "3. 用 requirements-dev.txt 管理开发依赖",
        "4. 定期运行 pip check 检查依赖冲突",
        "5. 发布包时用 pyproject.toml (现代标准)",
        "6. 不在代码中硬编码 pip install 命令",
        "7. 使用国内镜像加速下载",
        "8. 项目根目录放置 requirements.txt",
    ]
    for p in practices:
        print(f"  {p}")


if __name__ == "__main__":
    main()

# ============================================================
# 相关主题:
#   - 06-modules/01_module.py  → 模块与包的导入机制
#   - 06-modules/02_name_main.py → __name__ 与 __main__
#   - 09-stdlib/15_subprocess.py → subprocess 执行外部命令
# ============================================================