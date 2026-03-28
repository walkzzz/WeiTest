"""Smart Wait - intelligent waiting mechanism"""

import time
from typing import Callable, Optional, Any


class SmartWait:
    """
    智能等待器

    提供智能轮询等待机制，支持自定义条件和超时

    Example:
        >>> waiter = SmartWait(timeout=10, poll_interval=0.5)
        >>> waiter.wait_until(element.is_visible)
        >>> waiter.wait_for_condition(VisibleCondition(), element)
    """

    def __init__(self, timeout: int = 10, poll_interval: float = 0.5):
        """
        初始化智能等待器

        Args:
            timeout: 超时时间（秒）
            poll_interval: 轮询间隔（秒）
        """
        self.timeout = timeout
        self.poll_interval = poll_interval

    def wait_until(
        self,
        condition: Callable[[], bool],
        timeout: Optional[int] = None,
        error_message: str = "等待条件超时",
    ) -> bool:
        """
        等待直到条件满足

        Args:
            condition: 条件函数（返回 bool）
            timeout: 自定义超时时间（可选）
            error_message: 超时错误消息

        Returns:
            bool: 条件是否满足

        Raises:
            Exception: 超时后抛出
        """
        timeout = timeout or self.timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                if condition():
                    return True
            except Exception:
                pass  # 继续轮询

            time.sleep(self.poll_interval)

        # 最后一次尝试
        try:
            if condition():
                return True
        except Exception:
            pass

        raise Exception(f"{error_message} (timeout={timeout}s)")

    def wait_for_condition(
        self, condition: "WaitCondition", element: Any, timeout: Optional[int] = None
    ) -> bool:
        """
        等待特定条件

        Args:
            condition: WaitCondition 实例
            element: 元素实例
            timeout: 自定义超时时间

        Returns:
            bool: 条件是否满足
        """

        def check():
            return condition.check(element)

        return self.wait_until(check, timeout, f"等待条件 {condition.__class__.__name__} 超时")

    def wait_for_element(
        self, locator: "Locator", search_engine: "SearchEngine", timeout: Optional[int] = None
    ) -> Any:
        """
        等待元素出现

        Args:
            locator: 定位器
            search_engine: 搜索引擎
            timeout: 自定义超时时间

        Returns:
            元素实例

        Raises:
            Exception: 超时后抛出
        """

        def check():
            try:
                element = search_engine.find(locator, timeout=0)
                return element is not None
            except:
                return False

        result = self.wait_until(check, timeout, f"等待元素 {locator.value} 出现超时")

        if result:
            return search_engine.find(locator, timeout=0)
        else:
            raise Exception(f"元素未找到：{locator.value}")
