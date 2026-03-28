"""Application Mixin - manages application lifecycle"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.driver.application import ApplicationDriver, BackendType
    from core.driver.window import WindowDriver


class ApplicationMixin:
    """
    应用管理 Mixin

    职责：应用程序的启动、连接、关闭
    """

    _app_driver: Optional["ApplicationDriver"] = None
    _window: Optional["WindowDriver"] = None

    def start_app(self, app_path: str, timeout: int = 30) -> "ApplicationMixin":
        """
        启动应用程序

        Args:
            app_path: 应用程序路径
            timeout: 启动超时时间

        Returns:
            self: 支持链式调用
        """
        from core.driver.application import ApplicationDriver

        self._app_driver = ApplicationDriver()
        self._app_driver.start(app_path, timeout)
        return self

    def connect_app(
        self, title: Optional[str] = None, process_id: Optional[int] = None, timeout: int = 30
    ) -> "ApplicationMixin":
        """
        连接到已运行的应用程序

        Args:
            title: 窗口标题
            process_id: 进程 ID
            timeout: 连接超时时间

        Returns:
            self: 支持链式调用
        """
        from core.driver.application import ApplicationDriver

        self._app_driver = ApplicationDriver()
        self._app_driver.connect(title, process_id, timeout)
        return self

    def close_app(self) -> "ApplicationMixin":
        """关闭应用程序"""
        if self._app_driver:
            self._app_driver.close()
            self._app_driver = None
            self._window = None
        return self

    def get_window(self, title: str) -> "WindowDriver":
        """
        获取窗口驱动器

        Args:
            title: 窗口标题

        Returns:
            WindowDriver 实例

        Raises:
            RuntimeError: 应用未启动时抛出
        """
        if not self._app_driver:
            raise RuntimeError("应用未启动，请先调用 start_app() 或 connect_app()")

        self._window = self._app_driver.get_window(title)
        return self._window

    def set_window(self, window: "WindowDriver"):
        """
        设置窗口（供子类使用）

        Args:
            window: 窗口驱动器实例
        """
        self._window = window

    def get_current_window(self) -> Optional["WindowDriver"]:
        """获取当前窗口"""
        return self._window

    @property
    def app_driver(self) -> Optional["ApplicationDriver"]:
        """获取应用驱动器"""
        return self._app_driver
