"""Label 组件完整测试"""

import pytest
from unittest.mock import Mock
from engine.component.label import Label
from core.finder.locator import ByID


class TestLabel:
    """Label 组件测试"""

    @pytest.fixture
    def mock_page(self):
        return Mock()

    @pytest.fixture
    def label(self, mock_page):
        locator = ByID("lbl_test")
        return Label(mock_page, locator)

    def test_text(self, label, mock_page):
        """测试获取文本"""
        mock_page.get_control_text.return_value = "Label Text"
        result = label.text
        assert result == "Label Text"

    def test_get_text(self, label, mock_page):
        """测试获取文本方法"""
        mock_page.get_control_text.return_value = "Label Text"
        result = label.get_text()
        assert result == "Label Text"

    def test_is_enabled(self, label, mock_page):
        """测试检查可用状态"""
        mock_page.is_control_enabled.return_value = True
        result = label.is_enabled()
        assert result is True

    def test_is_visible(self, label, mock_page):
        """测试检查可见状态"""
        mock_page.is_control_visible.return_value = True
        result = label.is_visible()
        assert result is True

    def test_is_ready(self, label, mock_page):
        """测试检查就绪状态"""
        mock_page.is_control_enabled.return_value = True
        mock_page.is_control_visible.return_value = True
        result = label.is_ready()
        assert result is True
