# 插件系统使用指南

## 概述

AutoTestMe-NG v2.0 引入了强大的插件系统，支持:
- ✅ 运行时动态注册组件
- ✅ 自定义定位策略
- ✅ 自定义断言类型
- ✅ 无需修改核心代码即可扩展
- ✅ 插件依赖管理
- ✅ 插件生命周期管理

---

## 快速开始

### 1. 使用内置插件管理器

```python
from core.plugin.base import get_plugin_manager

# 获取插件管理器
manager = get_plugin_manager()

# 从目录加载所有插件
count = manager.load_all()
print(f"加载了 {count} 个插件")

# 初始化所有插件
manager.initialize_all()
```

### 2. 注册自定义组件

```python
from core.plugin.registry import register_component

# 定义自定义组件
class MyCustomButton:
    def __init__(self, page, locator):
        self.page = page
        self.locator = locator
    
    def click_with_effect(self):
        """带动画效果的点击"""
        print("点击带特效")
        return self

# 注册组件
register_component("my_button", MyCustomButton)

# 使用组件
from core.plugin.registry import create_component

button = create_component("my_button", page, locator)
button.click_with_effect()
```

---

## 创建插件

### 步骤 1: 创建插件类

```python
# my_plugin.py
from core.plugin.base import ComponentPlugin
from typing import Dict, Type

class MyComponentPlugin(ComponentPlugin):
    """我的自定义组件插件"""
    
    @property
    def name(self) -> str:
        """插件名称 (唯一标识)"""
        return "my_components"
    
    @property
    def version(self) -> str:
        """插件版本"""
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """插件描述"""
        return "我的自定义 UI 组件"
    
    @property
    def dependencies(self) -> list:
        """依赖的插件"""
        return []
    
    def get_components(self) -> Dict[str, Type]:
        """返回组件字典"""
        return {
            "custom_button": CustomButton,
            "custom_table": CustomTable,
        }

# 定义组件
class CustomButton:
    def __init__(self, page, locator):
        self.page = page
        self.locator = locator
    
    def double_click(self):
        """双击"""
        self.page.find_element(self.locator).double_click_input()
        return self

class CustomTable:
    def __init__(self, page, locator):
        self.page = page
        self.locator = locator
    
    def get_row_count(self) -> int:
        """获取行数"""
        return len(self.page.find_elements(self.locator))
```

### 步骤 2: 放置插件文件

将插件文件放入以下目录之一:
- `plugins/`
- `extensions/`

```
your_project/
├── plugins/
│   ├── my_plugin.py          # 你的插件
│   └── custom_components.py  # 其他插件
└── ...
```

### 步骤 3: 加载和使用

```python
from core.plugin.base import get_plugin_manager

# 获取管理器
manager = get_plugin_manager()

# 加载所有插件
count = manager.load_from_directory("plugins")
print(f"加载了 {count} 个插件")

# 初始化
manager.initialize_all()

# 查看已注册的组件
components = manager.list_components()
print(f"可用组件：{components}")
# 输出：['custom_button', 'custom_table']

# 获取组件类
CustomBtn = manager.get_component("custom_button")

# 使用组件
button = CustomBtn(page, locator)
button.double_click()
```

---

## 插件类型

### 1. 组件插件 (ComponentPlugin)

用于注册自定义 UI 组件:

```python
from core.plugin.base import ComponentPlugin

class MyComponentPlugin(ComponentPlugin):
    @property
    def name(self) -> str:
        return "my_components"
    
    def get_components(self) -> Dict[str, Type]:
        return {
            "my_button": MyButton,
            "my_input": MyInput,
        }
```

### 2. 定位器插件 (LocatorPlugin)

用于注册自定义定位策略:

```python
from core.plugin.base import LocatorPlugin

class MyLocatorPlugin(LocatorPlugin):
    @property
    def name(self) -> str:
        return "my_locators"
    
    def get_locators(self) -> Dict[str, Type]:
        return {
            "image": ImageLocator,
            "ocr": OcrLocator,
            "qr": QrCodeLocator,
        }
```

