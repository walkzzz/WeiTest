"""Window Driver - manages individual window operations"""

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pywinauto.controls.uia_wrapper import UIAWrapper
    from core.finder.locator import Locator
    from core.finder.search_engine import SearchEngine


class WindowDriver:
    """
    窗口驱动器

    负责管理单个窗口的操作

    Example:
        >>> window = app.get_window("Main Window")
        >>> window.maximize()
        >>> element = window.find_element(...)
    """

    def __init__(self, window: "UIAWrapper"):
        """
        初始化窗口驱动器

        Args:
            window: pywinauto 窗口实例
        """
        self._window = window

    # ========== 窗口操作 ==========

    def maximize(self) -> "WindowDriver":
        """最大化窗口"""
        self._window.maximize()
        return self

    def minimize(self) -> "WindowDriver":
        """最小化窗口"""
        self._window.minimize()
        return self

    def restore(self) -> "WindowDriver":
        """恢复窗口"""
        self._window.restore()
        return self

    def close(self) -> "WindowDriver":
        """关闭窗口"""
        self._window.close()
        return self

    # ========== 元素查找（延迟导入，避免循环依赖） ==========

    def find_element(self, locator: "Locator") -> "SearchEngine":
        """
        查找单个元素

        Args:
            locator: 定位器对象

        Returns:
            ElementWrapper 实例
        """
        from core.finder.search_engine import SearchEngine

        search_engine = SearchEngine(self)
        return search_engine.find(locator)

    def find_elements(self, locator: "Locator") -> List:
        """
        查找多个元素

        Args:
            locator: 定位器对象

        Returns:
            ElementWrapper 列表
        """
        from core.finder.search_engine import SearchEngine

        search_engine = SearchEngine(self)
        return search_engine.find_all(locator)

    # ========== 属性访问 ==========

    @property
    def title(self) -> str:
        """获取窗口标题"""
        return self._window.window_text()

    @property
    def is_visible(self) -> bool:
        """检查窗口是否可见"""
        return self._window.is_visible()

    @property
    def is_enabled(self) -> bool:
        """检查窗口是否可用"""
        return self._window.is_enabled()

    # ========== 内部方法 ==========

    def _get_pywinauto_window(self):
        """获取底层 pywinauto 窗口实例（供内部使用）"""
        return self._window
