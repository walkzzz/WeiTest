# AutoTestMe-NG

下一代 Windows UI 自动化测试框架

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 定义页面 (YAML)

创建 `framework/pages/login_page.yaml`:

```yaml
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
  
  login_button:
    locator_type: name
    locator_value: 登录
    control_type: Button
    description: "登录按钮"
```

### 3. 编写测试

创建 `tests/test_login.py`:

```python
from engine.page.yaml_page import YamlPage
from engine.component.button import Button
from engine.component.input import TextInput
from engine.assertion import Assert

def test_login():
    page = YamlPage.from_yaml("framework/pages/login_page.yaml")
    page.start_app("your_app.exe")
    page.set_window(page.get_window("登录"))
    
    # 使用组件
    username = TextInput(page, page.element("username_input"))
    login_btn = Button(page, page.element("login_button"))
    
    # 执行操作
    username.type("admin")
    login_btn.click()
    
    # 断言
    Assert.ui(page, page.element("login_button")).should_be_visible()
    
    page.close()
```

### 4. 运行测试

```bash
pytest tests/test_login.py -v
```

## 项目结构

```
autotestme-ng/
├── core/              # Core Layer - pywinauto 封装
├── engine/            # Engine Layer - PageObject/组件/断言
├── infra/             # Infra Layer - 配置/日志/报告
├── framework/         # Framework Layer - 业务页面和测试
└── tests/             # 框架自测
```

## 核心功能

### Core Layer
- ✅ ApplicationDriver - 应用生命周期管理
- ✅ WindowDriver - 窗口操作
- ✅ Locator - 类型安全的元素定位
- ✅ SearchEngine - 元素搜索
- ✅ SmartWait - 智能等待机制

### Engine Layer
- ✅ Page Mixin 架构 - 组合优于继承
- ✅ YamlPage - YAML 驱动页面定义
- ✅ UI 组件库 - Button/Input/CheckBox/ComboBox/Label
- ✅ 断言引擎 - UIAssertion + AssertionChain

### Infra Layer
- ✅ ConfigManager - YAML 配置管理
- ✅ Logger - 日志系统（文件轮转）
- ✅ ReportManager - Allure/HTML 报告

## 使用示例

### 使用组件

```python
from engine.component import Button, TextInput, CheckBox

# 按钮
btn = Button(page, ByID("btn_login"))
btn.click()

# 输入框
input_box = TextInput(page, ByID("txt_username"))
input_box.type("admin")

# 复选框
chk = CheckBox(page, ByID("chk_remember"))
chk.check()
```

### 使用断言

```python
from engine.assertion import Assert

# UI 断言
Assert.ui(page, ByID("btn_login")).should_be_visible()

# 链式断言
(Assert.that(title)
    .is_not_none()
    .contains("Login"))
```

### 使用配置

```python
from infra.config import ConfigManager

config = ConfigManager("framework/data")
env = config.get_env_config("test")
print(env["app_path"])
```

### 使用日志

```python
from infra.logging import Logger, get_logger

logger = Logger("MyTest")
logger.info("测试开始")
logger.error("发生错误")
```

### 使用报告

```python
from infra.reporting import ReportManager

reporter = ReportManager()
reporter.create_allure_report()
reporter.open_html_report()
```

## 运行测试

```bash
# 运行所有测试
pytest -v

# 运行特定测试
pytest tests/test_login.py -v

# 生成报告
pytest --alluredir=reports/allure-results -v
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 技术栈

- **Python**: 3.9+
- **UI 自动化**: pywinauto 0.6.8+
- **测试框架**: pytest 7.4.0+
- **配置管理**: PyYAML 6.0.1+
- **报告系统**: Allure + pytest-html
- **代码质量**: mypy + ruff + black

## 文档

- [设计文档](docs/superpowers/specs/2026-03-28-autotestme-ng-design.md)
- [Core Layer 计划](docs/superpowers/plans/2026-03-28-autotestme-ng-core-layer.md)
- [Engine Layer 计划](docs/superpowers/plans/2026-03-28-autotestme-ng-engine-layer.md)
- [Infra Layer 计划](docs/superpowers/plans/2026-03-28-autotestme-ng-infra-layer.md)

## 统计

- **代码行数**: 4,256 行
- **测试用例**: 75 个
- **提交数**: 14 个
- **模块数**: 32 个

## License

MIT
