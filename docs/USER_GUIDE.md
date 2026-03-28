# AutoTestMe-NG 使用指南

## 目录

1. [快速开始](#快速开始)
2. [PageObject 模式](#pageobject-模式)
3. [使用组件](#使用组件)
4. [使用断言](#使用断言)
5. [配置管理](#配置管理)
6. [日志系统](#日志系统)
7. [报告系统](#报告系统)
8. [最佳实践](#最佳实践)

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 验证安装

```bash
python -c "from core.driver import ApplicationDriver; print('✅ 安装成功')"
```

### 3. 创建第一个测试

**步骤 1**: 创建页面 YAML (`framework/pages/notepad_page.yaml`)

```yaml
elements:
  edit_area:
    locator_type: class_name
    locator_value: Edit
    control_type: Edit
    description: "编辑区域"
  
  file_menu:
    locator_type: name
    locator_value: 文件
    control_type: MenuItem
    description: "文件菜单"
```

**步骤 2**: 创建测试文件 (`tests/test_notepad.py`)

```python
from engine.page.yaml_page import YamlPage
from engine.assertion import Assert

def test_notepad():
    page = YamlPage.from_yaml("framework/pages/notepad_page.yaml")
    page.start_app("notepad.exe")
    page.set_window(page.get_window("无标题 - 记事本"))
    
    # 验证编辑区域存在
    Assert.ui(page, page.element("edit_area")).should_be_visible()
    
    page.close()
```

**步骤 3**: 运行测试

```bash
pytest tests/test_notepad.py -v
```

---

## PageObject 模式

### YAML 页面定义

```yaml
# framework/pages/login_page.yaml

elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
    component: input
  
  password_input:
    locator_type: id
    locator_value: txt_password
    control_type: Edit
    component: input
  
  login_button:
    locator_type: name
    locator_value: 登录
    control_type: Button
    component: button
  
  remember_checkbox:
    locator_type: id
    locator_value: chk_remember
    control_type: CheckBox
    component: checkbox
```

### 使用 YAML 页面

```python
from engine.page.yaml_page import YamlPage

# 加载页面
page = YamlPage.from_yaml("framework/pages/login_page.yaml")

# 启动应用
page.start_app("login.exe")
page.set_window(page.get_window("登录"))

# 获取元素定位器
locator = page.element("username_input")

# 检查元素是否存在
if page.has_element("login_button"):
    print("登录按钮已定义")
```

---

## 使用组件

### Button 按钮

```python
from engine.component import Button

btn = Button(page, ByID("btn_login"))

# 点击
btn.click()

# 双击
btn.double_click()

# 等待可点击
btn.wait_clickable(timeout=10).click()

# 获取属性
print(btn.text)           # 按钮文本
print(btn.is_enabled)     # 是否可用
print(btn.is_visible)     # 是否可见
print(btn.is_clickable)   # 是否可点击
```

### TextInput 输入框

```python
from engine.component import TextInput

input_box = TextInput(page, ByID("txt_username"))

# 输入文本
input_box.type("admin")

# 清空后输入
input_box.clear().type("new_value")

# 设置值（清空 + 输入）
input_box.set_value("admin")

# 获取值
print(input_box.value)

# 检查属性
print(input_box.is_editable)
print(input_box.placeholder)
```

### CheckBox 复选框

```python
from engine.component import CheckBox

chk = CheckBox(page, ByID("chk_remember"))

# 勾选
chk.check()

# 取消勾选
chk.uncheck()

# 切换状态
chk.toggle()

# 获取状态
print(chk.is_checked)
print(chk.label)
```

### ComboBox 下拉框

```python
from engine.component import ComboBox

combo = ComboBox(page, ByID("cmb_country"))

# 选择选项
combo.select("China")
combo.select_by_index(0)

# 获取选择
print(combo.selected_value)
print(combo.selected_index)

# 获取所有选项
print(combo.options)

# 检查状态
print(combo.is_expanded)
```

---

## 使用断言

### UI 断言

```python
from engine.assertion import Assert

# 存在性断言
Assert.ui(page, ByID("btn")).should_exist()
Assert.ui(page, ByID("btn")).should_not_exist()

# 可见性断言
Assert.ui(page, ByID("btn")).should_be_visible()

# 可用性断言
Assert.ui(page, ByID("btn")).should_be_enabled()
Assert.ui(page, ByID("btn")).should_be_disabled()

# 文本断言
Assert.ui(page, ByID("lbl")).text_should_equal("欢迎")
Assert.ui(page, ByID("lbl")).text_should_contain("欢迎")
Assert.ui(page, ByID("lbl")).text_should_not_be_empty()

# 链式调用
(Assert.ui(page, ByID("btn"))
    .should_be_visible()
    .and_()
    .should_be_enabled())
```

### 链式断言

```python
from engine.assertion import Assert

# 基本断言链
(Assert.that(value)
    .is_not_none()
    .is_not_empty()
    .contains("text"))

# 相等断言
(Assert.that(title)
    .is_equal_to("登录"))

# 布尔断言
(Assert.that(flag)
    .is_true())
```

---

## 配置管理

### 环境配置

```yaml
# framework/data/env.yaml

test:
  app_path: "C:\\App\\login.exe"
  app_title: "登录"
  timeout: 30

dev:
  app_path: "C:\\Dev\\login.exe"
  app_title: "登录 [开发]"
  timeout: 60
```

### 使用配置

```python
from infra.config import ConfigManager

# 创建配置管理器
config = ConfigManager("framework/data")

# 获取环境配置
env = config.get_env_config("test")
print(env["app_path"])

# 获取特定配置
timeout = config.get_env_config("test", key="timeout")
print(timeout)

# 加载所有配置
all_configs = config.load_all()
```

---

## 日志系统

### 基本使用

```python
from infra.logging import Logger

# 创建日志器
logger = Logger("MyTest")

# 记录日志
logger.debug("调试信息")
logger.info("测试开始")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

### 全局日志器

```python
from infra.logging import get_logger, log_info, log_error

# 获取全局日志器
logger = get_logger("AutoTestMe")

# 便捷函数
log_info("测试开始")
log_error("发生错误")
```

### 日志配置

```python
logger = Logger(
    name="MyTest",
    log_dir="logs",          # 日志目录
    level=logging.DEBUG,     # 日志级别
    log_file="test.log"      # 日志文件名
)
```

---

## 报告系统

### 报告管理

```python
from infra.reporting import ReportManager

reporter = ReportManager()

# 创建 Allure 报告
reporter.create_allure_report()

# 打开 Allure 报告
reporter.open_allure_report()

# 打开 HTML 报告
reporter.open_html_report()

# 保存截图
reporter.save_screenshot(image_data, "screenshot.png")

# 查看统计
reporter.print_stats()
```

### pytest 配置

```ini
# pytest.ini

[pytest]
addopts = 
    -v
    --alluredir=reports/allure-results
    --html=reports/pytest-report.html
```

---

## 最佳实践

### 1. 使用 YAML 定义页面

```yaml
# ✅ 推荐：YAML 定义
elements:
  login_button:
    locator_type: name
    locator_value: 登录
```

```python
# ❌ 不推荐：硬编码定位器
locator = Locator(LocatorType.NAME, "登录")
```

### 2. 使用组件库

```python
# ✅ 推荐：使用组件
btn = Button(page, page.element("login_button"))
btn.click()

# ❌ 不推荐：直接操作
page.find_element(page.element("login_button")).click_input()
```

### 3. 使用断言

```python
# ✅ 推荐：使用断言
Assert.ui(page, ByID("btn")).should_be_visible()

# ❌ 不推荐：直接判断
assert page.find_element(ByID("btn")).is_visible()
```

### 4. 使用配置管理

```python
# ✅ 推荐：从配置获取
config = ConfigManager("framework/data")
app_path = config.get_env_config("test")["app_path"]

# ❌ 不推荐：硬编码
app_path = "C:\\App\\login.exe"
```

### 5. 使用日志

```python
# ✅ 推荐：记录关键步骤
logger.info("开始登录测试")
logger.error("登录失败")

# ❌ 不推荐：print 调试
print("开始登录")
```

### 6. 页面对象模式

```python
# ✅ 推荐：封装页面对象
class LoginPage(YamlPage):
    def login(self, username, password):
        TextInput(self, self.element("username")).type(username)
        TextInput(self, self.element("password")).type(password)
        Button(self, self.element("login_button")).click()

# ❌ 不推荐：测试逻辑混杂
def test_login():
    page.type(...)
    page.click(...)
```

---

## 完整示例

```python
"""登录功能测试"""

import pytest
from engine.page.yaml_page import YamlPage
from engine.component import Button, TextInput, CheckBox
from engine.assertion import Assert
from infra.logging import Logger
from infra.config import ConfigManager


class TestLogin:
    """登录测试类"""
    
    @pytest.fixture
    def login_page(self):
        """测试夹具"""
        config = ConfigManager("framework/data")
        env = config.get_env_config("test")
        
        page = YamlPage.from_yaml("framework/pages/login_page.yaml")
        page.start_app(env["app_path"])
        page.set_window(page.get_window(env["app_title"]))
        
        logger = Logger("LoginTest")
        logger.info("登录页面已打开")
        
        yield page
        
        page.close()
        logger.info("测试完成")
    
    def test_login_success(self, login_page):
        """测试正常登录"""
        # 准备数据
        username = TextInput(login_page, login_page.element("username_input"))
        password = TextInput(login_page, login_page.element("password_input"))
        login_btn = Button(login_page, login_page.element("login_button"))
        remember = CheckBox(login_page, login_page.element("remember_checkbox"))
        
        # 执行登录
        username.type("admin")
        password.type("password123")
        remember.check()
        login_btn.click()
        
        # 验证结果
        Assert.ui(login_page, login_page.element("login_button")).should_be_visible()
```

---

**更多示例请查看**: `framework/tests/ui/test_login_example.py`
