"""CheckBox 组件完整测试"""

import pytest
from unittest.mock import Mock
from engine.component.checkbox import CheckBox
from core.finder.locator import ByID


class TestCheckBox:
    """CheckBox 组件测试"""

    @pytest.fixture
    def mock_page(self):
        """模拟页面对象"""
        return Mock()

    @pytest.fixture
    def checkbox(self, mock_page):
        """创建 CheckBox 实例"""
        locator = ByID("chk_test")
        return CheckBox(mock_page, locator)

    def test_check(self, checkbox, mock_page):
        """测试勾选操作"""
        checkbox.check()
        assert mock_page.click_checkbox.called

    def test_uncheck(self, checkbox, mock_page):
        """测试取消勾选"""
        checkbox.uncheck()
        assert mock_page.uncheck_checkbox.called

    def test_toggle(self, checkbox, mock_page):
        """测试切换状态"""
        checkbox.toggle()
        assert mock_page.toggle_checkbox.called

    def test_is_checked(self, checkbox, mock_page):
        """测试检查选中状态"""
        mock_page.is_checkbox_checked.return_value = True
        result = checkbox.is_checked()
        assert result is True

    def test_is_checked_false(self, checkbox, mock_page):
        """测试检查未选中状态"""
        mock_page.is_checkbox_checked.return_value = False
        result = checkbox.is_checked()
        assert result is False

    def test_wait_checked(self, checkbox, mock_page):
        """测试等待勾选"""
        result = checkbox.wait_checked(timeout=5)
        assert result is checkbox

    def test_wait_unchecked(self, checkbox, mock_page):
        """测试等待未勾选"""
        result = checkbox.wait_unchecked(timeout=5)
        assert result is checkbox

    def test_is_enabled(self, checkbox, mock_page):
        """测试检查可用状态"""
        mock_page.is_control_enabled.return_value = True
        result = checkbox.is_enabled()
        assert result is True

    def test_is_visible(self, checkbox, mock_page):
        """测试检查可见状态"""
        mock_page.is_control_visible.return_value = True
        result = checkbox.is_visible()
        assert result is True
