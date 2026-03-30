"""Menu Component - encapsulates menu operations"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.finder.locator import Locator
    from engine.page.base_page import BasePage


class Menu:
    """
    菜单组件

    封装菜单栏和上下文菜单的操作

    使用示例：
        >>> menu = Menu(page, ByID("menu_bar"))
        >>> menu.select("文件", "新建")
        >>> menu.click_menu_item("编辑", "复制")
    """

    def __init__(self, page: "BasePage", locator: "Locator"):
        """
        初始化菜单组件

        Args:
            page: 页面对象
            locator: 菜单定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def _get_element(self):
        """获取底层元素（延迟加载）"""
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    def select(self, *menu_path: str) -> "Menu":
        """
        选择菜单项

        Args:
            *menu_path: 菜单路径，如 ("文件", "新建")

        Returns:
            self: 支持链式调用
        """
        element = self._get_element()

        for item_text in menu_path:
            # 查找菜单项
            menu_item = element.child_window(title=item_text, control_type="MenuItem")

            if not menu_item.exists():
                raise ValueError(f"菜单项不存在：{item_text}")

            # 点击菜单项
            menu_item.click_input()

        return self

    def click_menu_item(self, *menu_path: str):
        """
        点击菜单项（便捷方法）

        Args:
            *menu_path: 菜单路径
        """
        self.select(*menu_path)

    def menu_item_exists(self, *menu_path: str) -> bool:
        """
        检查菜单项是否存在

        Args:
            *menu_path: 菜单路径

        Returns:
            bool: 是否存在
        """
        element = self._get_element()

        current_element = element
        for item_text in menu_path:
            menu_item = current_element.child_window(title=item_text, control_type="MenuItem")

            if not menu_item.exists():
                return False

            current_element = menu_item

        return True

    def get_menu_items(self) -> list:
        """
        获取所有菜单项文本

        Returns:
            菜单项文本列表
        """
        element = self._get_element()
        items = element.children(control_type="MenuItem")

        return [item.window_text() for item in items]

    @property
    def is_visible(self) -> bool:
        """检查菜单是否可见"""
        return self._get_element().is_visible()

    @property
    def is_enabled(self) -> bool:
        """检查菜单是否可用"""
        return self._get_element().is_enabled()


class ContextMenu:
    """
    上下文菜单（右键菜单）组件

    使用示例：
        >>> ctx = ContextMenu(page)
        >>> ctx.right_click_and_select(element, "复制")
    """

    def __init__(self, page: "BasePage"):
        """
        初始化上下文菜单

        Args:
            page: 页面对象
        """
        self.page = page

    def right_click_and_select(self, element_locator: "Locator", menu_item: str) -> "ContextMenu":
        """
        右键点击元素并选择菜单项

        Args:
            element_locator: 元素定位器
            menu_item: 菜单项文本

        Returns:
            self: 支持链式调用
        """
        # 右键点击元素
        element = self.page.find_element(element_locator)
        element.right_click_input()

        # 等待上下文菜单出现
        import time

        time.sleep(0.5)

        # 获取上下文菜单
        from pywinauto import Desktop

        desktop = Desktop(backend="uia")
        context_menu = desktop.window(control_type="Menu")

        if not context_menu.exists():
            raise RuntimeError("上下文菜单未出现")

        # 点击菜单项
        menu_item_elem = context_menu.child_window(title=menu_item, control_type="MenuItem")

        if not menu_item_elem.exists():
            raise ValueError(f"菜单项不存在：{menu_item}")

        menu_item_elem.click_input()

        return self

    def context_menu_exists(self) -> bool:
        """
        检查上下文菜单是否存在

        Returns:
            bool: 是否存在
        """
        from pywinauto import Desktop

        desktop = Desktop(backend="uia")
        context_menu = desktop.window(control_type="Menu")

        return context_menu.exists()
