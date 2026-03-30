# Infra API - 基础设施层 API 参考

**版本**: 2.0.2

---

## ConfigManager

配置管理器

### 方法

#### `__init__(config_dir)`

初始化配置管理器

**参数**:
- `config_dir`: 配置目录

---

#### `load_config(config_name)`

加载配置文件

**参数**:
- `config_name`: 配置文件名 (不含扩展名)

**返回**: dict

**示例**:
```python
config = ConfigManager("framework/data")
config.load_config("env")
```

---

#### `get_config(config_name)`

获取已加载的配置

**参数**:
- `config_name`: 配置名

**返回**: dict

---

#### `get_env_config(env_name)`

获取环境配置

**参数**:
- `env_name`: 环境名 (test/dev/prod)

**返回**: dict

**示例**:
```python
env_config = config.get_env_config("test")
app_path = env_config["app_path"]
```

---

## EnhancedConfigManager

增强配置管理器

### 方法

#### `load_with_env(filename)`

加载配置并应用环境变量

**参数**:
- `filename`: 配置文件名

**返回**: dict

**环境变量格式**: ATM_<KEY>=<VALUE>

---

#### `load_with_secrets(filename, key_path)`

加载配置并解密

**参数**:
- `filename`: 配置文件名
- `key_path`: 密钥文件路径

**返回**: dict

---

#### `validate(schema)`

验证配置

**参数**:
- `schema`: 验证模式

**返回**: list (错误列表)

---

## Logger

日志记录器

### 方法

#### `__init__(name, log_dir="logs")`

初始化日志器

**参数**:
- `name`: 日志器名称
- `log_dir`: 日志目录

---

#### `info(message)`

记录信息日志

**参数**:
- `message`: 日志消息

---

#### `warning(message)`

记录警告日志

---

#### `error(message)`

记录错误日志

---

#### `debug(message)`

记录调试日志

---

#### `critical(message)`

记录严重错误日志

---

### 便捷函数

#### `get_logger(name, log_dir)`

获取日志器实例

**参数**:
- `name`: 日志器名称
- `log_dir`: 日志目录

**返回**: Logger 实例

---

## ReportManager

报告管理器

### 方法

#### `create_allure_report()`

创建 Allure 报告

**返回**: None

---

#### `open_html_report()`

打开 HTML 报告

---

#### `generate_html_report(output_path)`

生成 HTML 报告

**参数**:
- `output_path`: 输出路径

---

## ScreenshotManager

截图管理器

### 方法

#### `__init__(output_dir="reports/screenshots")`

初始化截图管理器

**参数**:
- `output_dir`: 截图输出目录

---

#### `take_screenshot(page, filename=None)`

拍摄截图

**参数**:
- `page`: 页面对象
- `filename`: 文件名 (可选)

**返回**: str (文件路径)

---

#### `take_screenshot_on_failure(page, test_name)`

失败时截图

**参数**:
- `page`: 页面对象
- `test_name`: 测试名称

**返回**: str

---

#### `cleanup_old_screenshots(days=7)`

清理旧截图

**参数**:
- `days`: 保留天数

---

#### `output_dir` (属性)

输出目录

**类型**: Path

---

**Infra API 完整参考**
