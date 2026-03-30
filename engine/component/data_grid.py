"""DataGrid Component - encapsulates data grid operations"""

from typing import Any, List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from wei.core.finder.locator import Locator
    from engine.page.base_page import BasePage


class DataGrid:
    """
    数据表格组件

    封装数据表格的所有操作

    Example:
        >>> grid = DataGrid(page, ByID("grid_data"))
        >>> grid.get_cell(0, 0)  # 获取第一行第一列
        >>> grid.sort_by_column(1)  # 按第二列排序
        >>> data = grid.get_all_data()
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化数据表格

        Args:
            page: 页面对象
            locator: 定位器
        """
        self.page = page
        self.locator = locator
        self._element: Any = None

    def _get_element(self) -> Any:
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
        return element.row_count()

    def get_column_count(self) -> int:
        """
        获取列数

        Returns:
            列数
        """
        element = self._get_element()
        return element.column_count()

    def get_cell(self, row: int, column: int) -> str:
        """
        获取单元格内容

        Args:
            row: 行索引 (从 0 开始)
            column: 列索引 (从 0 开始)

        Returns:
            单元格内容
        """
        element = self._get_element()

        try:
            # 尝试获取单元格
            cell = element.item(row, column)
            return cell.text() if hasattr(cell, "text") else str(cell)
        except Exception:
            # 备用方法
            return ""

    def get_row(self, row: int) -> List[str]:
        """
        获取整行数据

        Args:
            row: 行索引

        Returns:
            行数据列表
        """
        columns = self.get_column_count()
        return [self.get_cell(row, col) for col in range(columns)]

    def get_column(self, column: int) -> List[str]:
        """
        获取整列数据

        Args:
            column: 列索引

        Returns:
            列数据列表
        """
        rows = self.get_row_count()
        return [self.get_cell(row, column) for row in range(rows)]

    def get_all_data(self) -> List[List[str]]:
        """
        获取所有数据

        Returns:
            二维数据列表
        """
        rows = self.get_row_count()
        return [self.get_row(row) for row in range(rows)]

    def get_headers(self) -> List[str]:
        """
        获取表头

        Returns:
            表头列表
        """
        # 通常第一行是表头
        if self.get_row_count() > 0:
            return self.get_row(0)
        return []

    def get_data_without_headers(self) -> List[List[str]]:
        """
        获取不含表头的数据

        Returns:
            数据列表
        """
        all_data = self.get_all_data()
        if len(all_data) > 1:
            return all_data[1:]
        return []

    def sort_by_column(self, column: int, reverse: bool = False) -> "DataGrid":
        """
        按列排序

        Args:
            column: 列索引
            reverse: 是否降序

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            # 点击列头进行排序
            header = element.item(0, column)
            if reverse:
                # 如果需要降序，可能需要点击两次
                header.click_input()
                header.click_input()
            else:
                header.click_input()
        except Exception:
            pass

        return self

    def filter_by_column(self, column: int, value: str) -> List[List[str]]:
        """
        按列筛选数据

        Args:
            column: 列索引
            value: 筛选值

        Returns:
            筛选后的数据
        """
        all_data = self.get_all_data()
        headers = all_data[0] if all_data else []

        filtered = [row for row in all_data[1:] if value in row[column]]

        # 添加表头
        return [headers] + filtered if filtered else []

    def find_row(self, column: int, value: str) -> int:
        """
        查找包含指定值的行

        Args:
            column: 列索引
            value: 查找值

        Returns:
            行索引，未找到返回 -1
        """
        rows = self.get_row_count()

        for row in range(1, rows):  # 跳过表头
            cell_value = self.get_cell(row, column)
            if value in cell_value:
                return row

        return -1

    def select_row(self, row: int) -> "DataGrid":
        """
        选择行

        Args:
            row: 行索引

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            # 点击行进行选择
            cell = element.item(row, 0)
            cell.click_input()
        except Exception:
            pass

        return self

    def get_selected_rows(self) -> List[int]:
        """
        获取选中的行索引

        Returns:
            选中的行索引列表
        """
        element = self._get_element()
        selected = []

        try:
            rows = self.get_row_count()
            for row in range(1, rows):
                cell = element.item(row, 0)
                if hasattr(cell, "is_selected") and cell.is_selected():
                    selected.append(row)
        except Exception:
            pass

        return selected

    def double_click_cell(self, row: int, column: int) -> "DataGrid":
        """
        双击单元格

        Args:
            row: 行索引
            column: 列索引

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            cell = element.item(row, column)
            cell.double_click_input()
        except Exception:
            pass

        return self

    def get_cell_count(self) -> int:
        """
        获取单元格总数

        Returns:
            单元格总数
        """
        return self.get_row_count() * self.get_column_count()

    def is_sorted(self, column: int, ascending: bool = True) -> bool:
        """
        检查列是否已排序

        Args:
            column: 列索引
            ascending: 是否升序

        Returns:
            bool: 是否已排序
        """
        data = self.get_column(column)[1:]  # 跳过表头

        if not data:
            return True

        try:
            # 尝试转换为数字比较
            numeric_data = [float(x) for x in data]
            if ascending:
                return numeric_data == sorted(numeric_data)
            else:
                return numeric_data == sorted(numeric_data, reverse=True)
        except ValueError:
            # 字符串比较
            if ascending:
                return data == sorted(data)
            else:
                return data == sorted(data, reverse=True)

    @property
    def row_count(self) -> int:
        """获取行数"""
        return self.get_row_count()

    @property
    def column_count(self) -> int:
        """获取列数"""
        return self.get_column_count()

    @property
    def headers(self) -> List[str]:
        """获取表头"""
        return self.get_headers()

    @property
    def data(self) -> List[List[str]]:
        """获取所有数据"""
        return self.get_all_data()
