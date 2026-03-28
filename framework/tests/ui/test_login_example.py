"""Engine Layer Integration Test Example"""

import pytest
from engine.page.yaml_page import YamlPage
from engine.component.button import Button
from engine.component.input import TextInput
from engine.component.checkbox import CheckBox
from engine.component.label import Label
from engine.assertion import Assert
from core.finder.locator import ByID, ByName


class TestLoginIntegration:
    """登录集成测试示例"""

    @pytest.fixture
    def login_page(self):
        """登录页面 fixture"""
        page = YamlPage.from_yaml("framework/pages/login_page.yaml")
        page.start_app("notepad.exe")  # 使用记事本作为示例
        page.set_window(page.get_window("无标题 - 记事本"))
        page.on_load()
        yield page
        page.close()

    def test_yaml_page_load(self, login_page):
        """测试 YAML 页面加载"""
        # 验证页面加载成功
        assert login_page.has_element("username_input")
        assert login_page.has_element("login_button")
        assert login_page.name == "login_page"

    def test_component_button(self, login_page):
        """测试按钮组件"""
        # 创建按钮组件
        btn = Button(login_page, login_page.element("login_button"))

        # 验证按钮属性
        assert btn.is_enabled is True
        assert btn.is_visible is True
        assert btn.is_clickable is True

    def test_component_input(self, login_page):
        """测试输入框组件"""
        # 创建输入框组件
        input_box = TextInput(login_page, login_page.element("username_input"))

        # 输入文本
        input_box.type("test_user")

        # 验证输入
        assert input_box.value == "test_user"
        assert input_box.is_editable is True

    def test_component_checkbox(self, login_page):
        """测试复选框组件"""
        # 创建复选框组件
        chk = CheckBox(login_page, login_page.element("remember_checkbox"))

        # 切换状态
        initial_state = chk.is_checked
        chk.toggle()
        assert chk.is_checked != initial_state

        # 恢复状态
        chk.toggle()
        assert chk.is_checked == initial_state

    def test_assertion_ui(self, login_page):
        """测试 UI 断言"""
        # 测试元素存在
        Assert.ui(login_page, login_page.element("login_button")).should_exist()

        # 测试元素可见
        Assert.ui(login_page, login_page.element("username_input")).should_be_visible()

        # 测试元素可用
        Assert.ui(login_page, login_page.element("login_button")).should_be_enabled()

    def test_assertion_chain(self, login_page):
        """测试链式断言"""
        # 获取页面标题
        title = "Test"

        # 链式断言
        (Assert.that(title).is_not_none().is_not_empty())

    def test_full_login_flow(self, login_page):
        """测试完整登录流程"""
        # 使用组件
        username = TextInput(login_page, login_page.element("username_input"))
        password = TextInput(login_page, login_page.element("password_input"))
        login_btn = Button(login_page, login_page.element("login_button"))
        remember = CheckBox(login_page, login_page.element("remember_checkbox"))

        # 执行登录操作
        username.type("admin")
        password.type("password123")
        remember.check()
        login_btn.click()

        # 验证操作成功（这里用记事本验证，实际应用中验证登录后的页面）
        Assert.ui(login_page, login_page.element("username_input")).should_be_visible()

    def test_error_handling(self, login_page):
        """测试错误处理"""
        # 测试不存在的元素
        with pytest.raises(KeyError):
            login_page.element("nonexistent_element")

        # 测试窗口未初始化
        page = YamlPage()
        with pytest.raises(RuntimeError):
            page.find_element(ByID("test"))

    def test_screenshot(self, login_page):
        """测试截图功能"""
        # 截取屏幕
        filepath = login_page.take_screenshot("test_screenshot.png")

        # 验证截图文件存在
        import os

        assert os.path.exists(filepath)

    def test_chainable_operations(self, login_page):
        """测试链式调用"""
        # 测试按钮链式调用
        btn = Button(login_page, login_page.element("login_button"))
        result = btn.wait_clickable().click()
        assert result is btn

        # 测试输入框链式调用
        input_box = TextInput(login_page, login_page.element("username_input"))
        result = input_box.clear().type("test")
        assert result is input_box


class TestComponentIntegration:
    """组件集成测试"""

    @pytest.fixture
    def page(self):
        """测试页面"""
        page = YamlPage.from_yaml("framework/pages/login_page.yaml")
        page.start_app("notepad.exe")
        page.set_window(page.get_window("无标题 - 记事本"))
        yield page
        page.close()

    def test_button_and_input_together(self, page):
        """测试按钮和输入框配合"""
        username = TextInput(page, page.element("username_input"))
        login_btn = Button(page, page.element("login_button"))

        # 输入后点击
        username.type("user123")
        login_btn.click()

        # 验证
        Assert.ui(page, page.element("username_input")).should_be_visible()

    def test_checkbox_and_button_together(self, page):
        """测试复选框和按钮配合"""
        remember = CheckBox(page, page.element("remember_checkbox"))
        login_btn = Button(page, page.element("login_button"))

        # 勾选后点击
        remember.check()
        assert remember.is_checked is True
        login_btn.click()

    def test_label_display(self, page):
        """测试标签显示"""
        label = Label(page, page.element("title_label"))

        # 验证标签属性
        assert label.is_visible is True
        # 注意：实际文本需要根据具体应用验证
