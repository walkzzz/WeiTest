"""Component Registry - dynamic component registration system"""

from typing import Dict, Type, Optional, Any
from threading import RLock


class ComponentRegistry:
    """
    组件注册表 - 单例模式

    支持运行时动态注册组件，无需修改核心代码

    Example:
        >>> registry = ComponentRegistry.get_instance()
        >>> registry.register("my_button", MyButton)
        >>> component_class = registry.get("my_button")
    """

    _instance: Optional["ComponentRegistry"] = None
    _lock = RLock()

    def __init__(self):
        """初始化组件注册表"""
        self._components: Dict[str, Type] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def get_instance(cls) -> "ComponentRegistry":
        """
        获取单例实例

        Returns:
            ComponentRegistry 实例
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def register(
        self, name: str, component: Type, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        注册组件

        Args:
            name: 组件名称
            component: 组件类
            metadata: 元数据（可选）
        """
        with self._lock:
            if name in self._components:
                raise ValueError(f"组件 '{name}' 已注册")

            self._components[name] = component

            if metadata:
                self._metadata[name] = metadata

    def unregister(self, name: str) -> None:
        """
        注销组件

        Args:
            name: 组件名称
        """
        with self._lock:
            if name not in self._components:
                raise ValueError(f"组件 '{name}' 未注册")

            del self._components[name]

            if name in self._metadata:
                del self._metadata[name]

    def get(self, name: str) -> Optional[Type]:
        """
        获取组件类

        Args:
            name: 组件名称

        Returns:
            组件类，不存在返回 None
        """
        return self._components.get(name)

    def get_or_default(self, name: str, default: Type) -> Type:
        """
        获取组件类或默认值

        Args:
            name: 组件名称
            default: 默认组件类

        Returns:
            组件类或默认类
        """
        return self._components.get(name, default)

    def has(self, name: str) -> bool:
        """
        检查组件是否已注册

        Args:
            name: 组件名称

        Returns:
            bool: 是否已注册
        """
        return name in self._components

    def list_all(self) -> Dict[str, Type]:
        """
        列出所有已注册的组件

        Returns:
            组件字典
        """
        return self._components.copy()

    def list_names(self) -> list:
        """
        列出所有组件名称

        Returns:
            名称列表
        """
        return list(self._components.keys())

    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """
        获取组件元数据

        Args:
            name: 组件名称

        Returns:
            元数据字典
        """
        return self._metadata.get(name)

    def clear(self) -> None:
        """清空所有注册"""
        with self._lock:
            self._components.clear()
            self._metadata.clear()

    def count(self) -> int:
        """
        获取已注册组件数量

        Returns:
            组件数量
        """
        return len(self._components)


# 便捷函数
def register_component(name: str, component: Type, metadata: Optional[Dict] = None) -> None:
    """
    注册组件的便捷函数

    Args:
        name: 组件名称
        component: 组件类
        metadata: 元数据
    """
    registry = ComponentRegistry.get_instance()
    registry.register(name, component, metadata)


def get_component(name: str) -> Optional[Type]:
    """
    获取组件类的便捷函数

    Args:
        name: 组件名称

    Returns:
        组件类
    """
    registry = ComponentRegistry.get_instance()
    return registry.get(name)


def create_component(name: str, *args, **kwargs) -> Any:
    """
    创建组件实例

    Args:
        name: 组件名称
        *args: 构造参数
        **kwargs: 构造参数关键字

    Returns:
        组件实例
    """
    registry = ComponentRegistry.get_instance()
    component_class = registry.get(name)

    if component_class is None:
        raise ValueError(f"组件 '{name}' 未注册")

    return component_class(*args, **kwargs)
