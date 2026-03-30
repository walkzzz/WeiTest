"""TabControl Component - encapsulates tab control operations"""

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from wei.engine.page.base_page import BasePage


class TabControl:
    """
    选项卡控件组件

    封装选项卡的所有操作

    Example:
        >>> tab = TabControl(page, ByID("tab_main"))
        >>> tab.select_tab(0)  # 选择第一个选项卡
        >>> tab.select_tab("Settings")  # 选择名为 Settings 的选项卡
        >>> current = tab.get_selected_tab()
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化选项卡控件

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

    def select_tab(self, index_or_name: Any) -> "TabControl":
        """
        选择选项卡

        Args:
            index_or_name: 选项卡索引 (int) 或名称 (str)

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        if isinstance(index_or_name, int):
            # 按索引选择
            element.select(index_or_name)
        else:
            # 按名称选择
            element.select(index_or_name)

        return self

    def get_selected_tab(self) -> str:
        """
        获取选中的选项卡名称

        Returns:
            选项卡名称
        """
        element = self._get_element()
        return element.selected_tab()

    def get_selected_index(self) -> int:
        """
        获取选中的选项卡索引

        Returns:
            选项卡索引
        """
        element = self._get_element()
        return element.selected_index()

    def get_tab_count(self) -> int:
        """
        获取选项卡数量

        Returns:
            选项卡数量
        """
        element = self._get_element()
        return element.item_count()

    def tab_exists(self, name: str) -> bool:
        """
        检查选项卡是否存在

        Args:
            name: 选项卡名称

        Returns:
            bool: 是否存在
        """
        tabs = self.get_all_tabs()
        return name in tabs

    def get_all_tabs(self) -> List[str]:
        """
        获取所有选项卡名称

        Returns:
            选项卡名称列表
        """
        element = self._get_element()
        tabs = []

        count = self.get_tab_count()
        for i in range(count):
            try:
                # 获取选项卡名称
                tab_name = element.item(i)
                tabs.append(tab_name)
            except Exception:
                break

        return tabs

    def get_tab_title(self, index: int) -> str:
        """
        获取指定选项卡的标题

        Args:
            index: 选项卡索引

        Returns:
            选项卡标题
        """
        tabs = self.get_all_tabs()
        if 0 <= index < len(tabs):
            return tabs[index]
        raise IndexError(f"选项卡索引超出范围：{index}")

    def is_tab_enabled(self, index_or_name: Any) -> bool:
        """
        检查选项卡是否可用

        Args:
            index_or_name: 选项卡索引或名称

        Returns:
            bool: 是否可用
        """
        element = self._get_element()

        if isinstance(index_or_name, int):
            # 获取指定索引的选项卡
            tab_item = element.item(index_or_name)
        else:
            tab_item = index_or_name

        # 检查是否启用
        return element.is_enabled()

    def wait_for_tab(self, name: str, timeout: int = 10) -> "TabControl":
        """
        等待选项卡出现

        Args:
            name: 选项卡名称
            timeout: 超时时间

        Returns:
            self: 支持链式调用
        """
        from core.waiter.smart_wait import SmartWait

        def tab_exists() -> bool:
            return name in self.get_all_tabs()

        waiter = SmartWait(timeout=timeout)
        waiter.wait_until(tab_exists, timeout)
        return self

    @property
    def selected_index(self) -> int:
        """获取选中选项卡的索引"""
        return self.get_selected_index()

    @property
    def selected_tab(self) -> str:
        """获取选中选项卡的名称"""
        return self.get_selected_tab()

    @property
    def tab_count(self) -> int:
        """获取选项卡数量"""
        return self.get_tab_count()
