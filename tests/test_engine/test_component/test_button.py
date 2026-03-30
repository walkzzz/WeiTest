"""Tests for Button component"""

import pytest
from unittest.mock import Mock
from engine.component.button import Button


class TestButton:
    """测试 Button 组件"""

    @pytest.fixture
    def mock_page(self):
        """模拟页面对象"""
        page = Mock()
        page.find_element = Mock()
        return page

    @pytest.fixture
    def mock_element(self):
        """模拟元素"""
        element = Mock()
        element.window_text.return_value = "按钮文本"
        element.is_enabled.return_value = True
        element.is_visible.return_value = True
        return element

    def test_button_init(self, mock_page):
        """测试按钮初始化"""
        from core.finder.locator import ByID

        locator = ByID("btn_test")
        button = Button(mock_page, locator)

        assert button.page is mock_page
        assert button.locator is locator
        assert button._element is None

    def test_button_click(self, mock_page, mock_element):
        """测试按钮点击"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))
        result = button.click()

        mock_element.click_input.assert_called_once()
        assert result is button  # 链式调用

    def test_button_double_click(self, mock_page, mock_element):
        """测试双击按钮"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))
        result = button.double_click()

        mock_element.double_click_input.assert_called_once()
        assert result is button

    def test_button_wait_clickable(self, mock_page, mock_element):
        """测试等待按钮可点击"""
        mock_page.find_element.return_value = mock_element
        mock_page.wait_element = Mock()

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))
        result = button.wait_clickable(timeout=10)

        mock_page.wait_element.assert_called_once()
        assert result is button

    def test_button_text_property(self, mock_page, mock_element):
        """测试按钮文本属性"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))

        text = button.text
        assert text == "按钮文本"
        mock_element.window_text.assert_called_once()

    def test_button_is_enabled_property(self, mock_page, mock_element):
        """测试按钮可用属性"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))

        enabled = button.is_enabled
        assert enabled is True
        mock_element.is_enabled.assert_called_once()

    def test_button_is_visible_property(self, mock_page, mock_element):
        """测试按钮可见属性"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))

        visible = button.is_visible
        assert visible is True
        mock_element.is_visible.assert_called_once()

    def test_button_is_clickable_property(self, mock_page, mock_element):
        """测试按钮可点击属性"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        button = Button(mock_page, ByID("btn_test"))

        clickable = button.is_clickable
        assert clickable is True
