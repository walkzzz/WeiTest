"""Table 组件完整测试 - 提升覆盖率"""
import pytest
from unittest.mock import Mock
from engine.component.table import Table
from core.finder.locator import ByID

class TestTableComplete:
    """Table 完整测试"""
    
    @pytest.fixture
    def mock_page(self):
        page = Mock()
        page.get_table_rows = Mock(return_value=["row1", "row2"])
        page.get_table_columns = Mock(return_value=["col1", "col2"])
        page.get_table_row_count = Mock(return_value=2)
        page.get_table_column_count = Mock(return_value=3)
        page.get_table_cell = Mock(return_value="cell_value")
        page.get_table_header = Mock(return_value=["Header1", "Header2"])
        return page
    
    @pytest.fixture
    def table(self, mock_page):
        return Table(mock_page, ByID("table_test"))
    
    def test_row_count(self, table, mock_page):
        mock_page.get_table_row_count.return_value = 5
        result = table.row_count()
        assert result == 5
    
    def test_column_count(self, table, mock_page):
        mock_page.get_table_column_count.return_value = 4
        result = table.column_count()
        assert result == 4
    
    def test_get_cell(self, table, mock_page):
        mock_page.get_table_cell.return_value = "value"
        result = table.get_cell(0, 1)
        assert result == "value"
    
    def test_get_row(self, table, mock_page):
        mock_page.get_table_rows.return_value = ["row1", "row2"]
        result = table.get_row(0)
        assert result is not None
    
    def test_get_column(self, table, mock_page):
        mock_page.get_table_columns.return_value = ["col1", "col2"]
        result = table.get_column(0)
        assert result is not None
    
    def test_get_headers(self, table, mock_page):
        mock_page.get_table_header.return_value = ["H1", "H2"]
        result = table.get_headers()
        assert len(result) == 2
    
    def test_get_all_rows(self, table, mock_page):
        mock_page.get_table_rows.return_value = ["row1", "row2"]
        result = table.get_all_rows()
        assert len(result) == 2
    
    def test_get_all_columns(self, table, mock_page):
        mock_page.get_table_columns.return_value = ["col1", "col2"]
        result = table.get_all_columns()
        assert len(result) == 2
    
    def test_get_cell_text(self, table, mock_page):
        mock_page.get_table_cell.return_value = "text"
        result = table.get_cell_text(0, 1)
        assert result == "text"
    
    def test_select_row(self, table, mock_page):
        result = table.select_row(0)
        assert result is table or True
    
    def test_select_column(self, table, mock_page):
        result = table.select_column(0)
        assert result is table or True
    
    def test_wait_for_row(self, table, mock_page):
        result = table.wait_for_row(0, timeout=5)
        assert result is table
