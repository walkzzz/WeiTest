"""Enhanced Action Mixin with advanced locators support"""

from typing import Optional, Union
from core.finder.locator import Locator
from engine.locators.image_locator import ImageLocator
from engine.locators.coord_locator import CoordLocator


class AdvancedActionMixin:
    """
    高级操作 Mixin

    支持图像定位、坐标定位等高级功能
    """

    _window = None

    def click(
        self, locator: Union[Locator, ImageLocator, CoordLocator, tuple]
    ) -> "AdvancedActionMixin":
        """
        点击元素（支持多种定位方式）

        Args:
            locator: 定位器（支持 Locator/ImageLocator/CoordLocator/坐标元组）

        Returns:
            self: 支持链式调用
        """
        coords = self._resolve_locator(locator)
        self._click_at_coords(coords)
        return self

    def double_click(
        self, locator: Union[Locator, ImageLocator, CoordLocator, tuple]
    ) -> "AdvancedActionMixin":
        """双击元素"""
        coords = self._resolve_locator(locator)
        import pyautogui

        pyautogui.doubleClick(coords[0], coords[1])
        return self

    def right_click(
        self, locator: Union[Locator, ImageLocator, CoordLocator, tuple]
    ) -> "AdvancedActionMixin":
        """右键点击"""
        coords = self._resolve_locator(locator)
        import pyautogui

        pyautogui.rightClick(coords[0], coords[1])
        return self

    def hover(
        self, locator: Union[Locator, ImageLocator, CoordLocator, tuple]
    ) -> "AdvancedActionMixin":
        """鼠标悬停"""
        coords = self._resolve_locator(locator)
        import pyautogui

        pyautogui.moveTo(coords[0], coords[1], duration=0.5)
        return self

    def _resolve_locator(self, locator) -> tuple:
        """解析定位器为坐标"""
        if isinstance(locator, tuple):
            return locator
        elif isinstance(locator, CoordLocator):
            return locator.locate(self._window)
        elif isinstance(locator, ImageLocator):
            return locator.locate()
        elif isinstance(locator, Locator):
            element = self.find_element(locator)
            rect = element.rectangle()
            return (
                rect.left + (rect.right - rect.left) // 2,
                rect.top + (rect.bottom - rect.top) // 2,
            )
        else:
            raise ValueError(f"不支持的定位器类型：{type(locator)}")

    def _click_at_coords(self, coords: tuple):
        """在指定坐标点击"""
        import pyautogui

        pyautogui.click(coords[0], coords[1])

    def type_at(self, x: int, y: int, text: str) -> "AdvancedActionMixin":
        """
        在指定坐标位置输入文本

        Args:
            x: X 坐标
            y: Y 坐标
            text: 要输入的文本

        Returns:
            self
        """
        import pyautogui

        pyautogui.click(x, y)
        pyautogui.write(text, interval=0.05)
        return self

    def drag_to(
        self, from_coords: tuple, to_coords: tuple, duration: float = 1.0
    ) -> "AdvancedActionMixin":
        """
        拖拽操作

        Args:
            from_coords: 起始坐标
            to_coords: 目标坐标
            duration: 拖拽时间（秒）

        Returns:
            self
        """
        import pyautogui

        pyautogui.dragTo(to_coords[0], to_coords[1], duration=duration, button="left")
        return self
