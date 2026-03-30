"""Waiter 集成测试"""
import pytest
from unittest.mock import Mock
from core.waiter.smart_wait import SmartWait
from core.waiter.wait_condition import (
    ExistsCondition, VisibleCondition, EnabledCondition,
    ClickableCondition, TextCondition, TextContainsCondition
)
from core.waiter.custom_conditions import ConditionBuilder

class TestWaitConditions:
    """等待条件测试"""
    
    @pytest.fixture
    def mock_element(self):
        elem = Mock()
        elem.exists.return_value = True
        elem.is_visible.return_value = True
        elem.is_enabled.return_value = True
        elem.window_text.return_value = "Test Text"
        return elem
    
    def test_exists_condition(self, mock_element):
        cond = ExistsCondition()
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True
    
    def test_visible_condition(self, mock_element):
        cond = VisibleCondition()
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True
    
    def test_enabled_condition(self, mock_element):
        cond = EnabledCondition()
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True
    
    def test_clickable_condition(self, mock_element):
        cond = ClickableCondition()
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True
    
    def test_text_condition(self, mock_element):
        cond = TextCondition("Test Text")
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True
    
    def test_text_contains_condition(self, mock_element):
        cond = TextContainsCondition("Test")
        result = cond.wait_for(mock_element, timeout=1)
        assert result is True

class TestSmartWait:
    """SmartWait 集成测试"""
    
    @pytest.fixture
    def mock_window(self):
        return Mock()
    
    @pytest.fixture
    def waiter(self, mock_window):
        return SmartWait(mock_window)
    
    def test_waiter_creation(self, waiter):
        assert waiter is not None
    
    def test_wait_until(self, waiter):
        cond = Mock()
        cond.wait_for.return_value = True
        result = waiter.wait_until(cond, timeout=1)
        assert result is waiter
    
    def test_wait_visible(self, waiter):
        locator = Mock()
        result = waiter.wait_visible(locator, timeout=1)
        assert result is waiter
    
    def test_wait_exists(self, waiter):
        locator = Mock()
        result = waiter.wait_exists(locator, timeout=1)
        assert result is waiter
    
    def test_wait_clickable(self, waiter):
        locator = Mock()
        result = waiter.wait_clickable(locator, timeout=1)
        assert result is waiter

class TestConditionBuilder:
    """ConditionBuilder 测试"""
    
    def test_builder_creation(self):
        builder = ConditionBuilder()
        assert builder is not None
    
    def test_builder_visible(self):
        builder = ConditionBuilder()
        result = builder.visible()
        assert result is builder
    
    def test_builder_enabled(self):
        builder = ConditionBuilder()
        result = builder.enabled()
        assert result is builder
    
    def test_builder_clickable(self):
        builder = ConditionBuilder()
        result = builder.clickable()
        assert result is builder
    
    def test_builder_build(self):
        builder = ConditionBuilder()
        result = builder.visible().enabled().build()
        assert result is not None
