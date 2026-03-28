"""Enhanced Config Manager - advanced configuration management"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from cryptography.fernet import Fernet
import re


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


class ConfigEncryption:
    """配置加密器"""

    def __init__(self, key: Optional[str] = None) -> None:
        """
        初始化加密器

        Args:
            key: 加密密钥 (可选，不提供则生成新密钥)
        """
        if key:
            self.key = key.encode()
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def encrypt(self, value: str) -> str:
        """
        加密值

        Args:
            value: 要加密的值

        Returns:
            加密后的值 (带 ENC[] 标记)
        """
        encrypted = self.cipher.encrypt(value.encode())
        return f"ENC[{encrypted.decode()}]"

    def decrypt(self, encrypted_value: str) -> str:
        """
        解密值

        Args:
            encrypted_value: 加密的值 (格式：ENC[...])

        Returns:
            解密后的值
        """
        if not encrypted_value.startswith("ENC[") or not encrypted_value.endswith("]"):
            raise ValueError("无效的加密值格式")

        encrypted_data = encrypted_value[4:-1].encode()
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()

    def is_encrypted(self, value: str) -> bool:
        """
        检查值是否已加密

        Args:
            value: 要检查的值

        Returns:
            bool: 是否已加密
        """
        return value.startswith("ENC[") and value.endswith("]")

    def save_key(self, key_path: str) -> None:
        """
        保存密钥到文件

        Args:
            key_path: 密钥文件路径
        """
        with open(key_path, "w") as f:
            f.write(self.key.decode())

    @classmethod
    def load_key(cls, key_path: str) -> "ConfigEncryption":
        """
        从文件加载密钥

        Args:
            key_path: 密钥文件路径

        Returns:
            ConfigEncryption 实例
        """
        with open(key_path, "r") as f:
            key = f.read().strip()
        return cls(key)


class EnhancedConfigManager:
    """
    增强的配置管理器

    支持:
    - YAML 配置加载
    - 环境变量覆盖
    - 配置加密/解密
    - 配置验证

    Example:
        >>> config = EnhancedConfigManager("framework/data")
        >>> config.load_with_env("env.yaml")
        >>> config.validate(schema)
    """

    def __init__(self, config_dir: str) -> None:
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录
        """
        self.config_dir = Path(config_dir)
        self._config: Dict[str, Any] = {}
        self._encryption: Optional[ConfigEncryption] = None

    def load(self, filename: str) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            filename: 配置文件名

        Returns:
            配置字典
        """
        config_path = self.config_dir / filename

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在：{config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        return self._config

    def load_with_env(self, filename: str) -> Dict[str, Any]:
        """
        加载配置文件并应用环境变量覆盖

        环境变量格式：ATM_<KEY>=<VALUE>

        Args:
            filename: 配置文件名

        Returns:
            配置字典
        """
        # 先加载基础配置
        self.load(filename)

        # 应用环境变量覆盖
        for key, value in os.environ.items():
            if key.startswith("ATM_"):
                config_key = key[4:].lower()  # 移除 ATM_ 前缀
                self._config[config_key] = self._parse_env_value(value)

        return self._config

    def load_with_secrets(self, filename: str, key_path: Optional[str] = None) -> Dict[str, Any]:
        """
        加载配置文件并解密加密的值

        Args:
            filename: 配置文件名
            key_path: 密钥文件路径 (可选)

        Returns:
            配置字典
        """
        self.load(filename)

        if key_path:
            self._encryption = ConfigEncryption.load_key(key_path)

        # 解密所有加密的值
        self._config = self._decrypt_config(self._config)

        return self._config

    def _decrypt_config(self, config: Any) -> Any:
        """递归解密配置"""
        if isinstance(config, str):
            if self._encryption and self._encryption.is_encrypted(config):
                return self._encryption.decrypt(config)
            return config
        elif isinstance(config, dict):
            return {key: self._decrypt_config(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [self._decrypt_config(item) for item in config]
        else:
            return config

    def _parse_env_value(self, value: str) -> Any:
        """
        解析环境变量值

        支持类型:
        - 布尔值：true/false
        - 整数：数字
        - 浮点数：带小数点的数字
        - 列表：逗号分隔

        Args:
            value: 环境变量值

        Returns:
            解析后的值
        """
        # 布尔值
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

        # 整数
        if re.match(r"^-?\d+$", value):
            return int(value)

        # 浮点数
        if re.match(r"^-?\d+\.\d+$", value):
            return float(value)

        # 列表 (逗号分隔)
        if "," in value:
            return [item.strip() for item in value.split(",")]

        # 默认字符串
        return value

    def validate(self, schema: Dict[str, Any]) -> List[str]:
        """
        验证配置

        Args:
            schema: 验证模式

        Returns:
            错误消息列表
        """
        validator = ConfigValidator(schema)
        return validator.validate(self._config)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def get_env_config(self, env_name: str = "test") -> Dict[str, Any]:
        """
        获取指定环境的配置

        Args:
            env_name: 环境名称 (test/dev/prod)

        Returns:
            环境配置字典
        """
        environments = self._config.get("environments", {})
        return environments.get(env_name, {})

    def set_encryption(self, encryption: ConfigEncryption) -> None:
        """
        设置加密器

        Args:
            encryption: 加密器实例
        """
        self._encryption = encryption

    def encrypt_value(self, value: str) -> str:
        """
        加密配置值

        Args:
            value: 要加密的值

        Returns:
            加密后的值
        """
        if not self._encryption:
            raise RuntimeError("未设置加密器")

        return self._encryption.encrypt(value)

    def decrypt_value(self, encrypted_value: str) -> str:
        """
        解密配置值

        Args:
            encrypted_value: 加密的值

        Returns:
            解密后的值
        """
        if not self._encryption:
            raise RuntimeError("未设置加密器")

        return self._encryption.decrypt(encrypted_value)

    def save(self, filename: str) -> None:
        """
        保存配置到文件

        Args:
            filename: 配置文件名
        """
        config_path = self.config_dir / filename

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)


# ========== 便捷函数 ==========


def load_config(config_dir: str, filename: str) -> Dict[str, Any]:
    """加载配置文件"""
    manager = EnhancedConfigManager(config_dir)
    return manager.load(filename)


def load_config_with_env(config_dir: str, filename: str) -> Dict[str, Any]:
    """加载配置文件并应用环境变量"""
    manager = EnhancedConfigManager(config_dir)
    return manager.load_with_env(filename)
