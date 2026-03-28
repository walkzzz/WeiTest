"""Screenshot Mixin - handles screenshot capture"""

import os
from typing import Optional
from datetime import datetime


class ScreenshotMixin:
    """
    截图 Mixin

    职责：屏幕和元素截图
    """

    _window = None  # 从 ApplicationMixin 继承

    def take_screenshot(self, filename: Optional[str] = None, element=None) -> str:
        """
        截取整个窗口或元素

        Args:
            filename: 文件名（可选，自动生成）
            element: 元素实例（可选，截取元素区域）

        Returns:
            截图文件路径
        """
        # 创建截图目录
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        filepath = os.path.join(screenshot_dir, filename)

        try:
            import pyautogui

            if element:
                # 截取元素区域
                rect = element.rectangle()
                screenshot = pyautogui.screenshot(
                    region=(rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
                )
            else:
                # 截取整个屏幕
                screenshot = pyautogui.screenshot()

            screenshot.save(filepath)
            return filepath

        except Exception as e:
            raise RuntimeError(f"截图失败：{e}")

    def capture_window(self, filename: Optional[str] = None) -> str:
        """
        截取窗口

        Args:
            filename: 文件名

        Returns:
            截图文件路径
        """
        if not self._window:
            raise RuntimeError("窗口未初始化")

        return self.take_screenshot(filename, self._window._get_pywinauto_window())
