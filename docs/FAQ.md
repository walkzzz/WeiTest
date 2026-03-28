# AutoTestMe-NG 常见问题解答 (FAQ)

**最后更新**: 2026-03-28  
**版本**: v1.0

---

## 📋 目录

1. [安装与配置](#1-安装与配置)
2. [测试编写](#2-测试编写)
3. [组件使用](#3-组件使用)
4. [错误处理](#4-错误处理)
5. [CI/CD 集成](#5-cicd-集成)
6. [性能优化](#6-性能优化)

---

## 1. 安装与配置

### Q1: 安装依赖时失败怎么办？

**A**: 按以下步骤排查：

```bash
# 1. 检查 Python 版本
python --version  # 需要 3.9+

# 2. 升级 pip
python -m pip install --upgrade pip

# 3. 清理缓存重装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

**常见问题**:
- ❌ Python 版本过低 → 升级到 3.9+
- ❌ 网络问题 → 使用国内镜像 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple`
- ❌ 权限问题 → 使用管理员权限或 `--user` 参数

---

### Q2: 健康检查失败怎么办？

**A**: 运行健康检查并查看详细错误：

```bash
python health_check.py
```

**常见错误及解决**:
- ❌ Core Layer 失败 → 检查 `pip install pywinauto`
- ❌ Engine Layer 失败 → 检查 YAML 包 `pip install pyyaml`
- ❌ Infra Layer 失败 → 检查 pytest `pip install pytest`

---

### Q3: 如何配置环境变量？

**A**: 编辑 `framework/data/env.yaml`：

```yaml
test:
  app_path: "C:\\YourApp\\app.exe"
  app_title: "您的应用标题"
  timeout: 30

dev:
  app_path: "C:\\YourApp\\app.exe"
  app_title: "您的应用标题 [开发]"
  timeout: 60
```

**注意**: Windows 路径使用双反斜杠 `\\`

---

## 2. 测试编写

### Q4: 如何创建第一个测试？

**A**: 按以下 3 步：

**步骤 1**: 创建页面 YAML (`framework/pages/my_page.yaml`)

```yaml
elements:
  my_button:
    locator_type: name
    locator_value: 我的按钮
    control_type: Button
```

**步骤 2**: 创建测试文件 (`tests/test_my_feature.py`)

```python
from engine.page.yaml_page import YamlPage
from engine.component import Button
from engine.assertion import Assert

def test_my_feature():
    page = YamlPage.from_yaml("framework/pages/my_page.yaml")
    page.start_app("notepad.exe")  # 或使用实际应用
    page.set_window(page.get_window("无标题 - 记事本"))
    
    btn = Button(page, page.element("my_button"))
    btn.click()
    
    Assert.ui(page, page.element("my_button")).should_be_visible()
    
    page.close()
```

**步骤 3**: 运行测试

```bash
pytest tests/test_my_feature.py -v
```

---

### Q5: 如何选择正确的定位方式？

**A**: 定位方式优先级：

1. **automation_id** (最稳定) - 适用于有 AutomationID 的控件
2. **id** (推荐) - 适用于大多数标准控件
3. **name** (常用) - 适用于有显示文本的控件
4. **class_name** - 适用于按类型定位
5. **xpath** (最后选择) - 适用于复杂层级

**示例**:
```yaml
# 最佳实践
btn_submit:
  locator_type: automation_id
  locator_value: SubmitBtn  # 唯一且稳定

# 备选方案
btn_submit:
  locator_type: name
  locator_value: 提交  # 文本可能变化
```

---

### Q6: 如何处理动态元素？

**A**: 使用智能等待：

```python
from engine.page.yaml_page import YamlPage
from core.waiter import SmartWait

page = YamlPage.from_yaml("pages/dynamic_page.yaml")

# 等待元素出现（最多 10 秒）
page.wait_element(page.element("dynamic_element"), timeout=10)

# 或使用自定义条件
from core.waiter.wait_condition import VisibleCondition
from core.waiter.smart_wait import SmartWait

waiter = SmartWait(timeout=10)
waiter.wait_for_condition(VisibleCondition(), element)
```

---

## 3. 组件使用

### Q7: Button 组件不响应点击怎么办？

**A**: 检查以下几点：

```python
btn = Button(page, page.element("my_button"))

# 1. 检查按钮是否可见
assert btn.is_visible, "按钮不可见"

# 2. 检查按钮是否可用
assert btn.is_enabled, "按钮不可用"

# 3. 等待按钮可点击
btn.wait_clickable(timeout=10).click()

# 4. 使用双击尝试
btn.double_click()
```

**常见原因**:
- 元素被遮挡 → 使用 `page.take_screenshot()` 查看
- 元素未加载 → 添加等待 `btn.wait_clickable()`
- 定位错误 → 使用 Inspect 工具验证

---

### Q8: TextInput 输入中文乱码怎么办？

**A**: 使用正确的输入方法：

```python
input_box = TextInput(page, page.element("txt_input"))

# 方法 1: 直接输入（推荐）
input_box.type("中文测试")

# 方法 2: 清空后输入
input_box.clear().type("中文测试")

# 方法 3: 设置值
input_box.set_value("中文测试")
```

**注意**: 确保应用支持中文输入

---

### Q9: 如何使用 Table 组件？

**A**: Table 组件使用示例：

```python
from engine.component import Table

table = Table(page, ByID("tbl_data"))

# 获取行数
row_count = table.get_row_count()

# 获取单元格数据
cell_value = table.get_cell(0, 0)  # 第 1 行第 1 列

# 获取整行
row_data = table.get_row(0)

# 获取所有数据
all_data = table.get_all_rows()

# 搜索行
row_index = table.find_row_by_text("搜索文本", column=0)
table.select_row(row_index)
```

---

## 4. 错误处理

### Q10: 测试失败如何调试？

**A**: 使用以下调试方法：

```python
from infra.logging import Logger

logger = Logger("MyTest")

def test_debug():
    try:
        # 测试代码
        page.click(locator)
    except Exception as e:
        # 记录错误
        logger.error(f"测试失败：{e}")
        
        # 截图
        page.take_screenshot("error_screenshot.png")
        
        # 重新抛出
        raise
```

**调试技巧**:
1. 添加详细日志 `logger.info("步骤描述")`
2. 截图验证 `page.take_screenshot()`
3. 使用 pytest 详细输出 `pytest -v -s`
4. 检查应用状态 `page.get_current_window()`

---

### Q11: 元素找不到怎么办？

**A**: 按以下步骤排查：

```python
# 1. 使用 Inspect 工具验证元素属性
# 下载 Windows Inspect 工具检查元素

# 2. 尝试多种定位方式
try:
    # 方式 1: ID
    element = page.find_element(ByID("my_id"))
except:
    try:
        # 方式 2: Name
        element = page.find_element(ByName("我的元素"))
    except:
        # 方式 3: XPath
        element = page.find_element(ByXPath("//Button"))

# 3. 等待元素出现
page.wait_element(locator, timeout=10)

# 4. 检查窗口是否正确
current_window = page.get_current_window()
logger.info(f"当前窗口：{current_window.title}")
```

---

### Q12: 测试超时怎么办？

**A**: 调整超时配置：

```python
# 方法 1: 单个元素超时
page.wait_element(locator, timeout=30)  # 30 秒

# 方法 2: 配置文件超时
# framework/data/env.yaml
test:
  timeout: 60  # 全局 60 秒

# 方法 3: pytest 超时
# pytest.ini
[pytest]
addopts = --timeout=300  # 300 秒
```

---

## 5. CI/CD 集成

### Q13: Jenkins 构建失败怎么办？

**A**: 检查以下配置：

**1. Windows Agent 配置**:
- 确保屏幕解锁
- 配置自动登录
- 检查 Python 路径

**2. Pipeline 配置**:
```groovy
// Jenkinsfile
environment {
    PYTHON_HOME = 'C:\\Python39'
    PATH = "${PYTHON_HOME};${env.PATH}"
}
```

**3. 查看构建日志**:
```bash
# Jenkins 控制台输出
# 搜索 "ERROR" 或 "FAILED"
```

---

### Q14: GitHub Actions 无法触发怎么办？

**A**: 检查以下配置：

**1. 工作流文件**:
```yaml
# .github/workflows/ci.yml
on:
  push:
    branches: [ main, master ]  # 检查分支名
```

**2. 权限设置**:
- Settings → Actions → General
- 允许所有 Actions

**3. 查看 Actions 日志**:
- 访问 https://github.com/用户名/仓库/actions
- 查看失败的工作流

---

## 6. 性能优化

### Q15: 测试执行太慢怎么办？

**A**: 使用以下优化方法：

**1. 并行执行**:
```bash
# 使用 pytest-xdist
pip install pytest-xdist
pytest -n 4  # 4 个进程并行
```

**2. 减少等待时间**:
```python
# 优化前
page.wait_element(locator, timeout=30)  # 总是等待 30 秒

# 优化后
page.wait_element(locator, timeout=5)   # 快速失败
```

**3. 复用应用实例**:
```python
@pytest.fixture(scope="class")
def app_page():
    page = YamlPage.from_yaml("pages/my_page.yaml")
    page.start_app("app.exe")
    page.set_window(page.get_window("应用"))
    yield page
    page.close()
```

---

### Q16: 内存占用过高怎么办？

**A**: 优化方法：

**1. 及时关闭应用**:
```python
def test_feature(page):
    try:
        # 测试代码
        pass
    finally:
        page.close()  # 确保关闭
```

**2. 减少截图**:
```python
# 仅在失败时截图
try:
    test_code()
except:
    page.take_screenshot("error.png")
    raise
```

**3. 定期清理**:
```python
import gc
gc.collect()  # 垃圾回收
```

---

## 📞 联系支持

**文档问题**: 查看 `docs/USER_GUIDE.md`  
**测试问题**: 运行 `python health_check.py`  
**CI/CD 问题**: 查看 `docs/CI_CD_SETUP_GUIDE.md`  

---

**最后更新**: 2026-03-28  
**文档版本**: v1.0  
**框架版本**: v1.0
