"""Action Mixin - handles user interactions with elements"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator


class ActionMixin:
    """
    操作 Mixin

    职责：元素交互操作（点击/输入/选择等）
    """

    _window = None  # 从 ApplicationMixin 继承

    def click(self, locator: "Locator") -> "ActionMixin":
        """
        点击元素

        Args:
            locator: 定位器

        Returns:
            self: 支持链式调用
        """
        element = self.find_element(locator)
        element.click_input()
        return self

    def double_click(self, locator: "Locator") -> "ActionMixin":
        """
        双击元素

        Args:
            locator: 定位器

        Returns:
            self: 支持链式调用
        """
        element = self.find_element(locator)
        element.double_click_input()
        return self

    def type_text(self, locator: "Locator", text: str, clear: bool = True) -> "ActionMixin":
        """
        输入文本

        Args:
            locator: 定位器
            text: 要输入的文本
            clear: 是否清空原有文本

        Returns:
            self: 支持链式调用
        """
        element = self.find_element(locator)

        if clear:
            element.click_input()
            element.select()
            element.type_keys("{BACKSPACE}")

        element.type_keys(text, with_spaces=True)
        return self

    def select_combobox(self, locator: "Locator", value: str) -> "ActionMixin":
        """
        选择下拉框项

        Args:
            locator: 定位器
            value: 要选择的值

        Returns:
            self: 支持链式调用
        """
        element = self.find_element(locator)
        element.select(value)
        return self

    def check_checkbox(self, locator: "Locator", check: bool = True) -> "ActionMixin":
        """
        勾选/取消勾选复选框

        Args:
            locator: 定位器
            check: True=勾选，False=取消勾选

        Returns:
            self: 支持链式调用
        """
        element = self.find_element(locator)
        is_checked = bool(element.get_toggle_state())

        if check != is_checked:
            element.click_input()

        return self

    def get_text(self, locator: "Locator") -> str:
        """
        获取元素文本

        Args:
            locator: 定位器

        Returns:
            元素文本
        """
        element = self.find_element(locator)
        return element.window_text()

    def is_enabled(self, locator: "Locator") -> bool:
        """
        检查元素是否可用

        Args:
            locator: 定位器

        Returns:
            bool: 是否可用
        """
        element = self.find_element(locator)
        return element.is_enabled()

    def is_visible(self, locator: "Locator") -> bool:
        """
        检查元素是否可见

        Args:
            locator: 定位器

        Returns:
            bool: 是否可见
        """
        element = self.find_element(locator)
        return element.is_visible()
