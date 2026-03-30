# WeiTest 快速开始指南

**版本**: 2.0.1  
**更新日期**: 2026-03-30

---

## 🚀 5 分钟快速开始

### 1. 安装 WeiTest

```bash
pip install wei-test
```

### 2. 创建第一个测试项目

```bash
# 使用 CLI 工具创建项目
wei init my_first_test
cd my_first_test
```

### 3. 定义页面对象

创建 `pages/login_page.yaml`:

```yaml
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
  
  password_input:
    locator_type: id
    locator_value: txt_password
    control_type: Edit
    description: "密码输入框"
  
  login_button:
    locator_type: id
    locator_value: btn_login
    control_type: Button
    description: "登录按钮"
```

### 4. 编写测试用例

创建 `tests/test_login.py`:

```python
from wei.engine.page.yaml_page import YamlPage
from wei.engine.component.input import TextInput
from wei.engine.component.button import Button
from wei.engine.assertion import Assert

def test_login_success():
    """测试成功登录"""
    # 加载页面
    page = YamlPage.from_yaml("pages/login_page.yaml")
    
    # 启动应用
    page.start_app("notepad.exe")
    
    # 使用组件
    username = TextInput(page, page.element("username_input"))
    password = TextInput(page, page.element("password_input"))
    login_btn = Button(page, page.element("login_button"))
    
    # 执行操作
    username.type("admin")
    password.type("password123")
    login_btn.click()
    
    # 断言验证
    Assert.ui(page, page.element("login_button")).should_be_visible()
    
    # 清理
    page.close()
```

### 5. 运行测试

```bash
# 运行单个测试
pytest tests/test_login.py -v

# 运行所有测试
pytest tests/ -v

# 生成报告
pytest tests/ --html=reports/report.html
```

---

## 📚 核心概念

### WeiTest 架构

```
┌─────────────────────────────────────────┐
│          Framework Layer                 │
│   (你的业务代码：pages + tests)           │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           Engine Layer                   │
│   (WeiTest 核心：Page + Component)        │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│            Core Layer                    │
│   (底层封装：Driver + Finder + Waiter)    │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         pywinauto                        │
└─────────────────────────────────────────┘
```

### 三大核心模块

#### 1. Core Layer - 核心层
```python
from wei.core import ApplicationDriver, WindowDriver

# 管理应用生命周期
app = ApplicationDriver()
app.start("notepad.exe")
window = app.get_window("无标题 - 记事本")
```

#### 2. Engine Layer - 引擎层
```python
from wei.engine import Page, Component
from wei.engine.component import Button, TextInput

# 页面对象和组件
page = Page()
button = Button(page, locator)
```

#### 3. Infra Layer - 基础设施层
```python
from wei.infra import ConfigManager, Logger, ReportManager

# 配置、日志、报告
config = ConfigManager("data")
logger = Logger("MyTest")
```

---

## 🎯 CLI 命令速查

### 项目管理

```bash
# 初始化新项目
wei init myproject

# 使用完整模板
wei init myproject --template full
```

### 创建资源

```bash
# 创建页面对象
wei create page login

# 创建 YAML 定义的页面
wei create page login --yaml

# 创建测试文件
wei create test test_login
```

### 执行测试

```bash
# 运行测试
wei run tests/

# 详细输出
wei run tests/ -v

# 并行执行
wei run tests/ --parallel
```

### 报告和维护

```bash
# 生成 HTML 报告
wei report --html

# 生成 Allure 报告
wei report --type allure

# 清理缓存
wei clean
```

---

## 📖 常用组件示例

### Button - 按钮

```python
from wei.engine.component import Button

btn = Button(page, ByID("btn_login"))
btn.click()
btn.wait_clickable(timeout=10)
```

### TextInput - 输入框

```python
from wei.engine.component import TextInput

input_box = TextInput(page, ByID("txt_username"))
input_box.type("admin")
input_box.clear()
```

### CheckBox - 复选框

```python
from wei.engine.component import CheckBox

chk = CheckBox(page, ByID("chk_remember"))
chk.check()
chk.uncheck()
chk.toggle()
```

