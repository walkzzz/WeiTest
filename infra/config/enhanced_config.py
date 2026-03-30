"""Enhanced Config Manager - advanced configuration management"""

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

from infra.config.config_validator import ConfigValidator
from infra.config.config_encryption import ConfigEncryption


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
