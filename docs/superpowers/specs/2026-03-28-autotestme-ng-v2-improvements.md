# AutoTestMe-NG v2.0 改进设计文档

**文档版本**: v1.0  
**创建日期**: 2026-03-28  
**状态**: 待实施  
**目标版本**: v2.0

---

## 📋 概述

本文档定义 AutoTestMe-NG v1.0 的 12 个缺点的修复方案，分为 11 个 Phase 实施。

---

## 🎯 改进目标

| 维度 | v1.0 评分 | v2.0 目标 | 提升幅度 |
|------|----------|----------|---------|
| 架构设计 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 保持 |
| 代码质量 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| 功能完整性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| 文档完善度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +25% |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +25% |
| 可扩展性 | ⭐⭐ | ⭐⭐⭐⭐⭐ | +150% |
| 稳定性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +67% |
| CI/CD 集成 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | +25% |

**总体目标**: ⭐⭐⭐ → ⭐⭐⭐⭐⭐ (3.5 → 4.8)

---

## Phase 1: 统一代码质量 ⭐⭐⭐ → ⭐⭐⭐⭐⭐

### 1.1 问题
- Engine/Infra 层缺少类型注解
- 文档字符串不完整
- 代码风格不一致

### 1.2 解决方案

#### 1.2.1 添加类型注解
```python
# Before
def type(self, text):
    self.element.send_keys(text)

# After
def type(self, text: str) -> "TextInput":
    """
    输入文本
    
    Args:
        text: 要输入的文本
        
    Returns:
        self: 支持链式调用
    """
    self.element.send_keys(text)
    return self
```

#### 1.2.2 完善文档字符串
所有公共 API 必须包含:
- 简短描述
- Args 参数说明
- Returns 返回值说明
- Raises 异常说明
- Example 使用示例

#### 1.2.3 代码质量门禁
```toml
# pyproject.toml
[tool.mypy]
strict = true  # 启用严格模式
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true

[tool.ruff]
select = ["E", "W", "F", "I", "N", "PYI", "D"]  # 添加 D (pydocstyle)
```

### 1.3 验收标准
- [ ] mypy 通过率 100%
- [ ] 所有公共 API 有文档字符串
- [ ] ruff 检查 0 警告

---

## Phase 2: 补充高级功能 ⭐⭐⭐ → ⭐⭐⭐⭐⭐

### 2.1 图像识别集成

#### 2.1.1 新增 ImageSearchEngine
```python
# core/finder/image_search_engine.py
class ImageSearchEngine:
    """图像搜索引擎 - 基于模板匹配的图像识别"""
    
    def __init__(self, confidence: float = 0.9):
        """
        Args:
            confidence: 匹配置信度阈值 (0-1)
        """
        self.confidence = confidence
    
    def find(
        self, 
        template_path: str, 
        region: Optional[Rect] = None,
        timeout: int = 10
    ) -> Optional[Point]:
        """查找图像位置"""
        
    def find_all(
        self, 
        template_path: str,
        region: Optional[Rect] = None
    ) -> List[Point]:
        """查找所有匹配位置"""
        
    def click(
        self, 
        template_path: str,
        button: str = "left"
    ) -> bool:
        """找到并点击图像"""
```

#### 2.1.2 图像定位器
```python
# engine/locators/image_locator.py
@dataclass(frozen=True)
class ImageLocator:
    """图像定位器"""
    template_path: str
    confidence: float = 0.9
    timeout: int = 10
    
    @classmethod
    def from_yaml(cls, data: dict) -> "ImageLocator":
        ...
```

#### 2.1.3 使用示例
```python
from engine.locators import ImageLocator
from engine.component import ImageElement

# YAML 中使用
# elements:
#   submit_button:
#     type: image
#     template_path: images/submit_btn.png
#     confidence: 0.95

locator = ImageLocator("images/submit_btn.png", confidence=0.95)
btn = ImageElement(page, locator)
btn.click()
```

### 2.2 自定义等待条件

#### 2.2.1 扩展 WaitCondition
```python
# core/waiter/wait_condition.py
class WaitCondition(ABC):
    """等待条件基类"""
    
    @abstractmethod
    def check(self, element: Any) -> bool:
        """检查条件是否满足"""

class CustomWaitCondition(WaitCondition):
    """自定义等待条件"""
    
    def __init__(self, predicate: Callable[[Any], bool]):
        self.predicate = predicate
    
    def check(self, element: Any) -> bool:
        return self.predicate(element)

# 使用示例
def is_data_loaded(element):
    return "loading" not in element.text.lower()

condition = CustomWaitCondition(is_data_loaded)
SmartWait.wait_for_condition(condition, element, timeout=30)
```

