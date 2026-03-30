# WeiTest 快速开始

**版本**: 2.0.1  
**位置**: E:\Huawei\WeiTest

---

## 🚀 5 分钟开始测试

### 1. 验证安装

```bash
cd E:\Huawei\WeiTest
wei --version
```

### 2. 运行示例测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_engine/test_component/test_button.py -v
```

### 3. 创建你的第一个测试

```bash
# 使用 CLI 创建项目
wei init my_test_project

# 进入项目
cd my_test_project
```

### 4. 定义页面

创建 `pages/login_page.yaml`:

```yaml
elements:
  username_input:
    locator_type: id
    locator_value: txt_username
    control_type: Edit
  
  login_button:
    locator_type: id
    locator_value: btn_login
    control_type: Button
```

### 5. 编写测试

创建 `tests/test_login.py`:

```python
from wei.engine.page.yaml_page import YamlPage
from wei.engine.component import TextInput, Button
from wei.engine.assertion import Assert

def test_login():
    page = YamlPage.from_yaml("pages/login_page.yaml")
    username = TextInput(page, page.element("username_input"))
    login_btn = Button(page, page.element("login_button"))
    
    username.type("admin")
    login_btn.click()
    
    Assert.ui(page, page.element("login_button")).should_be_visible()
```

### 6. 运行测试

```bash
pytest tests/test_login.py -v
```

---

## 📚 完整文档导航

| 文档 | 说明 |
|------|------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 详细快速开始指南 |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | 完整用户指南 |
| [docs/COMPONENT_EXAMPLES.md](docs/COMPONENT_EXAMPLES.md) | 组件使用示例 |
| [docs/FAQ.md](docs/FAQ.md) | 常见问题解答 |
| [docs/README_DOCS.md](docs/README_DOCS.md) | 文档索引 |

---

## 🎯 CLI 命令速查

```bash
# 项目管理
wei init myproject          # 初始化项目
wei create page login       # 创建页面
wei create test test_login  # 创建测试

# 执行测试
wei run tests/              # 运行测试
wei run tests/ -v           # 详细输出
wei run tests/ --parallel   # 并行执行

# 报告和维护
wei report --html           # 生成 HTML 报告
wei clean                   # 清理缓存
```

---

## 🔗 相关链接

- **项目位置**: `E:\Huawei\WeiTest`
- **文档**: `E:\Huawei\WeiTest\docs\`
- **GitHub**: https://github.com/wei-test/wei-test
- **PyPI**: https://pypi.org/project/wei-test

---

**开始测试吧！** 🚀

**WeiTest - 见微知著，质控无痕**
