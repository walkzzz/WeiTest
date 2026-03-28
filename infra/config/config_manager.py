"""Configuration Manager - loads and manages YAML configuration files"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigError(Exception):
    """配置错误"""

    pass


class ConfigManager:
    """
    配置管理器

    负责加载和管理 YAML 配置文件

    使用示例：
        >>> config = ConfigManager("framework/data")
        >>> env = config.get_env_config("test")
        >>> print(env["app_path"])
    """

    def __init__(self, config_dir: str):
        """
        初始化配置管理器

        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = Path(config_dir)
        self._configs: Dict[str, Dict[str, Any]] = {}

    def load_config(self, config_name: str) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            config_name: 配置文件名称（不含.yaml）

        Returns:
            配置字典

        Raises:
            ConfigError: 文件不存在或解析失败
        """
        config_file = self.config_dir / f"{config_name}.yaml"

        if not config_file.exists():
            raise ConfigError(f"配置文件不存在：{config_file}")

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            self._configs[config_name] = data
            return data

        except yaml.YAMLError as e:
            raise ConfigError(f"YAML 解析失败：{e}")

    def get_config(self, config_name: str, key: Optional[str] = None) -> Any:
        """
        获取配置

        Args:
            config_name: 配置文件名称
            key: 配置键（可选）

        Returns:
            配置值
        """
        if config_name not in self._configs:
            self.load_config(config_name)

        config = self._configs[config_name]

        if key:
            return config.get(key)
        return config

    def get_env_config(self, env: str, key: Optional[str] = None) -> Any:
        """
        获取环境配置

        Args:
            env: 环境名称 (test/dev/prod)
            key: 配置键（可选）

        Returns:
            环境配置

        Raises:
            ConfigError: 环境不存在
        """
        env_config = self.get_config("env")

        if env not in env_config:
            raise ConfigError(f"环境 '{env}' 不存在")

        env_data = env_config[env]

        if key:
            return env_data.get(key)
        return env_data

    def get_test_data(self, data_name: str, key: Optional[str] = None) -> Any:
        """
        获取测试数据

        Args:
            data_name: 测试数据名称
            key: 数据键（可选）

        Returns:
            测试数据
        """
        test_data = self.get_config("test_data")

        if data_name not in test_data:
            raise ConfigError(f"测试数据 '{data_name}' 不存在")

        data = test_data[data_name]

        if key:
            return data.get(key)
        return data

    def load_all(self) -> Dict[str, Dict[str, Any]]:
        """
        加载所有配置文件

        Returns:
            所有配置字典
        """
        if not self.config_dir.exists():
            raise ConfigError(f"配置目录不存在：{self.config_dir}")

        for yaml_file in self.config_dir.glob("*.yaml"):
            config_name = yaml_file.stem
            self.load_config(config_name)

        return self._configs

    def reload(self):
        """重新加载所有配置"""
        self._configs.clear()
        self.load_all()

    @property
    def loaded_configs(self) -> Dict[str, Dict[str, Any]]:
        """获取已加载的配置"""
        return self._configs.copy()
