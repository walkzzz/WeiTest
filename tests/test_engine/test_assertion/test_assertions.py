"""Tests for UI Assertion"""

import pytest
from unittest.mock import Mock
from engine.assertion.ui_assert import UIAssertion
from engine.assertion.assertion_chain import AssertionChain, Assert


class TestAssertionChain:
    """测试链式断言"""

    def test_assert_that_is_not_none(self):
        """测试不为 None 断言"""
        result = Assert.that("test").is_not_none()
        assert result is not None

    def test_assert_that_is_none_raises(self):
        """测试为 None 抛出异常"""
        with pytest.raises(AssertionError):
            Assert.that(None).is_not_none()

    def test_assert_that_is_not_empty(self):
        """测试不为空断言"""
        result = Assert.that([1, 2, 3]).is_not_empty()
        assert result is not None

    def test_assert_that_is_empty_raises(self):
        """测试为空抛出异常"""
        with pytest.raises(AssertionError):
            Assert.that([]).is_not_empty()

    def test_assert_that_is_equal_to(self):
        """测试相等断言"""
        result = Assert.that(5).is_equal_to(5)
        assert result is not None

    def test_assert_that_not_equal_raises(self):
        """测试不相等抛出异常"""
        with pytest.raises(AssertionError):
            Assert.that(5).is_equal_to(10)

    def test_assert_that_contains(self):
        """测试包含断言"""
        result = Assert.that("hello world").contains("world")
        assert result is not None

    def test_assert_that_not_contains_raises(self):
        """测试不包含抛出异常"""
        with pytest.raises(AssertionError):
            Assert.that("hello").contains("world")

    def test_assert_that_is_true(self):
        """测试为真断言"""
        result = Assert.that(True).is_true()
        assert result is not None

    def test_assert_that_is_false_raises(self):
        """测试为假抛出异常"""
        with pytest.raises(AssertionError):
            Assert.that(False).is_true()

    def test_assert_chain_multiple(self):
        """测试链式断言"""
        result = Assert.that("hello world").is_not_none().is_not_empty().contains("world")
        assert result is not None


class TestAssertThat:
    """测试 Assert.that()"""

    def test_assert_with_description(self):
        """测试带描述的断言"""
        with pytest.raises(AssertionError) as exc_info:
            (Assert.that(None, description="测试值").is_not_none())

        assert "测试值" in str(exc_info.value)
