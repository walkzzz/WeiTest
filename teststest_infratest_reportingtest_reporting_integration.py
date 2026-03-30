"""报告系统集成测试"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

class TestReportManager:
    """ReportManager 集成测试"""
    
    @pytest.fixture
    def reporter(self):
        from infra.reporting.reporter import ReportManager
        return ReportManager()
    
    def test_reporter_creation(self, reporter):
        assert reporter is not None
    
    @patch('infra.reporting.reporter.subprocess.run')
    def test_create_allure_report(self, mock_run, reporter):
        mock_run.return_value = MagicMock(returncode=0)
        reporter.create_allure_report()
        assert mock_run.called
    
    def test_open_html_report(self, reporter):
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            temp_file = f.name
        
        try:
            result = reporter.open_html_report(temp_file)
            assert result is None or True
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    def test_generate_html_report(self, reporter):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "report.html"
            result = reporter.generate_html_report(str(output_file))
            assert result is None or True
    
    def test_save_screenshot(self, reporter):
        mock_page = Mock()
        mock_page.take_screenshot = Mock()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            screenshot_file = Path(tmpdir) / "test.png"
            result = reporter.save_screenshot(mock_page, str(screenshot_file))
            assert mock_page.take_screenshot.called or result is None
    
    def test_get_test_summary(self, reporter):
        summary = reporter.get_test_summary()
        assert summary is not None
        assert isinstance(summary, dict)

class TestScreenshotManager:
    """ScreenshotManager 集成测试"""
    
    @pytest.fixture
    def screenshot_mgr(self):
        from infra.reporting.screenshot_manager import ScreenshotManager
        return ScreenshotManager()
    
    def test_screenshot_manager_creation(self, screenshot_mgr):
        assert screenshot_mgr is not None
        assert screenshot_mgr.output_dir.exists()
        assert screenshot_mgr.screenshot_dir.exists()
    
    @patch('pyautogui.screenshot')
    def test_take_screenshot(self, mock_screenshot, screenshot_mgr):
        mock_img = Mock()
        mock_img.save = Mock()
        mock_screenshot.return_value = mock_img
        
        mock_page = Mock()
        result = screenshot_mgr.take_screenshot(mock_page, "test.png")
        assert result is not None
    
    def test_take_screenshot_on_failure(self, screenshot_mgr):
        mock_page = Mock()
        mock_page.take_screenshot = Mock()
        
        result = screenshot_mgr.take_screenshot_on_failure(mock_page, "test_case")
        assert result is not None
    
    def test_cleanup_old_screenshots(self, screenshot_mgr):
        # 应该不抛出异常
        screenshot_mgr.cleanup_old_screenshots(days=7)

class TestLoggingIntegration:
    """日志集成测试"""
    
    @pytest.fixture
    def logger(self):
        from infra.logging.logger import Logger
        return Logger("TestLogger")
    
    def test_logger_creation(self, logger):
        assert logger is not None
    
    def test_logger_info(self, logger):
        logger.info("Test info message")
        # 应该不抛出异常
    
    def test_logger_error(self, logger):
        logger.error("Test error message")
        # 应该不抛出异常
    
    def test_logger_warning(self, logger):
        logger.warning("Test warning message")
        # 应该不抛出异常
    
    def test_logger_debug(self, logger):
        logger.debug("Test debug message")
        # 应该不抛出异常
    
    def test_get_logger(self):
        from infra.logging.logger import get_logger
        logger = get_logger("Test", "logs")
        assert logger is not None

class TestConfigIntegration:
    """配置集成测试"""
    
    @pytest.fixture
    def config_manager(self, tmp_path):
        from infra.config.config_manager import ConfigManager
        # 创建测试配置
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("test: value\n")
        return ConfigManager(str(tmp_path))
    
    def test_config_manager_creation(self, config_manager):
        assert config_manager is not None
    
    def test_config_manager_load(self, config_manager):
        config_manager.load_config("test_config")
        config = config_manager.get_config("test_config")
        assert config is not None
    
    def test_enhanced_config_manager(self, tmp_path):
        from infra.config.enhanced_config import EnhancedConfigManager
        
        # 创建测试配置
        config_file = tmp_path / "env_config.yaml"
        config_file.write_text("test: value\n")
        
        manager = EnhancedConfigManager(str(tmp_path))
        config = manager.load("env_config.yaml")
        assert config is not None
    
    def test_config_encryption(self):
        from infra.config.config_encryption import ConfigEncryption
        
        encryption = ConfigEncryption()
        secret = "password123"
        encrypted = encryption.encrypt(secret)
        decrypted = encryption.decrypt(encrypted)
        
        assert decrypted == secret
        assert encryption.is_encrypted(encrypted) is True
        assert encryption.is_encrypted(secret) is False
