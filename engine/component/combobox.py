"""ComboBox Component - encapsulates combobox operations"""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from wei.engine.page.base_page import BasePage


class ComboBox:
    """
    下拉框组件

    封装下拉框的所有操作

    使用示例：
        >>> combo = ComboBox(page, ByID("cmb_country"))
        >>> combo.select("China")
        >>> combo.selected_value
        >>> combo.options  # 获取所有选项
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化下拉框

        Args:
            page: 页面对象
            locator: 下拉框定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def select(self, value: str) -> "ComboBox":
        """选择选项"""
        self._get_element().select(value)
        return self

    def select_by_index(self, index: int) -> "ComboBox":
        """通过索引选择"""
        items = self._get_element().children()
        if 0 <= index < len(items):
            items[index].click_input()
        else:
            raise IndexError(f"索引 {index} 超出范围")
        return self

    @property
    def selected_value(self) -> str:
        """获取已选择的值"""
        return self._get_element().window_text()

    @property
    def selected_index(self) -> int:
        """获取已选择的索引"""
        items = self._get_element().children()
        selected = self.selected_value
        for i, item in enumerate(items):
            if item.window_text() == selected:
                return i
        return -1

    @property
    def options(self) -> List[str]:
        """获取所有选项"""
        items = self._get_element().children()
        return [item.window_text() for item in items]

    @property
    def is_expanded(self) -> bool:
        """检查下拉框是否已展开"""
        return len(self._get_element().children()) > 1
