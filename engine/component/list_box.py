"""ListBox Component - encapsulates list box operations"""

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class ListBox:
    """
    列表框组件

    封装列表框的所有操作

    Example:
        >>> listbox = ListBox(page, ByID("lst_items"))
        >>> listbox.select("Option 1")
        >>> listbox.select_by_index(0)
        >>> selected = listbox.get_selected()
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化列表框

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

    def select(self, text: str) -> "ListBox":
        """
        选择列表项

        Args:
            text: 列表项文本

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        element.select(text)
        return self

    def select_by_index(self, index: int) -> "ListBox":
        """
        按索引选择列表项

        Args:
            index: 列表项索引

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        element.select(index)
        return self

    def deselect(self, text: str) -> "ListBox":
        """
        取消选择列表项

        Args:
            text: 列表项文本

        Returns:
            self: 支持链式调用
        """
        # 对于单选列表框，选择其他项即可
        # 对于多选列表框，使用 deselect
        element = self._get_element()
        try:
            element.deselect(text)
        except Exception:
            pass
        return self

    def get_selected(self) -> str:
        """
        获取选中的列表项文本

        Returns:
            选中的列表项文本
        """
        element = self._get_element()
        return element.selected_text()

    def get_selected_index(self) -> int:
        """
        获取选中的列表项索引

        Returns:
            选中的列表项索引
        """
        element = self._get_element()
        return element.selected_index()

    def get_all_items(self) -> List[str]:
        """
        获取所有列表项

        Returns:
            列表项文本列表
        """
        element = self._get_element()
        items = []

        try:
            count = element.item_count()
            for i in range(count):
                try:
                    item_text = element.item(i)
                    items.append(item_text)
                except Exception:
                    break
        except Exception:
            pass

        return items

    def item_count(self) -> int:
        """
        获取列表项数量

        Returns:
            列表项数量
        """
        element = self._get_element()
        return element.item_count()

    def item_exists(self, text: str) -> bool:
        """
        检查列表项是否存在

        Args:
            text: 列表项文本

        Returns:
            bool: 是否存在
        """
        items = self.get_all_items()
        return text in items

    def get_item_index(self, text: str) -> int:
        """
        获取列表项的索引

        Args:
            text: 列表项文本

        Returns:
            列表项索引，不存在返回 -1
        """
        items = self.get_all_items()
        try:
            return items.index(text)
        except ValueError:
            return -1

    def double_click_item(self, text: str) -> "ListBox":
        """
        双击列表项

        Args:
            text: 列表项文本

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        index = self.get_item_index(text)

        if index >= 0:
            try:
                element.item(index).double_click_input()
            except Exception:
                pass

        return self

    def right_click_item(self, text: str) -> "ListBox":
        """
        右键点击列表项

        Args:
            text: 列表项文本

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        index = self.get_item_index(text)

        if index >= 0:
            try:
                element.item(index).right_click_input()
            except Exception:
                pass

        return self

    def scroll_to_item(self, text: str) -> "ListBox":
        """
        滚动到列表项

        Args:
            text: 列表项文本

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        index = self.get_item_index(text)

        if index >= 0:
            try:
                # pywinauto 会自动滚动到可见区域
                element.item(index).click_input()
            except Exception:
                pass

        return self

    def is_multiselect(self) -> bool:
        """
        检查是否支持多选

        Returns:
            bool: 是否支持多选
        """
        element = self._get_element()

        try:
            # 检查列表框的扩展样式
            return element.has_style(0x0008)  # LBS_EXTENDEDSEL
        except Exception:
            return False

    def get_selected_items(self) -> List[str]:
        """
        获取所有选中的列表项

        Returns:
            选中的列表项文本列表
        """
        element = self._get_element()
        selected = []

        try:
            count = element.item_count()
            for i in range(count):
                try:
                    item = element.item(i)
                    if item.is_selected():
                        selected.append(item.text())
                except Exception:
                    continue
        except Exception:
            pass

        return selected

    @property
    def selected_text(self) -> str:
        """获取选中的列表项文本"""
        return self.get_selected()

    @property
    def selected_index(self) -> int:
        """获取选中的列表项索引"""
        return self.get_selected_index()

    @property
    def items(self) -> List[str]:
        """获取所有列表项"""
        return self.get_all_items()

    @property
    def count(self) -> int:
        """获取列表项数量"""
        return self.item_count()
