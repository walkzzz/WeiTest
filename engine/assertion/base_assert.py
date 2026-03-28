"""Base Assertion - assertion base classes"""

from typing import Any
from abc import ABC, abstractmethod


class AssertionResult:
    """断言结果"""

    def __init__(self, passed: bool, message: str = ""):
        self.passed = passed
        self.message = message

    def __bool__(self):
        return self.passed

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status}: {self.message}"


class BaseAssertion(ABC):
    """
    断言基类

    所有断言必须继承此类
    """

    def __init__(self, actual: Any, description: str = ""):
        """
        初始化断言

        Args:
            actual: 实际值
            description: 描述信息
        """
        self.actual = actual
        self.description = description

    @abstractmethod
    def verify(self) -> AssertionResult:
        """执行验证"""
        pass

    def assert_true(self, message: str = "断言失败") -> AssertionResult:
        """断言为真"""
        return AssertionResult(bool(self.actual), message)

    def assert_false(self, message: str = "断言应为假") -> AssertionResult:
        """断言为假"""
        return AssertionResult(not bool(self.actual), message)

    def assert_equal(self, expected: Any) -> AssertionResult:
        """断言相等"""
        passed = self.actual == expected
        return AssertionResult(passed, f"期望：{expected}, 实际：{self.actual}")

    def assert_not_equal(self, expected: Any) -> AssertionResult:
        """断言不相等"""
        passed = self.actual != expected
        return AssertionResult(passed, f"不应等于：{expected}")

    def assert_contains(self, expected: Any) -> AssertionResult:
        """断言包含"""
        passed = expected in self.actual
        return AssertionResult(passed, f"应包含：{expected}, 实际：{self.actual}")
