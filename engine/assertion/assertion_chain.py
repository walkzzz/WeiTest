"""Assertion Chain - fluent chain assertions"""

from typing import Any


class AssertionChain:
    """
    链式断言

    支持流畅的链式断言语法

    使用示例：
        >>> (Assert.that(login_page.get_title())
        ...     .is_not_none()
        ...     .contains("Login")
        ...     .is_not_empty())
    """

    def __init__(self, actual: Any, description: str = ""):
        self.actual = actual
        self.description = description

    def is_not_none(self) -> "AssertionChain":
        """断言不为 None"""
        if self.actual is None:
            raise AssertionError(f"{self.description} 不应为 None")
        return self

    def is_not_empty(self) -> "AssertionChain":
        """断言不为空"""
        if not self.actual:
            raise AssertionError(f"{self.description} 不应为空")
        return self

    def is_equal_to(self, expected: Any) -> "AssertionChain":
        """断言相等"""
        if self.actual != expected:
            raise AssertionError(f"{self.description} 期望：{expected}, 实际：{self.actual}")
        return self

    def contains(self, expected: Any) -> "AssertionChain":
        """断言包含"""
        if expected not in self.actual:
            raise AssertionError(f"{self.description} 应包含 {expected}")
        return self

    def is_true(self) -> "AssertionChain":
        """断言为真"""
        if not self.actual:
            raise AssertionError(f"{self.description} 应为 True")
        return self

    def is_false(self) -> "AssertionChain":
        """断言为假"""
        if self.actual:
            raise AssertionError(f"{self.description} 应为 False")
        return self

    def starts_with(self, prefix: str) -> "AssertionChain":
        """断言字符串以指定前缀开头"""
        if not isinstance(self.actual, str):
            raise AssertionError(f"{self.description} 应为字符串类型")
        if not self.actual.startswith(prefix):
            raise AssertionError(f"{self.description} 应以 '{prefix}' 开头，实际：'{self.actual}'")
        return self

    def ends_with(self, suffix: str) -> "AssertionChain":
        """断言字符串以指定后缀结尾"""
        if not isinstance(self.actual, str):
            raise AssertionError(f"{self.description} 应为字符串类型")
        if not self.actual.endswith(suffix):
            raise AssertionError(f"{self.description} 应以 '{suffix}' 结尾，实际：'{self.actual}'")
        return self

    def length_greater_than(self, length: int) -> "AssertionChain":
        """断言长度大于指定值"""
        actual_length = len(self.actual)
        if actual_length <= length:
            raise AssertionError(f"{self.description} 长度应大于 {length}，实际：{actual_length}")
        return self

    def length_less_than(self, length: int) -> "AssertionChain":
        """断言长度小于指定值"""
        actual_length = len(self.actual)
        if actual_length >= length:
            raise AssertionError(f"{self.description} 长度应小于 {length}，实际：{actual_length}")
        return self

    def matches(self, pattern: Any) -> "AssertionChain":
        """断言匹配正则表达式"""
        import re

        if not isinstance(self.actual, str):
            raise AssertionError(f"{self.description} 应为字符串类型")
        if not re.search(pattern, self.actual):
            raise AssertionError(
                f"{self.description} 应匹配模式 '{pattern}'，实际：'{self.actual}'"
            )
        return self


# ========== Fluent API Entry Point ==========


class Assert:
    """断言快捷入口"""

    @staticmethod
    def that(actual: Any, description: str = "") -> AssertionChain:
        """创建断言链"""
        return AssertionChain(actual, description)

    @staticmethod
    def ui(page: "BasePage", locator: "Locator"):
        """创建 UI 断言"""
        from engine.assertion.ui_assert import UIAssertion

        return UIAssertion(page, locator)
