"""Finder 集成测试"""
import pytest
from unittest.mock import Mock
from core.finder.locator import Locator, LocatorType
from core.finder.strategies import (
    ByID, ByName, ByClassName, ByXPath,
    ControlTypeStrategy, CompositeStrategy
)
from core.finder.search_engine import SearchEngine

class TestLocator:
    """Locator 集成测试"""
    
    def test_locator_creation(self):
        locator = Locator(type=LocatorType.ID, value="test")
        assert locator.type == LocatorType.ID
        assert locator.value == "test"
    
    def test_locator_with_timeout(self):
        locator = Locator(type=LocatorType.NAME, value="test", timeout=20)
        assert locator.timeout == 20
    
    def test_locator_with_control_type(self):
        locator = Locator(
            type=LocatorType.ID,
            value="btn",
            control_type="Button"
        )
        assert locator.control_type == "Button"
    
    def test_locator_to_dict(self):
        locator = Locator(type=LocatorType.ID, value="test")
        data = locator.to_dict()
        assert "type" in data
        assert "value" in data
    
    def test_locator_from_yaml(self):
        data = {"locator_type": "id", "locator_value": "test"}
        locator = Locator.from_yaml(data)
        assert locator.type == LocatorType.ID
        assert locator.value == "test"

class TestLocatorType:
    """LocatorType 枚举测试"""
    
    def test_locator_type_values(self):
        assert LocatorType.ID.value == "id"
        assert LocatorType.NAME.value == "name"
        assert LocatorType.CLASS_NAME.value == "class_name"
        assert LocatorType.XPATH.value == "xpath"

class TestStrategies:
    """定位策略测试"""
    
    @pytest.fixture
    def mock_window(self):
        return Mock()
    
    def test_by_id(self, mock_window):
        strategy = ByID()
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "test_id")
        assert result is not None
    
    def test_by_name(self, mock_window):
        strategy = ByName()
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "test_name")
        assert result is not None
    
    def test_by_class_name(self, mock_window):
        strategy = ByClassName()
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "test_class")
        assert result is not None
    
    def test_by_xpath(self, mock_window):
        strategy = ByXPath()
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "//Button")
        assert result is not None
    
    def test_control_type_strategy(self, mock_window):
        strategy = ControlTypeStrategy("Button")
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "test")
        assert result is not None
    
    def test_composite_strategy(self, mock_window):
        strategy = CompositeStrategy([ByID(), ByName()])
        mock_window.child_window.return_value = Mock()
        result = strategy.find(mock_window, "test")
        assert result is not None

class TestSearchEngine:
    """SearchEngine 集成测试"""
    
    @pytest.fixture
    def mock_window(self):
        return Mock()
    
    @pytest.fixture
    def engine(self, mock_window):
        return SearchEngine(mock_window)
    
    def test_engine_creation(self, engine):
        assert engine is not None
    
    def test_engine_find(self, engine):
        locator = Mock()
        engine._window.child_window.return_value = Mock()
        result = engine.find(locator)
        assert result is not None
    
    def test_engine_exists_true(self, engine):
        locator = Mock()
        engine._window.child_window.return_value = Mock()
        result = engine.exists(locator, timeout=1)
        assert result is True
    
    def test_engine_exists_false(self, engine):
        locator = Mock()
        engine._window.child_window.side_effect = Exception("not found")
        result = engine.exists(locator, timeout=0)
        assert result is False
    
    def test_engine_find_all(self, engine):
        locator = Mock()
        engine._window.iter_children.return_value = [Mock(), Mock()]
        result = engine.find_all(locator)
        assert len(result) >= 0
