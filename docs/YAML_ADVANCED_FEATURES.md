# 高级 YAML 功能示例

## 1. YAML 继承

### 1.1 继承基础页面

```yaml
# framework/pages/login_page.yaml
extends: framework/pages/base_page.yaml

elements:
  # 继承并扩展基础按钮
  login_button:
    extends: base_button
    locator_type: id
    locator_value: btn_login
    description: "登录按钮"
  
  # 新元素
  username_input:
    extends: base_input
    locator_type: id
    locator_value: txt_username
    description: "用户名输入框"
```

### 1.2 跨文件继承

```yaml
# framework/pages/search_page.yaml
elements:
  search_button:
    extends: framework/pages/base_page.yaml:base_button
    locator_type: id
    locator_value: btn_search
    description: "搜索按钮"
```

---

## 2. 变量替换

### 2.1 使用变量

```yaml
# framework/pages/dynamic_page.yaml
elements:
  dynamic_label:
    locator_type: id
    locator_value: lbl_{{page_type}}
    control_type: Text
    description: "{{label_description}}"
```

```python
from engine.page.yaml_loader import YamlLoader

loader = YamlLoader()
data = loader.load_with_variables(
    "framework/pages/dynamic_page.yaml",
    variables={
        "page_type": "user",
        "label_description": "用户标签"
    }
)
```

### 2.2 带默认值的变量

```yaml
elements:
  button:
    locator_type: id
    locator_value: btn_{{action:submit}}
    description: "{{button_desc:默认按钮}}"
```

---

## 3. 环境变量

```yaml
# framework/pages/config_page.yaml
elements:
  app_title:
    locator_type: name
    locator_value: ${APP_TITLE}
    control_type: Text
    description: "应用程序标题"
  
  main_window:
    locator_type: title
    locator_value: ${WINDOW_TITLE}
    control_type: Window
```

```python
# 环境变量自动替换
import os
os.environ["APP_TITLE"] = "My Application"
os.environ["WINDOW_TITLE"] = "Main Window"

loader = YamlLoader()
data = loader.load_with_env("framework/pages/config_page.yaml")
```

---

## 4. 动态元素生成

### 4.1 列表元素

```python
from engine.page.yaml_generator import DynamicElementGenerator

generator = DynamicElementGenerator()

# 生成 10 个列表项
elements = generator.generate_list_elements(
    prefix="item_",
    count=10,
    template={
        "locator_type": "id",
        "locator_value": "list_item_{{index}}",
        "control_type": "ListItem",
        "description": "列表项 {{index}}"
    }
)

# 结果:
# {
#   "item_0": {"locator_value": "list_item_0", ...},
#   "item_1": {"locator_value": "list_item_1", ...},
#   ...
# }
```

### 4.2 参数化元素

```python
# 生成多个按钮
buttons = generator.generate_parametric_elements(
    name_pattern="btn_{action}",
    parameters=[
        {"action": "save"},
        {"action": "cancel"},
        {"action": "delete"}
    ],
    template={
        "locator_type": "id",
        "locator_value": "button_{action}",
        "control_type": "Button",
        "description": "{action}按钮"
    }
)

# 结果:
# {
#   "btn_save": {"locator_value": "button_save", ...},
#   "btn_cancel": {"locator_value": "button_cancel", ...},
#   "btn_delete": {"locator_value": "button_delete", ...}
# }
```

---

## 5. YAML 生成 Python 代码

### 5.1 单个文件生成

```python
from engine.page.yaml_generator import PageCodeGenerator

generator = PageCodeGenerator()

# 从 YAML 生成 Python 类
code = generator.generate(
    yaml_path="framework/pages/login_page.yaml",
    output_path="framework/pages/login_page.py",
    class_name="LoginPage",
    add_comments=True
)
```

### 5.2 批量生成

```python
# 批量生成所有页面类
output_files = generator.generate_all(
    yaml_dir="framework/pages",
    output_dir="framework/pages",
    pattern="*.yaml"
)

# 输出:
# ['framework/pages/login_page.py',
#  'framework/pages/search_page.py',
#  'framework/pages/settings_page.py']
```