### 3. 断言插件 (AssertionPlugin)

用于注册自定义断言类型:

```python
from core.plugin.base import AssertionPlugin

class MyAssertionPlugin(AssertionPlugin):
    @property
    def name(self) -> str:
        return "my_assertions"
    
    def get_assertions(self) -> Dict[str, Type]:
        return {
            "image": ImageAssertion,
            "database": DatabaseAssertion,
            "api": ApiAssertion,
        }
```

---

## 高级功能

### 1. 插件依赖

```python
class AdvancedPlugin(ComponentPlugin):
    @property
    def name(self) -> str:
        return "advanced_components"
    
    @property
    def dependencies(self) -> list:
        """声明依赖其他插件"""
        return ["my_components", "my_locators"]
    
    def get_components(self) -> Dict[str, Type]:
        return {
            "advanced_button": AdvancedButton,
        }
```

### 2. 插件生命周期

```python
class LifecyclePlugin(ComponentPlugin):
    def initialize(self, context: PluginContext) -> None:
        """插件初始化时调用"""
        print("插件初始化")
        
        # 获取服务
        logger = context.get_service("logger")
        config = context.get_config("app_config")
    
    def shutdown(self) -> None:
        """插件关闭时调用"""
        print("插件关闭，清理资源")
```

### 3. 使用插件上下文

```python
from core.plugin.base import PluginContext, Plugin

class ContextAwarePlugin(Plugin):
    def initialize(self, context: PluginContext) -> None:
        super().initialize(context)
        
        # 注册服务
        context.register_service("my_service", MyService())
        
        # 设置配置
        context.set_config("my_plugin_config", {"key": "value"})
        
        # 获取基础目录
        base_dir = context.base_dir
```

### 4. 动态注册/注销

```python
from core.plugin.base import get_plugin_manager

manager = get_plugin_manager()

# 运行时注册组件
manager._component_registry["dynamic_component"] = DynamicComponent

# 运行时注销组件
manager.unregister_plugin("old_plugin")

# 查看注册表
print(manager.list_components())
```

---

## 使用场景

### 场景 1: 企业自定义组件库

```python
# enterprise_plugin.py
class EnterpriseComponentPlugin(ComponentPlugin):
    @property
    def name(self) -> str:
        return "enterprise_components"
    
    def get_components(self) -> Dict[str, Type]:
        """企业标准组件库"""
        return {
            # 标准按钮
            "std_button": StandardButton,
            
            # 数据表格
            "data_grid": EnterpriseDataGrid,
            
            # 导航菜单
            "nav_menu": NavigationMenu,
            
            # 表单控件
            "form_input": FormInput,
            "form_select": FormSelect,
        }
```

### 场景 2: 第三方集成

```python
# sap_plugin.py
class SAPLocatorPlugin(LocatorPlugin):
    @property
    def name(self) -> str:
        return "sap_locators"
    
    def get_locators(self) -> Dict[str, Type]:
        """SAP 系统专用定位器"""
        return {
            "sap_gui": SAPGuiLocator,
            "sap_web": SAPWebLocator,
        }

# sap_assertions.py
class SAPAssertionPlugin(AssertionPlugin):
    def get_assertions(self) -> Dict[str, Type]:
        """SAP 专用断言"""
        return {
            "sap_transaction": SAPTransactionAssertion,
            "sap_data": SAPDataAssertion,
        }
```

### 场景 3: AI 增强功能

```python
# ai_plugin.py
class AIComponentPlugin(ComponentPlugin):
    def get_components(self) -> Dict[str, Type]:
        """AI 增强组件"""
        return {
            "ai_button": AIButton,  # 自动识别按钮
            "ai_input": AIInput,    # 智能输入
        }

class AILocatorPlugin(LocatorPlugin):
    def get_locators(self) -> Dict[str, Type]:
        """AI 定位器"""
        return {
            "ai_image": AIImageLocator,      # 图像识别
            "ai_ocr": AIOcrLocator,          # OCR 识别
            "ai_element": AIElementLocator,  # 智能元素定位
        }
```

