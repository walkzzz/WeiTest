"""ListBox 组件完整测试 - 提升覆盖率"""
import pytest
from unittest.mock import Mock
from engine.component.list_box import ListBox
from core.finder.locator import ByID

class TestListBoxComplete:
    """ListBox 完整测试"""
    
    @pytest.fixture
    def mock_page(self):
        page = Mock()
        page.select_listitem = Mock()
        page.select_listitem_by_index = Mock()
        page.select_listitem_by_value = Mock()
        page.get_listitems = Mock(return_value=["item1", "item2", "item3"])
        page.get_selected_listitem = Mock(return_value="item1")
        page.get_selected_listitem_index = Mock(return_value=0)
        page.get_listitem_count = Mock(return_value=3)
        page.listitem_exists = Mock(return_value=True)
        page.is_listitem_selected = Mock(return_value=True)
        return page
    
    @pytest.fixture
    def list_box(self, mock_page):
        return ListBox(mock_page, ByID("list_test"))
    
    def test_select(self, list_box, mock_page):
        list_box.select("item1")
        assert mock_page.select_listitem.called
    
    def test_select_by_index(self, list_box, mock_page):
        list_box.select_by_index(0)
        assert mock_page.select_listitem_by_index.called
    
    def test_select_multiple(self, list_box, mock_page):
        list_box.select_multiple(["item1", "item2"])
        assert mock_page.select_listitem.called
    
    def test_items(self, list_box, mock_page):
        mock_page.get_listitems.return_value = ["item1", "item2"]
        result = list_box.items
        assert len(result) == 2
    
    def test_selected_item(self, list_box, mock_page):
        mock_page.get_selected_listitem.return_value = "selected"
        result = list_box.selected_item
        assert result == "selected"
    
    def test_selected_items(self, list_box, mock_page):
        mock_page.get_selected_listitem.return_value = "selected"
        result = list_box.selected_items
        assert result is not None
    
    def test_count(self, list_box, mock_page):
        mock_page.get_listitem_count.return_value = 5
        result = list_box.count()
        assert result == 5
    
    def test_item_exists_true(self, list_box, mock_page):
        mock_page.listitem_exists.return_value = True
        result = list_box.item_exists("item1")
        assert result is True
    
    def test_item_exists_false(self, list_box, mock_page):
        mock_page.listitem_exists.return_value = False
        result = list_box.item_exists("nonexistent")
        assert result is False
    
    def test_is_selected(self, list_box, mock_page):
        mock_page.is_listitem_selected.return_value = True
        result = list_box.is_selected("item1")
        assert result is True
    
    def test_get_item_text(self, list_box, mock_page):
        mock_page.get_listitems.return_value = ["item1"]
        result = list_box.get_item_text(0)
        assert result == "item1"
    
    def test_wait_for_item(self, list_box, mock_page):
        result = list_box.wait_for_item("item1", timeout=5)
        assert result is list_box
    
    def test_is_enabled(self, list_box, mock_page):
        mock_page.is_control_enabled.return_value = True
        result = list_box.is_enabled()
        assert result is True
    
    def test_is_visible(self, list_box, mock_page):
        mock_page.is_control_visible.return_value = True
        result = list_box.is_visible()
        assert result is True
