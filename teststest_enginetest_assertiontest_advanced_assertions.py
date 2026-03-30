"""高级断言完整测试"""

import pytest
from engine.assertion.advanced_assertions import (
    assert_not_none,
    assert_not_empty,
    assert_equal,
    assert_not_equal,
    assert_true,
    assert_false,
    assert_contains,
    assert_not_contains,
    assert_starts_with,
    assert_ends_with,
    assert_greater,
    assert_less,
    assert_between,
    assert_in,
    assert_not_in,
    assert_instance_of,
    assert_raises
)


class TestAdvancedAssertions:
    """高级断言测试"""

    def test_assert_not_none_success(self):
        """测试 assert_not_none 成功"""
        assert_not_none("value", "test")

    def test_assert_not_none_failure(self):
        """测试 assert_not_none 失败"""
        with pytest.raises(AssertionError):
            assert_not_none(None, "test")

    def test_assert_not_empty_success(self):
        """测试 assert_not_empty 成功"""
        assert_not_empty([1, 2, 3], "test")
        assert_not_empty("hello", "test")

    def test_assert_not_empty_failure(self):
        """测试 assert_not_empty 失败"""
        with pytest.raises(AssertionError):
            assert_not_empty([], "test")
        with pytest.raises(AssertionError):
            assert_not_empty("", "test")

    def test_assert_equal_success(self):
        """测试 assert_equal 成功"""
        assert_equal(1, 1, "test")
        assert_equal("a", "a", "test")

    def test_assert_equal_failure(self):
        """测试 assert_equal 失败"""
        with pytest.raises(AssertionError):
            assert_equal(1, 2, "test")

    def test_assert_not_equal_success(self):
        """测试 assert_not_equal 成功"""
        assert_not_equal(1, 2, "test")

    def test_assert_not_equal_failure(self):
        """测试 assert_not_equal 失败"""
        with pytest.raises(AssertionError):
            assert_not_equal(1, 1, "test")

    def test_assert_true_success(self):
        """测试 assert_true 成功"""
        assert_true(True, "test")

    def test_assert_true_failure(self):
        """测试 assert_true 失败"""
        with pytest.raises(AssertionError):
            assert_true(False, "test")

    def test_assert_false_success(self):
        """测试 assert_false 成功"""
        assert_false(False, "test")

    def test_assert_false_failure(self):
        """测试 assert_false 失败"""
        with pytest.raises(AssertionError):
            assert_false(True, "test")

    def test_assert_contains_success(self):
        """测试 assert_contains 成功"""
        assert_contains("hello", "ell", "test")
        assert_contains([1, 2, 3], 2, "test")

    def test_assert_contains_failure(self):
        """测试 assert_contains 失败"""
        with pytest.raises(AssertionError):
            assert_contains("hello", "xyz", "test")

    def test_assert_not_contains_success(self):
        """测试 assert_not_contains 成功"""
        assert_not_contains("hello", "xyz", "test")

    def test_assert_not_contains_failure(self):
        """测试 assert_not_contains 失败"""
        with pytest.raises(AssertionError):
            assert_not_contains("hello", "ell", "test")

    def test_assert_starts_with_success(self):
        """测试 assert_starts_with 成功"""
        assert_starts_with("hello", "he", "test")

    def test_assert_starts_with_failure(self):
        """测试 assert_starts_with 失败"""
        with pytest.raises(AssertionError):
            assert_starts_with("hello", "xy", "test")

    def test_assert_ends_with_success(self):
        """测试 assert_ends_with 成功"""
        assert_ends_with("hello", "lo", "test")

    def test_assert_ends_with_failure(self):
        """测试 assert_ends_with 失败"""
        with pytest.raises(AssertionError):
            assert_ends_with("hello", "xy", "test")

    def test_assert_greater_success(self):
        """测试 assert_greater 成功"""
        assert_greater(5, 3, "test")

    def test_assert_greater_failure(self):
        """测试 assert_greater 失败"""
        with pytest.raises(AssertionError):
            assert_greater(3, 5, "test")

    def test_assert_less_success(self):
        """测试 assert_less 成功"""
        assert_less(3, 5, "test")

    def test_assert_less_failure(self):
        """测试 assert_less 失败"""
        with pytest.raises(AssertionError):
            assert_less(5, 3, "test")

    def test_assert_between_success(self):
        """测试 assert_between 成功"""
        assert_between(5, 1, 10, "test")

    def test_assert_between_failure(self):
        """测试 assert_between 失败"""
        with pytest.raises(AssertionError):
            assert_between(15, 1, 10, "test")

    def test_assert_in_success(self):
        """测试 assert_in 成功"""
        assert_in(1, [1, 2, 3], "test")

    def test_assert_in_failure(self):
        """测试 assert_in 失败"""
        with pytest.raises(AssertionError):
            assert_in(4, [1, 2, 3], "test")

    def test_assert_not_in_success(self):
        """测试 assert_not_in 成功"""
        assert_not_in(4, [1, 2, 3], "test")

    def test_assert_not_in_failure(self):
        """测试 assert_not_in 失败"""
        with pytest.raises(AssertionError):
            assert_not_in(1, [1, 2, 3], "test")

    def test_assert_instance_of_success(self):
        """测试 assert_instance_of 成功"""
        assert_instance_of("hello", str, "test")
        assert_instance_of(123, int, "test")

    def test_assert_instance_of_failure(self):
        """测试 assert_instance_of 失败"""
        with pytest.raises(AssertionError):
            assert_instance_of("hello", int, "test")

    def test_assert_raises_success(self):
        """测试 assert_raises 成功"""
        def raise_error():
            raise ValueError("error")
        assert_raises(ValueError, raise_error, "test")

    def test_assert_raises_failure(self):
        """测试 assert_raises 失败"""
        def no_error():
            pass
        with pytest.raises(AssertionError):
            assert_raises(ValueError, no_error, "test")
