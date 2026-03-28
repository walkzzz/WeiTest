"""Tests for Waiter module"""

import pytest
from unittest.mock import Mock
from core.waiter.wait_condition import (
    WaitConditionType,
    ExistsCondition,
    VisibleCondition,
    EnabledCondition,
    ClickableCondition,
    TextMatchCondition,
    TextContainsCondition,
)
from core.waiter.smart_wait import SmartWait


class TestWaitConditions:
    """测试等待条件"""

    def test_exists_condition_true(self):
        """测试存在条件（存在）"""
        mock_element = Mock()
        mock_element.exists.return_value = True

        condition = ExistsCondition()
        assert condition.check(mock_element) is True

    def test_exists_condition_false(self):
        """测试存在条件（不存在）"""
        mock_element = Mock()
        mock_element.exists.return_value = False

        condition = ExistsCondition()
        assert condition.check(mock_element) is False

    def test_visible_condition(self):
        """测试可见条件"""
        mock_element = Mock()
        mock_element.is_visible.return_value = True

        condition = VisibleCondition()
        assert condition.check(mock_element) is True

    def test_enabled_condition(self):
        """测试可用条件"""
        mock_element = Mock()
        mock_element.is_enabled.return_value = True

        condition = EnabledCondition()
        assert condition.check(mock_element) is True

    def test_clickable_condition_both_true(self):
        """测试可点击条件（都满足）"""
        mock_element = Mock()
        mock_element.is_visible.return_value = True
        mock_element.is_enabled.return_value = True

        condition = ClickableCondition()
        assert condition.check(mock_element) is True

    def test_clickable_condition_visible_false(self):
        """测试可点击条件（不可见）"""
        mock_element = Mock()
        mock_element.is_visible.return_value = False
        mock_element.is_enabled.return_value = True

        condition = ClickableCondition()
        assert condition.check(mock_element) is False

    def test_clickable_condition_enabled_false(self):
        """测试可点击条件（不可用）"""
        mock_element = Mock()
        mock_element.is_visible.return_value = True
        mock_element.is_enabled.return_value = False

        condition = ClickableCondition()
        assert condition.check(mock_element) is False

    def test_text_match_condition_success(self):
        """测试文本匹配（成功）"""
        mock_element = Mock()
        mock_element.window_text.return_value = "Hello"

        condition = TextMatchCondition("Hello")
        assert condition.check(mock_element) is True

    def test_text_match_condition_failure(self):
        """测试文本匹配（失败）"""
        mock_element = Mock()
        mock_element.window_text.return_value = "Hello"

        condition = TextMatchCondition("World")
        assert condition.check(mock_element) is False

    def test_text_contains_condition_success(self):
        """测试文本包含（成功）"""
        mock_element = Mock()
        mock_element.window_text.return_value = "Hello World"

        condition = TextContainsCondition("World")
        assert condition.check(mock_element) is True

    def test_text_contains_condition_failure(self):
        """测试文本包含（失败）"""
        mock_element = Mock()
        mock_element.window_text.return_value = "Hello"

        condition = TextContainsCondition("World")
        assert condition.check(mock_element) is False


class TestSmartWait:
    """测试智能等待"""

    def test_wait_until_success(self):
        """测试等待成功"""
        waiter = SmartWait(timeout=2, poll_interval=0.1)

        call_count = 0

        def condition():
            nonlocal call_count
            call_count += 1
            return call_count >= 3

        result = waiter.wait_until(condition)
        assert result is True
        assert call_count == 3

    def test_wait_until_timeout(self):
        """测试等待超时"""
        waiter = SmartWait(timeout=0.5, poll_interval=0.1)

        def condition():
            return False

        with pytest.raises(Exception, match="等待条件超时"):
            waiter.wait_until(condition)

    def test_wait_until_custom_timeout(self):
        """测试自定义超时"""
        waiter = SmartWait(timeout=10, poll_interval=0.1)

        def condition():
            return True

        result = waiter.wait_until(condition, timeout=1)
        assert result is True

    def test_wait_for_condition(self):
        """测试等待条件"""
        waiter = SmartWait(timeout=2, poll_interval=0.1)
        mock_element = Mock()
        mock_element.is_visible.return_value = True

        condition = VisibleCondition()
        result = waiter.wait_for_condition(condition, mock_element)
        assert result is True

    def test_wait_for_condition_timeout(self):
        """测试等待条件超时"""
        waiter = SmartWait(timeout=0.5, poll_interval=0.1)
        mock_element = Mock()
        mock_element.is_visible.return_value = False

        condition = VisibleCondition()
        with pytest.raises(Exception):
            waiter.wait_for_condition(condition, mock_element)