#### 2.2.2 内置高级条件
```python
class WaitConditions:
    """内置等待条件工厂"""
    
    @staticmethod
    def text_contains(expected: str) -> WaitCondition:
        """等待文本包含"""
        
    @staticmethod
    def text_matches(pattern: str) -> WaitCondition:
        """等待文本匹配正则"""
        
    @staticmethod
    def attribute_equals(name: str, value: str) -> WaitCondition:
        """等待属性等于"""
        
    @staticmethod
    def style_contains(property: str, value: str) -> WaitCondition:
        """等待样式包含"""
```

### 2.3 验收标准
- [ ] 图像识别准确率 >95%
- [ ] 支持自定义等待条件
- [ ] 内置 10+ 高级等待条件

---

## Phase 3: 增强 YAML 能力

### 3.1 元素继承
```yaml
# framework/pages/base_page.yaml
# 基础页面元素
elements:
  base_menu:
    locator_type: automation_id
    locator_value: menu_bar
    component: menu

# framework/pages/login_page.yaml
extends: base_page.yaml
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    extends: base.base_input  # 继承基础输入框样式
```

### 3.2 动态数据支持
```yaml
# framework/pages/search_page.yaml
elements:
  search_results:
    locator_type: automation_id
    locator_value: lst_results
    component: list
    dynamic: true
    template:
      item:
        locator_type: class_name
        locator_value: SearchResultItem
      variables:
        - index
```

### 3.3 YAML 到 Python 代码生成器
```python
# scripts/generate_page_from_yaml.py
from engine.codegen import PageGenerator

generator = PageGenerator()
generator.generate(
    yaml_path="framework/pages/login_page.yaml",
    output_path="framework/pages/login_page.py"
)

# 生成的代码:
# class LoginPage(YamlPage):
#     username_input: TextInput
#     password_input: TextInput
#     login_button: Button
```

### 3.4 验收标准
- [ ] 支持 YAML 继承
- [ ] 支持动态元素
- [ ] YAML→Python 代码生成器可用

---

## Phase 4: 改进扩展性 ⭐⭐ → ⭐⭐⭐⭐⭐

### 4.1 插件机制

#### 4.1.1 插件接口
```python
# core/plugin/base.py
class Plugin(ABC):
    """插件基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        
    @abstractmethod
    def initialize(self, context: PluginContext) -> None:
        """初始化插件"""
        
    @abstractmethod
    def shutdown(self) -> None:
        """关闭插件"""

class ComponentPlugin(Plugin):
    """组件插件"""
    
    @abstractmethod
    def get_components(self) -> Dict[str, Type[BaseComponent]]:
        """返回组件字典"""

class LocatorPlugin(Plugin):
    """定位器插件"""
    
    @abstractmethod
    def get_locators(self) -> Dict[str, Type[BaseLocator]]:
        """返回定位器字典"""
```

#### 4.1.2 插件管理器
```python
# core/plugin/manager.py
class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugin_dirs: List[str]):
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dirs = plugin_dirs
    
    def load_all(self) -> None:
        """加载所有插件"""
        
    def register_plugin(self, plugin: Plugin) -> None:
        """注册插件"""
        
    def get_component(self, name: str) -> Type[BaseComponent]:
        """获取组件"""
        
    def get_locator(self, name: str) -> Type[BaseLocator]:
        """获取定位器"""
```

#### 4.1.3 插件示例
```python
# plugins/custom_components.py
from core.plugin import ComponentPlugin

class CustomComponentsPlugin(ComponentPlugin):
    @property
    def name(self) -> str:
        return "custom_components"
    
    def get_components(self) -> Dict[str, Type[BaseComponent]]:
        return {
            "custom_button": CustomButton,
            "custom_table": CustomTable,
        }
```

### 4.2 开闭原则改进

#### 4.2.1 组件注册表
```python
# engine/component/registry.py
class ComponentRegistry:
    """组件注册表 - 支持动态注册"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> "ComponentRegistry":
        ...
    
    def register(self, name: str, component: Type[BaseComponent]) -> None:
        """注册组件"""
        
    def get(self, name: str) -> Type[BaseComponent]:
        """获取组件"""
        
    def unregister(self, name: str) -> None:
        """注销组件"""

# 使用
ComponentRegistry.get_instance().register("my_button", MyButton)
```

### 4.3 验收标准
- [ ] 插件机制可用
- [ ] 支持运行时注册组件
- [ ] 无需修改核心代码即可扩展

---

## Phase 5: 完善日志报告

### 5.1 结构化日志
```python
# infra/logging/structured_logger.py
import json
from datetime import datetime

class StructuredLogger:
    """结构化日志 - JSON 格式"""
    
    def __init__(self, name: str, output_dir: str):
        self.name = name
        self.output_dir = output_dir
    
    def log(self, level: str, message: str, **kwargs) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "logger": self.name,
            "message": message,
            **kwargs
        }
        # 写入 JSON 文件
```

