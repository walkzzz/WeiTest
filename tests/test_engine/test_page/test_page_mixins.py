"""Page Mixin 完整测试"""
import pytest
from unittest.mock import Mock, patch, mock_open
from engine.page.mixins.action_mixin import ActionMixin
from engine.page.mixins.application_mixin import ApplicationMixin
from engine.page.mixins.element_mixin import ElementMixin
from engine.page.mixins.screenshot_mixin import ScreenshotMixin
from core.finder.locator import ByID

class TestActionMixin:
    """ActionMixin 测试"""
    
    @pytest.fixture
    def mixin(self):
        mixin = ActionMixin()
        mixin._window = Mock()
        return mixin
    
    def test_click(self, mixin):
        locator = ByID("btn_test")
        mixin.click(locator)
        assert mixin._window.click.called
    
    def test_double_click(self, mixin):
        locator = ByID("btn_test")
        mixin.double_click(locator)
        assert mixin._window.double_click.called
    
    def test_right_click(self, mixin):
        locator = ByID("btn_test")
        mixin.right_click(locator)
        assert mixin._window.right_click.called
    
    def test_type_text(self, mixin):
        locator = ByID("inp_test")
        mixin.type_text(locator, "test")
        assert mixin._window.type_text.called
    
    def test_clear_text(self, mixin):
        locator = ByID("inp_test")
        mixin.clear_text(locator)
        assert mixin._window.clear_text.called

class TestApplicationMixin:
    """ApplicationMixin 测试"""
    
    @pytest.fixture
    def mixin(self):
        mixin = ApplicationMixin()
        mixin._app = Mock()
        return mixin
    
    def test_start_app(self, mixin):
        mixin.start_app("notepad.exe")
        assert mixin._app.start.called
    
    def test_close_app(self, mixin):
        mixin.close_app()
        assert mixin._app.kill.called if hasattr(mixin._app, 'kill') else True
    
    def test_get_window(self, mixin):
        mixin._app.top_window.return_value = Mock()
        window = mixin.get_window("title")
        assert window is not None

class TestElementMixin:
    """ElementMixin 测试"""
    
    @pytest.fixture
    def mixin(self):
        mixin = ElementMixin()
        mixin._window = Mock()
        return mixin
    
    def test_find_element(self, mixin):
        locator = ByID("btn_test")
        mixin.find_element(locator)
        assert mixin._window.child_window.called
    
    def test_element_exists(self, mixin):
        locator = ByID("btn_test")
        mixin._window.child_window.side_effect = Exception("not found")
        exists = mixin.element_exists(locator, timeout=0)
        assert exists is False
    
    def test_get_element_text(self, mixin):
        locator = ByID("lbl_test")
        mock_elem = Mock()
        mock_elem.window_text.return_value = "Text"
        mixin._window.child_window.return_value = mock_elem
        text = mixin.get_element_text(locator)
        assert text == "Text"

class TestScreenshotMixin:
    """ScreenshotMixin 测试"""
    
    @pytest.fixture
    def mixin(self):
        mixin = ScreenshotMixin()
        mixin._window = Mock()
        return mixin
    
    @patch('engine.page.mixins.screenshot_mixin.pyautogui')
    def test_take_screenshot(self, mock_gui, mixin):
        mock_img = Mock()
        mock_gui.screenshot.return_value = mock_img
        mixin.take_screenshot("test.png")
        assert mock_gui.screenshot.called
    
    def test_wait_element(self, mixin):
        locator = ByID("btn_test")
        mock_elem = Mock()
        mixin._window.child_window.return_value = mock_elem
        elem = mixin.wait_element(locator, timeout=1)
        assert elem is not None
