"""Example Plugins - demonstration of plugin system usage"""

from typing import Dict, Type
from core.plugin.base import ComponentPlugin, LocatorPlugin, PluginContext


# ========== 示例自定义组件 ==========


class CustomButton:
    """自定义按钮组件示例"""

    def __init__(self, page, locator):
        """
        初始化自定义按钮

        Args:
            page: 页面对象
            locator: 定位器
        """
        self.page = page
        self.locator = locator
        self._element = None

    def click_with_animation(self) -> "CustomButton":
        """带动画效果的点击"""
        # 模拟动画效果
        element = self.page.find_element(self.locator)
        element.click_input(button="left", double=False)
        return self

    def flash(self, times: int = 3) -> "CustomButton":
        """闪烁效果"""
        element = self.page.find_element(self.locator)

        for _ in range(times):
            # 模拟闪烁
            element.click_input()

        return self


class CustomTable:
    """自定义表格组件示例"""

    def __init__(self, page, locator):
        """
        初始化自定义表格

        Args:
            page: 页面对象
            locator: 定位器
        """
        self.page = page
        self.locator = locator

    def get_sorted_data(self, column_index: int, reverse: bool = False) -> list:
        """
        获取排序后的表格数据

        Args:
            column_index: 列索引
            reverse: 是否降序

        Returns:
            排序后的数据列表
        """
        # 获取原始数据
        data = self._get_column_data(column_index)

        # 排序
        return sorted(data, reverse=reverse)

    def _get_column_data(self, column_index: int) -> list:
        """获取列数据"""
        # 简化实现
        return []


# ========== 示例自定义定位器 ==========


class CssSelectorLocator:
    """CSS 选择器定位器示例"""

    def __init__(self, selector: str):
        """
        初始化 CSS 选择器定位器

        Args:
            selector: CSS 选择器
        """
        self.selector = selector

    def locate(self, context):
        """
        定位元素

        Args:
            context: 定位上下文

        Returns:
            元素实例
        """
        # 实际实现会使用 CSS 选择器引擎
        print(f"定位 CSS 选择器：{self.selector}")
        return None


# ========== 插件实现 ==========


class ExampleComponentPlugin(ComponentPlugin):
    """
    示例组件插件

    注册自定义组件
    """

    @property
    def name(self) -> str:
        return "example_components"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "示例自定义组件插件"

    def get_components(self) -> Dict[str, Type]:
        """获取组件字典"""
        return {
            "custom_button": CustomButton,
            "custom_table": CustomTable,
        }


class ExampleLocatorPlugin(LocatorPlugin):
    """
    示例定位器插件

    注册自定义定位策略
    """

    @property
    def name(self) -> str:
        return "example_locators"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "示例自定义定位器插件"

    def get_locators(self) -> Dict[str, Type]:
        """获取定位器字典"""
        return {
            "css": CssSelectorLocator,
        }


# ========== 插件使用示例 ==========


def setup_example_plugins():
    """
    设置示例插件

    Example:
        >>> from core.plugin.example_plugins import setup_example_plugins
        >>> setup_example_plugins()
    """
    from core.plugin.base import get_plugin_manager

    manager = get_plugin_manager()

    # 创建并注册插件
    component_plugin = ExampleComponentPlugin()
    locator_plugin = ExampleLocatorPlugin()

    manager.register_plugin(component_plugin)
    manager.register_plugin(locator_plugin)

    print("✅ 示例插件已注册")
    print(f"   组件：{manager.list_components()}")
    print(f"   定位器：{manager.list_locators()}")


if __name__ == "__main__":
    # 测试插件
    setup_example_plugins()

    # 使用注册的组件
    from core.plugin.base import get_component

    CustomBtn = get_component("custom_button")
    print(f"获取自定义按钮组件：{CustomBtn}")
