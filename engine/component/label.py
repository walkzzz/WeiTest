"""Label Component - encapsulates label/text operations"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wei.core.finder.locator import Locator
    from engine.page.base_page import BasePage


class Label:
    """
    标签组件

    封装标签/文本元素的操作

    使用示例：
        >>> lbl = Label(page, ByID("lbl_title"))
        >>> lbl.text
        >>> lbl.is_visible
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化标签

        Args:
            page: 页面对象
            locator: 标签定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    @property
    def text(self) -> str:
        """获取标签文本"""
        return self._get_element().window_text()

    @property
    def is_visible(self) -> bool:
        """检查是否可见"""
        return self._get_element().is_visible()

    @property
    def is_enabled(self) -> bool:
        """检查是否可用"""
        return self._get_element().is_enabled()
