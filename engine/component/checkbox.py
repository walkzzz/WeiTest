"""CheckBox Component - encapsulates checkbox operations"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class CheckBox:
    """
    复选框组件

    封装复选框的所有操作

    使用示例：
        >>> chk = CheckBox(page, ByID("chk_remember"))
        >>> chk.check()
        >>> chk.uncheck()
        >>> chk.toggle()
        >>> chk.is_checked
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化复选框

        Args:
            page: 页面对象
            locator: 复选框定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def check(self) -> "CheckBox":
        """勾选"""
        if not self.is_checked:
            self._get_element().click_input()
        return self

    def uncheck(self) -> "CheckBox":
        """取消勾选"""
        if self.is_checked:
            self._get_element().click_input()
        return self

    def toggle(self) -> "CheckBox":
        """切换状态"""
        self._get_element().click_input()
        return self

    @property
    def is_checked(self) -> bool:
        """检查是否已勾选"""
        return bool(self._get_element().get_toggle_state())

    @property
    def label(self) -> str:
        """获取复选框标签文本"""
        return self._get_element().window_text()
