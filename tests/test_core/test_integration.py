"""Tests for Core layer integration"""

import pytest
from unittest.mock import Mock, patch

from core.driver.application import ApplicationDriver, BackendType
from core.driver.window import WindowDriver
from core.finder.locator import Locator, LocatorType, ByID
from core.finder.search_engine import SearchEngine
from core.waiter.wait_condition import VisibleCondition, ExistsCondition
from core.waiter.smart_wait import SmartWait
from core.exceptions import ElementNotFoundError


class TestCoreIntegration:
    """测试 Core 层各模块集成"""

    def test_driver_finder_integration(self):
        """测试 Driver 和 Finder 集成"""
        # 模拟 ApplicationDriver
        with patch("core.driver.application.Application") as mock_app_class:
            mock_app = Mock()
            mock_app.process = 1234
            mock_app_class.return_value = mock_app

            # 创建 driver
            driver = ApplicationDriver()
            driver.start("test.exe")

            # 模拟窗口
            mock_window = Mock()
            driver._app.window.return_value = mock_window

            # 获取 WindowDriver
            window = driver.get_window("Test Window")

            # 验证窗口获取
            assert window is not None
            assert isinstance(window, WindowDriver)

    def test_finder_waiter_integration(self):
        """测试 Finder 和 Waiter 集成"""
        # 模拟窗口和元素
        mock_pw_window = Mock()
        mock_element = Mock()
        mock_element.exists.return_value = True

        # 配置 SearchEngine 返回元素
        mock_pw_window.child_window.return_value = mock_element

        window = WindowDriver(mock_pw_window)
        search_engine = SearchEngine(window)

        # 使用 Waiter 等待元素
        waiter = SmartWait(timeout=2, poll_interval=0.1)

        locator = ByID("test_element")

        # 应该成功找到元素
        result = waiter.wait_for_element(locator, search_engine)
        assert result is not None

    def test_full_element_location_flow(self):
        """测试完整的元素定位流程"""
        # 模拟 pywinauto 窗口
        mock_pw_window = Mock()
        mock_element = Mock()
        mock_element.exists.return_value = True
        mock_element.is_visible.return_value = True

        mock_pw_window.child_window.return_value = mock_element

        # 创建 WindowDriver
        window = WindowDriver(mock_pw_window)

        # 创建 SearchEngine
        search_engine = SearchEngine(window, timeout=5)

        # 查找元素
        locator = ByID("btn_test", control_type="Button")
        element = search_engine.find(locator)

        # 验证
        assert element is not None
        mock_pw_window.child_window.assert_called_once_with(
            auto_id="btn_test", control_type="Button"
        )

    def test_element_not_found_flow(self):
        """测试元素未找到的异常流程"""
        mock_pw_window = Mock()
        mock_pw_window.child_window.side_effect = Exception("Element not found")

        window = WindowDriver(mock_pw_window)
        search_engine = SearchEngine(window, timeout=2)

        locator = ByID("nonexistent")

        with pytest.raises(ElementNotFoundError):
            search_engine.find(locator)

    def test_wait_condition_with_real_element(self):
        """测试等待条件与真实元素"""
        # 模拟元素生命周期
        mock_element = Mock()
        mock_element.exists.return_value = False  # 初始不存在

        call_count = 0

        def simulate_element_appearance():
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                mock_element.exists.return_value = True
            return mock_element.exists.return_value

        # 使用 Waiter 等待元素出现
        waiter = SmartWait(timeout=2, poll_interval=0.1)

        def condition():
            return simulate_element_appearance()

        result = waiter.wait_until(condition)
        assert result is True
        assert call_count == 3

    def test_backend_switching(self):
        """测试后端切换"""
        from core.driver.backend import BackendManager

        # 获取 UIA 后端
        uia_backend = BackendManager.get_backend(BackendType.UIA)
        assert uia_backend.get_backend_name() == "uia"

        # 获取 Win32 后端
        win32_backend = BackendManager.get_backend(BackendType.WIN32)
        assert win32_backend.get_backend_name() == "win32"

        # 验证单例
        uia_backend2 = BackendManager.get_backend(BackendType.UIA)
        assert uia_backend is uia_backend2

    def test_locator_to_dict_roundtrip(self):
        """测试 Locator 序列化和反序列化"""
        # 创建 Locator
        original = Locator(type=LocatorType.ID, value="test_id", control_type="Button", timeout=15)

        # 转换为字典
        data = original.to_dict()

        # 从 YAML 格式重建
        yaml_format = {
            "locator_type": data["type"],
            "locator_value": data["value"],
            "control_type": data.get("control_type"),
            "timeout": data.get("timeout"),
        }

        restored = Locator.from_yaml(yaml_format)

        # 验证
        assert restored.type == original.type
        assert restored.value == original.value
        assert restored.control_type == original.control_type
        assert restored.timeout == original.timeout

    def test_search_engine_exists_method(self):
        """测试 SearchEngine.exists() 方法"""
        mock_pw_window = Mock()
        mock_element = Mock()
        mock_element.exists.return_value = True

        mock_pw_window.child_window.return_value = mock_element

        window = WindowDriver(mock_pw_window)
        search_engine = SearchEngine(window)

        locator = ByID("test")
        result = search_engine.exists(locator)

        assert result is True

    def test_search_engine_exists_not_found(self):
        """测试 SearchEngine.exists() 元素不存在"""
        mock_pw_window = Mock()
        mock_pw_window.child_window.side_effect = Exception("Not found")

        window = WindowDriver(mock_pw_window)
        search_engine = SearchEngine(window)

        locator = ByID("nonexistent")
        result = search_engine.exists(locator, timeout=0)

        assert result is False

    def test_chainable_window_operations(self):
        """测试窗口操作的链式调用"""
        mock_pw_window = Mock()
        window = WindowDriver(mock_pw_window)

        # 链式调用
        result = window.maximize().minimize().restore()

        # 验证是同一个实例
        assert result is window

        # 验证方法都被调用了
        assert mock_pw_window.maximize.called
        assert mock_pw_window.minimize.called
        assert mock_pw_window.restore.called

    def test_application_lifecycle(self):
        """测试应用生命周期管理"""
        with patch("core.driver.application.Application") as mock_app_class:
            mock_app_instance = Mock()
            mock_app_instance.process = 1234

            mock_app_class.return_value.start.return_value = mock_app_instance
            mock_app_class.return_value.process = 1234

            driver = ApplicationDriver()

            # 初始状态
            assert driver.is_running is False
            assert driver.process_id is None

            # 启动
            driver.start("test.exe")
            assert driver.is_running is True
            assert driver.process_id == 1234

            # 关闭
            driver.close()
            assert driver.is_running is False
            assert driver.process_id is None

    def test_smart_wait_custom_timeout(self):
        """测试自定义超时时间"""
        waiter = SmartWait(timeout=10, poll_interval=0.1)

        call_count = 0

        def quick_condition():
            nonlocal call_count
            call_count += 1
            return call_count >= 2

        # 使用更短的超时
        result = waiter.wait_until(quick_condition, timeout=1)
        assert result is True

    def test_locator_immutability_in_search(self):
        """测试 Locator 在搜索中的不可变性"""
        mock_pw_window = Mock()
        mock_element = Mock()
        mock_pw_window.child_window.return_value = mock_element

        window = WindowDriver(mock_pw_window)
        search_engine = SearchEngine(window)

        # 创建不可变 Locator
        locator = ByID("test_btn")
        original_value = locator.value

        # 执行搜索
        try:
            search_engine.find(locator)
        except:
            pass

        # 验证 Locator 未被修改
        assert locator.value == original_value
        assert locator.type == LocatorType.ID


