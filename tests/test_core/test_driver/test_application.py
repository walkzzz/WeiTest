"""Tests for ApplicationDriver"""

import pytest
from unittest.mock import Mock, patch
from core.driver.application import ApplicationDriver, BackendType
from core.exceptions import ApplicationStartError, ApplicationConnectError, WindowNotFoundError


class TestApplicationDriver:
    """测试 ApplicationDriver 类"""

    def test_init_default_backend(self):
        """测试默认后端初始化"""
        driver = ApplicationDriver()
        assert driver.backend == BackendType.UIA
        assert driver.is_running is False

    def test_init_custom_backend(self):
        """测试自定义后端初始化"""
        driver = ApplicationDriver(backend=BackendType.WIN32)
        assert driver.backend == BackendType.WIN32

    @patch("core.driver.application.Application")
    def test_start_success(self, mock_app_class):
        """测试成功启动应用"""
        mock_app_instance = Mock()
        mock_app_instance.process = 1234

        mock_app_class.return_value.start.return_value = mock_app_instance
        mock_app_class.return_value.process = 1234

        driver = ApplicationDriver()
        result = driver.start("notepad.exe")

        assert result is driver  # 链式调用
        assert driver.is_running is True
        assert driver.process_id == 1234
        mock_app_class.return_value.start.assert_called_once_with("notepad.exe")

    @patch("core.driver.application.Application")
    def test_start_failure(self, mock_app_class):
        """测试启动失败"""
        mock_app_class.return_value.start.side_effect = Exception("启动失败")

        driver = ApplicationDriver()
        with pytest.raises(ApplicationStartError) as exc_info:
            driver.start("notepad.exe")

        assert "notepad.exe" in str(exc_info.value)
        assert "启动失败" in str(exc_info.value)

    @patch("core.driver.application.Application")
    def test_connect_by_title(self, mock_app_class):
        """测试通过标题连接"""
        mock_app = Mock()
        mock_app.process = 5678
        mock_app_class.return_value.connect.return_value = mock_app

        driver = ApplicationDriver()
        result = driver.connect(title="Notepad")

        assert result is driver
        assert driver.process_id == 5678

    @patch("core.driver.application.Application")
    def test_connect_by_process_id(self, mock_app_class):
        """测试通过进程 ID 连接"""
        mock_app = Mock()
        mock_app.process = 5678
        mock_app_class.return_value.connect.return_value = mock_app

        driver = ApplicationDriver()
        result = driver.connect(process_id=5678)

        assert result is driver
        assert driver.process_id == 5678

    def test_connect_no_params(self):
        """测试连接时不提供参数"""
        from core.exceptions import ApplicationConnectError

        driver = ApplicationDriver()
        with pytest.raises(ApplicationConnectError):
            driver.connect()

    def test_close(self):
        """测试关闭应用"""
        driver = ApplicationDriver()
        driver._app = Mock()
        driver._process_id = 1234

        driver.close()

        assert driver._app is None
        assert driver.process_id is None
        assert driver.is_running is False

    def test_get_window(self):
        """测试获取窗口"""
        driver = ApplicationDriver()
        driver._app = Mock()
        mock_window = Mock()
        driver._app.window.return_value = mock_window

        window = driver.get_window("Test Window")

        assert window is not None
        driver._app.window.assert_called_once_with(title="Test Window")

    def test_get_window_not_started(self):
        """测试获取窗口时应用未启动"""
        driver = ApplicationDriver()

        with pytest.raises(ApplicationConnectError, match="应用未启动"):
            driver.get_window("Test Window")

    def test_get_window_not_found(self):
        """测试窗口未找到"""
        driver = ApplicationDriver()
        driver._app = Mock()
        driver._app.window.side_effect = Exception("窗口不存在")

        with pytest.raises(WindowNotFoundError):
            driver.get_window("Nonexistent Window")

    def test_process_id_property(self):
        """测试进程 ID 属性"""
        driver = ApplicationDriver()
        assert driver.process_id is None

        driver._process_id = 1234
        assert driver.process_id == 1234

    def test_is_running_property(self):
        """测试运行状态属性"""
        driver = ApplicationDriver()
        assert driver.is_running is False

        driver._app = Mock()
        driver._process_id = 1234
        assert driver.is_running is True

        driver._app = None
        assert driver.is_running is False
