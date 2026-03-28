"""Tests for Logger"""

import pytest
import os
import shutil
from pathlib import Path
from infra.logging.logger import Logger, get_logger


class TestLogger:
    """测试 Logger"""

    @pytest.fixture
    def test_log_dir(self):
        """创建测试日志目录"""
        test_dir = Path("test_logs")
        test_dir.mkdir(exist_ok=True)
        yield str(test_dir)
        # 清理
        shutil.rmtree(test_dir, ignore_errors=True)

    def test_logger_init(self, test_log_dir):
        """测试日志器初始化"""
        logger = Logger("TestLogger", log_dir=test_log_dir)

        assert logger.name == "TestLogger"
        assert logger.log_dir == Path(test_log_dir)
        assert logger.log_file_path.exists()

    def test_logger_log_info(self, test_log_dir):
        """测试记录信息日志"""
        logger = Logger("TestLogger", log_dir=test_log_dir)
        logger.info("测试信息")

        # 验证日志文件存在
        assert logger.log_file_path.exists()

    def test_logger_log_error(self, test_log_dir):
        """测试记录错误日志"""
        logger = Logger("TestLogger", log_dir=test_log_dir)
        logger.error("测试错误")

        assert logger.log_file_path.exists()

    def test_logger_log_debug(self, test_log_dir):
        """测试记录调试日志"""
        logger = Logger("TestLogger", log_dir=test_log_dir, level=10)
        logger.debug("调试信息")

        assert logger.log_file_path.exists()

    def test_logger_log_warning(self, test_log_dir):
        """测试记录警告日志"""
        logger = Logger("TestLogger", log_dir=test_log_dir)
        logger.warning("警告信息")

        assert logger.log_file_path.exists()

    def test_logger_log_critical(self, test_log_dir):
        """测试记录严重错误日志"""
        logger = Logger("TestLogger", log_dir=test_log_dir)
        logger.critical("严重错误")

        assert logger.log_file_path.exists()

    def test_get_log_file(self, test_log_dir):
        """测试获取日志文件路径"""
        logger = Logger("TestLogger", log_dir=test_log_dir)
        log_file = logger.get_log_file()

        assert isinstance(log_file, Path)
        assert log_file.exists()

    def test_get_logger_singleton(self, test_log_dir):
        """测试全局日志器单例"""
        import infra.logging.logger as logger_module

        logger_module._global_logger = None

        logger1 = get_logger("GlobalTest")
        logger2 = get_logger("GlobalTest")

        assert logger1 is logger2


class TestLoggerConvenience:
    """测试便捷函数"""

    @pytest.fixture
    def test_log_dir(self):
        """创建测试日志目录"""
        test_dir = Path("test_logs")
        test_dir.mkdir(exist_ok=True)
        yield str(test_dir)
        shutil.rmtree(test_dir, ignore_errors=True)

    def test_log_info(self, test_log_dir):
        """测试便捷信息日志"""
        import infra.logging.logger as logger_module

        logger_module._global_logger = None

        from infra.logging.logger import log_info

        log_info("测试信息")

    def test_log_error(self, test_log_dir):
        """测试便捷错误日志"""
        import infra.logging.logger as logger_module

        logger_module._global_logger = None

        from infra.logging.logger import log_error

        log_error("测试错误")
