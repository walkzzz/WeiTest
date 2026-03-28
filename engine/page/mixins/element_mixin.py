"""Element Mixin - handles element location and waiting"""

from typing import Any, List, Literal, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from core.finder.locator import Locator


WaitConditionType = Literal["exists", "visible", "enabled", "clickable"]


class ElementMixin:
    """
    元素定位 Mixin

    职责：元素的查找和等待
    """

    _window = None  # 从 ApplicationMixin 继承

    def find_element(self, locator: "Locator") -> Any:
        """
        查找单个元素

        Args:
            locator: 定位器

        Returns:
            元素实例
        """
        if not self._window:
            raise RuntimeError("窗口未初始化")

        from core.finder.search_engine import SearchEngine

        search_engine = SearchEngine(self._window)
        return search_engine.find(locator)

    def find_elements(self, locator: "Locator") -> List[Any]:
        """
        查找多个元素

        Args:
            locator: 定位器

        Returns:
            元素列表
        """
        if not self._window:
            raise RuntimeError("窗口未初始化")

        from core.finder.search_engine import SearchEngine

        search_engine = SearchEngine(self._window)
        return search_engine.find_all(locator)

    def wait_element(
        self,
        locator: "Locator",
        condition: Optional[WaitConditionType] = None,
        timeout: int = 10,
    ) -> Any:
        """
        等待元素满足条件

        Args:
            locator: 定位器
            condition: 等待条件类型 (exists/visible/enabled/clickable)
            timeout: 超时时间

        Returns:
            元素实例
        """
        from core.waiter.smart_wait import SmartWait
        from core.waiter.wait_condition import (
            VisibleCondition,
            EnabledCondition,
            ExistsCondition,
            ClickableCondition,
        )
        from core.finder.search_engine import SearchEngine

        if not self._window:
            raise RuntimeError("窗口未初始化")

        # 映射条件类型
        condition_map = {
            "visible": VisibleCondition,
            "enabled": EnabledCondition,
            "exists": ExistsCondition,
            "clickable": ClickableCondition,
        }

        # 默认使用 visible
        if condition is None or condition not in condition_map:
            condition = "visible"

        condition_class = condition_map[condition]

        # 创建搜索引擎和等待器
        search_engine = SearchEngine(self._window)
        waiter = SmartWait(timeout=timeout)

        # 等待元素
        return waiter.wait_for_element(locator, search_engine, timeout)

    def element_exists(self, locator: "Locator", timeout: int = 0) -> bool:
        """
        检查元素是否存在

        Args:
            locator: 定位器
            timeout: 超时时间（0=立即检查）

        Returns:
            bool: 元素是否存在
        """
        if not self._window:
            raise RuntimeError("窗口未初始化")

        from core.finder.search_engine import SearchEngine

        search_engine = SearchEngine(self._window)
        return search_engine.exists(locator, timeout)
