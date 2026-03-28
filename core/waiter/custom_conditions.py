"""Custom Wait Conditions - advanced waiting conditions with customization support"""

from typing import Any, Callable, Pattern
import re
from core.waiter.wait_condition import WaitCondition


class CustomWaitCondition(WaitCondition):
    """
    自定义等待条件

    通过传入谓词函数来自定义等待条件

    Example:
        >>> def is_data_loaded(element):
        ...     return "loading" not in element.text().lower()
        >>> condition = CustomWaitCondition(is_data_loaded)
        >>> SmartWait.wait_for_condition(condition, element, timeout=30)
    """

    def __init__(self, predicate: Callable[[Any], bool], description: str = "") -> None:
        """
        初始化自定义等待条件

        Args:
            predicate: 谓词函数，接收元素返回 bool
            description: 条件描述
        """
        self.predicate = predicate
        self.description = description

    def check(self, element: Any) -> bool:
        """
        检查条件是否满足

        Args:
            element: 元素实例

        Returns:
            bool: 条件是否满足
        """
        return self.predicate(element)


class TextContainsCondition(WaitCondition):
    """
    文本包含条件

    等待元素文本包含指定字符串
    """

    def __init__(self, expected_text: str) -> None:
        """
        初始化

        Args:
            expected_text: 期望包含的文本
        """
        self.expected_text = expected_text

    def check(self, element: Any) -> bool:
        """检查元素文本是否包含期望文本"""
        if hasattr(element, "window_text"):
            actual_text = element.window_text()
            return self.expected_text in actual_text
        return False


class TextMatchesCondition(WaitCondition):
    """
    文本正则匹配条件

    等待元素文本匹配正则表达式
    """

    def __init__(self, pattern: str) -> None:
        """
        初始化

        Args:
            pattern: 正则表达式模式
        """
        self.pattern: Pattern[str] = re.compile(pattern)

    def check(self, element: Any) -> bool:
        """检查元素文本是否匹配正则表达式"""
        if hasattr(element, "window_text"):
            actual_text = element.window_text()
            return bool(self.pattern.match(actual_text))
        return False


class AttributeEqualsCondition(WaitCondition):
    """
    属性等于条件

    等待元素属性等于指定值
    """

    def __init__(self, name: str, value: str) -> None:
        """
        初始化

        Args:
            name: 属性名
            value: 属性值
        """
        self.name = name
        self.value = value

    def check(self, element: Any) -> bool:
        """检查元素属性是否等于期望值"""
        if hasattr(element, "get_element_info"):
            info = element.get_element_info()
            if hasattr(info, self.name):
                return getattr(info, self.name) == self.value
        return False


class StyleContainsCondition(WaitCondition):
    """
    样式包含条件

    等待元素样式包含指定值
    """

    def __init__(self, property_name: str, value: str) -> None:
        """
        初始化

        Args:
            property_name: 样式属性名
            value: 样式值
        """
        self.property_name = property_name
        self.value = value

    def check(self, element: Any) -> bool:
        """检查元素样式是否包含期望值"""
        if hasattr(element, "get_style"):
            try:
                style_value = element.get_style(self.property_name)
                return self.value in style_value
            except Exception:
                return False
        return False


class WaitConditions:
    """
    等待条件工厂

    提供便捷的等待条件创建方法

    Example:
        >>> condition = WaitConditions.text_contains("完成")
        >>> condition = WaitConditions.text_matches(r"\\d+ 条记录")
        >>> condition = WaitConditions.attribute_equals("AutomationId", "btn_submit")
    """

    @staticmethod
    def text_contains(expected: str) -> WaitCondition:
        """
        创建文本包含条件

        Args:
            expected: 期望包含的文本

        Returns:
            WaitCondition 实例
        """
        return TextContainsCondition(expected)

    @staticmethod
    def text_matches(pattern: str) -> WaitCondition:
        """
        创建文本正则匹配条件

        Args:
            pattern: 正则表达式模式

        Returns:
            WaitCondition 实例
        """
        return TextMatchesCondition(pattern)

    @staticmethod
    def attribute_equals(name: str, value: str) -> WaitCondition:
        """
        创建属性等于条件

        Args:
            name: 属性名
            value: 属性值

        Returns:
            WaitCondition 实例
        """
        return AttributeEqualsCondition(name, value)

    @staticmethod
    def style_contains(property_name: str, value: str) -> WaitCondition:
        """
        创建样式包含条件

        Args:
            property_name: 样式属性名
            value: 样式值

        Returns:
            WaitCondition 实例
        """
        return StyleContainsCondition(property_name, value)

    @staticmethod
    def custom(predicate: Callable[[Any], bool], description: str = "") -> WaitCondition:
        """
        创建自定义等待条件

        Args:
            predicate: 谓词函数
            description: 条件描述

        Returns:
            WaitCondition 实例
        """
        return CustomWaitCondition(predicate, description)
