"""插件系统集成测试"""
import pytest
from unittest.mock import Mock, patch
from core.plugin.base import ComponentPlugin, PluginContext, PluginManager

class TestPluginContext:
    """PluginContext 测试"""
    
    def test_creation(self):
        ctx = PluginContext()
        assert ctx is not None
    
    def test_set_get(self):
        ctx = PluginContext()
        ctx.set("key", "value")
        assert ctx.get("key") == "value"
    
    def test_get_default(self):
        ctx = PluginContext()
        assert ctx.get("nonexistent", "default") == "default"

class TestComponentPlugin:
    """ComponentPlugin 测试"""
    
    @pytest.fixture
    def plugin(self):
        class TestPlugin(ComponentPlugin):
            name = "test"
            version = "1.0.0"
            description = "Test plugin"
        return TestPlugin()
    
    def test_plugin_attributes(self, plugin):
        assert plugin.name == "test"
        assert plugin.version == "1.0.0"
        assert plugin.description == "Test plugin"
    
    def test_plugin_initialize(self, plugin):
        ctx = PluginContext()
        plugin.initialize(ctx)
        assert plugin._context is ctx
    
    def test_plugin_register_component(self, plugin):
        plugin._context = PluginContext()
        plugin.register_component("test_comp", lambda: None)
        registry = plugin._context.get("component_registry")
        assert registry is not None
    
    def test_plugin_register_locator(self, plugin):
        plugin._context = PluginContext()
        plugin.register_locator("test_loc", lambda: None)
        registry = plugin._context.get("locator_registry")
        assert registry is not None

class TestPluginManager:
    """PluginManager 测试"""
    
    @pytest.fixture
    def manager(self):
        return PluginManager()
    
    def test_manager_creation(self, manager):
        assert manager is not None
        assert manager.plugins == {}
    
    def test_manager_register_plugin(self, manager):
        plugin = Mock()
        plugin.name = "test"
        manager.register_plugin(plugin)
        assert "test" in manager.plugins
    
    def test_manager_plugins_property(self, manager):
        assert hasattr(manager, 'plugins')
        assert isinstance(manager.plugins, dict)
    
    def test_manager_get_component(self, manager):
        result = manager.get_component("nonexistent")
        assert result is None
    
    def test_manager_get_locator(self, manager):
        result = manager.get_locator("nonexistent")
        assert result is None
    
    def test_manager_initialize_all(self, manager):
        manager.initialize_all()
        # 应该不抛出异常
    
    def test_manager_shutdown_all(self, manager):
        manager.shutdown_all()
        # 应该不抛出异常