### 5.2 失败自动截图
```python
# infra/reporting/screenshot_on_failure.py
class ScreenshotOnFailure:
    """失败自动截图"""
    
    def __init__(self, output_dir: str = "reports/screenshots"):
        self.output_dir = output_dir
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
        if call.failed:
            # 自动截图
            screenshot_path = self.take_screenshot(item.name)
            # 附加到报告
            self.attach_to_report(screenshot_path)
```

### 5.3 自定义报告模板
```python
# infra/reporting/custom_template.py
class CustomReportTemplate:
    """自定义报告模板"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
    
    def generate(
        self,
        test_results: TestResults,
        output_path: str
    ) -> str:
        """生成自定义报告"""
```

### 5.4 验收标准
- [ ] 支持 JSON 格式日志
- [ ] 失败自动截图
- [ ] 自定义报告模板

---

## Phase 6: 补充缺失组件

### 6.1 新增组件清单

| 组件 | 优先级 | 预计工作量 |
|------|-------|----------|
| TabControl | P0 | 2h |
| TreeView | P0 | 3h |
| ListBox | P1 | 1h |
| DataGrid | P0 | 4h |
| RadioButton | P1 | 1h |
| Spinner | P2 | 1h |
| Slider | P2 | 1h |
| Hyperlink | P2 | 0.5h |

### 6.2 组件接口标准
```python
class TabControl(BaseComponent):
    """选项卡控件"""
    
    def select_tab(self, index_or_name: Union[int, str]) -> "TabControl":
        """选择选项卡"""
        
    def get_selected_tab(self) -> str:
        """获取选中的选项卡"""
        
    def get_tab_count(self) -> int:
        """获取选项卡数量"""
        
    def tab_exists(self, name: str) -> bool:
        """检查选项卡是否存在"""

class TreeView(BaseComponent):
    """树形控件"""
    
    def expand(self, path: str) -> "TreeView":
        """展开节点"""
        
    def collapse(self, path: str) -> "TreeView":
        """折叠节点"""
        
    def select(self, path: str) -> "TreeView":
        """选择节点"""
        
    def get_selected_path(self) -> str:
        """获取选中路径"""
```

### 6.3 验收标准
- [ ] 8 个新组件全部实现
- [ ] 每个组件有单元测试
- [ ] 使用示例文档

---

## Phase 7: 增强断言系统

### 7.1 图像对比断言
```python
class ImageAssertion:
    """图像断言"""
    
    def __init__(self, expected_path: str, confidence: float = 0.95):
        self.expected_path = expected_path
        self.confidence = confidence
    
    def should_match(self, region: Optional[Rect] = None) -> "ImageAssertion":
        """验证区域图像匹配"""
        
    def should_not_match(self) -> "ImageAssertion":
        """验证区域图像不匹配"""
```

### 7.2 属性断言
```python
class PropertyAssertion:
    """属性断言"""
    
    def has_property(self, name: str, expected_value: Any) -> "PropertyAssertion":
        """验证属性值"""
        
    def has_style(self, property: str, expected_value: str) -> "PropertyAssertion":
        """验证样式"""
        
    def has_attribute(self, name: str, expected_value: str) -> "PropertyAssertion":
        """验证自动化属性"""
```

### 7.3 自定义断言扩展
```python
class CustomAssertion(Assertion):
    """自定义断言"""
    
    def __init__(self, predicate: Callable[[], bool], description: str):
        self.predicate = predicate
        self.description = description
    
    def verify(self) -> bool:
        return self.predicate()

# 使用
Assert.that_custom(
    lambda: page.element("btn").is_enabled(),
    "按钮应该启用"
).should_be_true()
```

### 7.4 验收标准
- [ ] 图像对比断言可用
- [ ] 属性断言覆盖 10+ 属性
- [ ] 支持自定义断言

---

## Phase 8: 配置管理增强

### 8.1 环境变量覆盖
```python
# infra/config/config_manager.py
class ConfigManager:
    def get_env_config(self, env: str) -> dict:
        config = self._load_yaml_config(env)
        
        # 环境变量覆盖
        for key, value in os.environ.items():
            if key.startswith("ATM_"):
                config_key = key[4:].lower()
                config[config_key] = value
        
        return config
```

### 8.2 配置加密
```python
# infra/config/encryption.py
from cryptography.fernet import Fernet

class ConfigEncryption:
    """配置加密"""
    
    def __init__(self, key: Optional[str] = None):
        self.key = key or self._load_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, value: str) -> str:
        """加密值"""
        
    def decrypt(self, encrypted_value: str) -> str:
        """解密值"""

# YAML 使用
# database:
#   password: ENC[AES256_GCM,aes256_key,iv]
```

