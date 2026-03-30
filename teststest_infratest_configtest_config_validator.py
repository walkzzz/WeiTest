"""配置验证器完整测试"""

import pytest
from infra.config.config_validator import ConfigValidator


class TestConfigValidator:
    """配置验证器测试"""

    def test_validate_required_field_missing(self):
        """测试必填字段缺失"""
        schema = {"name": {"type": "string", "required": True}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({})
        assert len(errors) > 0
        assert "缺少必需" in errors[0]

    def test_validate_required_field_present(self):
        """测试必填字段存在"""
        schema = {"name": {"type": "string", "required": True}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"name": "test"})
        assert len(errors) == 0

    def test_validate_type_string(self):
        """测试字符串类型验证"""
        schema = {"name": {"type": "string"}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"name": 123})
        assert len(errors) > 0
        assert "类型错误" in errors[0]

    def test_validate_type_integer(self):
        """测试整数类型验证"""
        schema = {"age": {"type": "integer"}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"age": "not a number"})
        assert len(errors) > 0

    def test_validate_min_value(self):
        """测试最小值验证"""
        schema = {"age": {"type": "integer", "min": 0}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"age": -1})
        assert len(errors) > 0
        assert "太小" in errors[0]

    def test_validate_max_value(self):
        """测试最大值验证"""
        schema = {"age": {"type": "integer", "max": 100}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"age": 150})
        assert len(errors) > 0
        assert "太大" in errors[0]

    def test_validate_enum(self):
        """测试枚举验证"""
        schema = {"status": {"type": "string", "enum": ["active", "inactive"]}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"status": "unknown"})
        assert len(errors) > 0
        assert "枚举范围" in errors[0]

    def test_validate_file_exists(self):
        """测试文件存在性验证"""
        schema = {"config": {"type": "string", "exists": True}}
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"config": "/nonexistent/file"})
        assert len(errors) > 0
        assert "不存在" in errors[0]

    def test_validate_valid_config(self):
        """测试有效配置"""
        schema = {
            "name": {"type": "string", "required": True},
            "age": {"type": "integer", "min": 0, "max": 150},
        }
        validator = ConfigValidator(schema)
        
        errors = validator.validate({"name": "test", "age": 25})
        assert len(errors) == 0

    def test_get_type_class(self):
        """测试获取类型类"""
        schema = {"test": {"type": "string"}}
        validator = ConfigValidator(schema)
        
        assert validator._get_type_class("string") == str
        assert validator._get_type_class("integer") == int
        assert validator._get_type_class("float") == float
        assert validator._get_type_class("boolean") == bool
        assert validator._get_type_class("list") == list
        assert validator._get_type_class("dict") == dict
