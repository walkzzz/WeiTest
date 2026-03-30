"""TreeView Component - encapsulates tree view operations"""

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class TreeView:
    """
    树形控件组件

    封装树形控件的所有操作

    Example:
        >>> tree = TreeView(page, ByID("tree_files"))
        >>> tree.expand("Documents/Work/2024")
        >>> tree.select("Documents/Work/2024/Report.docx")
        >>> selected = tree.get_selected_path()
    """

    def __init__(self, page: "BasePage", locator: "Locator") -> None:
        """
        初始化树形控件

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

    def expand(self, path: str, separator: str = "/") -> "TreeView":
        """
        展开节点

        Args:
            path: 节点路径 (如 "Parent/Child/Leaf")
            separator: 路径分隔符

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()
        path_parts = path.split(separator)

        # 逐级展开
        for i in range(len(path_parts)):
            current_path = separator.join(path_parts[: i + 1])
            self._expand_node(element, current_path, separator)

        return self

    def _expand_node(self, element: Any, path: str, separator: str) -> None:
        """展开单个节点"""
        try:
            # 使用 pywinauto 的 tree item 操作
            item = element.get_item(path)
            if item:
                item.expand()
        except Exception:
            # 如果路径方式失败，尝试递归查找
            pass

    def collapse(self, path: str, separator: str = "/") -> "TreeView":
        """
        折叠节点

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            item = element.get_item(path)
            if item:
                item.collapse()
        except Exception:
            pass

        return self

    def select(self, path: str, separator: str = "/") -> "TreeView":
        """
        选择节点

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        # 先展开路径
        self.expand(path, separator)

        # 选择节点
        try:
            item = element.get_item(path)
            if item:
                item.select()
        except Exception:
            pass

        return self

    def get_selected_path(self) -> str:
        """
        获取选中节点的路径

        Returns:
            节点路径
        """
        element = self._get_element()

        try:
            selected_item = element.get_item()
            if selected_item:
                return selected_item.text()
        except Exception:
            pass

        return ""

    def get_node_text(self, path: str, separator: str = "/") -> str:
        """
        获取节点的文本

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            节点文本
        """
        element = self._get_element()

        try:
            item = element.get_item(path)
            if item:
                return item.text()
        except Exception:
            pass

        return ""

    def node_exists(self, path: str, separator: str = "/") -> bool:
        """
        检查节点是否存在

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            bool: 是否存在
        """
        element = self._get_element()

        try:
            item = element.get_item(path)
            return item is not None
        except Exception:
            return False

    def get_all_nodes(self, root_path: str = "", separator: str = "/") -> List[str]:
        """
        获取所有节点路径

        Args:
            root_path: 起始节点路径
            separator: 路径分隔符

        Returns:
            节点路径列表
        """
        nodes = []
        element = self._get_element()

        try:
            # 获取根节点
            if root_path:
                root_item = element.get_item(root_path)
            else:
                root_item = element.get_item()

            if root_item:
                # 递归获取所有子节点
                self._collect_nodes(root_item, root_path, separator, nodes)
        except Exception:
            pass

        return nodes

    def _collect_nodes(self, item: Any, parent_path: str, separator: str, nodes: List[str]) -> None:
        """递归收集节点"""
        try:
            item_text = item.text()
            current_path = f"{parent_path}{separator}{item_text}" if parent_path else item_text
            nodes.append(current_path)

            # 获取子节点
            if item.has_children():
                item.expand()
                children = item.children()
                for child in children:
                    self._collect_nodes(child, current_path, separator, nodes)
        except Exception:
            pass

    def get_children(self, path: str, separator: str = "/") -> List[str]:
        """
        获取子节点列表

        Args:
            path: 父节点路径
            separator: 路径分隔符

        Returns:
            子节点文本列表
        """
        children = []
        element = self._get_element()

        try:
            # 展开父节点
            self.expand(path, separator)

            # 获取子节点
            parent_item = element.get_item(path)
            if parent_item and parent_item.has_children():
                parent_item.expand()
                for child in parent_item.children():
                    try:
                        children.append(child.text())
                    except Exception:
                        continue
        except Exception:
            pass

        return children

    def is_node_expanded(self, path: str, separator: str = "/") -> bool:
        """
        检查节点是否已展开

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            bool: 是否已展开
        """
        element = self._get_element()

        try:
            item = element.get_item(path)
            if item:
                return item.is_expanded()
        except Exception:
            pass

        return False

    def is_node_selected(self, path: str, separator: str = "/") -> bool:
        """
        检查节点是否被选中

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            bool: 是否被选中
        """
        selected_path = self.get_selected_path()
        return selected_path == path or selected_path.endswith(f"{separator}{path}")

    def double_click_node(self, path: str, separator: str = "/") -> "TreeView":
        """
        双击节点

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            self.expand(path, separator)
            item = element.get_item(path)
            if item:
                item.double_click_input()
        except Exception:
            pass

        return self

    def right_click_node(self, path: str, separator: str = "/") -> "TreeView":
        """
        右键点击节点

        Args:
            path: 节点路径
            separator: 路径分隔符

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        try:
            self.expand(path, separator)
            item = element.get_item(path)
            if item:
                item.right_click_input()
        except Exception:
            pass

        return self

    @property
    def selected_path(self) -> str:
        """获取选中节点的路径"""
        return self.get_selected_path()

    @property
    def node_count(self) -> int:
        """获取节点总数"""
        return len(self.get_all_nodes())