### ComboBox - 下拉框

```python
from wei.engine.component import ComboBox

combo = ComboBox(page, ByID("combo_city"))
combo.select("北京")
combo.select_by_index(0)
```

---

## ✅ 断言使用

### 基本断言

```python
from wei.engine.assertion import Assert

# 值断言
Assert.that(value).is_not_none()
Assert.that(text).contains("expected")
Assert.that(number).equals(100)
```

### UI 断言

```python
# 元素存在性
Assert.ui(page, locator).should_exist()

# 可见性
Assert.ui(page, locator).should_be_visible()

# 可用性
Assert.ui(page, locator).should_be_enabled()

# 文本断言
Assert.ui(page, locator).text_should_equal("标题")
```

### 链式断言

```python
(Assert.that(title, "窗口标题")
    .is_not_none()
    .contains("Login")
    .length_greater_than(5))
```

---

## 🔧 配置示例

### 环境配置

创建 `data/env.yaml`:

```yaml
environments:
  test:
    app_path: "C:\\Apps\\MyApp\\app.exe"
    timeout: 30
    environment: test
  
  dev:
    app_path: "C:\\Dev\\MyApp\\app.exe"
    timeout: 60
    environment: dev
  
  prod:
    app_path: "C:\\Program Files\\MyApp\\app.exe"
    timeout: 90
    environment: prod
```

### 使用配置

```python
from wei.infra.config import ConfigManager

config = ConfigManager("data")
env_config = config.get_env_config("test")
print(env_config["app_path"])
```

---

## 📊 测试报告

### HTML 报告

```bash
# 生成 HTML 报告
pytest tests/ --html=reports/report.html --self-contained-html

# 自动打开
wei report --html --open
```

### Allure 报告

```bash
# 生成 Allure 数据
pytest tests/ --alluredir=reports/allure-results

# 生成报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

---

## 🐛 常见问题

### Q1: 元素找不到怎么办？

```python
# 1. 检查定位器是否正确
locator = ByID("btn_login")

# 2. 添加等待
page.wait_element(locator, "visible", timeout=10)

# 3. 使用更稳健的定位方式
locator = ByXPath("//Button[@Name='登录']")
```

### Q2: 测试执行太慢？

```bash
# 使用并行测试
pytest tests/ -n auto

# 失败重试
pytest tests/ --reruns 2 --reruns-delay 2
```

### Q3: 如何调试测试？

```python
# 1. 添加日志
from wei.infra.logging import Logger
logger = Logger("MyTest")
logger.info("步骤 1: 打开应用")

# 2. 截图
page.take_screenshot("step1.png")

# 3. 使用断点
import pdb; pdb.set_trace()
```

---

## 📚 下一步学习

### 入门教程
- [安装指南](docs/guides/installation.md)
- [第一个测试](docs/guides/first-test.md)
- [页面对象模式](docs/guides/page-object.md)

### 进阶指南
- [组件高级用法](docs/guides/advanced-components.md)
- [数据驱动测试](docs/guides/data-driven.md)
- [关键字驱动测试](docs/guides/keyword-driven.md)

### API 参考
- [Core API](docs/api/core.md)
- [Engine API](docs/api/engine.md)
- [Infra API](docs/api/infra.md)

### 最佳实践
- [测试设计模式](docs/best-practices.md)
- [性能优化](docs/guides/performance.md)
- [CI/CD 集成](docs/ci-cd-guide.md)

---

## 🎯 品牌理念

> **见微知著，质控无痕**
> 
> 在软件的世界里，Bug 往往藏在最细微的地方。
> WeiTest 帮助你发现每一个细节问题，
> 让质量控制变得简单而优雅。

---

**需要帮助？**

- 📖 [完整文档](https://docs.wei-test.dev)
- 💬 [社区论坛](https://github.com/wei-test/wei-test/discussions)
- 🐛 [问题反馈](https://github.com/wei-test/wei-test/issues)
- 📧 [联系我们](mailto:support@wei-test.dev)

---

**开始你的自动化测试之旅吧！** 🚀
