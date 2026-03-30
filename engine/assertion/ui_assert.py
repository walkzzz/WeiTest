"""UI Assertion - assertions for UI elements"""

from typing import TYPE_CHECKING

from wei.core.finder.locator import Locator

if TYPE_CHECKING:
    from engine.page.base_page import BasePage


class UIAssertion:
    """
    UI 断言

    用于验证 UI 元素的状态

    使用示例：
        >>> UIAssertion(page, ByID("lbl_error")).should_be_visible()
        >>> UIAssertion(page, ByID("btn_submit")).should_be_enabled()
        >>> UIAssertion(page, ByID("txt_title")).text_should_equal("欢迎")
    """

    def __init__(self, page: "BasePage", locator: Locator, description: str = ""):
        self.page = page
        self.locator = locator
        self.description = description or locator.value
        self._element = None

    def _get_element(self):
        if self._element is None:
            self._element = self.page.find_element(self.locator)
        return self._element

    # ========== 存在性断言 ==========

    def should_exist(self, timeout: int = 0) -> "UIAssertion":
        """断言元素存在"""
        from wei.core.waiter.smart_wait import SmartWait
        from wei.core.waiter.wait_condition import ExistsCondition

        passed = SmartWait(timeout).wait_for_condition(ExistsCondition(), self._get_element())
        if not passed:
            raise AssertionError(f"元素不存在：{self.description}")
        return self

    def should_not_exist(self) -> "UIAssertion":
        """断言元素不存在"""
        try:
            element = self._get_element()
            if hasattr(element, "exists") and element.exists():
                raise AssertionError(f"元素不应存在：{self.description}")
        except:
            pass  # 元素不存在，符合预期
        return self

    # ========== 可见性断言 ==========

    def should_be_visible(self, timeout: int = 10) -> "UIAssertion":
        """断言元素可见"""
        from wei.core.waiter.smart_wait import SmartWait
        from wei.core.waiter.wait_condition import VisibleCondition

        passed = SmartWait(timeout).wait_for_condition(VisibleCondition(), self._get_element())
        if not passed:
            raise AssertionError(f"元素不可见：{self.description}")
        return self

    # ========== 可用性断言 ==========

    def should_be_enabled(self) -> "UIAssertion":
        """断言元素可用"""
        if not self._get_element().is_enabled():
            raise AssertionError(f"元素不可用：{self.description}")
        return self

    def should_be_disabled(self) -> "UIAssertion":
        """断言元素不可用"""
        if self._get_element().is_enabled():
            raise AssertionError(f"元素应为禁用状态：{self.description}")
        return self

    # ========== 文本断言 ==========

    def text_should_equal(self, expected: str) -> "UIAssertion":
        """断言文本相等"""
        actual = self._get_element().window_text()
        if actual != expected:
            raise AssertionError(f"文本不匹配 - 期望：'{expected}', 实际：'{actual}'")
        return self

    def text_should_contain(self, expected: str) -> "UIAssertion":
        """断言文本包含"""
        actual = self._get_element().window_text()
        if expected not in actual:
            raise AssertionError(f"文本不包含 '{expected}' - 实际：'{actual}'")
        return self

    def text_should_not_be_empty(self) -> "UIAssertion":
        """断言文本不为空"""
        actual = self._get_element().window_text()
        if not actual or not actual.strip():
            raise AssertionError(f"文本不应为空：{self.description}")
        return self

    # ========== 链式调用 ==========

    def and_(self) -> "UIAssertion":
        """链式调用连接符"""
        return self
