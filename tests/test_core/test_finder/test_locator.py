"""Tests for Locator class"""

import pytest
from core.finder.locator import (
    Locator,
    LocatorType,
    ByID,
    ByName,
    ByClassName,
    ByAutomationID,
    ByXPath,
)


class TestLocator:
    """测试 Locator 类"""

    def test_create_locator(self):
        """测试创建定位器"""
        locator = Locator(LocatorType.ID, "btn_login")
        assert locator.type == LocatorType.ID
        assert locator.value == "btn_login"

    def test_create_locator_with_control_type(self):
        """测试创建带控件类型的定位器"""
        locator = Locator(type=LocatorType.NAME, value="登录", control_type="Button")
        assert locator.control_type == "Button"

    def test_create_locator_with_timeout(self):
        """测试创建带超时的定位器"""
        locator = Locator(type=LocatorType.ID, value="btn_submit", timeout=15)
        assert locator.timeout == 15

    def test_create_locator_empty_value_raises(self):
        """测试空值抛出异常"""
        with pytest.raises(ValueError):
            Locator(LocatorType.ID, "")

    def test_create_locator_whitespace_value_raises(self):
        """测试空白值抛出异常"""
        with pytest.raises(ValueError):
            Locator(LocatorType.ID, "   ")

    def test_from_yaml(self):
        """测试从 YAML 创建"""
        yaml_data = {"locator_type": "id", "locator_value": "txt_user", "control_type": "Edit"}
        locator = Locator.from_yaml(yaml_data)
        assert locator.type == LocatorType.ID
        assert locator.value == "txt_user"
        assert locator.control_type == "Edit"

    def test_from_yaml_minimal(self):
        """测试从 YAML 创建（最小字段）"""
        yaml_data = {"locator_type": "name", "locator_value": "登录"}
        locator = Locator.from_yaml(yaml_data)
        assert locator.type == LocatorType.NAME
        assert locator.value == "登录"
        assert locator.control_type is None

    def test_to_dict(self):
        """测试转换为字典"""
        locator = Locator(LocatorType.ID, "btn_login", control_type="Button")
        result = locator.to_dict()
        assert result == {"type": "id", "value": "btn_login", "control_type": "Button"}

    def test_to_dict_minimal(self):
        """测试转换为字典（最小字段）"""
        locator = Locator(LocatorType.NAME, "登录")
        result = locator.to_dict()
        assert result == {"type": "name", "value": "登录"}

    def test_to_dict_with_timeout(self):
        """测试转换为字典（含超时）"""
        locator = Locator(LocatorType.ID, "btn", timeout=20)
        result = locator.to_dict()
        assert "timeout" in result
        assert result["timeout"] == 20

    def test_immutability(self):
        """测试不可变性"""
        locator = Locator(LocatorType.ID, "btn")
        with pytest.raises(Exception):
            locator.value = "new_value"


class TestLocatorFunctions:
    """测试便捷函数"""

    def test_by_id(self):
        locator = ByID("btn_login")
        assert locator.type == LocatorType.ID
        assert locator.value == "btn_login"

    def test_by_id_with_control_type(self):
        locator = ByID("btn_login", control_type="Button")
        assert locator.control_type == "Button"

    def test_by_name(self):
        locator = ByName("登录")
        assert locator.type == LocatorType.NAME
        assert locator.value == "登录"

    def test_by_name_with_control_type(self):
        locator = ByName("登录", control_type="Button")
        assert locator.control_type == "Button"

    def test_by_class_name(self):
        locator = ByClassName("Edit")
        assert locator.type == LocatorType.CLASS_NAME
        assert locator.value == "Edit"

    def test_by_automation_id(self):
        locator = ByAutomationID("auto_id_123")
        assert locator.type == LocatorType.AUTOMATION_ID
        assert locator.value == "auto_id_123"

    def test_by_xpath(self):
        locator = ByXPath("/Button")
        assert locator.type == LocatorType.XPATH
        assert locator.value == "/Button"
