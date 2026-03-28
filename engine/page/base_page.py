"""Base Page - combines all mixins into a single page object"""

from typing import Optional

from engine.page.mixins.application_mixin import ApplicationMixin
from engine.page.mixins.element_mixin import ElementMixin
from engine.page.mixins.action_mixin import ActionMixin
from engine.page.mixins.screenshot_mixin import ScreenshotMixin


class BasePage(ApplicationMixin, ElementMixin, ActionMixin, ScreenshotMixin):
    """
    页面对象基类

    组合所有 Mixin，提供完整的页面操作能力

    使用示例：
        class LoginPage(BasePage):
            def __init__(self):
                super().__init__()

            def open(self, app_path: str):
                self.start_app(app_path)
                self.set_window(self.get_window("登录"))
                return self

            def login(self, username: str, password: str):
                self.type_text(self.username_input, username)
                self.type_text(self.password_input, password)
                self.click(self.login_button)
                return self
    """

    def __init__(self, timeout: int = 10):
        """
        初始化页面对象

        Args:
            timeout: 默认超时时间
        """
        self.timeout = timeout
        self._window = None
        self._app_driver = None

    def close(self):
        """关闭页面（清理资源）"""
        self.close_app()

    # ========== 生命周期钩子 ==========

    def on_load(self):
        """
        页面加载钩子

        子类可重写此方法执行页面加载后的初始化
        """
        pass

    def on_unload(self):
        """
        页面卸载钩子

        子类可重写此方法执行页面关闭前的清理
        """
        pass
