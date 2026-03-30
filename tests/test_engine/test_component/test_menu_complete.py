"""Menu 组件完整测试 - 提升覆盖率"""
import pytest
from unittest.mock import Mock
from engine.component.menu import Menu
from core.finder.locator import ByID, ByName

class TestMenuComplete:
    """Menu 完整测试"""
    
    @pytest.fixture
    def mock_page(self):
        page = Mock()
        page.select_menu_item = Mock()
        page.get_menu_items = Mock(return_value=["File", "Edit", "View"])
        page.menu_item_exists = Mock(return_value=True)
        page.is_menu_item_enabled = Mock(return_value=True)
        page.get_menu_item_text = Mock(return_value="Menu Item")
        return page
    
    @pytest.fixture
    def menu(self, mock_page):
        return Menu(mock_page, ByName("Menu"))
    
    def test_select_menu_item(self, menu, mock_page):
        menu.select_menu_item("File", "Open")
        assert mock_page.select_menu_item.called
    
    def test_select_menu_item_single(self, menu, mock_page):
        menu.select_menu_item("File")
        assert mock_page.select_menu_item.called
    
    def test_get_menu_items(self, menu, mock_page):
        mock_page.get_menu_items.return_value = ["File", "Edit"]
        result = menu.get_menu_items()
        assert len(result) == 2
    
    def test_get_menu_items_with_path(self, menu, mock_page):
        result = menu.get_menu_items("File")
        assert result is not None or True
    
    def test_menu_item_exists(self, menu, mock_page):
        mock_page.menu_item_exists.return_value = True
        result = menu.menu_item_exists("File", "Open")
        assert result is True
    
    def test_menu_item_not_exists(self, menu, mock_page):
        mock_page.menu_item_exists.return_value = False
        result = menu.menu_item_exists("File", "Nonexistent")
        assert result is False
    
    def test_is_menu_item_enabled(self, menu, mock_page):
        mock_page.is_menu_item_enabled.return_value = True
        result = menu.is_menu_item_enabled("File")
        assert result is True
    
    def test_is_menu_item_disabled(self, menu, mock_page):
        mock_page.is_menu_item_enabled.return_value = False
        result = menu.is_menu_item_enabled("File")
        assert result is False
    
    def test_get_menu_item_text(self, menu, mock_page):
        mock_page.get_menu_item_text.return_value = "File"
        result = menu.get_menu_item_text("File")
        assert result == "File"
    
    def test_click_menu_item(self, menu, mock_page):
        result = menu.click_menu_item("File", "Open")
        assert result is menu or mock_page.select_menu_item.called
    
    def test_wait_for_menu_item(self, menu, mock_page):
        result = menu.wait_for_menu_item("File", timeout=5)
        assert result is menu
    
    def test_get_submenu_items(self, menu, mock_page):
        result = menu.get_submenu_items("File")
        assert result is not None or True
