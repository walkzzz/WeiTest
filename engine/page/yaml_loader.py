"""YAML Loader - enhanced YAML loading with inheritance and dynamic data support"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
import re
from datetime import datetime


class YamlLoader:
    """
    增强的 YAML 加载器

    支持:
    - 元素继承 (extends)
    - 动态数据变量 (variables)
    - 模板引用 (template)
    - 环境变量替换 (${ENV_VAR})

    Example:
        >>> loader = YamlLoader()
        >>> data = loader.load_with_inheritance("login_page.yaml")
        >>> data = loader.load_with_variables("search_page.yaml", {"keyword": "test"})
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        初始化 YAML 加载器

        Args:
            base_dir: 基础目录，用于解析相对路径
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self._cache: Dict[str, Dict[str, Any]] = {}

    def load_with_inheritance(self, yaml_path: str) -> Dict[str, Any]:
        """
        加载 YAML 并处理继承

        Args:
            yaml_path: YAML 文件路径

        Returns:
            合并后的 YAML 数据
        """
        path = self._resolve_path(yaml_path)

        # 检查缓存
        cache_key = str(path)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 加载 YAML
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 处理继承
        if "extends" in data:
            base_path = data["extends"]
            base_data = self.load_with_inheritance(base_path)
            data = self._merge_yaml(base_data, data)

        # 处理元素级别的继承
        if "elements" in data:
            data["elements"] = self._process_element_inheritance(data["elements"])

        # 缓存
        self._cache[cache_key] = data

        return data

    def load_with_variables(
        self, yaml_path: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        加载 YAML 并替换变量

        Args:
            yaml_path: YAML 文件路径
            variables: 变量字典

        Returns:
            变量替换后的 YAML 数据
        """
        data = self.load_with_inheritance(yaml_path)

        if variables:
            data = self._replace_variables(data, variables)

        return data

    def load_with_env(self, yaml_path: str) -> Dict[str, Any]:
        """
        加载 YAML 并替换环境变量

        Args:
            yaml_path: YAML 文件路径

        Returns:
            环境变量替换后的 YAML 数据
        """
        import os

        data = self.load_with_inheritance(yaml_path)

        # 替换 ${ENV_VAR} 格式的环境变量
        data = self._replace_env_variables(data, os.environ)

        return data

    def _resolve_path(self, yaml_path: str) -> Path:
        """解析路径"""
        path = Path(yaml_path)
        if not path.is_absolute():
            path = self.base_dir / path
        return path

    def _merge_yaml(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        深度合并 YAML

        Args:
            base: 基础数据
            override: 覆盖数据

        Returns:
            合并后的数据
        """
        result = base.copy()

        for key, value in override.items():
            if key == "extends":
                continue

            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_yaml(result[key], value)
            else:
                result[key] = value

        return result

    def _process_element_inheritance(
        self, elements: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        处理元素级别的继承

        Args:
            elements: 元素字典

        Returns:
            处理后的元素字典
        """
        result = {}

        for name, element_def in elements.items():
            if "extends" in element_def:
                # 解析继承引用 (格式：base_element_name 或 base_file.yaml:base_element_name)
                extends_ref = element_def["extends"]

                if ":" in extends_ref:
                    # 跨文件继承：base_file.yaml:element_name
                    base_file, base_element = extends_ref.split(":", 1)
                    base_data = self.load_with_inheritance(base_file)
                    base_element_def = base_data.get("elements", {}).get(base_element, {})
                else:
                    # 同文件继承
                    base_element_def = elements.get(extends_ref, {})

                # 合并定义
                merged = self._merge_yaml(base_element_def, element_def)
                del merged["extends"]
                result[name] = merged
            else:
                result[name] = element_def

        return result

    def _replace_variables(self, data: Any, variables: Dict[str, Any]) -> Any:
        """
        替换变量

        支持格式:
        - {{variable_name}} - 直接替换
        - {{variable_name.default}} - 带默认值

        Args:
            data: YAML 数据
            variables: 变量字典

        Returns:
            替换后的数据
        """
        if isinstance(data, str):
            return self._replace_string_variables(data, variables)
        elif isinstance(data, dict):
            return {key: self._replace_variables(value, variables) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._replace_variables(item, variables) for item in data]
        else:
            return data

    def _replace_string_variables(self, text: str, variables: Dict[str, Any]) -> str:
        """替换字符串中的变量"""
        # 匹配 {{variable}} 或 {{variable:default}}
        pattern = r"\{\{(\w+)(?::([^}]+))?\}\}"

        def replacer(match):
            var_name = match.group(1)
            default = match.group(2)

            if var_name in variables:
                return str(variables[var_name])
            elif default is not None:
                return default
            else:
                return match.group(0)  # 保持不变

        return re.sub(pattern, replacer, text)

    def _replace_env_variables(self, data: Any, env: Dict[str, str]) -> Any:
        """
        替换环境变量

        支持格式: ${ENV_VAR}

        Args:
            data: YAML 数据
            env: 环境变量字典

        Returns:
            替换后的数据
        """
        if isinstance(data, str):
            return self._replace_string_env_variables(data, env)
        elif isinstance(data, dict):
            return {key: self._replace_env_variables(value, env) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._replace_env_variables(item, env) for item in data]
        else:
            return data

    def _replace_string_env_variables(self, text: str, env: Dict[str, str]) -> str:
        """替换字符串中的环境变量"""
        # 匹配 ${ENV_VAR}
        pattern = r"\$\{(\w+)\}"

        def replacer(match):
            var_name = match.group(1)
            return env.get(var_name, match.group(0))

        return re.sub(pattern, replacer, text)

    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()


class DynamicElementGenerator:
    """
    动态元素生成器

    用于生成重复性元素 (如列表项、表格行等)

    Example:
        >>> generator = DynamicElementGenerator()
        >>> elements = generator.generate_list_elements(
        ...     prefix="item_",
        ...     count=10,
        ...     template={"locator_type": "id", "locator_value": "item_{{index}}"}
        ... )
    """

    def generate_list_elements(
        self, prefix: str, count: int, template: Dict[str, Any], start_index: int = 0
    ) -> Dict[str, Dict[str, Any]]:
        """
        生成列表元素

        Args:
            prefix: 元素名称前缀
            count: 生成数量
            template: 元素模板
            start_index: 起始索引

        Returns:
            元素字典
        """
        elements = {}

        for i in range(count):
            index = start_index + i
            name = f"{prefix}{index}"

            # 深度复制模板
            element_def = self._deep_copy(template)

            # 替换模板变量
            element_def = self._replace_template_vars(element_def, {"index": index, "name": name})

            elements[name] = element_def

        return elements

    def generate_parametric_elements(
        self, name_pattern: str, parameters: List[Dict[str, Any]], template: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        生成参数化元素

        Args:
            name_pattern: 名称模式 (如 "btn_{action}")
            parameters: 参数列表
            template: 元素模板

        Returns:
            元素字典
        """
        elements = {}

        for params in parameters:
            # 生成名称
            name = name_pattern.format(**params)

            # 深度复制模板
            element_def = self._deep_copy(template)

            # 替换模板变量
            element_def = self._replace_template_vars(element_def, params)

            elements[name] = element_def

        return elements

    def _deep_copy(self, obj: Any) -> Any:
        """深度复制"""
        if isinstance(obj, dict):
            return {key: self._deep_copy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj

    def _replace_template_vars(self, data: Any, variables: Dict[str, Any]) -> Any:
        """替换模板变量"""
        if isinstance(data, str):
            try:
                return data.format(**variables)
            except KeyError:
                return data
        elif isinstance(data, dict):
            return {
                key: self._replace_template_vars(value, variables) for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self._replace_template_vars(item, variables) for item in data]
        else:
            return data
