"""TextInput Component - encapsulates text input operations with full type annotations"""

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class TextInput:
    """
    文本输入框组件

    封装输入框的所有操作

    Example:
        >>> input_box = TextInput(page, ByID("txt_username"))
        >>> input_box.type("admin").clear().type("user")
        >>> input_box.value  # 获取当前值
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化文本输入框

        Args:
            page: 页面对象
            locator: 输入框定位器
        """
        self.page = page
        self.locator = locator
        self._element: Any = None

    def _get_element(self) -> Any:
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def type(self, text: str, delay: float = 0.01) -> "TextInput":
        """
        输入文本

        Args:
            text: 要输入的文本
            delay: 字符间隔时间

        Returns:
            self: 支持链式调用
        """
        self._get_element().type_keys(text, with_spaces=True, pauses=delay)
        return self

    def clear(self) -> "TextInput":
        """
        清空文本

        Returns:
            self: 支持链式调用
        """
        elem = self._get_element()
        elem.click_input()
        elem.select()
        elem.type_keys("{BACKSPACE}")
        return self

    def set_value(self, text: str) -> "TextInput":
        """
        设置值（先清空后输入）

        Args:
            text: 要设置的值

        Returns:
            self: 支持链式调用
        """
        return self.clear().type(text)

    @property
    def value(self) -> str:
        """获取当前值"""
        return self._get_element().window_text()

    @property
    def is_editable(self) -> bool:
        """检查是否可编辑"""
        return self._get_element().is_enabled()

    @property
    def placeholder(self) -> Optional[str]:
        """获取占位符文本（如果支持）"""
        try:
            return self._get_element().element_info.help_text
        except Exception:
            return None
