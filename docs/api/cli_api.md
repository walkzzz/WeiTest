# CLI API - 命令行工具 API 参考

**版本**: 2.0.2

---

## wei

WeiTest 命令行工具

### 命令概览

```bash
wei <command> [options]
```

---

## wei init

初始化新测试项目

### 语法

```bash
wei init <project_name> [--template <basic|full>]
```

### 参数

- `project_name`: 项目名称

### 选项

- `--template`: 项目模板 (basic/full, 默认 basic)

### 示例

```bash
# 创建基础项目
wei init my_test_project

# 创建完整项目
wei init my_test_project --template full
```

### 创建的文件结构

```
my_test_project/
├── tests/          # 测试用例
├── pages/          # 页面对象
├── data/           # 测试数据
├── reports/        # 测试报告
├── logs/           # 日志文件
├── README.md
├── requirements.txt
└── pytest.ini
```

---

## wei create

创建测试资源

### 子命令

#### wei create page

创建页面对象

**语法**:
```bash
wei create page <page_name> [--yaml]
```

**参数**:
- `page_name`: 页面名称

**选项**:
- `--yaml`: 同时生成 YAML 定义文件

**示例**:
```bash
wei create page login
wei create page login --yaml
```

**生成文件**:
- pages/login_page.py
- pages/login_page.yaml (如果指定 --yaml)

---

#### wei create test

创建测试文件

**语法**:
```bash
wei create test <test_name>
```

**参数**:
- `test_name`: 测试名称

**示例**:
```bash
wei create test test_login
```

**生成文件**:
- tests/test_login.py

---

## wei run

运行测试

### 语法

```bash
wei run [path] [-v] [--parallel]
```

### 参数

- `path`: 测试路径 (默认：tests/)

### 选项

- `-v, --verbose`: 详细输出
- `--parallel`: 并行执行

### 示例

```bash
# 运行所有测试
wei run

# 运行指定目录
wei run tests/ui/

# 详细输出
wei run -v

# 并行执行
wei run --parallel
```

---

## wei report

生成测试报告

### 语法

```bash
wei report [--type <html|allure>] [--open]
```

### 选项

- `--type`: 报告类型 (html/allure, 默认 html)
- `--open`: 生成后打开报告

### 示例

```bash
# 生成 HTML 报告
wei report --type html

# 生成并打开 Allure 报告
wei report --type allure --open
```

---

## wei clean

清理缓存和临时文件

### 语法

```bash
wei clean
```

### 清理的内容

- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `reports/`
- `.mypy_cache/`
- `.ruff_cache/`

### 示例

```bash
wei clean
```

---

## wei --version

查看版本

### 语法

```bash
wei --version
```

---

## wei --help

查看帮助

### 语法

```bash
wei --help
wei <command> --help
```

### 示例

```bash
wei --help
wei init --help
```

---

**CLI API 完整参考**
