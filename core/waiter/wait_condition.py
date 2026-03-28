"""Wait Conditions - conditions for waiting on elements"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class WaitConditionType(Enum):
    """等待条件类型"""

    EXISTS = "exists"
    VISIBLE = "visible"
    ENABLED = "enabled"
    CLICKABLE = "clickable"
    EDITABLE = "editable"
    TEXT_MATCH = "text_match"
    TEXT_CONTAINS = "text_contains"


class WaitCondition(ABC):
    """等待条件基类"""

    @abstractmethod
    def check(self, element: Any) -> bool:
        """
        检查条件是否满足

        Args:
            element: 元素实例

        Returns:
            bool: 条件是否满足
        """
        pass


class ExistsCondition(WaitCondition):
    """存在条件"""

    def check(self, element: Any) -> bool:
        if hasattr(element, "exists"):
            return element.exists()
        return element is not None


class VisibleCondition(WaitCondition):
    """可见条件"""

    def check(self, element: Any) -> bool:
        if hasattr(element, "is_visible"):
            return element.is_visible()
        return True


class EnabledCondition(WaitCondition):
    """可用条件"""

    def check(self, element: Any) -> bool:
        if hasattr(element, "is_enabled"):
            return element.is_enabled()
        return True


class ClickableCondition(WaitCondition):
    """可点击条件（可见 + 可用）"""

    def check(self, element: Any) -> bool:
        visible = True
        enabled = True

        if hasattr(element, "is_visible"):
            visible = element.is_visible()
        if hasattr(element, "is_enabled"):
            enabled = element.is_enabled()

        return visible and enabled


class TextMatchCondition(WaitCondition):
    """文本匹配条件"""

    def __init__(self, expected_text: str):
        self.expected_text = expected_text

    def check(self, element: Any) -> bool:
        if hasattr(element, "window_text"):
            actual_text = element.window_text()
            return actual_text == self.expected_text
        return False


class TextContainsCondition(WaitCondition):
    """文本包含条件"""

    def __init__(self, expected_text: str):
        self.expected_text = expected_text

    def check(self, element: Any) -> bool:
        if hasattr(element, "window_text"):
            actual_text = element.window_text()
            return self.expected_text in actual_text
        return False
