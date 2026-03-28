"""Locator Strategies - different strategies for locating elements"""

from abc import ABC, abstractmethod
from typing import Any


class LocatorStrategy(ABC):
    """定位策略基类"""

    @abstractmethod
    def locate(self, context: Any, value: str) -> Any:
        """
        执行定位

        Args:
            context: 查找上下文（窗口或元素）
            value: 定位值

        Returns:
            控件实例
        """
        pass


class IDStrategy(LocatorStrategy):
    """ID 定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        return context.child_window(auto_id=value)


class NameStrategy(LocatorStrategy):
    """名称定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        return context.child_window(title=value)


class ClassNameStrategy(LocatorStrategy):
    """类名定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        return context.child_window(class_name=value)


class AutomationIDStrategy(LocatorStrategy):
    """Automation ID 定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        return context.child_window(auto_id=value)


class XPathStrategy(LocatorStrategy):
    """XPath 定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        # Simplified XPath support
        return context.child_window().child_window(path=value)


class ControlTypeStrategy(LocatorStrategy):
    """控件类型定位策略"""

    def locate(self, context: Any, value: str) -> Any:
        return context.child_window(control_type=value)


# ========== Strategy Registry ==========


class StrategyRegistry:
    """策略注册表"""

    _strategies = {
        "id": IDStrategy(),
        "name": NameStrategy(),
        "class_name": ClassNameStrategy(),
        "automation_id": AutomationIDStrategy(),
        "xpath": XPathStrategy(),
        "control_type": ControlTypeStrategy(),
    }

    @classmethod
    def get(cls, locator_type: str) -> LocatorStrategy:
        """
        获取策略

        Args:
            locator_type: 定位类型

        Returns:
            LocatorStrategy 实例

        Raises:
            ValueError: 策略不存在时抛出
        """
        if locator_type not in cls._strategies:
            raise ValueError(f"未找到定位策略：{locator_type}")
        return cls._strategies[locator_type]

    @classmethod
    def register(cls, locator_type: str, strategy: LocatorStrategy):
        """
        注册策略

        Args:
            locator_type: 定位类型
            strategy: 策略实例
        """
        cls._strategies[locator_type] = strategy
