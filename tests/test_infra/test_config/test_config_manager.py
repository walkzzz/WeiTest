"""Tests for ConfigManager"""

import pytest
import yaml
import shutil
from pathlib import Path
from infra.config.config_manager import ConfigManager, ConfigError


class TestConfigManager:
    """测试 ConfigManager"""

    @pytest.fixture
    def config_dir(self):
        """创建测试配置目录"""
        test_dir = Path("test_configs")
        test_dir.mkdir(exist_ok=True)
        yield test_dir
        # 清理
        shutil.rmtree(test_dir, ignore_errors=True)

    @pytest.fixture
    def env_config_file(self, config_dir):
        """创建环境配置文件"""
        config_data = {
            "test": {"app_path": "C:\\Test\\app.exe", "app_title": "测试应用", "timeout": 30},
            "dev": {"app_path": "C:\\Dev\\app.exe", "app_title": "开发应用", "timeout": 60},
        }

        config_file = config_dir / "env.yaml"
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, allow_unicode=True)

        return config_dir

    @pytest.fixture
    def test_data_file(self, config_dir):
        """创建测试数据文件"""
        test_data = {
            "users": ["admin", "user1", "user2"],
            "settings": {"language": "zh-CN", "theme": "dark"},
        }

        config_file = config_dir / "test_data.yaml"
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(test_data, f, allow_unicode=True)

        return config_dir

    def test_config_manager_init(self, config_dir):
        """测试配置管理器初始化"""
        config = ConfigManager(str(config_dir))
        assert config.config_dir == config_dir
        assert config._configs == {}

    def test_load_config(self, env_config_file):
        """测试加载配置"""
        config = ConfigManager(str(env_config_file))
        data = config.load_config("env")

        assert data is not None
        assert "test" in data
        assert "dev" in data
        assert data["test"]["timeout"] == 30

    def test_load_config_not_found(self, config_dir):
        """测试加载不存在的配置"""
        config = ConfigManager(str(config_dir))

        with pytest.raises(ConfigError, match="配置文件不存在"):
            config.load_config("nonexistent")

    def test_get_env_config(self, env_config_file):
        """测试获取环境配置"""
        config = ConfigManager(str(env_config_file))
        env = config.get_env_config("test")

        assert env["app_path"] == "C:\\Test\\app.exe"
        assert env["app_title"] == "测试应用"
        assert env["timeout"] == 30

    def test_get_env_config_with_key(self, env_config_file):
        """测试获取环境配置的特定键"""
        config = ConfigManager(str(env_config_file))
        app_path = config.get_env_config("test", key="app_path")

        assert app_path == "C:\\Test\\app.exe"

    def test_get_env_config_not_found(self, env_config_file):
        """测试获取不存在的环境"""
        config = ConfigManager(str(env_config_file))

        with pytest.raises(ConfigError, match="环境 'production' 不存在"):
            config.get_env_config("production")

    def test_get_config(self, env_config_file):
        """测试获取配置"""
        config = ConfigManager(str(env_config_file))
        data = config.get_config("env")

        assert "test" in data
        assert "dev" in data

    def test_get_config_with_key(self, env_config_file):
        """测试获取配置的特定键"""
        config = ConfigManager(str(env_config_file))
        test_env = config.get_config("env", key="test")

        assert test_env["app_path"] == "C:\\Test\\app.exe"

    def test_load_all(self, config_dir):
        """测试加载所有配置"""
        # 创建 env.yaml
        env_data = {"test": {"timeout": 30}}
        with open(config_dir / "env.yaml", "w", encoding="utf-8") as f:
            yaml.dump(env_data, f)

        # 创建 test_data.yaml
        test_data = {"users": ["admin"]}
        with open(config_dir / "test_data.yaml", "w", encoding="utf-8") as f:
            yaml.dump(test_data, f)

        config = ConfigManager(str(config_dir))
        all_configs = config.load_all()

        assert "env" in all_configs
        assert "test_data" in all_configs

    def test_reload(self, env_config_file):
        """测试重新加载配置"""
        config = ConfigManager(str(env_config_file))
        config.load_config("env")

        assert len(config._configs) > 0

        config.reload()
        assert len(config._configs) > 0

    def test_loaded_configs(self, env_config_file):
        """测试获取已加载的配置"""
        config = ConfigManager(str(env_config_file))
        config.load_config("env")

        loaded = config.loaded_configs
        assert "env" in loaded

    def test_get_test_data(self, test_data_file):
        """测试获取测试数据"""
        config = ConfigManager(str(test_data_file))
        # 直接通过 get_config 获取
        data = config.get_config("test_data")

        assert "users" in data
        assert "admin" in data["users"]

    def test_get_test_data_with_key(self, test_data_file):
        """测试获取测试数据的特定键"""
        config = ConfigManager(str(test_data_file))
        # 直接通过 get_config 获取
        data = config.get_config("test_data")
        users = data.get("users", [])

        assert "admin" in users
        assert len(users) == 3

    def test_get_test_data_not_found(self, test_data_file):
        """测试获取不存在的测试数据"""
        config = ConfigManager(str(test_data_file))

        with pytest.raises(ConfigError, match="测试数据 'nonexistent' 不存在"):
            config.get_test_data("nonexistent")

    def test_config_manager_yaml_unicode(self, config_dir):
        """测试 YAML 支持 Unicode 字符"""
        config_data = {"test": {"app_title": "测试应用 🚀", "description": "自动化测试框架"}}

        config_file = config_dir / "unicode_test.yaml"
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, allow_unicode=True)

        config = ConfigManager(str(config_dir))
        data = config.load_config("unicode_test")

        assert "测试应用" in data["test"]["app_title"]


class TestConfigManagerIntegration:
    """测试 ConfigManager 集成"""

    @pytest.fixture
    def full_config_dir(self):
        """创建完整配置目录"""
        test_dir = Path("test_configs_full")
        test_dir.mkdir(exist_ok=True)

        # 创建多个配置文件
        configs = {
            "env": {
                "test": {"app_path": "C:\\Test\\app.exe", "timeout": 30},
                "prod": {"app_path": "C:\\Prod\\app.exe", "timeout": 60},
            },
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "logging": {"level": "INFO", "format": "%(asctime)s - %(levelname)s - %(message)s"},
        }

        for name, data in configs.items():
            config_file = test_dir / f"{name}.yaml"
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True)

        yield test_dir
        shutil.rmtree(test_dir, ignore_errors=True)

    def test_load_multiple_configs(self, full_config_dir):
        """测试加载多个配置文件"""
        config = ConfigManager(str(full_config_dir))
        all_configs = config.load_all()

        assert "env" in all_configs
        assert "database" in all_configs
        assert "logging" in all_configs

    def test_get_nested_config(self, full_config_dir):
        """测试获取嵌套配置"""
        config = ConfigManager(str(full_config_dir))
        config.load_all()

        db_host = config.get_config("database", key="host")
        assert db_host == "localhost"

        log_level = config.get_config("logging", key="level")
        assert log_level == "INFO"

    def test_config_chaining(self, full_config_dir):
        """测试配置链式访问"""
        config = ConfigManager(str(full_config_dir))
        config.load_config("env")

        test_app = config.get_env_config("test")["app_path"]
        assert "Test" in test_app
