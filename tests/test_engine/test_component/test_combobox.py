"""ComboBox 组件完整测试"""

import pytest
from unittest.mock import Mock
from engine.component.combobox import ComboBox
from core.finder.locator import ByID


class TestComboBox:
    """ComboBox 组件测试"""

    @pytest.fixture
    def mock_page(self):
        return Mock()

    @pytest.fixture
    def combobox(self, mock_page):
        locator = ByID("combo_test")
        return ComboBox(mock_page, locator)

    def test_select(self, combobox, mock_page):
        """测试选择选项"""
        combobox.select("option1")
        assert mock_page.select_combo_item.called

    def test_select_by_index(self, combobox, mock_page):
        """测试按索引选择"""
        combobox.select_by_index(0)
        assert mock_page.select_combo_item_by_index.called

    def test_select_by_value(self, combobox, mock_page):
        """测试按值选择"""
        combobox.select_by_value("value1")
        assert mock_page.select_combo_item_by_value.called

    def test_options(self, combobox, mock_page):
        """测试获取选项列表"""
        mock_page.get_combo_items.return_value = ["opt1", "opt2"]
        result = combobox.options
        assert len(result) == 2

    def test_selected_value(self, combobox, mock_page):
        """测试获取已选值"""
        mock_page.get_selected_combo_item.return_value = "selected"
        result = combobox.selected_value
        assert result == "selected"

    def test_selected_index(self, combobox, mock_page):
        """测试获取已选索引"""
        mock_page.get_selected_combo_index.return_value = 2
        result = combobox.selected_index
        assert result == 2

    def test_is_enabled(self, combobox, mock_page):
        """测试检查可用状态"""
        mock_page.is_control_enabled.return_value = True
        result = combobox.is_enabled()
        assert result is True

    def test_wait_for_option(self, combobox, mock_page):
        """测试等待选项"""
        result = combobox.wait_for_option("option1", timeout=5)
        assert result is combobox
