"""ProgressBar Component - encapsulates progress bar operations"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class ProgressBar:
    """
    进度条组件

    封装进度条控件的所有操作

    使用示例：
        >>> progress = ProgressBar(page, ByID("prog_download"))
        >>> progress.get_value()
        >>> progress.wait_complete()
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化进度条组件

        Args:
            page: 页面对象
            locator: 进度条定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def get_value(self) -> int:
        """
        获取当前进度值（0-100）

        Returns:
            进度百分比
        """
        element = self._get_element()

        # 尝试获取 RangeValue 模式
        try:
            value = element.get_value()
            return int(value)
        except:
            pass

        # 如果无法直接获取，尝试从文本解析
        try:
            text = element.window_text()
            # 解析 "50%" 或 "50/100" 格式
            if "%" in text:
                return int(text.replace("%", "").strip())
        except:
            pass

        return 0

    def get_min_value(self) -> int:
        """获取最小值"""
        return 0

    def get_max_value(self) -> int:
        """获取最大值"""
        return 100

    def is_complete(self) -> bool:
        """
        检查进度是否完成

        Returns:
            bool: 是否完成
        """
        return self.get_value() >= self.get_max_value()

    def wait_complete(self, timeout: int = 60) -> bool:
        """
        等待进度完成

        Args:
            timeout: 超时时间（秒）

        Returns:
            bool: 是否完成
        """
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.is_complete():
                return True
            time.sleep(0.5)

        return False

    def wait_progress(self, target: int, timeout: int = 30) -> bool:
        """
        等待进度达到指定值

        Args:
            target: 目标进度值
            timeout: 超时时间（秒）

        Returns:
            bool: 是否达到目标
        """
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.get_value() >= target:
                return True
            time.sleep(0.5)

        return False

    @property
    def is_visible(self) -> bool:
        """检查进度条是否可见"""
        return self._get_element().is_visible()

    @property
    def is_enabled(self) -> bool:
        """检查进度条是否可用"""
        return self._get_element().is_enabled()
