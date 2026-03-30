"""业务测试示例 - 记事本应用"""

import pytest
from engine.page.yaml_page import YamlPage
from engine.component import Button, TextInput, Label
from engine.assertion import Assert
from wei.infra.logging import Logger, get_logger
from wei.infra.config import ConfigManager


class TestNotepad:
    """记事本应用测试"""

    @pytest.fixture
    def notepad_page(self):
        """测试夹具"""
        page = YamlPage.from_yaml("framework/pages/notepad_page.yaml")
        page.start_app("notepad.exe")
        page.set_window(page.get_window("无标题 - 记事本"))

        logger = get_logger("NotepadTest")
        logger.info("记事本已打开")

        yield page

        page.close()
        logger.info("测试完成")

    def test_notepad_launch(self, notepad_page):
        """测试记事本启动"""
        # 验证编辑区域存在
        Assert.ui(notepad_page, notepad_page.element("edit_area")).should_be_visible()

        # 验证菜单栏存在
        Assert.ui(notepad_page, notepad_page.element("menu_file")).should_be_visible()
        Assert.ui(notepad_page, notepad_page.element("menu_edit")).should_be_visible()

    def test_edit_area(self, notepad_page):
        """测试编辑区域"""
        edit = TextInput(notepad_page, notepad_page.element("edit_area"))

        # 输入文本
        test_text = "Hello, AutoTestMe-NG!"
        edit.type(test_text)

        # 验证文本已输入
        assert test_text in edit.value

    def test_status_bar(self, notepad_page):
        """测试状态栏"""
        # 验证状态栏存在
        Assert.ui(notepad_page, notepad_page.element("status_bar")).should_be_visible()

    def test_menu_items_exist(self, notepad_page):
        """测试菜单项存在"""
        # 验证所有菜单项存在
        Assert.ui(notepad_page, notepad_page.element("menu_file")).should_be_visible()
        Assert.ui(notepad_page, notepad_page.element("menu_edit")).should_be_visible()
        Assert.ui(notepad_page, notepad_page.element("menu_format")).should_be_visible()
