"""
Core layer exceptions

异常层次结构：
CoreError
├── DriverError
│   ├── ApplicationStartError
│   ├── ApplicationConnectError
│   └── WindowNotFoundError
├── FinderError
│   ├── ElementNotFoundError
│   └── InvalidLocatorError
└── WaiterError
    └── WaitTimeoutError
"""

from typing import Optional


class CoreError(Exception):
    """核心层异常基类"""

    pass


# ========== Driver Exceptions ==========


class DriverError(CoreError):
    """驱动器错误"""

    pass


class ApplicationStartError(DriverError):
    """应用启动失败"""

    def __init__(self, app_path: str, message: str):
        self.app_path = app_path
        super().__init__(f"启动应用失败 [{app_path}]: {message}")


class ApplicationConnectError(DriverError):
    """应用连接失败"""

    def __init__(self, title: Optional[str], process_id: Optional[int], message: str):
        self.title = title
        self.process_id = process_id
        super().__init__(f"连接应用失败 [title={title}, pid={process_id}]: {message}")


class WindowNotFoundError(DriverError):
    """窗口未找到"""

    def __init__(self, title: str):
        super().__init__(f"窗口未找到：{title}")


# ========== Finder Exceptions ==========


class FinderError(CoreError):
    """查找器错误"""

    pass


class ElementNotFoundError(FinderError):
    """元素未找到"""

    def __init__(self, locator_type: str, locator_value: str, timeout: int):
        self.locator_type = locator_type
        self.locator_value = locator_value
        self.timeout = timeout
        super().__init__(
            f"元素未找到 [type={locator_type}, value={locator_value}, timeout={timeout}s]"
        )


class InvalidLocatorError(FinderError):
    """无效定位器"""

    def __init__(self, message: str):
        super().__init__(f"无效定位器：{message}")


# ========== Waiter Exceptions ==========


class WaiterError(CoreError):
    """等待器错误"""

    pass


class WaitTimeoutError(WaiterError):
    """等待超时"""

    def __init__(self, condition_type: str, timeout: int):
        super().__init__(f"等待超时 [{condition_type}], timeout={timeout}s]")
