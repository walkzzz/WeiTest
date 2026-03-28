"""Button Component - encapsulates button operations with full type annotations"""

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class Button:
    """
    按钮组件

    封装按钮的所有操作

    Example:
        >>> btn = Button(page, ByID("btn_login"))
        >>> btn.click()
        >>> btn.wait_clickable().click()
        >>> btn.text  # 获取按钮文本
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化按钮组件

        Args:
            page: 页面对象
            locator: 按钮定位器
        """
        self.page = page
        self.locator = locator
        self._element: Any = None

    def _get_element(self) -> Any:
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    # ========== 操作 ==========

    def click(self) -> "Button":
        """
        点击按钮

        Returns:
            self: 支持链式调用
        """
        self._get_element().click_input()
        return self

    def double_click(self) -> "Button":
        """
        双击按钮

        Returns:
            self: 支持链式调用
        """
        self._get_element().double_click_input()
        return self

    def wait_clickable(self, timeout: int = 10) -> "Button":
        """
        等待按钮可点击

        Args:
            timeout: 超时时间（秒）

        Returns:
            self: 支持链式调用
        """
        self.page.wait_element(self.locator, "clickable", timeout)
        return self

    # ========== 属性 ==========

    @property
    def text(self) -> str:
        """获取按钮文本"""
        return self._get_element().window_text()

    @property
    def is_enabled(self) -> bool:
        """检查按钮是否可用"""
        return self._get_element().is_enabled()

    @property
    def is_visible(self) -> bool:
        """检查按钮是否可见"""
        return self._get_element().is_visible()

    @property
    def is_clickable(self) -> bool:
        """检查按钮是否可点击"""
        return self.is_visible and self.is_enabled
