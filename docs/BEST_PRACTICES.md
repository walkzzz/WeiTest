# AutoTestMe-NG 最佳实践指南

**最后更新**: 2026-03-28  
**版本**: v1.0

---

## 📋 目录

1. [页面设计](#1-页面设计)
2. [测试编写](#2-测试编写)
3. [组件使用](#3-组件使用)
4. [数据管理](#4-数据管理)
5. [日志与报告](#5-日志与报告)
6. [CI/CD 实践](#6-cicd-实践)

---

## 1. 页面设计

### ✅ 推荐：使用 YAML 定义页面

```yaml
# framework/pages/login_page.yaml

elements:
  # 清晰的命名
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
    description: "用户名输入框"
    component: input  # 指定组件类型
  
  # 使用稳定定位
  login_button:
    locator_type: automation_id
    locator_value: LoginBtn
    control_type: Button
    description: "登录按钮"
    component: button
    wait_condition: clickable  # 自动等待可点击
```

### ❌ 不推荐：硬编码定位器

```python
# ❌ 坏代码
def test_login():
    locator = Locator(LocatorType.NAME, "登录")
    page.click(locator)

# ✅ 好代码
def test_login():
    page.click(page.element("login_button"))
```

---

### ✅ 推荐：页面分组

```yaml
# 按功能分组
elements:
  # 登录区域
  login_username:
  login_password:
  login_button:
  
  # 注册区域
  register_username:
  register_email:
  register_button:
```

---

## 2. 测试编写

### ✅ 推荐：测试结构

```python
"""用户管理功能测试"""

import pytest
from engine.page.yaml_page import YamlPage
from engine.component import Button, TextInput
from engine.assertion import Assert
from infra.logging import Logger


class TestUserManagement:
    """用户管理测试类"""
    
    @pytest.fixture(scope="class")
    def app_page(self):
        """应用页面夹具"""
        page = YamlPage.from_yaml("framework/pages/main_page.yaml")
        page.start_app("app.exe")
        page.set_window(page.get_window("主界面"))
        yield page
        page.close()
    
    def test_create_user(self, app_page):
        """测试创建用户"""
        # 准备数据
        username = "test_user"
        
        # 执行操作
        # ...
        
        # 验证结果
        Assert.ui(app_page, app_page.element("user_created")).should_be_visible()
```

**结构要点**:
- ✅ 使用测试类组织相关测试
- ✅ 使用夹具复用资源
- ✅ 清晰的测试方法命名
- ✅ AAA 模式 (Arrange-Act-Assert)

---

### ✅ 推荐：断言使用

```python
from engine.assertion import Assert

# ✅ 好的断言
Assert.ui(page, page.element("btn_submit")).should_be_visible()
Assert.ui(page, page.element("lbl_error")).text_should_contain("错误")

# ❌ 坏的断言
assert page.find_element(locator).is_visible()  # 错误信息不清晰
```

---

### ✅ 推荐：错误处理

```python
from infra.logging import Logger

logger = Logger("MyTest")

def test_with_error_handling(page):
    """带错误处理的测试"""
    try:
        logger.info("开始测试...")
        
        # 测试代码
        page.click(page.element("btn_action"))
        
        logger.info("操作成功")
        
    except Exception as e:
        logger.error(f"测试失败：{e}")
        page.take_screenshot("error.png")
        raise
```

---

## 3. 组件使用

### ✅ 推荐：组件链式调用

```python
from engine.component import Button, TextInput

# ✅ 链式调用
username = TextInput(page, page.element("username"))
username.clear().type("admin")

login_btn = Button(page, page.element("login_button"))
login_btn.wait_clickable().click()

# ❌ 冗长写法
username = TextInput(page, page.element("username"))
username.clear()
username.type("admin")

login_btn = Button(page, page.element("login_button"))
login_btn.wait_clickable(timeout=10)
login_btn.click()
```

---

### ✅ 推荐：Table 组件使用

```python
from engine.component import Table

table = Table(page, ByID("tbl_data"))

# ✅ 获取数据
all_rows = table.get_all_rows()
for row in all_rows:
    print(row)

# ✅ 搜索并选择
row_index = table.find_row_by_text("目标数据", column=0)
if row_index is not None:
    table.select_row(row_index)

# ❌ 直接操作底层元素
element = page.find_element(ByID("tbl_data"))
rows = element.children()
# ... 复杂的手动处理
```

---

## 4. 数据管理

### ✅ 推荐：测试数据分离

```yaml
# framework/data/test_data.yaml

login:
  valid_users:
    - username: "admin"
      password: "Admin123"
      role: "管理员"
    - username: "user"
      password: "User123"
      role: "普通用户"
  
  invalid_users:
    - username: ""
      password: "password"
      expected_error: "用户名不能为空"
```

```python
# 测试中使用
@pytest.mark.parametrize("user", [
    {"username": "admin", "password": "Admin123"},
    {"username": "user", "password": "User123"}
])
def test_login(page, user):
    TextInput(page, page.element("username")).type(user["username"])
    # ...
```

---

### ✅ 推荐：环境配置

```yaml
# framework/data/env.yaml

test:
  app_path: "C:\\Test\\app.exe"
  timeout: 30
  retry_count: 3

dev:
  app_path: "C:\\Dev\\app.exe"
  timeout: 60
  retry_count: 5

prod:
  app_path: "C:\\Prod\\app.exe"
  timeout: 90
  retry_count: 1
```

---

## 5. 日志与报告

### ✅ 推荐：日志使用

```python
from infra.logging import Logger

logger = Logger("MyTest")

def test_with_logging(page):
    """带日志的测试"""
    logger.info("=" * 50)
    logger.info("测试开始")
    logger.info("=" * 50)
    
    logger.info("步骤 1: 打开应用")
    page.start_app("app.exe")
    
    logger.info("步骤 2: 执行操作")
    page.click(page.element("btn_action"))
    
    logger.info("步骤 3: 验证结果")
    Assert.ui(page, page.element("result")).should_be_visible()
    
    logger.info("测试完成 ✓")
```

---

### ✅ 推荐：截图策略

```python
from infra.reporting import ReportManager

reporter = ReportManager()

def test_with_screenshots(page):
    """带截图的测试"""
    try:
        # 测试代码
        pass
    except Exception as e:
        # 失败时截图
        screenshot_path = page.take_screenshot(f"error_{timestamp}.png")
        reporter.save_screenshot(image_data, f"error_{timestamp}.png")
        raise
```

---

## 6. CI/CD 实践

### ✅ 推荐：Jenkins Pipeline

```groovy
// Jenkinsfile

pipeline {
    agent {
        label 'windows-ui-agent'
    }
    
    options {
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }
    
    stages {
        stage('Setup') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                bat 'pytest framework/tests/ui/ -v --alluredir=reports/allure-results'
            }
        }
        
        stage('Report') {
            steps {
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            emailext(
                subject: "❌ 测试失败：${env.JOB_NAME}",
                body: "请查看：${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
    }
}
```

---

### ✅ 推荐：测试分层

```
tests/
├── unit/                    # 单元测试（快速）
│   ├── test_components.py   # < 1 分钟
│   └── test_utils.py
│
├── integration/             # 集成测试（中等）
│   ├── test_api.py          # < 5 分钟
│   └── test_database.py
│
└── ui/                      # UI 测试（慢速）
    ├── test_login.py        # < 10 分钟
    └── test_workflow.py
```

**执行策略**:
```bash
# 冒烟测试（快速验证）
pytest -m smoke -v

# 完整回归
pytest -v

# 仅 UI 测试
pytest framework/tests/ui/ -v
```

---

## 📊 代码审查清单

### 页面设计
- [ ] 使用 YAML 定义元素
- [ ] 使用稳定的定位方式
- [ ] 添加元素描述
- [ ] 指定组件类型

### 测试编写
- [ ] 使用测试类组织
- [ ] 使用夹具复用资源
- [ ] AAA 模式清晰
- [ ] 断言信息明确

### 组件使用
- [ ] 使用组件库
- [ ] 链式调用
- [ ] 适当的等待

### 数据管理
- [ ] 测试数据分离
- [ ] 环境配置独立
- [ ] 敏感信息加密

### 日志报告
- [ ] 关键步骤记录日志
- [ ] 失败时截图
- [ ] 生成测试报告

---

## 🎯 性能优化建议

### 测试执行优化

```bash
# 1. 并行执行
pytest -n 4 -v

# 2. 只运行失败测试
pytest --lf -v

# 3. 使用标记
pytest -m smoke -v
```

### 资源管理优化

```python
# 1. 使用类级别夹具
@pytest.fixture(scope="class")
def app_page():
    page = YamlPage.from_yaml("pages/main.yaml")
    page.start_app("app.exe")
    yield page
    page.close()

# 2. 及时释放资源
def test_feature(page):
    try:
        # 测试代码
        pass
    finally:
        page.close()  # 确保关闭
```

---

## 📞 参考资源

- [用户指南](USER_GUIDE.md)
- [FAQ](FAQ.md)
- [CI/CD 指南](CI_CD_SETUP_GUIDE.md)

---

**最后更新**: 2026-03-28  
**文档版本**: v1.0  
**框架版本**: v1.0
