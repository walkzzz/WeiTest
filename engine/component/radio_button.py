"""RadioButton Component - encapsulates radio button operations"""

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from wei.engine.page.base_page import BasePage


class RadioButton:
    """
    单选按钮组件

    封装单选按钮的所有操作

    Example:
        >>> radio = RadioButton(page, ByID("radio_male"))
        >>> radio.check()
        >>> is_checked = radio.is_checked()
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化单选按钮

        Args:
            page: 页面对象
            locator: 定位器
        """
        self.page = page
        self.locator = locator
        self._element: Any = None

    def _get_element(self) -> Any:
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def check(self) -> "RadioButton":
        """
        选中单选按钮

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        element.click_input()
        return self

    def uncheck(self) -> "RadioButton":
        """
        取消选中单选按钮

        注意：单选按钮通常不能手动取消选中，
        只能选中同组的其他按钮来取消当前按钮

        Returns:
            self: 支持链式调用
        """
        # 单选按钮通常不能取消选中
        # 这里只在不选中时执行操作
        if self.is_checked():
            # 尝试点击取消（可能不起作用）
            element = self._get_element()
            element.click_input()
        return self

    def toggle(self) -> "RadioButton":
        """
        切换选中状态

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        element.click_input()
        return self

    def is_checked(self) -> bool:
        """
        检查是否被选中

        Returns:
            bool: 是否被选中
        """
        element = self._get_element()

        try:
            # 使用 ToggleState
            return element.get_toggle_state() == 1  # ToggleState.On
        except Exception:
            # 备用方法：检查选中状态
            return element.is_selected()

    def get_text(self) -> str:
        """
        获取单选按钮文本

        Returns:
            按钮文本
        """
        element = self._get_element()
        return element.window_text()

    def is_enabled(self) -> bool:
        """
        检查单选按钮是否可用

        Returns:
            bool: 是否可用
        """
        element = self._get_element()
        return element.is_enabled()

    def is_visible(self) -> bool:
        """
        检查单选按钮是否可见

        Returns:
            bool: 是否可见
        """
        element = self._get_element()
        return element.is_visible()

    def wait_until_checked(self, timeout: int = 10) -> "RadioButton":
        """
        等待直到选中

        Args:
            timeout: 超时时间

        Returns:
            self: 支持链式调用
        """
        from core.waiter.smart_wait import SmartWait

        def is_checked() -> bool:
            return self.is_checked()

        waiter = SmartWait(timeout=timeout)
        waiter.wait_until(is_checked, timeout)
        return self

    def wait_until_enabled(self, timeout: int = 10) -> "RadioButton":
        """
        等待直到可用

        Args:
            timeout: 超时时间

        Returns:
            self: 支持链式调用
        """
        from core.waiter.smart_wait import SmartWait

        def is_enabled() -> bool:
            return self.is_enabled()

        waiter = SmartWait(timeout=timeout)
        waiter.wait_until(is_enabled, timeout)
        return self

    @property
    def checked(self) -> bool:
        """获取选中状态"""
        return self.is_checked()

    @property
    def text(self) -> str:
        """获取按钮文本"""
        return self.get_text()

    @property
    def enabled(self) -> bool:
        """获取可用状态"""
        return self.is_enabled()


class RadioButtonGroup:
    """
    单选按钮组

    管理一组单选按钮

    Example:
        >>> group = RadioButtonGroup(page, [
        ...     ByID("radio_male"),
        ...     ByID("radio_female"),
        ...     ByID("radio_other")
        ... ])
        >>> group.select("radio_female")
        >>> selected = group.get_selected()
    """

    def __init__(
        self, page: "BasePage", locators: List["Locator"], names: Optional[List[str]] = None
    ) -> None:
        """
        初始化单选按钮组

        Args:
            page: 页面对象
            locators: 定位器列表
            names: 按钮名称列表 (可选)
        """
        self.page = page
        self._buttons: List[RadioButton] = []
        self._names: List[str] = []

        for i, locator in enumerate(locators):
            button = RadioButton(page, locator)
            self._buttons.append(button)

            if names and i < len(names):
                self._names.append(names[i])
            else:
                self._names.append(f"button_{i}")

    def select(self, name_or_index: Any) -> "RadioButtonGroup":
        """
        选择按钮

        Args:
            name_or_index: 按钮名称或索引

        Returns:
            self: 支持链式调用
        """
        if isinstance(name_or_index, int):
            # 按索引选择
            if 0 <= name_or_index < len(self._buttons):
                self._buttons[name_or_index].check()
        else:
            # 按名称选择
            try:
                index = self._names.index(name_or_index)
                self._buttons[index].check()
            except ValueError:
                pass

        return self

    def get_selected(self) -> Optional[str]:
        """
        获取选中的按钮名称

        Returns:
            选中的按钮名称，未选中返回 None
        """
        for i, button in enumerate(self._buttons):
            if button.is_checked():
                return self._names[i]
        return None

    def get_selected_index(self) -> int:
        """
        获取选中的按钮索引

        Returns:
            选中的按钮索引，未选中返回 -1
        """
        for i, button in enumerate(self._buttons):
            if button.is_checked():
                return i
        return -1

    def get_all_options(self) -> List[str]:
        """
        获取所有选项文本

        Returns:
            选项文本列表
        """
        options = []
        for button in self._buttons:
            options.append(button.get_text())
        return options

    def is_checked(self, name_or_index: Any) -> bool:
        """
        检查按钮是否被选中

        Args:
            name_or_index: 按钮名称或索引

        Returns:
            bool: 是否被选中
        """
        if isinstance(name_or_index, int):
            if 0 <= name_or_index < len(self._buttons):
                return self._buttons[name_or_index].is_checked()
        else:
            try:
                index = self._names.index(name_or_index)
                return self._buttons[index].is_checked()
            except ValueError:
                pass
        return False

    @property
    def selected(self) -> Optional[str]:
        """获取选中的按钮名称"""
        return self.get_selected()

    @property
    def options(self) -> List[str]:
        """获取所有选项文本"""
        return self.get_all_options()
