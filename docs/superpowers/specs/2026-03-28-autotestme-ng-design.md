# WeiTest 框架设计文档

**文档版本**: v1.0  
**创建日期**: 2026-03-28  
**作者**: AI Agent  
**状态**: 已批准  
**项目名称**: WeiTest (Next Generation)

---

## 📋 目录

1. [概述](#1-概述)
2. [项目结构](#2-项目结构)
3. [核心层设计](#3-核心层设计)
4. [引擎层设计](#4-引擎层设计)
5. [YAML PageObject 规范](#5-yaml-pageobject-规范)
6. [测试分层策略](#6-测试分层策略)
7. [Jenkins Pipeline 设计](#7-jenkins-pipeline-设计)
8. [文档结构](#8-文档结构)
9. [实施计划](#9-实施计划)

---

## 1. 概述

### 1.1 项目背景

WeiTest 是 AutoTestMe 框架的下一代版本，采用**激进式重构**策略重新设计，旨在解决原框架的架构问题，提供清晰的分层、模块化设计和企业级 CI/CD 集成。

### 1.2 设计目标

| 目标 | 说明 |
|------|------|
| **清晰分层** | Core/Engine/Framework/Infra 四层分离 |
| **单一职责** | Mixin 模式拆分功能，每个类只做一件事 |
| **YAML 驱动** | 零代码定义页面对象 |
| **组件化** | 可复用的 UI 组件库 |
| **测试分层** | Unit/Integration/UI金字塔 |
| **CI/CD集成** | 完整的 Jenkins Pipeline |
| **中英双语** | 完整的文档体系 |

### 1.3 技术选型

| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **UI 自动化** | pywinauto | ≥0.6.8 | UIA 后端 |
| **测试框架** | pytest | ≥7.4.0 | 测试执行器 |
| **配置管理** | pyyaml | ≥6.0.1 | YAML 解析 |
| **报告系统** | allure-pytest | ≥2.13.2 | 交互式报告 |
| **报告系统** | pytest-html | ≥4.0.0 | HTML 报告 |
| **代码质量** | mypy | ≥1.0.0 | 类型检查 |
| **代码质量** | ruff | ≥0.1.0 | Lint 检查 |
| **代码格式** | black | ≥23.0.0 | 代码格式化 |
| **CI/CD** | Jenkins | 最新 | Pipeline |

### 1.4 架构原则

```
┌─────────────────────────────────────────────────────────┐
│                    Framework Layer                       │
│  (团队编写：pages/ + tests/ + data/)                      │
└────────────────────┬────────────────────────────────────┘
                     ↓ depends on
┌─────────────────────────────────────────────────────────┐
│                     Engine Layer                         │
│  (PageObject 基类 + 组件库 + 断言引擎)                      │
└────────────────────┬────────────────────────────────────┘
                     ↓ depends on
┌─────────────────────────────────────────────────────────┐
│                      Core Layer                          │
│  (Driver + Finder + Waiter - 封装 pywinauto)              │
└────────────────────┬────────────────────────────────────┘
                     ↓ depends on
┌─────────────────────────────────────────────────────────┐
│                   External Libraries                     │
│  (pywinauto + pyyaml + pytest + allure)                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Infra Layer (横向)                      │
│  (CI + Config + Reporting + Logging - 服务所有层)          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 项目结构

### 2.1 目录结构

```
autotestme-ng/
│
├── README.md                    # 项目介绍（中英双语索引）
├── README_CN.md                 # 中文 README
├── LICENSE
├── pyproject.toml               # 项目配置（mypy/ruff/black/pytest）
├── requirements.txt             # 生产依赖
├── requirements-dev.txt         # 开发依赖（pytest/mypy/ruff）
│
├── core/                        # 【核心层】框架核心，不可变
│   ├── __init__.py
│   ├── driver/                  # pywinauto 封装
│   │   ├── __init__.py
│   │   ├── application.py       # Application 启动/连接/关闭
│   │   ├── window.py            # Window 获取/操作
│   │   └── backend.py           # 后端管理（UIA/Win32 切换）
│   ├── finder/                  # 元素定位引擎
│   │   ├── __init__.py
│   │   ├── locator.py           # 定位器定义（类型安全）
│   │   ├── search_engine.py     # 元素搜索策略
│   │   └── strategies.py        # 定位策略（ID/Name/XPath 等）
│   └── waiter/                  # 智能等待机制
│       ├── __init__.py
│       ├── wait_condition.py    # 等待条件（Visible/Enabled/Exists）
│       └── smart_wait.py        # 智能等待（轮询 + 超时）
│
├── engine/                      # 【引擎层】可扩展
│   ├── __init__.py
│   ├── page/                    # PageObject 引擎
│   │   ├── __init__.py
│   │   ├── base_page.py         # 页面对象基类（组合 Mixin）
│   │   └── yaml_page.py         # YAML 驱动的页面对象
│   ├── component/               # UI 组件库
│   │   ├── __init__.py
│   │   ├── button.py            # 按钮组件
│   │   ├── input.py             # 输入框组件
│   │   ├── combobox.py          # 下拉框组件
│   │   ├── checkbox.py          # 复选框组件
│   │   ├── table.py             # 表格组件
│   │   └── label.py             # 标签组件
│   └── assertion/               # 断言引擎
│       ├── __init__.py
│       ├── base_assert.py       # 断言基类
│       ├── ui_assert.py         # UI 断言（存在/可见/文本）
│       └── assertion_chain.py   # 链式断言
│
├── framework/                   # 【框架层】团队业务层
│   ├── __init__.py
│   ├── pages/                   # 业务页面对象
│   │   ├── __init__.py
│   │   └── login_page.py        # 登录页面示例
│   │   └── login_page.yaml      # 登录页面 YAML 定义
│   ├── tests/                   # 测试用例
│   │   ├── __init__.py
│   │   ├── unit/                # 单元测试
│   │   ├── integration/         # 集成测试
│   │   └── ui/                  # UI 测试
│   └── data/                    # 测试数据
│       ├── __init__.py
│       ├── env.yaml             # 环境配置（test/dev/prod）
│       └── test_data.yaml       # 测试数据（参数化）
│
├── infra/                       # 【基础设施】
│   ├── __init__.py
│   ├── ci/                      # CI/CD
│   │   ├── __init__.py
│   │   ├── Jenkinsfile          # Jenkins Pipeline
│   │   └── deploy.ps1           # 部署脚本
│   ├── config/                  # 配置管理
│   │   ├── __init__.py
│   │   ├── config_manager.py    # 配置加载器
│   │   └── yaml_loader.py       # YAML 加载器
│   ├── reporting/               # 报告系统
│   │   ├── __init__.py
│   │   ├── allure_report.py     # Allure 报告生成
│   │   └── html_report.py       # pytest-html 报告
│   └── logging/                 # 日志系统
│       ├── __init__.py
│       └── logger.py            # 结构化日志
│
├── tests/                       # 【框架自测】测试框架本身
│   ├── __init__.py
│   ├── test_core/               # 核心层测试
│   ├── test_engine/             # 引擎层测试
│   └── test_infra/              # 基础设施测试
│
├── docs/                        # 【文档】中英双语
│   ├── en/                      # 英文文档
│   ├── zh-CN/                   # 中文文档
│   └── api/                     # 自动生成的 API 文档
│
└── examples/                    # 【示例】完整示例
    └── login_example/
```

### 2.2 模块职责

| 层级 | 模块 | 职责 | 可变性 |
|------|------|------|--------|
| **Core** | `driver` | pywinauto 封装，隐藏底层细节 | 🔒 不可变 |
| **Core** | `finder` | 元素定位策略和搜索引擎 | 🔒 不可变 |
| **Core** | `waiter` | 智能等待机制（轮询 + 超时） | 🔒 不可变 |
| **Engine** | `page` | PageObject 基类和 YAML 支持 | 🔧 可扩展 |
| **Engine** | `component` | UI 组件库（按钮/输入框等） | 🔧 可扩展 |
| **Engine** | `assertion` | 断言引擎和链式断言 | 🔧 可扩展 |
| **Framework** | `pages` | 业务页面对象（团队自定义） | ✏️ 自定义 |
| **Framework** | `tests` | 测试用例（团队自定义） | ✏️ 自定义 |
| **Infra** | `ci` | Jenkins Pipeline 配置 | ⚙️ 可配置 |
| **Infra** | `config` | 配置管理（YAML 加载） | ⚙️ 可配置 |
| **Infra** | `reporting` | 报告生成（Allure/HTML） | ⚙️ 可配置 |

---

## 3. 核心层设计

### 3.1 Driver 模块

#### ApplicationDriver

```python
class ApplicationDriver:
    """应用程序驱动器 - 管理 Windows 应用的生命周期"""
    
    def start(self, app_path: str, timeout: int = 30) -> 'ApplicationDriver'
    def connect(self, title: Optional[str] = None, process_id: Optional[int] = None, timeout: int = 30) -> 'ApplicationDriver'
    def close(self) -> 'ApplicationDriver'
    def get_window(self, title: str) -> 'WindowDriver'
```

#### WindowDriver

```python
class WindowDriver:
    """窗口驱动器 - 管理单个窗口的操作"""
    
    def maximize() -> 'WindowDriver'
    def minimize() -> 'WindowDriver'
    def close() -> 'WindowDriver'
    def find_element(locator: 'Locator') -> 'ElementWrapper'
```

### 3.2 Finder 模块

#### Locator

```python
@dataclass(frozen=True)
class Locator:
    """定位器 - 类型安全的元素定位定义"""
    
    type: LocatorType
    value: str
    control_type: Optional[str] = None
    timeout: Optional[int] = None
    
    @classmethod
    def from_yaml(cls, data: dict) -> 'Locator'
    def to_dict(self) -> dict
```

#### SearchEngine

```python
class SearchEngine:
    """元素搜索引擎"""
    
    def find(locator: Locator, timeout: Optional[int] = None) -> 'ElementWrapper'
    def find_all(locator: Locator) -> List['ElementWrapper']
    def exists(locator: Locator, timeout: int = 0) -> bool
```

### 3.3 Waiter 模块

#### WaitCondition

```python
class WaitCondition(ABC):
    """等待条件基类"""
    
    @abstractmethod
    def check(element: Any) -> bool
```

#### SmartWait

```python
class SmartWait:
    """智能等待器"""
    
    def wait_until(condition: Callable[[], bool], timeout: Optional[int] = None) -> bool
    def wait_for_condition(condition: 'WaitCondition', element: Any, timeout: Optional[int] = None) -> bool
    def wait_for_element(locator: 'Locator', search_engine: 'SearchEngine', timeout: Optional[int] = None) -> 'ElementWrapper'
```

### 3.4 异常层次

```python
CoreError
├── DriverError
│   ├── ApplicationStartError
│   ├── ApplicationConnectError
│   └── WindowNotFoundError
├── FinderError
│   ├── ElementNotFoundError
│   └── InvalidLocatorError
└── WaiterError
    └── WaitTimeoutError
```

---

## 4. 引擎层设计

### 4.1 Page 模块 - Mixin 架构

```python
class ApplicationMixin:
    """应用管理 Mixin - 职责：应用程序的启动、连接、关闭"""
    
    def start_app(app_path: str, timeout: int = 30) -> 'ApplicationMixin'
    def connect_app(title: Optional[str] = None, process_id: Optional[int] = None, timeout: int = 30) -> 'ApplicationMixin'
    def close_app() -> 'ApplicationMixin'

class ElementMixin:
    """元素定位 Mixin - 职责：元素的查找和等待"""
    
    def find_element(locator: Locator) -> 'ElementWrapper'
    def find_elements(locator: Locator) -> List['ElementWrapper']
    def wait_element(locator: Locator, condition: WaitConditionType, timeout: int = 10) -> 'ElementWrapper'

class ActionMixin:
    """操作 Mixin - 职责：元素交互操作"""
    
    def click(locator: Locator) -> 'ActionMixin'
    def double_click(locator: Locator) -> 'ActionMixin'
    def type_text(locator: Locator, text: str, clear: bool = True) -> 'ActionMixin'
    def select_combobox(locator: Locator, value: str) -> 'ActionMixin'
    def check_checkbox(locator: Locator, check: bool = True) -> 'ActionMixin'

class ScreenshotMixin:
    """截图 Mixin - 职责：屏幕和元素截图"""
    
    def take_screenshot(filename: str) -> str
    def capture_element(locator: Locator, filename: str) -> str

class BasePage(ApplicationMixin, ElementMixin, ActionMixin, ScreenshotMixin, ABC):
    """页面对象基类 - 组合所有 Mixin"""
```

### 4.2 Component 模块

| 组件 | 说明 | 主要方法 |
|------|------|----------|
| `Button` | 按钮组件 | `click()`, `double_click()`, `wait_clickable()`, `text` |
| `TextInput` | 输入框组件 | `type()`, `clear()`, `set_value()`, `value` |
| `ComboBox` | 下拉框组件 | `select()`, `select_by_index()`, `options`, `selected_value` |
| `CheckBox` | 复选框组件 | `check()`, `uncheck()`, `toggle()`, `is_checked` |

### 4.3 Assertion 模块

#### UIAssertion

```python
class UIAssertion:
    """UI 断言 - 验证 UI 元素的状态"""
    
    # 存在性断言
    def should_exist(timeout: int = 0) -> 'UIAssertion'
    def should_not_exist() -> 'UIAssertion'
    
    # 可见性断言
    def should_be_visible(timeout: int = 10) -> 'UIAssertion'
    
    # 可用性断言
    def should_be_enabled() -> 'UIAssertion'
    def should_be_disabled() -> 'UIAssertion'
    
    # 文本断言
    def text_should_equal(expected: str) -> 'UIAssertion'
    def text_should_contain(expected: str) -> 'UIAssertion'
    def text_should_not_be_empty() -> 'UIAssertion'

class Assert:
    """断言快捷入口"""
    
    @staticmethod
    def that(actual: Any, description: str = "") -> AssertionChain
    @staticmethod
    def ui(page: BasePage, locator: Locator) -> UIAssertion
```

---

## 5. YAML PageObject 规范

### 5.1 YAML Schema

```yaml
elements:
  <element_name>:
    locator_type: <type>       # 必需：id/name/class_name/automation_id/xpath
    locator_value: <value>     # 必需：定位值
    
    # 可选字段
    control_type: <type>       # 控件类型
    description: <text>        # 元素描述
    timeout: <seconds>         # 自定义超时
    component: <type>          # 组件类型：button/input/combobox/checkbox
    wait_condition: <type>     # 等待条件：visible/enabled/clickable
    actions:                   # 预定义操作序列
      - type: <action_type>
        value: <action_value>
```

### 5.2 完整示例

```yaml
# framework/pages/login_page.yaml

elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
    component: input
    wait_condition: visible
  
  password_input:
    locator_type: id
    locator_value: txt_password
    control_type: Edit
    description: "密码输入框"
    component: input
  
  login_button:
    locator_type: name
    locator_value: 登录
    control_type: Button
    description: "登录按钮"
    component: button
    wait_condition: clickable
  
  remember_checkbox:
    locator_type: id
    locator_value: chk_remember
    control_type: CheckBox
    description: "记住密码复选框"
    component: checkbox
```

### 5.3 使用方式

```python
from engine.page.yaml_page import YamlPage

page = YamlPage.from_yaml("framework/pages/login_page.yaml")
page.start_app("app.exe")
page.set_window(page.get_window("登录"))

# 获取元素定位器
locator = page.element("username_input")

# 使用组件
from engine.component.input import TextInput
username = TextInput(page, page.element("username_input"))
username.type("admin")

# 使用断言
from engine.assertion import Assert
Assert.ui(page, page.element("login_button")).should_be_visible()
```

---

## 6. 测试分层策略

### 6.1 测试金字塔

```
                    ╱╲
                   ╱  ╲
                  ╱ UI ╲                 10-20 个
                 ╱──────╲                (端到端流程)
                ╱        ╲
               ╱Integration╲             50-100 个
              ╱────────────╲            (模块集成)
             ╱              ╲
            ╱    Unit Tests   ╲          200-500 个
           ╱──────────────────╲         (函数/类级别)
```

### 6.2 单元测试层

**位置**: `tests/unit/`  
**目标**: 测试框架本身的核心功能

```python
# tests/unit/core/test_finder.py

class TestLocator:
    def test_create_locator(self)
    def test_from_yaml(self)
    def test_to_dict(self)

class TestSmartWait:
    def test_wait_until_success(self)
    def test_wait_until_timeout(self)
```

### 6.3 集成测试层

**位置**: `tests/integration/`  
**目标**: 测试模块间的集成

```python
# tests/integration/test_page_component_integration.py

class TestPageComponentIntegration:
    def test_button_component_with_page(self)
    def test_yaml_page_factory(self)
```

### 6.4 UI 测试层

**位置**: `framework/tests/ui/`  
**目标**: 测试真实应用的 UI 功能

```python
# framework/tests/ui/test_login.py

@allure.feature("登录模块")
class TestLoginUI:
    @pytest.mark.smoke
    def test_login_success(self, login_page)
    
    @pytest.mark.regression
    def test_login_wrong_password(self, login_page)
```

### 6.5 测试标签

```ini
[pytest]
markers =
    smoke: 冒烟测试（核心功能，快速验证）
    regression: 回归测试（完整功能验证）
    p0: P0 优先级（阻塞性）
    p1: P1 优先级（高优先级）
    p2: P2 优先级（中优先级）
```

### 6.6 测试执行

```bash
# 冒烟测试
pytest -m smoke -v

# 回归测试
pytest -m regression -v

# UI 测试
pytest framework/tests/ui/ -v

# 并行执行
pytest -n 4 -v

# 失败重试
pytest --reruns 2 --reruns-delay 2 -v
```

---

## 7. Jenkins Pipeline 设计

### 7.1 Pipeline 流程

```
1. Checkout → 2. Setup → 3. Test → 4. Report → 5. Archive → 6. Notify
```

### 7.2 关键配置

```groovy
pipeline {
    agent { label 'windows-agent' }
    
    stages {
        stage('Checkout') { }
        stage('Environment Setup') { }
        stage('Install Dependencies') { }
        stage('Health Check') { }
        stage('Code Quality') {
            parallel {
                stage('Lint Check') { }
                stage('Type Check') { }
                stage('Format Check') { }
            }
        }
        stage('Run Tests') {
            parallel {
                stage('Unit Tests') { }
                stage('Integration Tests') { }
                stage('UI Tests') { }
            }
        }
        stage('Generate Reports') { }
        stage('Archive Artifacts') { }
        stage('Deploy') { }
    }
    
    post {
        success { send_success_email() }
        failure { send_failure_email() }
    }
}
```

### 7.3 触发器

- **Git 推送**: 每 5 分钟检查
- **定时触发**: 工作日早上 8 点运行完整测试
- **手动触发**: Jenkins UI

### 7.4 部署脚本

```powershell
# infra/ci/deploy.ps1

# 1. 备份现有部署
# 2. 停止相关服务
# 3. 复制新文件
# 4. 安装新版本
# 5. 验证部署
# 6. 运行健康检查
# 7. 启动服务
```

---

## 8. 文档结构

### 8.1 目录结构

```
docs/
├── en/                      # 英文文档
│   ├── getting-started.md
│   ├── user-guide/
│   ├── api-reference/
│   └── ci-cd/
├── zh-CN/                   # 中文文档
│   ├── getting-started.md
│   ├── user-guide/
│   ├── api-reference/
│   └── ci-cd/
└── api/                     # 自动生成的 API 文档
```

### 8.2 文档生成

```bash
# 生成 API 文档
pdoc --html --output-directory docs/api core engine infra

# 运行文档生成脚本
python scripts/generate_docs.py
```

---

## 9. 实施计划

### 9.1 阶段划分

| 阶段 | 任务 | 输出 | 预计轮次 |
|------|------|------|---------|
| **阶段 1** | 核心层实现 | core/ 完整功能 | 3-4 轮 |
| **阶段 2** | 引擎层实现 | engine/ 完整功能 | 3-4 轮 |
| **阶段 3** | 基础设施 | infra/ + Jenkins | 2-3 轮 |
| **阶段 4** | 示例与文档 | examples/ + docs/ | 2-3 轮 |
| **阶段 5** | 框架自测 | tests/ 完整覆盖 | 2-3 轮 |

### 9.2 优先级

| 优先级 | 模块 | 说明 |
|--------|------|------|
| **P0** | `core/driver/` | 应用/窗口管理 - 基础中的基础 |
| **P0** | `core/finder/` | 元素定位 - 核心能力 |
| **P0** | `core/waiter/` | 智能等待 - 稳定性保障 |
| **P1** | `engine/page/` | PageObject 基类 |
| **P1** | `engine/component/` | UI 组件库 |
| **P1** | `engine/assertion/` | 断言引擎 |
| **P2** | `infra/ci/` | Jenkins Pipeline |
| **P2** | `infra/config/` | 配置管理 |
| **P2** | `framework/` | 示例和模板 |

---

## 附录

### A. 术语表

| 术语 | 说明 |
|------|------|
| **UIA** | Windows UI Automation |
| **PageObject** | 页面对象模式 |
| **Mixin** | 混入类，组合优于继承 |
| **Locator** | 元素定位器 |
| **Fixture** | pytest 测试夹具 |

### B. 参考资源

- [pywinauto 文档](https://pywinauto.readthedocs.io/)
- [pytest 文档](https://docs.pytest.org/)
- [Allure 文档](https://docs.qameta.io/allure/)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)

---

**文档结束**
