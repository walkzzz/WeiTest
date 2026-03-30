"""业务测试示例 - 计算器应用"""

import pytest
from engine.page.yaml_page import YamlPage
from engine.component import Button, Label
from engine.assertion import Assert
from wei.infra.logging import get_logger


class TestCalculator:
    """计算器应用测试"""

    @pytest.fixture
    def calc_page(self):
        """测试夹具"""
        page = YamlPage.from_yaml("framework/pages/calculator_page.yaml")
        page.start_app("calc.exe")
        page.set_window(page.get_window("计算器"))

        logger = get_logger("CalculatorTest")
        logger.info("计算器已打开")

        yield page

        page.close()
        logger.info("测试完成")

    def test_calculator_launch(self, calc_page):
        """测试计算器启动"""
        # 验证数字按钮存在
        Assert.ui(calc_page, calc_page.element("btn_0")).should_be_visible()
        Assert.ui(calc_page, calc_page.element("btn_1")).should_be_visible()
        Assert.ui(calc_page, calc_page.element("btn_2")).should_be_visible()

    def test_number_buttons_exist(self, calc_page):
        """测试所有数字按钮存在"""
        for i in range(4):
            btn_name = f"btn_{i}"
            Assert.ui(calc_page, calc_page.element(btn_name)).should_be_visible()

    def test_operator_buttons_exist(self, calc_page):
        """测试运算符按钮存在"""
        operators = ["btn_add", "btn_subtract", "btn_multiply", "btn_divide"]

        for op in operators:
            Assert.ui(calc_page, calc_page.element(op)).should_be_visible()

    def test_equals_button_exists(self, calc_page):
        """测试等于按钮存在"""
        Assert.ui(calc_page, calc_page.element("btn_equals")).should_be_visible()
        Assert.ui(calc_page, calc_page.element("btn_equals")).should_be_enabled()

    def test_clear_button_exists(self, calc_page):
        """测试清除按钮存在"""
        Assert.ui(calc_page, calc_page.element("btn_clear")).should_be_visible()
        Assert.ui(calc_page, calc_page.element("btn_clear")).should_be_enabled()
