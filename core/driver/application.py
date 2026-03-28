"""Application Driver - manages Windows application lifecycle"""

from typing import Optional
from enum import Enum

from pywinauto.application import Application

from core.exceptions import ApplicationStartError, ApplicationConnectError, WindowNotFoundError
from core.driver.window import WindowDriver


class BackendType(Enum):
    """后端类型枚举"""

    UIA = "uia"  # Windows UI Automation (recommended)
    WIN32 = "win32"  # Win32 API (legacy support)


class ApplicationDriver:
    """
    应用程序驱动器

    负责管理 Windows 应用的生命周期

    Example:
        >>> app = ApplicationDriver()
        >>> app.start("notepad.exe")
        >>> app.connect(title="Untitled - Notepad")
        >>> app.close()
    """

    def __init__(self, backend: BackendType = BackendType.UIA):
        """
        初始化应用程序驱动器

        Args:
            backend: 后端类型，默认 UIA
        """
        self.backend = backend
        self._app: Optional[Application] = None
        self._process_id: Optional[int] = None

    def start(self, app_path: str, timeout: int = 30) -> "ApplicationDriver":
        """
        启动应用程序

        Args:
            app_path: 应用程序路径
            timeout: 启动超时时间（秒）

        Returns:
            self: 支持链式调用

        Raises:
            ApplicationStartError: 启动失败时抛出
        """
        try:
            self._app = Application(backend=self.backend.value).start(app_path)
            self._process_id = self._app.process
            return self
        except Exception as e:
            raise ApplicationStartError(app_path, str(e))

    def connect(
        self, title: Optional[str] = None, process_id: Optional[int] = None, timeout: int = 30
    ) -> "ApplicationDriver":
        """
        连接到已运行的应用程序

        Args:
            title: 窗口标题（可选）
            process_id: 进程 ID（可选）
            timeout: 连接超时时间（秒）

        Returns:
            self: 支持链式调用

        Raises:
            ApplicationConnectError: 连接失败时抛出
        """
        try:
            if title:
                self._app = Application(backend=self.backend.value).connect(title=title)
            elif process_id:
                self._app = Application(backend=self.backend.value).connect(process=process_id)
            else:
                raise ValueError("必须提供 title 或 process_id 参数")

            self._process_id = self._app.process
            return self
        except Exception as e:
            raise ApplicationConnectError(title, process_id, str(e))

    def close(self) -> "ApplicationDriver":
        """关闭应用程序"""
        if self._app:
            self._app.kill()
            self._app = None
            self._process_id = None
        return self

    def get_window(self, title: str) -> WindowDriver:
        """
        获取窗口驱动器

        Args:
            title: 窗口标题

        Returns:
            WindowDriver 实例

        Raises:
            WindowNotFoundError: 窗口未找到时抛出
        """
        if not self._app:
            raise ApplicationConnectError(None, None, "应用未启动")

        try:
            window = self._app.window(title=title)
            return WindowDriver(window)
        except Exception as e:
            raise WindowNotFoundError(title)

    @property
    def process_id(self) -> Optional[int]:
        """获取进程 ID"""
        return self._process_id

    @property
    def is_running(self) -> bool:
        """检查应用是否正在运行"""
        return self._app is not None and self._process_id is not None
