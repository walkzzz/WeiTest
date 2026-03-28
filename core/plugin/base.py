"""Plugin System - core plugin infrastructure for extensibility"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Set
from pathlib import Path
import importlib.util
import sys


class PluginContext:
    """
    插件上下文

    为插件提供运行时环境和所需服务

    Example:
        >>> context = PluginContext()
        >>> context.register_service("logger", logger_instance)
        >>> logger = context.get_service("logger")
    """

    def __init__(self):
        """初始化插件上下文"""
        self._services: Dict[str, Any] = {}
        self._config: Dict[str, Any] = {}
        self._base_dir: Path = Path.cwd()

    def register_service(self, name: str, service: Any) -> None:
        """
        注册服务

        Args:
            name: 服务名称
            service: 服务实例
        """
        self._services[name] = service

    def get_service(self, name: str) -> Optional[Any]:
        """
        获取服务

        Args:
            name: 服务名称

        Returns:
            服务实例，不存在返回 None
        """
        return self._services.get(name)

    def set_config(self, key: str, value: Any) -> None:
        """
        设置配置

        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def set_base_dir(self, path: Path) -> None:
        """设置基础目录"""
        self._base_dir = path

    @property
    def base_dir(self) -> Path:
        """获取基础目录"""
        return self._base_dir


class Plugin(ABC):
    """
    插件基类

    所有插件必须继承此类并实现必要的方法

    Example:
        >>> class MyComponentPlugin(ComponentPlugin):
        ...     @property
        ...     def name(self) -> str:
        ...         return "my_component"
        ...
        ...     def get_components(self):
        ...         return {"my_button": MyButton}
    """

    def __init__(self):
        """初始化插件"""
        self._context: Optional[PluginContext] = None
        self._initialized: bool = False

    @property
    @abstractmethod
    def name(self) -> str:
        """
        插件名称

        Returns:
            唯一的插件名称
        """
        pass

    @property
    def version(self) -> str:
        """
        插件版本

        Returns:
            版本号，默认 "1.0.0"
        """
        return "1.0.0"

    @property
    def description(self) -> str:
        """
        插件描述

        Returns:
            插件描述信息
        """
        return ""

    @property
    def dependencies(self) -> List[str]:
        """
        插件依赖

        Returns:
            依赖的插件名称列表
        """
        return []

    def initialize(self, context: PluginContext) -> None:
        """
        初始化插件

        Args:
            context: 插件上下文
        """
        self._context = context
        self._initialized = True

    def shutdown(self) -> None:
        """关闭插件，清理资源"""
        self._initialized = False

    def is_initialized(self) -> bool:
        """
        检查插件是否已初始化

        Returns:
            bool: 是否已初始化
        """
        return self._initialized

    def get_context(self) -> Optional[PluginContext]:
        """
        获取插件上下文

        Returns:
            插件上下文
        """
        return self._context


class ComponentPlugin(Plugin):
    """
    组件插件基类

    用于注册自定义 UI 组件

    Example:
        >>> class CustomComponentsPlugin(ComponentPlugin):
        ...     @property
        ...     def name(self) -> str:
        ...         return "custom_components"
        ...
        ...     def get_components(self) -> Dict[str, Type]:
        ...         return {
        ...             "custom_button": CustomButton,
        ...             "custom_table": CustomTable
        ...         }
    """

    @abstractmethod
    def get_components(self) -> Dict[str, Type]:
        """
        获取组件字典

        Returns:
            组件名称到组件类的映射
        """
        pass


class LocatorPlugin(Plugin):
    """
    定位器插件基类

    用于注册自定义定位策略

    Example:
        >>> class CustomLocatorsPlugin(LocatorPlugin):
        ...     @property
        ...     def name(self) -> str:
        ...         return "custom_locators"
        ...
        ...     def get_locators(self) -> Dict[str, Type]:
        ...         return {
        ...             "image": ImageLocator,
        ...             "ocr": OcrLocator
        ...         }
    """

    @abstractmethod
    def get_locators(self) -> Dict[str, Type]:
        """
        获取定位器字典

        Returns:
            定位器名称到定位器类的映射
        """
        pass