class TestCoreExceptionHandling:
    """测试 Core 层异常处理"""

    def test_application_start_error(self):
        """测试应用启动异常"""
        from core.exceptions import ApplicationStartError

        with patch("core.driver.application.Application") as mock_app_class:
            mock_app_class.return_value.start.side_effect = Exception("Failed")

            driver = ApplicationDriver()

            with pytest.raises(ApplicationStartError) as exc_info:
                driver.start("test.exe")

            assert "test.exe" in str(exc_info.value)

    def test_window_not_found_error(self):
        """测试窗口未找到异常"""
        from core.exceptions import WindowNotFoundError

        with patch("core.driver.application.Application") as mock_app_class:
            mock_app = Mock()
            mock_app_class.return_value = mock_app

            driver = ApplicationDriver()
            driver.start("test.exe")

            driver._app.window.side_effect = Exception("Window not found")

            with pytest.raises(WindowNotFoundError):
                driver.get_window("Nonexistent")

    def test_invalid_locator_error(self):
        """测试无效定位器异常"""
        from core.exceptions import InvalidLocatorError

        # Locator 应该在创建时验证
        with pytest.raises(ValueError):
            Locator(LocatorType.ID, "")


class TestCoreDataFlow:
    """测试 Core 层数据流"""

    def test_locator_yaml_roundtrip(self):
        """测试 Locator YAML 往返转换"""
        import yaml

        # 创建 Locator
        locator = Locator(
            type=LocatorType.NAME, value="登录按钮", control_type="Button", timeout=10
        )

        # 转换为 YAML
        yaml_data = locator.to_dict()

        # 模拟 YAML 文件内容（添加 locator_type 以匹配 from_yaml 期望的格式）
        yaml_data_with_keys = {
            "locator_type": yaml_data["type"],
            "locator_value": yaml_data["value"],
            "control_type": yaml_data.get("control_type"),
            "timeout": yaml_data.get("timeout"),
        }

        # 从 YAML 加载
        restored = Locator.from_yaml(yaml_data_with_keys)

        # 验证
        assert restored.type == locator.type
        assert restored.value == locator.value
        assert restored.control_type == locator.control_type
        assert restored.timeout == locator.timeout

    def test_search_engine_timeout_propagation(self):
        """测试 SearchEngine 超时传递"""
        mock_pw_window = Mock()
        window = WindowDriver(mock_pw_window)

        # 自定义超时
        search_engine = SearchEngine(window, timeout=20)

        # 验证 timeout 属性
        assert search_engine.timeout == 20

    def test_waiter_poll_interval(self):
        """测试 Waiter 轮询间隔"""
        waiter = SmartWait(timeout=2, poll_interval=0.05)

        call_count = 0
        start_time = __import__("time").time()

        def condition():
            nonlocal call_count
            call_count += 1
            return call_count >= 5

        waiter.wait_until(condition)

        elapsed = __import__("time").time() - start_time

        # 验证轮询间隔大致正确（允许误差）
        expected_min = 5 * 0.05  # 4 次等待 × 0.05 秒
        assert elapsed >= expected_min * 0.8  # 80% 容差
