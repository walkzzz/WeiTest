"""Report Manager - manages test report generation"""

import os
from pathlib import Path
from typing import Optional, List
import shutil


class ReportManager:
    """
    报告管理器

    负责生成和管理测试报告

    支持：
    - Allure 报告
    - pytest-html 报告
    - 截图管理
    - 测试统计

    使用示例：
        >>> reporter = ReportManager()
        >>> reporter.create_allure_report()
        >>> reporter.open_html_report()
    """

    DEFAULT_REPORT_DIR = "reports"
    ALLURE_DIR = "allure-results"
    HTML_REPORT = "pytest-report.html"
    SCREENSHOT_DIR = "screenshots"

    def __init__(self, report_dir: Optional[str] = None):
        """
        初始化报告管理器

        Args:
            report_dir: 报告目录
        """
        self.report_dir = Path(report_dir or self.DEFAULT_REPORT_DIR)
        self.report_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        (self.report_dir / self.ALLURE_DIR).mkdir(exist_ok=True)
        (self.report_dir / self.SCREENSHOT_DIR).mkdir(exist_ok=True)

    def get_allure_dir(self) -> Path:
        """获取 Allure 报告目录"""
        return self.report_dir / self.ALLURE_DIR

    def get_html_report_path(self) -> Path:
        """获取 HTML 报告路径"""
        return self.report_dir / self.HTML_REPORT

    def get_screenshot_dir(self) -> Path:
        """获取截图目录"""
        return self.report_dir / self.SCREENSHOT_DIR

    def save_screenshot(self, screenshot_data: bytes, filename: str) -> Path:
        """
        保存截图

        Args:
            screenshot_data: 截图数据
            filename: 文件名

        Returns:
            截图文件路径
        """
        screenshot_dir = self.get_screenshot_dir()
        filepath = screenshot_dir / filename

        with open(filepath, "wb") as f:
            f.write(screenshot_data)

        return filepath

    def create_allure_report(self) -> bool:
        """
        创建 Allure 报告

        Returns:
            bool: 是否成功
        """
        try:
            # 检查 allure 是否安装
            result = os.system("allure --version")
            if result != 0:
                print("⚠️  Allure 未安装，请运行：pip install allure-pytest")
                return False

            # 生成报告
            allure_dir = self.get_allure_dir()
            output_dir = self.report_dir / "allure-report"

            cmd = f"allure generate {allure_dir} -o {output_dir} --clean"
            result = os.system(cmd)

            if result == 0:
                print(f"✅ Allure 报告已生成：{output_dir}")
                return True
            else:
                print("❌ Allure 报告生成失败")
                return False

        except Exception as e:
            print(f"❌ Allure 报告生成异常：{e}")
            return False

    def open_allure_report(self) -> bool:
        """
        打开 Allure 报告

        Returns:
            bool: 是否成功
        """
        try:
            output_dir = self.report_dir / "allure-report"

            if not output_dir.exists():
                print("⚠️  Allure 报告不存在，请先生成报告")
                return False

            # 打开报告
            cmd = f"allure open {output_dir}"
            os.system(cmd)
            return True

        except Exception as e:
            print(f"❌ 打开 Allure 报告异常：{e}")
            return False

    def open_html_report(self) -> bool:
        """
        打开 HTML 报告

        Returns:
            bool: 是否成功
        """
        html_path = self.get_html_report_path()

        if not html_path.exists():
            print("⚠️  HTML 报告不存在")
            return False

        # 根据操作系统打开文件
        import platform

        system = platform.system()

        if system == "Windows":
            os.startfile(str(html_path))
        elif system == "Darwin":
            os.system(f"open {html_path}")
        else:
            os.system(f"xdg-open {html_path}")

        print(f"✅ HTML 报告已打开：{html_path}")
        return True

    def cleanup_old_reports(self, keep_days: int = 7):
        """
        清理旧报告

        Args:
            keep_days: 保留天数
        """
        import time

        now = time.time()
        cutoff = now - (keep_days * 86400)

        for root, dirs, files in os.walk(self.report_dir):
            for file in files:
                filepath = Path(root) / file
                if filepath.stat().st_mtime < cutoff:
                    filepath.unlink()
                    print(f"已删除旧文件：{filepath}")

    def get_report_stats(self) -> dict:
        """
        获取报告统计

        Returns:
            统计字典
        """
        stats = {
            "total_screenshots": 0,
            "allure_results": 0,
            "html_report_exists": False,
            "total_size_mb": 0,
        }

        # 统计截图
        screenshot_dir = self.get_screenshot_dir()
        if screenshot_dir.exists():
            stats["total_screenshots"] = len(list(screenshot_dir.glob("*.png")))

        # 统计 Allure 结果
        allure_dir = self.get_allure_dir()
        if allure_dir.exists():
            stats["allure_results"] = len(list(allure_dir.glob("*.json")))

        # 检查 HTML 报告
        html_path = self.get_html_report_path()
        stats["html_report_exists"] = html_path.exists()

        # 计算总大小
        total_size = 0
        for root, dirs, files in os.walk(self.report_dir):
            for file in files:
                filepath = Path(root) / file
                total_size += filepath.stat().st_size

        stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)

        return stats

    def print_stats(self):
        """打印报告统计"""
        stats = self.get_report_stats()

        print("\n📊 报告统计")
        print("=" * 50)
        print(f"截图数量：{stats['total_screenshots']}")
        print(f"Allure 结果：{stats['allure_results']}")
        print(f"HTML 报告：{'✅ 存在' if stats['html_report_exists'] else '❌ 不存在'}")
        print(f"总大小：{stats['total_size_mb']} MB")
        print("=" * 50)
