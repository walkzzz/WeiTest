"""集成测试：配置和日志系统的集成测试"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch


@pytest.mark.integration
class TestConfigLoggingIntegration:
    """配置和日志系统集成测试"""

    def test_config_manager_loads_yaml(self, tmp_path):
        """测试配置管理器加载 YAML 文件"""
        from infra.config.config_manager import ConfigManager

        # 创建测试配置文件
        config_content = """
app:
  name: TestApp
  version: 1.0.0
  
environments:
  test:
    app_path: /path/to/test/app
    timeout: 30
  
  prod:
    app_path: /path/to/prod/app
    timeout: 60
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        # 加载配置
        manager = ConfigManager(str(tmp_path))
        manager.load_config("test_config")

        # 验证配置
        config = manager.get_config("test_config")
        assert config["app"]["name"] == "TestApp"

        env_config = manager.get_env_config("test")
        assert env_config["app_path"] == "/path/to/test/app"
        assert env_config["timeout"] == 30

    def test_enhanced_config_with_env_variables(self, tmp_path):
        """测试增强配置与环境变量集成"""
        from infra.config.enhanced_config import EnhancedConfigManager

        # 创建配置文件
        config_content = """
database:
  host: localhost
  port: 5432
  timeout: 30
"""
        config_file = tmp_path / "env_config.yaml"
        config_file.write_text(config_content)

        # 设置环境变量
        with patch.dict(os.environ, {"ATM_TIMEOUT": "60", "ATM_DEBUG": "true"}):
            manager = EnhancedConfigManager(str(tmp_path))
            config = manager.load_with_env("env_config.yaml")

            # 验证环境变量覆盖
            assert config["timeout"] == 60
            assert config["debug"] is True

    def test_config_encryption(self, tmp_path):
        """测试配置加密功能"""
        from infra.config.config_encryption import ConfigEncryption

        encryption = ConfigEncryption()

        # 加密
        secret = "my_password_123"
        encrypted = encryption.encrypt(secret)

        assert encrypted.startswith("ENC[")
        assert encrypted.endswith("]")

        # 解密
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == secret

        # 检查加密状态
        assert encryption.is_encrypted(encrypted)
        assert not encryption.is_encrypted(secret)

    def test_config_validator(self, tmp_path):
        """测试配置验证器"""
        from infra.config.config_validator import ConfigValidator

        schema = {
            "app_name": {"type": "string", "required": True},
            "timeout": {"type": "integer", "min": 1, "max": 300},
            "environment": {"type": "string", "enum": ["dev", "test", "prod"]},
        }

        validator = ConfigValidator(schema)

        # 有效配置
        valid_config = {"app_name": "TestApp", "timeout": 30, "environment": "test"}
        errors = validator.validate(valid_config)
        assert len(errors) == 0

        # 无效配置 - 缺少必填字段
        invalid_config_1 = {"timeout": 30}
        errors = validator.validate(invalid_config_1)
        assert len(errors) == 1
        assert "缺少必需的配置项" in errors[0]

        # 无效配置 - 类型错误
        invalid_config_2 = {"app_name": "TestApp", "timeout": "not_a_number"}
        errors = validator.validate(invalid_config_2)
        assert len(errors) == 1
        assert "类型错误" in errors[0]

        # 无效配置 - 超出范围
        invalid_config_3 = {"app_name": "TestApp", "timeout": 500}
        errors = validator.validate(invalid_config_3)
        assert len(errors) == 1
        assert "值太大" in errors[0]


@pytest.mark.integration
class TestLoggingIntegration:
    """日志系统集成测试"""

    def test_logger_creation(self):
        """测试日志记录器创建"""
        from infra.logging.logger import Logger

        logger = Logger("TestLogger")
        assert logger is not None

        # 验证日志可以正常写入
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")

    def test_structured_logger(self):
        """测试结构化日志"""
        from infra.logging.structured_logger import StructuredLogger

        logger = StructuredLogger("TestStructuredLogger")

        # 结构化日志
        logger.info("User action", user_id=123, action="login")
        logger.error("System error", error_code=500, details="Database connection failed")

        assert logger is not None

    def test_logger_with_config(self, tmp_path):
        """测试日志与配置集成"""
        from infra.logging.logger import Logger
        from infra.config.config_manager import ConfigManager

        # 创建日志配置
        config_content = """
logging:
  level: DEBUG
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: test.log
"""
        config_file = tmp_path / "logging_config.yaml"
        config_file.write_text(config_content)

        # 加载配置
        manager = ConfigManager(str(tmp_path))
        manager.load_config("logging_config")

        # 使用配置创建日志
        log_config = manager.get_config("logging_config")
        assert "logging" in log_config


@pytest.mark.integration
class TestReportingIntegration:
    """报告系统集成测试"""

    def test_report_manager_creation(self):
        """测试报告管理器创建"""
        from infra.reporting.reporter import ReportManager

        reporter = ReportManager()
        assert reporter is not None

    def test_screenshot_on_failure(self):
        """测试失败截图功能"""
        from infra.reporting.screenshot_on_failure import ScreenshotManager

        manager = ScreenshotManager()
        assert manager is not None

        # 验证截图目录存在
        screenshot_dir = manager.screenshot_dir
        assert screenshot_dir.exists() or screenshot_dir.parent.exists()
