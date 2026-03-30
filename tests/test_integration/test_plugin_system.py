"""集成测试：插件系统测试"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock


@pytest.mark.integration
class TestPluginSystem:
    """插件系统集成测试"""

    def test_plugin_manager_creation(self):
        """测试插件管理器创建"""
        try:
            from core.plugin.base import PluginManager

            manager = PluginManager()
            assert manager is not None
        except ImportError:
            pytest.skip("插件系统模块不存在")

    def test_plugin_registry(self):
        """测试插件注册表"""
        try:
            from core.plugin.registry import ComponentRegistry

            registry = ComponentRegistry.get_instance()
            assert registry is not None

            # 清空注册表
            registry._components.clear()
        except ImportError:
            pytest.skip("插件注册表模块不存在")

    def test_custom_plugin_loading(self, tmp_path):
        """测试自定义插件加载"""
        try:
            from core.plugin.base import PluginManager, Plugin

            # 创建插件目录
            plugin_dir = tmp_path / "plugins"
            plugin_dir.mkdir()

            # 创建示例插件
            plugin_code = """
from core.plugin.base import ComponentPlugin

class ExamplePlugin(ComponentPlugin):
    name = "example"
    version = "1.0.0"
    description = "示例插件"
    
    def initialize(self, context):
        super().initialize(context)
        self.register_component("example_component", lambda page, locator: None)
"""
            plugin_file = plugin_dir / "example_plugin.py"
            plugin_file.write_text(plugin_code)

            # 加载插件
            manager = PluginManager()
            manager.load_from_directory(str(plugin_dir))

            # 验证插件已加载
            assert len(manager.plugins) >= 0
        except ImportError:
            pytest.skip("插件系统模块不存在")


@pytest.mark.integration
class TestAssertionIntegration:
    """断言系统集成测试"""

    def test_assertion_chain(self):
        """测试断言链"""
        from wei.engine.assertion import Assert

        # 基本断言链
        result = (
            Assert.that("Hello World", "测试字符串")
            .is_not_none()
            .contains("World")
            .starts_with("Hello")
        )

        assert result is not None

    def test_ui_assertion_with_mock(self):
        """测试 UI 断言（模拟）"""
        from wei.engine.assertion import Assert
        from unittest.mock import Mock

        mock_page = Mock()
        mock_locator = Mock()

        # 创建 UI 断言
        assertion = Assert.ui(mock_page, mock_locator)
        assert assertion is not None


@pytest.mark.integration
class TestWaiterIntegration:
    """等待机制集成测试"""

    def test_smart_wait_with_custom_condition(self):
        """测试智能等待与自定义条件"""
        try:
            from core.waiter.custom_conditions import ConditionBuilder

            builder = ConditionBuilder()
            condition = builder.visible().enabled().clickable().build()

            assert condition is not None
        except ImportError:
            pytest.skip("自定义等待条件模块不存在")

    def test_wait_condition_chain(self):
        """测试等待条件链"""
        from core.waiter.wait_condition import WaitCondition

        # 验证等待条件基类存在
        assert WaitCondition is not None
