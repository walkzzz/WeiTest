"""Tests for TextInput component"""

import pytest
from unittest.mock import Mock
from engine.component.input import TextInput


class TestTextInput:
    """测试 TextInput 组件"""

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
        element.window_text.return_value = "测试文本"
        element.is_enabled.return_value = True
        return element

    def test_input_init(self, mock_page):
        """测试输入框初始化"""
        from core.finder.locator import ByID

        locator = ByID("txt_test")
        input_box = TextInput(mock_page, locator)

        assert input_box.page is mock_page
        assert input_box.locator is locator

    def test_input_type(self, mock_page, mock_element):
        """测试输入文本"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        input_box = TextInput(mock_page, ByID("txt_test"))
        result = input_box.type("测试内容")

        mock_element.type_keys.assert_called_once()
        assert result is input_box

    def test_input_clear(self, mock_page, mock_element):
        """测试清空输入框"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        input_box = TextInput(mock_page, ByID("txt_test"))
        result = input_box.clear()

        assert mock_element.click_input.called
        assert mock_element.select.called
        assert mock_element.type_keys.called
        assert result is input_box

    def test_input_set_value(self, mock_page, mock_element):
        """测试设置值"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        input_box = TextInput(mock_page, ByID("txt_test"))
        result = input_box.set_value("新值")

        assert result is input_box

    def test_input_value_property(self, mock_page, mock_element):
        """测试获取值"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        input_box = TextInput(mock_page, ByID("txt_test"))

        value = input_box.value
        assert value == "测试文本"

    def test_input_is_editable_property(self, mock_page, mock_element):
        """测试可编辑属性"""
        mock_page.find_element.return_value = mock_element

        from core.finder.locator import ByID

        input_box = TextInput(mock_page, ByID("txt_test"))

        editable = input_box.is_editable
        assert editable is True
