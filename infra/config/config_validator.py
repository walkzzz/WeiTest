"""Configuration Validator - validates configuration schemas"""

from pathlib import Path
from typing import Any, Dict, List


class ConfigValidator:
    """配置验证器"""

    def __init__(self, schema: Dict[str, Any]) -> None:
        """
        初始化验证器

        Args:
            schema: 验证模式
        """
        self.schema = schema

    def validate(self, config: Dict[str, Any]) -> List[str]:
        """
        验证配置

        Args:
            config: 配置字典

        Returns:
            错误消息列表
        """
        errors = []

        for key, rules in self.schema.items():
            value = config.get(key)

            # 检查必填字段
            if rules.get("required", False) and key not in config:
                errors.append(f"缺少必需的配置项：{key}")
                continue

            if value is None:
                continue

            # 类型检查
            expected_type = rules.get("type")
            if expected_type:
                if not isinstance(value, self._get_type_class(expected_type)):
                    errors.append(f"配置项 '{key}' 类型错误，期望 {expected_type}")
                    continue

            # 范围检查
            if expected_type == "integer":
                min_val = rules.get("min")
                max_val = rules.get("max")

                if min_val is not None and value < min_val:
                    errors.append(f"配置项 '{key}' 值太小，最小值为 {min_val}")

                if max_val is not None and value > max_val:
                    errors.append(f"配置项 '{key}' 值太大，最大值为 {max_val}")

            # 枚举检查
            enum_values = rules.get("enum")
            if enum_values and value not in enum_values:
                errors.append(f"配置项 '{key}' 值不在枚举范围内：{enum_values}")

            # 文件存在性检查
            if rules.get("exists", False):
                if not Path(value).exists():
                    errors.append(f"配置项 '{key}' 指定的文件不存在：{value}")

        return errors

    def _get_type_class(self, type_name: str) -> type:
        """获取类型类"""
        type_map = {
            "string": str,
            "integer": int,
            "float": float,
            "boolean": bool,
            "list": list,
            "dict": dict,
        }
        return type_map.get(type_name, str)