### 5.3 命令行使用

```bash
# 生成单个页面
python -m engine.page.yaml_generator framework/pages/login_page.yaml

# 自动生成输出文件 (login_page.py)
```

---

## 6. 生成的代码示例

### 输入 YAML

```yaml
# login_page.yaml
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
    component: input
  
  login_button:
    locator_type: id
    locator_value: btn_login
    control_type: Button
    description: "登录按钮"
    component: button
```

### 生成的 Python 代码

```python
"""
Auto-generated page class: LoginPage
Generated at: 2026-03-28 15:30:45
"""

from typing import TYPE_CHECKING
from engine.page.yaml_page import YamlPage
from engine.component import *
from core.finder.locator import *

if TYPE_CHECKING:
    from engine.page.base_page import BasePage


class LoginPage(YamlPage):
    """
    LoginPage - Auto-generated from YAML
    """

    # ========== UI Components ==========

    # 用户名输入框
    username_input: TextInput

    # 登录按钮
    login_button: Button

    def __init__(self):
        """Initialize page and create UI components"""
        super().__init__()

    # ========== Component Factory Methods ==========

    def create_username_input(self) -> TextInput:
        """
        Create 用户名输入框 component
        
        Returns:
            TextInput instance
        """
        locator = self.element("username_input")
        return TextInput(self, locator)

    def create_login_button(self) -> Button:
        """
        Create 登录按钮 component
        
        Returns:
            Button instance
        """
        locator = self.element("login_button")
        return Button(self, locator)

    # ========== Business Methods ==========

    # TODO: Add business methods here
```

---

## 7. 完整集成示例

```python
from engine.page.yaml_loader import YamlLoader
from engine.page.yaml_generator import PageCodeGenerator, DynamicElementGenerator

# 1. 加载带继承的 YAML
loader = YamlLoader()
page_data = loader.load_with_inheritance("framework/pages/login_page.yaml")

# 2. 添加动态元素
generator = DynamicElementGenerator()
dynamic_elements = generator.generate_list_elements(
    prefix="error_",
    count=5,
    template={
        "locator_type": "id",
        "locator_value": "error_{{index}}",
        "control_type": "Text",
        "description": "错误消息 {{index}}"
    }
)

page_data["elements"].update(dynamic_elements)

# 3. 替换变量
page_data = loader._replace_variables(
    page_data,
    {"app_name": "MyApp", "version": "1.0"}
)

# 4. 生成 Python 代码
code_gen = PageCodeGenerator()
code = code_gen._generate_class_code(
    class_name="LoginPage",
    elements=page_data["elements"]
)

# 5. 保存
with open("framework/pages/login_page_enhanced.py", "w", encoding="utf-8") as f:
    f.write(code)
```

---

## 8. 最佳实践

### 8.1 使用继承减少重复

```yaml
# ✅ 推荐：使用继承
elements:
  submit_btn:
    extends: base_button
    locator_value: btn_submit
  
  cancel_btn:
    extends: base_button
    locator_value: btn_cancel

# ❌ 不推荐：重复定义
elements:
  submit_btn:
    locator_type: class_name
    locator_value: Button
    control_type: Button
    component: button
  
  cancel_btn:
    locator_type: class_name
    locator_value: Button
    control_type: Button
    component: button
```

### 8.2 使用变量提高灵活性

```yaml
# ✅ 推荐：使用变量
elements:
  title:
    locator_value: lbl_{{page_name}}
    description: "{{page_name}}标题"

# ❌ 不推荐：硬编码
elements:
  title:
    locator_value: lbl_user_page
    description: "用户页面标题"
```

### 8.3 使用动态生成处理重复元素

```python
# ✅ 推荐：动态生成
elements = generator.generate_list_elements(
    prefix="row_",
    count=100,
    template={...}
)

# ❌ 不推荐：手动定义 100 个元素
elements:
  row_0: {...}
  row_1: {...}
  ...
  row_99: {...}
```

---

**文档结束**
