"""Backend Manager - manages UIA/Win32 backend switching"""

from typing import Dict
from pywinauto.application import Application

from core.driver.application import BackendType


class BackendManager:
    """
    后端管理器

    负责管理不同后端的创建和切换

    支持的后端：
    - UIA: Windows UI Automation（推荐，支持现代应用）
    - Win32: Win32 API（支持传统应用）
    """

    _instances: Dict[BackendType, "BackendManager"] = {}
    _backend_map: Dict[BackendType, str] = {
        BackendType.UIA: "uia",
        BackendType.WIN32: "win32",
    }

    @classmethod
    def get_backend(cls, backend_type: BackendType) -> "BackendManager":
        """
        获取后端实例（单例模式）

        Args:
            backend_type: 后端类型

        Returns:
            BackendManager 实例
        """
        if backend_type not in cls._instances:
            cls._instances[backend_type] = cls(backend_type)
        return cls._instances[backend_type]

    def __init__(self, backend_type: BackendType):
        """
        初始化后端管理器

        Args:
            backend_type: 后端类型
        """
        self.backend_type = backend_type

    def create_application(self) -> Application:
        """
        创建 pywinauto Application 实例

        Returns:
            Application 实例
        """
        backend_name = self._backend_map[self.backend_type]
        return Application(backend=backend_name)

    def get_backend_name(self) -> str:
        """
        获取后端名称

        Returns:
            后端名称字符串（"uia" 或 "win32"）
        """
        return self._backend_map[self.backend_type]

    @classmethod
    def reset(cls):
        """重置所有实例（测试用）"""
        cls._instances.clear()
