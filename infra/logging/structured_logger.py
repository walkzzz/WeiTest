"""Enhanced Logging - structured logging with JSON support"""

import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """
    JSON 格式化器 - 结构化日志
    
    Example:
        >>> formatter = JSONFormatter()
        >>> handler = logging.FileHandler("app.log")
        >>> handler.setFormatter(formatter)
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录为 JSON
        
        Args:
            record: 日志记录
            
        Returns:
            JSON 格式字符串
        """
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加额外字段
        if hasattr(record, "context"):
            log_data["context"] = record.context
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


class StructuredLogger:
    """
    结构化日志记录器
    
    支持:
    - JSON 格式输出
    - 文件轮转
    - 控制台输出
    - 日志上下文
    
    Example:
        >>> logger = StructuredLogger("TestExecution", "reports/logs")
        >>> logger.info("测试开始", context={"test": "login_test"})
        >>> logger.error("测试失败", context={"error": "timeout"})
    """
    
    def __init__(
        self,
        name: str,
        log_dir: Optional[str] = None,
        level: int = logging.INFO,
        use_json: bool = True
    ) -> None:
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            log_dir: 日志目录
            level: 日志级别
            use_json: 是否使用 JSON 格式
        """
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers.clear()
        
        # 设置格式化器
        if use_json:
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        
        # 文件处理器
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """
        记录 DEBUG 级别日志
        
        Args:
            message: 日志消息
            **kwargs: 额外上下文
        """
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """
        记录 INFO 级别日志
        
        Args:
            message: 日志消息
            **kwargs: 额外上下文
        """
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """
        记录 WARNING 级别日志
        
        Args:
            message: 日志消息
            **kwargs: 额外上下文
        """
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """
        记录 ERROR 级别日志
        
        Args:
            message: 日志消息
            **kwargs: 额外上下文
        """
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """
        记录 CRITICAL 级别日志
        
        Args:
            message: 日志消息
            **kwargs: 额外上下文
        """
        self._log(logging.CRITICAL, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs: Any) -> None:
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外上下文
        """
        extra = {"context": kwargs} if kwargs else {}
        self.logger.log(level, message, extra=extra)
    
    def step(self, step_name: str, status: str = "start") -> None:
        """
        记录测试步骤
        
        Args:
            step_name: 步骤名称
            status: 状态 (start/success/failure)
        """
        self.info(
            f"步骤：{step_name}",
            step=step_name,
            status=status
        )
    
    def action(self, action: str, target: str, result: str = "") -> None:
        """
        记录操作
        
        Args:
            action: 操作类型 (click/type/select 等)
            target: 目标元素
            result: 操作结果
        """
        self.info(
            f"操作：{action}",
            action=action,
            target=target,
            result=result
        )
    
    def assertion(self, check_name: str, passed: bool, details: str = "") -> None:
        """
        记录断言结果
        
        Args:
            check_name: 断言名称
            passed: 是否通过
            details: 详细信息
        """
        level = logging.INFO if passed else logging.WARNING
        self.log(
            level,
            f"断言：{check_name}",
            assertion=check_name,
            passed=passed,
            details=details
        )


# ========== 便捷函数 ==========

def get_logger(name: str, log_dir: Optional[str] = None) -> StructuredLogger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        log_dir: 日志目录
        
    Returns:
        StructuredLogger 实例
    """
    return StructuredLogger(name, log_dir)
