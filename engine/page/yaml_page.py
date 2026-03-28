"""YAML Page - drives page objects from YAML definitions"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from engine.page.base_page import BasePage
from core.finder.locator import Locator


class YamlPage(BasePage):
    """
    YAML 驱动的页面对象

    通过 YAML 文件定义页面元素，无需编写代码

    YAML 格式示例：
        elements:
          username_input:
            locator_type: id
            locator_value: txt_username
            control_type: Edit
            description: "用户名输入框"

          login_button:
            locator_type: name
            locator_value: 登录
            control_type: Button

    使用方式：
        >>> page = YamlPage.from_yaml("login_page.yaml")
        >>> page.open("app.exe")
        >>> page.set_window(page.get_window("Login"))
        >>> page.type_text(page.element("username_input"), "admin")
        >>> page.click(page.element("login_button"))
    """

    def __init__(self, yaml_path: Optional[str] = None):
        """
        初始化 YAML 页面对象

        Args:
            yaml_path: YAML 文件路径
        """
        super().__init__()
        self._yaml_path = yaml_path
        self._elements: Dict[str, Dict[str, Any]] = {}
        self._name = ""

        if yaml_path:
            self.load_yaml(yaml_path)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "YamlPage":
        """
        从 YAML 文件创建页面对象

        Args:
            yaml_path: YAML 文件路径

        Returns:
            YamlPage 实例
        """
        page = cls(yaml_path)
        return page

    def load_yaml(self, yaml_path: str) -> "YamlPage":
        """
        加载 YAML 文件

        Args:
            yaml_path: YAML 文件路径

        Returns:
            self: 支持链式调用
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"YAML 文件不存在：{yaml_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 验证 Schema
        self._validate_schema(data)

        # 加载元素定义
        self._elements = data.get("elements", {})
        self._name = path.stem

        return self

    def _validate_schema(self, data: dict):
        """验证 YAML Schema"""
        if "elements" not in data:
            raise ValueError("YAML 必须包含 'elements' 键")

        for name, element_def in data["elements"].items():
            if "locator_type" not in element_def:
                raise ValueError(f"元素 '{name}' 缺少 'locator_type'")
            if "locator_value" not in element_def:
                raise ValueError(f"元素 '{name}' 缺少 'locator_value'")

    def element(self, name: str) -> Locator:
        """
        获取元素定位器

        Args:
            name: 元素名称

        Returns:
            Locator 实例
        """
        if name not in self._elements:
            raise KeyError(f"元素 '{name}' 未定义")

        elem_def = self._elements[name]
        return Locator.from_yaml(elem_def)

    def element_description(self, name: str) -> str:
        """获取元素描述"""
        if name not in self._elements:
            raise KeyError(f"元素 '{name}' 未定义")
        return self._elements[name].get("description", name)

    def has_element(self, name: str) -> bool:
        """检查元素是否已定义"""
        return name in self._elements

    def get_all_elements(self) -> Dict[str, Dict[str, Any]]:
        """获取所有元素定义"""
        return self._elements.copy()

    @property
    def name(self) -> str:
        """获取页面名称"""
        return self._name
