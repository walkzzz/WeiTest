"""Logger - structured logging with file rotation"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class Logger:
    """
    日志器

    支持文件和控制台输出
    支持日志轮转（10MB/文件）
    可配置日志级别

    使用示例：
        >>> logger = Logger("MyTest")
        >>> logger.info("测试开始")
        >>> logger.error("发生错误")
    """

    DEFAULT_LOG_DIR = "logs"
    MAX_BYTES = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5

    def __init__(
        self,
        name: str = "AutoTestMe",
        log_dir: Optional[str] = None,
        level: int = logging.DEBUG,
        log_file: Optional[str] = None,
    ):
        """
        初始化日志器

        Args:
            name: 日志器名称
            log_dir: 日志文件目录
            level: 日志级别
            log_file: 日志文件名（可选）
        """
        self.name = name
        self.log_dir = Path(log_dir or self.DEFAULT_LOG_DIR)
        self.level = level

        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 日志文件名
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"{name}_{timestamp}.log"

        self.log_file_path = self.log_dir / log_file

        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 清除现有处理器
        self.logger.handlers.clear()

        # 添加处理器
        self._add_file_handler()
        self._add_console_handler()

    def _add_file_handler(self):
        """添加文件处理器"""
        try:
            file_handler = RotatingFileHandler(
                self.log_file_path,
                maxBytes=self.MAX_BYTES,
                backupCount=self.BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setLevel(self.level)
        except ImportError:
            file_handler = logging.FileHandler(self.log_file_path, encoding="utf-8")
            file_handler.setLevel(self.level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _add_console_handler(self):
        """添加控制台处理器"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        """调试日志"""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """信息日志"""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """警告日志"""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """错误日志"""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """严重错误日志"""
        self.logger.critical(message)

    def get_log_file(self) -> Path:
        """获取日志文件路径"""
        return self.log_file_path


# ========== Global Logger ==========

_global_logger: Optional[Logger] = None


def get_logger(name: str = "AutoTestMe") -> Logger:
    """
    获取全局日志器

    Args:
        name: 日志器名称

    Returns:
        Logger 实例
    """
    global _global_logger
    if _global_logger is None or _global_logger.name != name:
        _global_logger = Logger(name)
    return _global_logger


# ========== Convenience Functions ==========


def log_info(message: str) -> None:
    """记录信息日志"""
    get_logger().info(message)


def log_error(message: str) -> None:
    """记录错误日志"""
    get_logger().error(message)


def log_debug(message: str) -> None:
    """记录调试日志"""
    get_logger().debug(message)


def log_warning(message: str) -> None:
    """记录警告日志"""
    get_logger().warning(message)