### 8.3 配置校验
```python
# infra/config/validator.py
class ConfigValidator:
    """配置校验器"""
    
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate(self, config: dict) -> ValidationResult:
        """校验配置"""
        
# Schema 示例
schema = {
    "app_path": {"type": "string", "required": true, "exists": true},
    "timeout": {"type": "integer", "min": 1, "max": 300},
    "environment": {"type": "string", "enum": ["dev", "test", "prod"]}
}
```

### 8.4 验收标准
- [ ] 环境变量覆盖可用
- [ ] 支持配置加密
- [ ] 配置校验机制完善

---

## Phase 9: 性能优化

### 9.1 pytest-xdist 配置
```toml
# pytest.ini
[pytest]
addopts = -n auto  # 自动检测 CPU 核心数
          --reruns 2
          --reruns-delay 2
          --timeout 300
```

### 9.2 失败重试配置
```python
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--retry-flaky",
        action="store_true",
        help="Retry flaky tests"
    )

@pytest.hookimpl
def pytest_collection_modifyitems(config, items):
    if config.getoption("--retry-flaky"):
        for item in items:
            item.add_marker(pytest.mark.flaky(reruns=3, reruns_delay=2))
```

### 9.3 超时控制
```python
# core/driver/timeout.py
class TimeoutManager:
    """超时管理器"""
    
    def __init__(
        self,
        default_timeout: int = 30,
        global_timeout: int = 300
    ):
        self.default_timeout = default_timeout
        self.global_timeout = global_timeout
    
    def with_timeout(self, timeout: int) -> TimeoutContext:
        """设置超时上下文"""
```

### 9.4 验收标准
- [ ] 并行测试可用
- [ ] 失败自动重试
- [ ] 全局超时控制

---

## Phase 10: 文档同步

### 10.1 文档审查清单
- [ ] README 统计数字与实际一致
- [ ] 设计文档与实现一致
- [ ] API 文档完整
- [ ] 使用示例可运行

### 10.2 自动化文档生成
```bash
# 生成 API 文档
pdoc --html --output-directory docs/api core engine infra

# 生成使用统计
python scripts/generate_stats.py
```

### 10.3 验收标准
- [ ] 文档 100% 与实现同步
- [ ] 所有示例可运行
- [ ] API 文档自动生成

---

## Phase 11: Git 历史整理

### 11.1 版本标签
```bash
# 创建版本标签
git tag -a v1.0.0 -m "AutoTestMe-NG v1.0.0 - Initial Release"
git tag -a v2.0.0 -m "AutoTestMe-NG v2.0.0 - Major Improvements"
git push origin --tags
```

### 11.2 提交历史清理
```bash
# 整理提交历史 (谨慎使用)
git filter-branch --msg-filter '
    if [[ $GIT_COMMIT == docs:* ]]; then
        echo "docs: " ${GIT_COMMIT#docs: }
    else
        echo $GIT_COMMIT
    fi
'
```

### 11.3 验收标准
- [ ] v1.0.0 和 v2.0.0 标签创建
- [ ] 提交历史清晰
- [ ] CHANGELOG.md 更新

---

## 📅 实施计划

| Phase | 预计工时 | 依赖 | 优先级 |
|-------|---------|------|--------|
| Phase 1: 代码质量 | 8h | 无 | P0 |
| Phase 2: 高级功能 | 12h | 无 | P0 |
| Phase 3: YAML 增强 | 8h | Phase 1 | P1 |
| Phase 4: 扩展性 | 10h | Phase 1 | P1 |
| Phase 5: 日志报告 | 8h | Phase 1 | P1 |
| Phase 6: 新组件 | 14h | Phase 1 | P1 |
| Phase 7: 断言增强 | 6h | Phase 2 | P2 |
| Phase 8: 配置增强 | 6h | Phase 1 | P2 |
| Phase 9: 性能优化 | 4h | Phase 1 | P2 |
| Phase 10: 文档同步 | 6h | All | P2 |
| Phase 11: Git 整理 | 2h | All | P3 |

**总工时**: 约 84 小时

---

## ✅ 验收标准汇总

### v2.0 完成标准

| 维度 | 验收标准 |
|------|---------|
| 代码质量 | mypy 100% 通过，0 警告 |
| 功能完整性 | 12 个缺点全部修复 |
| 扩展性 | 插件机制可用，无需修改核心代码 |
| 稳定性 | 并行测试 + 失败重试 + 超时控制 |
| 文档 | 100% 与实现同步 |

---

**文档结束**
