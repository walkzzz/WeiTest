"""Coordinate Locator - locate elements by coordinates"""

from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class CoordLocator:
    """
    坐标定位器

    使用绝对或相对坐标定位

    使用示例：
        >>> locator = CoordLocator(100, 200)
        >>> page.click(locator)

        >>> locator = CoordLocator(x=50, y=50, relative_to="window")
        >>> page.click(locator)
    """

    x: int  # X 坐标
    y: int  # Y 坐标
    relative_to: Optional[str] = None  # "window" 或 None (屏幕坐标)
    description: str = ""

    def locate(self, window=None) -> Tuple[int, int]:
        """
        定位坐标

        Args:
            window: 窗口对象（如果 relative_to="window"）

        Returns:
            (x, y) 屏幕坐标
        """
        if self.relative_to == "window" and window:
            # 相对于窗口
            window_rect = window._get_pywinauto_window().rectangle()
            return (window_rect.left + self.x, window_rect.top + self.y)
        else:
            # 绝对屏幕坐标
            return (self.x, self.y)

    def move(self, dx: int = 0, dy: int = 0) -> "CoordLocator":
        """
        移动坐标

        Args:
            dx: X 轴偏移
            dy: Y 轴偏移

        Returns:
            self: 支持链式调用
        """
        self.x += dx
        self.y += dy
        return self


@dataclass
class RegionLocator:
    """
    区域定位器

    定义矩形区域

    使用示例：
        >>> region = RegionLocator(100, 100, 200, 200)
        >>> page.take_screenshot(region=region)
    """

    x: int  # 左上角 X
    y: int  # 左上角 Y
    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """转换为元组 (x, y, width, height)"""
        return (self.x, self.y, self.width, self.height)

    def contains(self, x: int, y: int) -> bool:
        """检查点是否在区域内"""
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def center(self) -> Tuple[int, int]:
        """获取区域中心点"""
        return (self.x + self.width // 2, self.y + self.height // 2)
