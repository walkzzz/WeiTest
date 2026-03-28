"""Element Search Engine - responsible for finding elements in windows"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.driver.window import WindowDriver
    from core.finder.locator import Locator


class SearchEngine:
    """
    元素搜索引擎

    负责在窗口中查找元素，提供智能重试机制

    Example:
        >>> engine = SearchEngine(window)
        >>> element = engine.find(ByID("btn_login"))
        >>> elements = engine.find_all(ByClassName("Edit"))
    """

    def __init__(self, window: "WindowDriver", timeout: int = 10):
        """
        初始化搜索引擎

        Args:
            window: 窗口驱动器
            timeout: 默认超时时间（秒）
        """
        self.window = window
        self.timeout = timeout

    def find(self, locator: "Locator", timeout: Optional[int] = None) -> any:
        """
        查找单个元素

        Args:
            locator: 定位器
            timeout: 自定义超时时间（可选）

        Returns:
            ElementWrapper 实例

        Raises:
            ElementNotFoundError: 未找到元素时抛出
        """
        from core.finder.strategies import StrategyRegistry
        from core.exceptions import ElementNotFoundError

        # Get the pywinauto window
        pw_window = self.window._get_pywinauto_window()

        # Get appropriate strategy
        strategy = StrategyRegistry.get(locator.type.value)

        # Execute search
        try:
            control_type = locator.control_type
            child_window_kwargs = {}

            # Map locator type to pywinauto parameters
            if locator.type.value == "id":
                child_window_kwargs["auto_id"] = locator.value
            elif locator.type.value == "name":
                child_window_kwargs["title"] = locator.value
            elif locator.type.value == "class_name":
                child_window_kwargs["class_name"] = locator.value
            elif locator.type.value == "automation_id":
                child_window_kwargs["auto_id"] = locator.value
            elif locator.type.value == "control_type":
                child_window_kwargs["control_type"] = locator.value

            if control_type:
                child_window_kwargs["control_type"] = control_type

            element = pw_window.child_window(**child_window_kwargs)
            return element
        except Exception as e:
            raise ElementNotFoundError(locator.type.value, locator.value, timeout or self.timeout)

    def find_all(self, locator: "Locator") -> List:
        """
        查找多个元素

        Args:
            locator: 定位器

        Returns:
            ElementWrapper 列表
        """
        pw_window = self.window._get_pywinauto_window()

        # Map locator type to pywinauto parameters
        if locator.type.value == "class_name":
            return pw_window.children(class_name=locator.value)
        elif locator.type.value == "control_type":
            return pw_window.children(control_type=locator.value)
        elif locator.type.value == "name":
            return pw_window.children(title=locator.value)
        else:
            # For other types, return single element in list
            element = self.find(locator)
            return [element] if element else []

    def exists(self, locator: "Locator", timeout: int = 0) -> bool:
        """
        检查元素是否存在

        Args:
            locator: 定位器
            timeout: 超时时间（0=立即检查）

        Returns:
            bool: 元素是否存在
        """
        try:
            element = self.find(locator, timeout)
            return element.exists() if hasattr(element, "exists") else True
        except:
            return False
