"""Page Code Generator - generates Python page classes from YAML definitions"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
from datetime import datetime


class PageCodeGenerator:
    """
    页面代码生成器

    从 YAML 定义生成 Python 页面类代码

    Example:
        >>> generator = PageCodeGenerator()
        >>> generator.generate(
        ...     yaml_path="framework/pages/login_page.yaml",
        ...     output_path="framework/pages/login_page.py"
        ... )
    """

    COMPONENT_MAP = {
        "button": "Button",
        "input": "TextInput",
        "checkbox": "CheckBox",
        "combobox": "ComboBox",
        "label": "Label",
        "table": "Table",
        "progressbar": "ProgressBar",
        "menu": "Menu",
    }

    def __init__(self, template_dir: Optional[str] = None):
        """
        初始化代码生成器

        Args:
            template_dir: 模板目录
        """
        self.template_dir = Path(template_dir) if template_dir else None

    def generate(
        self,
        yaml_path: str,
        output_path: str,
        class_name: Optional[str] = None,
        add_comments: bool = True,
    ) -> str:
        """
        生成 Python 页面类

        Args:
            yaml_path: YAML 文件路径
            output_path: 输出 Python 文件路径
            class_name: 类名 (可选，默认从文件名推导)
            add_comments: 是否添加注释

        Returns:
            生成的代码
        """
        # 加载 YAML
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 推导类名
        if not class_name:
            yaml_file = Path(yaml_path).stem
            class_name = self._snake_to_pascal(yaml_file)

        # 生成代码
        code = self._generate_class_code(
            class_name=class_name, elements=data.get("elements", {}), add_comments=add_comments
        )

        # 写入文件
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(code)

        return code

    def _generate_class_code(
        self, class_name: str, elements: Dict[str, Dict[str, Any]], add_comments: bool = True
    ) -> str:
        """
        生成类代码

        Args:
            class_name: 类名
            elements: 元素定义
            add_comments: 是否添加注释

        Returns:
            生成的类代码
        """
        lines = []

        # 文件头注释
        lines.append('"""')
        lines.append(f"Auto-generated page class: {class_name}")
        lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append('"""')
        lines.append("")

        # 导入语句
        lines.append("from typing import TYPE_CHECKING")
        lines.append("from wei.engine.page.yaml_page import YamlPage")
        lines.append("from wei.engine.component import *")
        lines.append("from core.finder.locator import *")
        lines.append("")
        lines.append("if TYPE_CHECKING:")
        lines.append("    from wei.engine.page.base_page import BasePage")
        lines.append("")

        # 类定义
        lines.append(f"class {class_name}(YamlPage):")
        lines.append(f'    """')
        lines.append(f"    {class_name} - Auto-generated from YAML")
        lines.append(f'    """')
        lines.append("")

        # 类变量 - 组件属性
        lines.append("    # ========== UI Components ==========")
        lines.append("")

        for name, element_def in elements.items():
            component_type = element_def.get("component")
            description = element_def.get("description", name)

            if component_type and component_type in self.COMPONENT_MAP:
                component_class = self.COMPONENT_MAP[component_type]
                var_name = name

                if add_comments:
                    lines.append(f"    # {description}")

                lines.append(f"    {var_name}: {component_class}")
                lines.append("")

        # __init__ 方法
        lines.append("    def __init__(self):")
        lines.append('        """Initialize page and create UI components"""')
        lines.append("        super().__init__()")
        lines.append("")
        lines.append("        # UI components will be created after loading YAML")
        lines.append("")

        # 组件创建方法
        lines.append("    # ========== Component Factory Methods ==========")
        lines.append("")

        for name, element_def in elements.items():
            component_type = element_def.get("component")
            description = element_def.get("description", name)

            if component_type and component_type in self.COMPONENT_MAP:
                component_class = self.COMPONENT_MAP[component_type]
                method_name = f"create_{name}"

                lines.append(f"    def {method_name}(self) -> {component_class}:")
                lines.append(f'        """')
                lines.append(f"        Create {description} component")
                lines.append(f"        ")
                lines.append(f"        Returns:")
                lines.append(f"            {component_class} instance")
                lines.append(f'        """')
                lines.append(f'        locator = self.element("{name}")')
                lines.append(f"        return {component_class}(self, locator)")
                lines.append("")

        # 业务方法占位符
        lines.append("    # ========== Business Methods ==========")
        lines.append("")
        lines.append("    # TODO: Add business methods here")
        lines.append("")

        return "\n".join(lines)

    def _snake_to_pascal(self, snake_case: str) -> str:
        """
        将蛇形命名转换为帕斯卡命名

        Args:
            snake_case: 蛇形命名字符串

        Returns:
            帕斯卡命名字符串
        """
        parts = snake_case.split("_")
        return "".join(part.capitalize() for part in parts)

    def generate_all(self, yaml_dir: str, output_dir: str, pattern: str = "*.yaml") -> List[str]:
        """
        批量生成页面类

        Args:
            yaml_dir: YAML 文件目录
            output_dir: 输出目录
            pattern: 文件匹配模式

        Returns:
            生成的文件列表
        """
        from pathlib import Path
        import glob

        yaml_files = glob.glob(str(Path(yaml_dir) / pattern))
        output_files = []

        for yaml_file in yaml_files:
            # 跳过 base_page.yaml
            if Path(yaml_file).name == "base_page.yaml":
                continue

            # 推导输出路径
            yaml_name = Path(yaml_file).stem
            output_file = Path(output_dir) / f"{yaml_name}_page.py"

            # 生成
            self.generate(yaml_file, str(output_file))
            output_files.append(str(output_file))

        return output_files


class YamlToPythonCLI:
    """
    命令行工具 - YAML to Python

    Usage:
        python -m engine.page.yaml_generator framework/pages/login_page.yaml
    """

    @staticmethod
    def main():
        import sys

        if len(sys.argv) < 2:
            print("Usage: python -m engine.page.yaml_generator <yaml_file> [output_file]")
            sys.exit(1)

        yaml_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None

        if not output_path:
            # 自动生成输出路径
            yaml_file = Path(yaml_path)
            output_path = str(yaml_file.with_suffix(".py"))

        generator = PageCodeGenerator()
        code = generator.generate(yaml_path, output_path)

        print(f"✅ Generated: {output_path}")
        print(f"   Lines: {len(code.splitlines())}")


if __name__ == "__main__":
    YamlToPythonCLI.main()
