"""
AutoTestMe-NG Core Layer

核心层提供 pywinauto 的类型安全封装，包括：
- Driver: 应用和窗口管理
- Finder: 元素定位
- Waiter: 智能等待
"""

from core.exceptions import (
    CoreError,
    DriverError,
    ApplicationStartError,
    ApplicationConnectError,
    WindowNotFoundError,
    FinderError,
    ElementNotFoundError,
    InvalidLocatorError,
    WaiterError,
    WaitTimeoutError,
)

__all__ = [
    "CoreError",
    "DriverError",
    "ApplicationStartError",
    "ApplicationConnectError",
    "WindowNotFoundError",
    "FinderError",
    "ElementNotFoundError",
    "InvalidLocatorError",
    "WaiterError",
    "WaitTimeoutError",
]
