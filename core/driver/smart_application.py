"""Smart Application Driver - Auto-detect backend"""

from typing import Optional
from core.driver.application import ApplicationDriver, BackendType
from core.exceptions import ApplicationStartError


class SmartApplicationDriver(ApplicationDriver):
    """
    智能应用驱动器

    自动检测并选择最佳后端（UIA/Win32）

    使用示例：
        >>> driver = SmartApplicationDriver()
        >>> driver.start("old_app.exe")  # 自动检测
        >>> driver.backend  # BackendType.WIN32 (老旧应用)

        >>> driver.start("modern_app.exe")  # 自动检测
        >>> driver.backend  # BackendType.UIA (现代应用)
    """

    def __init__(self, backend: Optional[BackendType] = None, auto_detect: bool = True):
        """
        初始化智能驱动器

        Args:
            backend: 指定后端（可选）
            auto_detect: 是否自动检测（默认 True）
        """
        super().__init__(backend or BackendType.UIA)
        self.auto_detect = auto_detect
        self._detection_tried = False

    def start(self, app_path: str, timeout: int = 30) -> "SmartApplicationDriver":
        """
        启动应用程序（自动检测后端）

        Args:
            app_path: 应用程序路径
            timeout: 启动超时时间

        Returns:
            self: 支持链式调用
        """
        if not self.auto_detect or self._detection_tried:
            # 使用指定后端或已检测的后端
            return super().start(app_path, timeout)

        # 先尝试 UIA（现代应用）
        try:
            self.backend = BackendType.UIA
            result = super().start(app_path, timeout)
            self._detection_tried = True
            return result
        except Exception as e:
            # UIA 失败，回退到 Win32（老旧应用）
            try:
                self.backend = BackendType.WIN32
                result = super().start(app_path, timeout)
                self._detection_tried = True
                return result
            except Exception as e2:
                raise ApplicationStartError(
                    app_path, f"UIA 和 Win32 后端均启动失败：UIA({e}), Win32({e2})"
                )

    def get_detected_backend(self) -> Optional[BackendType]:
        """获取检测到的后端类型"""
        if self._detection_tried:
            return self.backend
        return None

    def is_modern_app(self) -> bool:
        """是否为现代应用（使用 UIA）"""
        return self.backend == BackendType.UIA

    def is_legacy_app(self) -> bool:
        """是否为老旧应用（使用 Win32）"""
        return self.backend == BackendType.WIN32


class BackendDetector:
    """
    后端检测器

    静态方法检测应用推荐后端
    """

    @staticmethod
    def detect_by_path(app_path: str) -> BackendType:
        """
        根据路径检测推荐后端

        Args:
            app_path: 应用路径

        Returns:
            推荐后端类型
        """
        app_path_lower = app_path.lower()

        # 现代应用特征
        modern_keywords = ["msedge", "chrome", "store", "uwp", "winui"]
        for keyword in modern_keywords:
            if keyword in app_path_lower:
                return BackendType.UIA

        # 老旧应用特征
        legacy_keywords = ["vb6", "delphi", "mfc", "win32", "win95", "win98"]
        for keyword in legacy_keywords:
            if keyword in app_path_lower:
                return BackendType.WIN32

        # 默认推荐 UIA
        return BackendType.UIA

    @staticmethod
    def detect_by_title(window_title: str) -> BackendType:
        """
        根据窗口标题检测推荐后端

        Args:
            window_title: 窗口标题

        Returns:
            推荐后端类型
        """
        # 简单启发式检测
        # 可结合实际经验扩展
        return BackendType.UIA
