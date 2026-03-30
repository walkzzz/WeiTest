#!/usr/bin/env python3
"""WeiTest - 微测试命令行工具"""

import argparse
import sys
from pathlib import Path


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        prog="wei",
        description="微测试 - Windows UI 自动化测试框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  wei init myproject        创建新的测试项目
  wei create page login     创建登录页面对象
  wei run tests/            运行测试
  wei report                生成测试报告
        """,
    )

    parser.add_argument("-v", "--version", action="version", version="%(prog)s 2.0.1")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化新的测试项目")
    init_parser.add_argument("project_name", help="项目名称")
    init_parser.add_argument(
        "--template", choices=["basic", "full"], default="basic", help="项目模板 (默认：basic)"
    )
    init_parser.set_defaults(func=cmd_init)

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建测试资源")
    create_subparsers = create_parser.add_subparsers(dest="resource", help="资源类型")

    # create page
    page_parser = create_subparsers.add_parser("page", help="创建页面对象")
    page_parser.add_argument("page_name", help="页面名称")
    page_parser.add_argument("--yaml", action="store_true", help="同时生成 YAML 定义文件")
    page_parser.set_defaults(func=cmd_create_page)

    # create test
    test_parser = create_subparsers.add_parser("test", help="创建测试文件")
    test_parser.add_argument("test_name", help="测试名称")
    test_parser.set_defaults(func=cmd_create_test)

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行测试")
    run_parser.add_argument("path", nargs="?", default="tests", help="测试路径 (默认：tests)")
    run_parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    run_parser.add_argument("--parallel", action="store_true", help="并行执行")
    run_parser.set_defaults(func=cmd_run)

    # report 命令
    report_parser = subparsers.add_parser("report", help="生成测试报告")
    report_parser.add_argument(
        "--type", choices=["html", "allure"], default="html", help="报告类型 (默认：html)"
    )
    report_parser.add_argument("--open", action="store_true", help="生成后打开报告")
    report_parser.set_defaults(func=cmd_report)

    # clean 命令
    clean_parser = subparsers.add_parser("clean", help="清理缓存和临时文件")
    clean_parser.set_defaults(func=cmd_clean)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if hasattr(args, "func"):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n操作已取消")
            sys.exit(1)
        except Exception as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)


def cmd_init(args):
    """初始化新项目"""
    project_name = args.project_name
    template = args.template

    print(f"创建项目：{project_name}")
    print(f"模板：{template}")

    project_dir = Path(project_name)
    if project_dir.exists():
        print(f"错误：目录 '{project_name}' 已存在")
        sys.exit(1)

    # 创建目录结构
    directories = [
        project_dir / "tests",
        project_dir / "pages",
        project_dir / "data",
        project_dir / "reports",
        project_dir / "logs",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ 创建目录：{directory}")

    # 创建基础文件
    files = {
        project_dir / "README.md": f"# {project_name}\n\n测试项目\n",
        project_dir / "requirements.txt": "# 测试依赖\npytest>=7.4.0\npywinauto>=0.6.8\n",
        project_dir / "pytest.ini": "[pytest]\ntestpaths = tests\naddopts = -v\n",
    }

    if template == "full":
        files.update(
            {
                project_dir / "conftest.py": "# pytest fixtures\nimport pytest\n\n",
                project_dir / "pages/login_page.yaml": "elements:\n  # 在此定义页面元素\n",
            }
        )

    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ 创建文件：{file_path}")

    print(f"\n✅ 项目 '{project_name}' 创建完成!")
    print(f"\n快速开始:")
    print(f"  cd {project_name}")
    print(f"  pip install -r requirements.txt")
    print(f"  atm create page login --yaml")
    print(f"  atm create test test_login")
    print(f"  atm run")


def cmd_create_page(args):
    """创建页面对象"""
    page_name = args.page_name
    generate_yaml = args.yaml

    pages_dir = Path("pages")
    pages_dir.mkdir(exist_ok=True)

    # 创建 Python 文件
    py_file = pages_dir / f"{page_name}_page.py"
    py_content = f'''"""{page_name} 页面对象"""

from engine.page.base_page import BasePage


class {page_name.capitalize()}Page(BasePage):
    """{page_name} 页面对象"""
    
    def __init__(self, page):
        super().__init__()
        self.page = page
    
    # TODO: 添加页面方法和属性
'''

    with open(py_file, "w", encoding="utf-8") as f:
        f.write(py_content)
    print(f"  ✓ 创建页面：{py_file}")

    # 创建 YAML 文件
    yaml_file = None
    if generate_yaml:
        yaml_file = pages_dir / f"{page_name}_page.yaml"
        yaml_content = f"""# {page_name} 页面定义