class AssertionPlugin(Plugin):
    """
    断言插件基类

    用于注册自定义断言类型

    Example:
        >>> class CustomAssertionsPlugin(AssertionPlugin):
        ...     @property
        ...     def name(self) -> str:
        ...         return "custom_assertions"
        ...
        ...     def get_assertions(self) -> Dict[str, Type]:
        ...         return {
        ...             "image_assertion": ImageAssertion,
        ...             "database_assertion": DatabaseAssertion
        ...         }
    """

    @abstractmethod
    def get_assertions(self) -> Dict[str, Type]:
        """
        获取断言字典

        Returns:
            断言名称到断言类的映射
        """
        pass


class PluginManager:
    """
    插件管理器

    负责加载、注册和管理所有插件

    Example:
        >>> manager = PluginManager()
        >>> manager.load_from_directory("plugins")
        >>> manager.initialize_all()
        >>>
        >>> # 获取组件
        >>> component_class = manager.get_component("custom_button")
        >>>
        >>> # 获取定位器
        >>> locator_class = manager.get_locator("image")
    """

    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        """
        初始化插件管理器

        Args:
            plugin_dirs: 插件目录列表
        """
        self._plugins: Dict[str, Plugin] = {}
        self._plugin_dirs: List[Path] = [Path(d) for d in (plugin_dirs or [])]

        # 添加默认插件目录
        self._plugin_dirs.append(Path.cwd() / "plugins")
        self._plugin_dirs.append(Path.cwd() / "extensions")

        # 组件和定位器注册表
        self._component_registry: Dict[str, Type] = {}
        self._locator_registry: Dict[str, Type] = {}
        self._assertion_registry: Dict[str, Type] = {}

        # 上下文
        self._context = PluginContext()

    def register_plugin(self, plugin: Plugin) -> None:
        """
        注册插件

        Args:
            plugin: 插件实例
        """
        plugin_name = plugin.name

        if plugin_name in self._plugins:
            raise ValueError(f"插件 '{plugin_name}' 已注册")

        # 检查依赖
        for dep in plugin.dependencies:
            if dep not in self._plugins:
                raise ValueError(f"插件 '{plugin_name}' 依赖未满足：{dep}")

        self._plugins[plugin_name] = plugin

        # 初始化插件
        plugin.initialize(self._context)

        # 注册组件/定位器/断言
        self._register_plugin_features(plugin)

    def _register_plugin_features(self, plugin: Plugin) -> None:
        """
        注册插件功能

        Args:
            plugin: 插件实例
        """
        # 注册组件
        if isinstance(plugin, ComponentPlugin):
            components = plugin.get_components()
            for name, component_class in components.items():
                self._component_registry[name] = component_class

        # 注册定位器
        if isinstance(plugin, LocatorPlugin):
            locators = plugin.get_locators()
            for name, locator_class in locators.items():
                self._locator_registry[name] = locator_class

        # 注册断言
        if isinstance(plugin, AssertionPlugin):
            assertions = plugin.get_assertions()
            for name, assertion_class in assertions.items():
                self._assertion_registry[name] = assertion_class

    def unregister_plugin(self, plugin_name: str) -> None:
        """
        注销插件

        Args:
            plugin_name: 插件名称
        """
        if plugin_name not in self._plugins:
            raise ValueError(f"插件 '{plugin_name}' 未注册")

        plugin = self._plugins[plugin_name]
        plugin.shutdown()

        del self._plugins[plugin_name]

        # 从注册表中移除
        self._unregister_plugin_features(plugin_name)

    def _unregister_plugin_features(self, plugin_name: str) -> None:
        """从注册表中移除插件功能"""
        # 这里简化处理，实际应该只移除该插件注册的功能
        pass

    def load_plugin(self, plugin_path: str) -> Plugin:
        """
        从文件加载插件

        Args:
            plugin_path: 插件文件路径

        Returns:
            插件实例
        """
        path = Path(plugin_path)

        if not path.exists():
            raise FileNotFoundError(f"插件文件不存在：{plugin_path}")

        # 动态加载模块
        module_name = path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)

        if spec is None or spec.loader is None:
            raise ImportError(f"无法加载插件模块：{plugin_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # 查找插件类
        plugin_class = self._find_plugin_class(module)

        if plugin_class is None:
            raise ValueError(f"插件文件未找到 Plugin 子类：{plugin_path}")

        # 实例化插件
        plugin: Plugin = plugin_class()

        return plugin

    def _find_plugin_class(self, module) -> Optional[Type[Plugin]]:
        """
        在模块中查找插件类

        Args:
            module: 导入的模块

        Returns:
            插件类
        """
        for name in dir(module):
            obj = getattr(module, name)

            if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                return obj

        return None

    def load_from_directory(self, directory: str) -> int:
        """
        从目录加载所有插件

        Args:
            directory: 插件目录

        Returns:
            加载的插件数量
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            return 0

        count = 0

        for file in dir_path.glob("*.py"):
            # 跳过私有文件和 __init__.py
            if file.name.startswith("_"):
                continue

            try:
                plugin = self.load_plugin(str(file))
                self.register_plugin(plugin)
                count += 1
            except Exception as e:
                print(f"⚠️  加载插件失败 {file.name}: {e}")

        return count

    def load_all(self) -> int:
        """
        从所有插件目录加载插件

        Returns:
            加载的插件总数
        """
        total_count = 0

        for plugin_dir in self._plugin_dirs:
            if plugin_dir.exists():
                count = self.load_from_directory(str(plugin_dir))
                total_count += count

        return total_count

    def initialize_all(self) -> None:
        """初始化所有已加载的插件"""
        for plugin in self._plugins.values():
            if not plugin.is_initialized():
                plugin.initialize(self._context)

    def shutdown_all(self) -> None:
        """关闭所有插件"""
        for plugin in reversed(list(self._plugins.values())):
            plugin.shutdown()

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """
        获取插件

        Args:
            name: 插件名称

        Returns:
            插件实例
        """
        return self._plugins.get(name)

    def get_component(self, name: str) -> Optional[Type]:
        """
        获取组件类

        Args:
            name: 组件名称

        Returns:
            组件类
        """
        return self._component_registry.get(name)

    def get_locator(self, name: str) -> Optional[Type]:
        """
        获取定位器类

        Args:
            name: 定位器名称

        Returns:
            定位器类
        """
        return self._locator_registry.get(name)

    def get_assertion(self, name: str) -> Optional[Type]:
        """
        获取断言类

        Args:
            name: 断言名称

        Returns:
            断言类
        """
        return self._assertion_registry.get(name)

    def list_plugins(self) -> List[str]:
        """
        列出所有已注册的插件

        Returns:
            插件名称列表
        """
        return list(self._plugins.keys())

    def list_components(self) -> List[str]:
        """
        列出所有已注册的组件

        Returns:
            组件名称列表
        """
        return list(self._component_registry.keys())

    def list_locators(self) -> List[str]:
        """
        列出所有已注册的定位器

        Returns:
            定位器名称列表
        """
        return list(self._locator_registry.keys())

    def list_assertions(self) -> List[str]:
        """
        列出所有已注册的断言

        Returns:
            断言名称列表
        """
        return list(self._assertion_registry.keys())


# 全局插件管理器实例
_global_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """
    获取全局插件管理器

    Returns:
        PluginManager 实例
    """
    global _global_plugin_manager

    if _global_plugin_manager is None:
        _global_plugin_manager = PluginManager()

    return _global_plugin_manager


def register_plugin(plugin: Plugin) -> None:
    """
    注册插件到全局管理器

    Args:
        plugin: 插件实例
    """
    manager = get_plugin_manager()
    manager.register_plugin(plugin)


def get_component(name: str) -> Optional[Type]:
    """
    从全局管理器获取组件

    Args:
        name: 组件名称

    Returns:
        组件类
    """
    manager = get_plugin_manager()
    return manager.get_component(name)


def get_locator(name: str) -> Optional[Type]:
    """
    从全局管理器获取定位器

    Args:
        name: 定位器名称

    Returns:
        定位器类
    """
    manager = get_plugin_manager()
    return manager.get_locator(name)
