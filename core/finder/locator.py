"""Element Locator - type-safe element location definition"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class LocatorType(Enum):
    """定位方式枚举"""

    ID = "id"
    NAME = "name"
    CLASS_NAME = "class_name"
    AUTOMATION_ID = "automation_id"
    XPATH = "xpath"
    CONTROL_TYPE = "control_type"
    BEST_MATCH = "best_match"


@dataclass(frozen=True)
class Locator:
    """
    定位器

    不可变的数据类，确保定位信息在查找过程中不被修改

    Attributes:
        type: 定位方式
        value: 定位值
        control_type: 控件类型（可选，用于精确匹配）
        timeout: 自定义超时时间（可选）

    Example:
        >>> locator = Locator(LocatorType.ID, "btn_login")
        >>> locator = Locator(
        ...     type=LocatorType.NAME,
        ...     value="登录",
        ...     control_type="Button",
        ...     timeout=10
        ... )
    """

    type: LocatorType
    value: str
    control_type: Optional[str] = None
    timeout: Optional[int] = None

    def __post_init__(self):
        """验证定位器有效性"""
        if not self.value or not self.value.strip():
            raise ValueError("定位值不能为空")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（用于 YAML 加载）"""
        result: Dict[str, Any] = {"type": self.type.value, "value": self.value}
        if self.control_type:
            result["control_type"] = self.control_type
        if self.timeout:
            result["timeout"] = self.timeout
        return result

    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "Locator":
        """
        从 YAML 数据创建定位器

        Args:
            data: YAML 中定义的元素信息

        Returns:
            Locator 实例
        """
        return cls(
            type=LocatorType(data["locator_type"]),
            value=data["locator_value"],
            control_type=data.get("control_type"),
            timeout=data.get("timeout"),
        )


# ========== 便捷创建函数 ==========


def ByID(value: str, control_type: Optional[str] = None) -> Locator:
    """通过 ID 定位"""
    return Locator(LocatorType.ID, value, control_type)


def ByName(value: str, control_type: Optional[str] = None) -> Locator:
    """通过名称定位"""
    return Locator(LocatorType.NAME, value, control_type)


def ByClassName(value: str) -> Locator:
    """通过类名定位"""
    return Locator(LocatorType.CLASS_NAME, value)


def ByAutomationID(value: str, control_type: Optional[str] = None) -> Locator:
    """通过 Automation ID 定位"""
    return Locator(LocatorType.AUTOMATION_ID, value, control_type)


def ByXPath(value: str) -> Locator:
    """通过 XPath 定位"""
    return Locator(LocatorType.XPATH, value)