elements:
  # 示例元素:
  # example_button:
  #   locator_type: id
  #   locator_value: btn_example
  #   control_type: Button
  #   description: "示例按钮"
"""
        with open(yaml_file, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        print(f"  ✓ 创建 YAML: {yaml_file}")

    print(f"\n✅ 页面 '{page_name}' 创建完成!")
    print(f"\n下一步:")
    print(f"  1. 编辑 {py_file} 添加页面方法")
    if generate_yaml and yaml_file:
        print(f"  2. 编辑 {yaml_file} 定义页面元素")


def cmd_create_test(args):
    """创建测试文件"""
    test_name = args.test_name

    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)

    test_file = tests_dir / f"{test_name}.py"

    test_content = f'''"""{test_name} 测试"""

import pytest


class Test{test_name.replace("_", " ").title().replace(" ", "")}:
    """{test_name} 测试类"""
    
    @pytest.mark.smoke
    def test_example(self):
        """示例测试"""
        # TODO: 实现测试逻辑
        assert True
    
    # TODO: 添加更多测试方法
'''

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    print(f"  ✓ 创建测试：{test_file}")

    print(f"\n✅ 测试 '{test_name}' 创建完成!")
    print(f"\n下一步:")
    print(f"  编辑 {test_file} 实现测试逻辑")


def cmd_run(args):
    """运行测试"""
    import subprocess

    path = args.path
    verbose = args.verbose
    parallel = args.parallel

    cmd = ["pytest", path]

    if verbose:
        cmd.append("-v")

    if parallel:
        cmd.extend(["-n", "auto"])

    print(f"运行测试：{' '.join(cmd)}")

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def cmd_report(args):
    """生成测试报告"""
    import subprocess

    report_type = args.type

    if report_type == "html":
        print("生成 HTML 报告...")
        result = subprocess.run(
            ["pytest", "--html=reports/report.html", "--self-contained-html"], capture_output=True
        )
        if result.returncode == 0:
            print("  ✓ HTML 报告生成：reports/report.html")
            if args.open:
                import webbrowser

                webbrowser.open(f"file://{Path('reports/report.html').absolute()}")

    elif report_type == "allure":
        print("生成 Allure 报告...")
        subprocess.run(["pytest", "--alluredir=reports/allure-results"])
        subprocess.run(
            [
                "allure",
                "generate",
                "reports/allure-results",
                "-o",
                "reports/allure-report",
                "--clean",
            ]
        )
        print("  ✓ Allure 报告生成：reports/allure-report")
        if args.open:
            subprocess.run(["allure", "open", "reports/allure-report"])


def cmd_clean(args):
    """清理缓存和临时文件"""
    import shutil

    patterns = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        "reports",
        ".mypy_cache",
        ".ruff_cache",
    ]

    cleaned = 0

    for pattern in patterns:
        for path in Path(".").rglob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"  ✓ 清理：{path}")
                cleaned += 1
            except Exception:
                pass

    print(f"\n✅ 清理完成，共清理 {cleaned} 个文件/目录")


if __name__ == "__main__":
    main()
