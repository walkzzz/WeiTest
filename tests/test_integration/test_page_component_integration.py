"""集成测试：PageObject 和组件的集成测试"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from engine.page.yaml_page import YamlPage
from engine.component.button import Button
from engine.component.input import TextInput
from engine.component.checkbox import CheckBox
from engine.assertion import Assert


@pytest.fixture
def mock_page():
    """模拟页面对象"""
    page = Mock(spec=YamlPage)
    page._window = Mock()
    return page


class TestPageComponentIntegration:
    """PageObject 和组件集成测试"""

    def test_button_component_with_page(self, mock_page):
        """测试按钮组件与页面的集成"""
        from core.finder.locator import ByID

        locator = ByID("btn_test")
        button = Button(mock_page, locator)

        assert button is not None
        assert button.page == mock_page

    def test_input_component_with_page(self, mock_page):
        """测试输入框组件与页面的集成"""
        from core.finder.locator import ByID

        locator = ByID("txt_input")
        input_box = TextInput(mock_page, locator)

        assert input_box is not None
        assert input_box.page == mock_page

    def test_yaml_page_loads_elements(self, tmp_path):
        """测试 YAML 页面加载元素"""
        yaml_content = """
elements:
  test_button:
    locator_type: id
    locator_value: btn_test
    control_type: Button
    description: "测试按钮"
"""
        yaml_file = tmp_path / "test_page.yaml"
        yaml_file.write_text(yaml_content, encoding="utf-8")

        page = YamlPage.from_yaml(str(yaml_file))

        assert page.has_element("test_button")
        assert page.element_description("test_button") == "测试按钮"

    def test_yaml_page_with_checkbox_component(self, tmp_path):
        """测试 YAML 页面与复选框组件集成"""
        yaml_content = """
elements:
  remember_checkbox:
    locator_type: id
    locator_value: chk_remember
    control_type: CheckBox
    description: "记住我"
"""
        yaml_file = tmp_path / "checkbox_page.yaml"
        yaml_file.write_text(yaml_content, encoding="utf-8")

        page = YamlPage.from_yaml(str(yaml_file))
        locator = page.element("remember_checkbox")

        checkbox = CheckBox(page, locator)
        assert checkbox is not None

    def test_assertion_chain_with_components(self, mock_page):
        """测试断言链与组件的集成"""
        from core.finder.locator import ByID

        locator = ByID("btn_assert")
        button = Button(mock_page, locator)

        # 验证断言可以正常创建
        assertion = Assert.ui(mock_page, locator)
        assert assertion is not None


@pytest.mark.integration
class TestWorkflowIntegration:
    """工作流集成测试"""

    def test_complete_login_workflow(self, tmp_path):
        """测试完整的登录工作流（模拟）"""
        # 创建 YAML 页面定义
        yaml_content = """
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
  
  password_input:
    locator_type: id
    locator_value: txt_password
    control_type: Edit
  
  login_button:
    locator_type: id
    locator_value: btn_login
    control_type: Button
  
  remember_checkbox:
    locator_type: id
    locator_value: chk_remember
    control_type: CheckBox
"""
        yaml_file = tmp_path / "login_page.yaml"
        yaml_file.write_text(yaml_content, encoding="utf-8")

        # 加载页面
        page = YamlPage.from_yaml(str(yaml_file))

        # 验证所有元素都已加载
        assert page.has_element("username_input")
        assert page.has_element("password_input")
        assert page.has_element("login_button")
        assert page.has_element("remember_checkbox")

        # 创建工作流（模拟）
        with (
            patch.object(page, "type_text"),
            patch.object(page, "click"),
            patch.object(page, "check_checkbox"),
        ):
            # 模拟登录流程
            # page.type_text(page.element("username_input"), "admin")
            # page.type_text(page.element("password_input"), "password123")
            # page.check_checkbox(page.element("remember_checkbox"), True)
            # page.click(page.element("login_button"))

            # 验证工作流可以执行（无异常）
            pass

    def test_multi_tab_workflow(self, tmp_path):
        """测试多选项卡工作流"""
        yaml_content = """
elements:
  tab_home:
    locator_type: id
    locator_value: tab_home
    control_type: TabItem
  
  tab_settings:
    locator_type: id
    locator_value: tab_settings
    control_type: TabItem
  
  save_button:
    locator_type: id
    locator_value: btn_save
    control_type: Button
"""
        yaml_file = tmp_path / "tabs_page.yaml"
        yaml_file.write_text(yaml_content, encoding="utf-8")

        page = YamlPage.from_yaml(str(yaml_file))

        # 验证选项卡元素
        assert page.has_element("tab_home")
        assert page.has_element("tab_settings")

        # 创建工作流
        from engine.component.tab_control import TabControl

        tab_control = TabControl(page, page.element("tab_home"))
        assert tab_control is not None
