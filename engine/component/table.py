"""Table Component - encapsulates table/grid operations"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class Table:
    """
    表格组件

    封装表格/网格控件的所有操作

    使用示例：
        >>> table = Table(page, ByID("tbl_data"))
        >>> table.get_row_count()
        >>> table.get_cell(0, 0)  # 第 1 行第 1 列
        >>> table.select_row(0)
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化表格组件

        Args:
            page: 页面对象
            locator: 表格定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def get_row_count(self) -> int:
        """
        获取行数

        Returns:
            行数
        """
        element = self._get_element()
        # 获取表格的子元素（行）
        rows = element.children()
        return len(rows)

    def get_column_count(self) -> int:
        """
        获取列数

        Returns:
            列数
        """
        element = self._get_element()
        rows = element.children()

        if not rows:
            return 0

        # 获取第一行的列数
        first_row = rows[0]
        cells = first_row.children()
        return len(cells)

    def get_cell(self, row: int, column: int) -> str:
        """
        获取单元格文本

        Args:
            row: 行索引（从 0 开始）
            column: 列索引（从 0 开始）

        Returns:
            单元格文本
        """
        element = self._get_element()
        rows = element.children()

        if row < 0 or row >= len(rows):
            raise IndexError(f"行索引超出范围：{row}")

        target_row = rows[row]
        cells = target_row.children()

        if column < 0 or column >= len(cells):
            raise IndexError(f"列索引超出范围：{column}")

        return cells[column].window_text()

    def get_row(self, row: int) -> List[str]:
        """
        获取整行数据

        Args:
            row: 行索引

        Returns:
            单元格文本列表
        """
        element = self._get_element()
        rows = element.children()

        if row < 0 or row >= len(rows):
            raise IndexError(f"行索引超出范围：{row}")

        target_row = rows[row]
        cells = target_row.children()

        return [cell.window_text() for cell in cells]

    def get_all_rows(self) -> List[List[str]]:
        """
        获取所有行数据

        Returns:
            二维列表 [[cell1, cell2, ...], ...]
        """
        row_count = self.get_row_count()
        return [self.get_row(i) for i in range(row_count)]

    def select_row(self, row: int) -> "Table":
        """
        选择行

        Args:
            row: 行索引

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        rows = element.children()

        if row < 0 or row >= len(rows):
            raise IndexError(f"行索引超出范围：{row}")

        rows[row].click_input()
        return self

    def find_row_by_text(self, text: str, column: int = 0) -> Optional[int]:
        """
        根据文本查找行

        Args:
            text: 要查找的文本
            column: 搜索的列索引

        Returns:
            行索引，未找到返回 None
        """
        row_count = self.get_row_count()

        for i in range(row_count):
            cell_text = self.get_cell(i, column)
            if text in cell_text:
                return i

        return None

    @property
    def is_visible(self) -> bool:
        """检查表格是否可见"""
        return self._get_element().is_visible()

    @property
    def is_enabled(self) -> bool:
        """检查表格是否可用"""
        return self._get_element().is_enabled()