---

## 最佳实践

### 1. 命名规范

```python
# ✅ 推荐：清晰唯一的命名
@property
def name(self) -> str:
    return "company_team_components"

# ❌ 不推荐：过于通用
@property
def name(self) -> str:
    return "my_plugin"
```

### 2. 版本管理

```python
# ✅ 推荐：语义化版本
@property
def version(self) -> str:
    return "1.2.3"  # major.minor.patch

# 在文档中说明版本兼容性
"""
兼容性:
- v1.x: AutoTestMe-NG v2.0+
- v2.x: AutoTestMe-NG v3.0+ (计划中)
"""
```

### 3. 错误处理

```python
class RobustPlugin(ComponentPlugin):
    def initialize(self, context: PluginContext) -> None:
        try:
            super().initialize(context)
            # 初始化逻辑
        except Exception as e:
            print(f"插件初始化失败：{e}")
            raise
    
    def shutdown(self) -> None:
        try:
            # 清理逻辑
            pass
        except Exception as e:
            print(f"插件关闭失败：{e}")
```

### 4. 文档说明

```python
class WellDocumentedPlugin(ComponentPlugin):
    """
    完善的插件文档
    
    功能:
        - 提供 5 个自定义组件
        - 支持 SAP 系统集成
        - 需要 SAP GUI 7.6+
    
    使用方法:
        >>> from core.plugin.base import get_plugin_manager
        >>> manager = get_plugin_manager()
        >>> manager.load_from_directory("plugins")
    
    依赖:
        - SAP GUI 7.6+
        - pywin32
    
    示例:
        参见 examples/sap_example.py
    """
    
    @property
    def name(self) -> str:
        return "sap_integration"
```

---

## 故障排除

### 问题 1: 插件未加载

**检查**:
1. 插件文件是否在正确的目录
2. 插件类是否继承自正确的基类
3. 是否实现了所有必需的属性/方法

**调试**:
```python
manager = get_plugin_manager()
print(f"插件目录：{manager._plugin_dirs}")
print(f"已加载：{manager.list_plugins()}")
```

### 问题 2: 依赖冲突

**解决**:
```python
# 按正确顺序加载插件
manager.load_plugin("base_plugin.py")  # 先加载基础插件
manager.load_plugin("dependent_plugin.py")  # 再加载依赖插件
```

### 问题 3: 组件未注册

**检查**:
```python
manager = get_plugin_manager()

# 查看已注册组件
print(manager.list_components())

# 检查特定组件
if manager.get_component("my_button"):
    print("组件已注册")
else:
    print("组件未注册")
```

---

## API 参考

### PluginManager

| 方法 | 说明 |
|------|------|
| `load_plugin(path)` | 从文件加载插件 |
| `load_from_directory(dir)` | 从目录加载所有插件 |
| `load_all()` | 从所有默认目录加载 |
| `register_plugin(plugin)` | 注册插件 |
| `unregister_plugin(name)` | 注销插件 |
| `get_plugin(name)` | 获取插件实例 |
| `get_component(name)` | 获取组件类 |
| `get_locator(name)` | 获取定位器类 |
| `get_assertion(name)` | 获取断言类 |
| `list_plugins()` | 列出所有插件 |
| `list_components()` | 列出所有组件 |
| `initialize_all()` | 初始化所有插件 |
| `shutdown_all()` | 关闭所有插件 |

### ComponentRegistry

| 方法 | 说明 |
|------|------|
| `register(name, component)` | 注册组件 |
| `unregister(name)` | 注销组件 |
| `get(name)` | 获取组件类 |
| `has(name)` | 检查是否已注册 |
| `list_all()` | 列出所有组件 |
| `clear()` | 清空注册表 |

---

**文档结束**
