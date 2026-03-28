"""Screenshot on Failure - automatic screenshot when tests fail"""

import pytest
from pathlib import Path
from datetime import datetime
from typing import Any, Optional


class ScreenshotOnFailure:
    """
    失败自动截图插件

    pytest hook 实现，测试失败时自动截图

    Example:
        # conftest.py
        pytest_plugins = ["infra.reporting.screenshot_on_failure"]
    """

    def __init__(self, output_dir: str = "reports/screenshots") -> None:
        """
        初始化截图插件

        Args:
            output_dir: 截图输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item: pytest.Item, call: pytest.CallInfo) -> Any:
        """
        测试失败时自动截图

        Args:
            item: 测试项
            call: 调用信息
        """
        # 执行测试
        outcome = yield
        report = outcome.get_result()

        # 只在失败时截图
        if report.when == "call" and report.failed:
            self._take_screenshot(item.name)

    def _take_screenshot(self, test_name: str) -> Optional[Path]:
        """
        截取屏幕

        Args:
            test_name: 测试名称

        Returns:
            截图文件路径
        """
        try:
            import pyautogui

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_failure_{timestamp}.png"
            filepath = self.output_dir / filename

            # 截图
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))

            print(f"\n📸 失败截图已保存：{filepath}")

            # 添加到 Allure 报告
            self._attach_to_allure(filepath)

            return filepath
        except Exception as e:
            print(f"\n⚠️  截图失败：{e}")
            return None

    def _attach_to_allure(self, filepath: Path) -> None:
        """
        附加截图到 Allure 报告

        Args:
            filepath: 截图文件路径
        """
        try:
            import allure

            # 附加为 PNG
            allure.attach.file(
                str(filepath), name="失败截图", attachment_type=allure.attachment_type.PNG
            )
        except ImportError:
            # Allure 未安装，忽略
            pass


class ScreenshotPlugin:
    """
    截图插件 - 支持手动调用

    Example:
        >>> plugin = ScreenshotPlugin()
        >>> plugin.screenshot("before_action")
        >>> plugin.screenshot("after_action")
    """

    def __init__(self, output_dir: str = "reports/screenshots") -> None:
        """
        初始化截图插件

        Args:
            output_dir: 截图输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def screenshot(self, name: str, description: str = "") -> Optional[Path]:
        """
        截取屏幕

        Args:
            name: 截图名称
            description: 描述信息

        Returns:
            截图文件路径
        """
        try:
            import pyautogui

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.output_dir / filename

            # 截图
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))

            # 保存描述信息
            if description:
                description_file = filepath.with_suffix(".txt")
                with open(description_file, "w", encoding="utf-8") as f:
                    f.write(f"截图名称：{name}\n")
                    f.write(f"描述：{description}\n")
                    f.write(f"时间：{timestamp}\n")

            print(f"📸 截图已保存：{filepath}")

            # 附加到 Allure
            self._attach_to_allure(filepath, name)

            return filepath
        except Exception as e:
            print(f"⚠️  截图失败：{e}")
            return None

    def _attach_to_allure(self, filepath: Path, name: str) -> None:
        """附加截图到 Allure 报告"""
        try:
            import allure

            allure.attach.file(str(filepath), name=name, attachment_type=allure.attachment_type.PNG)
        except ImportError:
            pass


# pytest 插件注册
def pytest_configure(config: pytest.Config) -> None:
    """配置 pytest 插件"""
    config.pluginmanager.register(ScreenshotOnFailure(), "screenshot_on_failure")


# 便捷函数
def take_screenshot(name: str, description: str = "") -> Optional[Path]:
    """
    截取屏幕的便捷函数

    Args:
        name: 截图名称
        description: 描述信息

    Returns:
        截图文件路径
    """
    plugin = ScreenshotPlugin()
    return plugin.screenshot(name, description)
