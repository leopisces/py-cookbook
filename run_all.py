"""
批量运行所有 demo 文件 — 验证项目完整性
========================================
运行方式: python run_all.py

此脚本会:
1. 按章节顺序运行所有 demo 文件
2. 检测每个文件是否成功执行（无报错）
3. 统计总耗时和成功率
4. 输出汇总报告
"""

import subprocess
import sys
import time
import os
from pathlib import Path

# Windows GBK 兼容: 设置 stdout 编码为 UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# 所有 demo 文件列表（按章节顺序）
DEMO_FILES = [
    # 01-basics
    "01-basics/01_hello_world.py",
    "01-basics/02_syntax.py",
    "01-basics/03_comments.py",
    "01-basics/04_operators.py",
    "01-basics/05_type_conversion.py",
    "01-basics/06_number.py",
    "01-basics/07_string.py",
    # 02-datatypes
    "02-datatypes/01_list.py",
    "02-datatypes/02_tuple.py",
    "02-datatypes/03_dict.py",
    "02-datatypes/04_set.py",
    "02-datatypes/05_data_structure.py",
    "02-datatypes/06_bytes.py",
    "02-datatypes/07_none.py",
    # 03-control-flow
    "03-control-flow/01_conditional.py",
    "03-control-flow/02_for_loop.py",
    "03-control-flow/03_while_loop.py",
    "03-control-flow/04_comprehensions.py",
    # 04-functions
    "04-functions/01_function.py",
    "04-functions/02_lambda.py",
    "04-functions/03_decorator.py",
    "04-functions/04_iterator_generator.py",
    "04-functions/05_namespace_scope.py",
    # 05-oop
    "05-oop/01_class.py",
    "05-oop/02_inheritance.py",
    "05-oop/03_magic_methods.py",
    # 06-modules
    "06-modules/01_module.py",
    "06-modules/02_name_main.py",
    "06-modules/03_pip_package.py",
    # 07-io
    "07-io/01_input_output.py",
    "07-io/02_file.py",
    "07-io/03_os_module.py",
    "07-io/04_with_statement.py",
    # 08-errors
    "08-errors/01_try_except.py",
    "08-errors/02_custom_exceptions.py",
    "08-errors/03_exception_chaining.py",
    "08-errors/04_warnings.py",
    # 09-stdlib
    "09-stdlib/01_math.py",
    "09-stdlib/02_random.py",
    "09-stdlib/03_datetime.py",
    "09-stdlib/04_re.py",
    "09-stdlib/05_json.py",
    "09-stdlib/06_csv.py",
    "09-stdlib/07_sys.py",
    "09-stdlib/08_os_path.py",
    "09-stdlib/09_operator.py",
    "09-stdlib/10_statistics.py",
    "09-stdlib/11_hashlib.py",
    "09-stdlib/12_pickle.py",
    "09-stdlib/13_stringio.py",
    "09-stdlib/14_logging.py",
    "09-stdlib/15_subprocess.py",
    "09-stdlib/16_queue.py",
    "09-stdlib/17_itertools.py",
    "09-stdlib/18_collections.py",
    "09-stdlib/19_functools.py",
    # 10-advanced
    "10-advanced/01_threading.py",
    "10-advanced/02_asyncio.py",
    "10-advanced/03_xml.py",
    "10-advanced/04_socket.py",
    "10-advanced/05_multiprocessing.py",
    # 11-builtin
    "11-builtin/01_type_functions.py",
    "11-builtin/02_math_iteration.py",
    "11-builtin/03_object_io.py",
    # 12-pattern-matching
    "12-pattern-matching/01_match_case.py",
    # 13-dataclass_enum
    "13-dataclass_enum/01_dataclass.py",
    "13-dataclass_enum/02_enum.py",
    # 14-typing
    "14-typing/01_type_annotations.py",
    "14-typing/02_advanced_typing.py",
    # 15-testing (skip — these are pytest test files, not standalone demos)
]


def run_demo(filepath: str) -> tuple[bool, float, str]:
    """运行单个 demo 文件，返回 (成功?, 耗时秒, 错误信息)"""
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(Path(__file__).parent),
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            return True, elapsed, ""
        else:
            # 截取 stderr 的关键错误信息
            error_lines = result.stderr.strip().split("\n")
            error_summary = "\n".join(error_lines[-5:]) if len(error_lines) > 5 else result.stderr.strip()
            return False, elapsed, error_summary
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return False, elapsed, "超时 (>60s)"
    except Exception as e:
        elapsed = time.time() - start
        return False, elapsed, str(e)


def main():
    project_root = Path(__file__).parent
    print("=" * 60)
    print("  Python Cookbook — 批量运行验证")
    print("=" * 60)
    print(f"  项目目录: {project_root}")
    print(f"  Python: {sys.version}")
    print(f"  待验证文件数: {len(DEMO_FILES)}")
    print()

    # 过滤出实际存在的文件
    existing_files = []
    missing_files = []
    for filepath in DEMO_FILES:
        full_path = project_root / filepath
        if full_path.exists():
            existing_files.append(filepath)
        else:
            missing_files.append(filepath)

    if missing_files:
        print("  ⚠ 缺失文件:")
        for f in missing_files:
            print(f"    - {f}")
        print()

    print(f"  实际运行: {len(existing_files)} 个文件")
    print("-" * 60)

    success_count = 0
    fail_count = 0
    failed_files = []
    total_time = 0.0

    for i, filepath in enumerate(existing_files, 1):
        short_name = filepath.replace("/", "/").split("/")[-1]
        chapter = filepath.split("/")[0]
        print(f"  [{i}/{len(existing_files)}] {chapter}/{short_name} ... ", end="", flush=True)

        ok, elapsed, error = run_demo(filepath)
        total_time += elapsed

        if ok:
            success_count += 1
            print(f"[OK] ({elapsed:.1f}s)")
        else:
            fail_count += 1
            failed_files.append((filepath, error))
            print(f"[FAIL] ({elapsed:.1f}s)")

    # 汇总报告
    print()
    print("=" * 60)
    print("  汇总报告")
    print("=" * 60)
    print(f"  总文件数:   {len(existing_files)}")
    print(f"  成功:       {success_count} [OK]")
    print(f"  失败:       {fail_count} [FAIL]")
    print(f"  缺失:       {len(missing_files)} [WARN]")
    print(f"  总耗时:     {total_time:.1f}s")
    print(f"  通过率:     {success_count / len(existing_files) * 100:.1f}%")

    if failed_files:
        print()
        print("  [FAIL] 失败详情:")
        for filepath, error in failed_files:
            print(f"    {filepath}:")
            for line in error.split("\n")[:3]:
                print(f"      {line}")

    if missing_files:
        print()
        print("  [WARN] 缺失文件 (可能尚未创建):")
        for f in missing_files:
            print(f"    - {f}")

    print()
    if fail_count == 0 and len(missing_files) == 0:
        print("  [ALL OK] 所有 demo 文件运行成功! 项目完整性验证通过。")
    elif fail_count == 0:
        print("  [OK] 所有已有文件运行成功，但部分文件尚未创建。")
    else:
        print("  [WARN] 有文件运行失败，请检查错误详情。")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())