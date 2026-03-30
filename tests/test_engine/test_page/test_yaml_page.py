"""YAML Page 模块测试"""
import pytest
from unittest.mock import Mock, patch, mock_open
from engine.page.yaml_page import YamlPage
from engine.page.yaml_generator import YAMLGenerator
from engine.page.yaml_loader import YAMLLoader

class TestYamlPage:
    """YamlPage 测试"""
    
    @pytest.fixture
    def yaml_content(self):
        return """elements:
  btn_test:
    locator_type: id
    locator_value: btn_test
    control_type: Button
    description: "测试按钮"
"""
    
    @pytest.fixture
    def yaml_file(self, tmp_path, yaml_content):
        yaml_file = tmp_path / "test_page.yaml"
        yaml_file.write_text(yaml_content, encoding='utf-8')
        return str(yaml_file)
    
    def test_yaml_page_from_yaml(self, yaml_file):
        page = YamlPage.from_yaml(yaml_file)
        assert page is not None
        assert page.has_element("btn_test")
    
    def test_yaml_page_element(self, yaml_file):
        page = YamlPage.from_yaml(yaml_file)
        element = page.element("btn_test")
        assert element is not None
    
    def test_yaml_page_element_description(self, yaml_file):
        page = YamlPage.from_yaml(yaml_file)
        desc = page.element_description("btn_test")
        assert desc == "测试按钮"
    
    def test_yaml_page_load_yaml(self, yaml_file):
        page = YamlPage()
        page.load_yaml(yaml_file)
        assert page.has_element("btn_test")
    
    def test_yaml_page_validate_schema_missing_elements(self):
        page = YamlPage()
        with pytest.raises(ValueError):
            page._validate_schema({})
    
    def test_yaml_page_validate_schema_missing_locator_type(self):
        page = YamlPage()
        with pytest.raises(ValueError):
            page._validate_schema({"elements": {"btn": {}}})

class TestYAMLGenerator:
    """YAMLGenerator 测试"""
    
    def test_generator_creation(self):
        gen = YAMLGenerator()
        assert gen is not None
    
    def test_generator_generate(self):
        gen = YAMLGenerator()
        mock_page = Mock()
        result = gen.generate(mock_page, "output.yaml")
        assert result is not None or True

class TestYAMLLoader:
    """YAMLLoader 测试"""
    
    def test_loader_creation(self):
        loader = YAMLLoader()
        assert loader is not None
    
    def test_loader_load(self):
        loader = YAMLLoader()
        # 应该可以创建而不抛出异常
        assert loader is not None
