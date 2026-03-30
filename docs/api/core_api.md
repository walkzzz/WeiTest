# Core API - 核心层 API 参考

**版本**: 2.0.2

---

## ApplicationDriver

应用生命周期管理

### 方法

#### `__init__(backend=BackendType.UIA)`

初始化应用驱动

**参数**:
- `backend`: 后端类型 (UIA/WIN32)

**返回**: ApplicationDriver 实例

**示例**:
```python
driver = ApplicationDriver()
driver = ApplicationDriver(backend=BackendType.WIN32)
```

---

#### `start(app_path)`

启动应用程序

**参数**:
- `app_path`: 应用程序路径

**返回**: self (链式调用)

**异常**: ApplicationStartError

**示例**:
```python
driver.start("notepad.exe")
driver.start(r"C:\Windows\notepad.exe")
```

---

#### `connect(title=None, process_id=None)`

连接已运行的应用

**参数**:
- `title`: 窗口标题
- `process_id`: 进程 ID

**返回**: self

**异常**: ApplicationConnectError

**示例**:
```python
driver.connect(title="无标题 - 记事本")
driver.connect(process_id=1234)
```

---

#### `get_window(locator)`

获取窗口

**参数**:
- `locator`: 窗口定位器

**返回**: WindowDriver 实例

**示例**:
```python
window = driver.get_window(ByName("无标题 - 记事本"))
```

---

#### `close()`

关闭应用

**返回**: None

**示例**:
```python
driver.close()
```

---

#### `is_running` (属性)

应用是否正在运行

**类型**: bool

---

#### `process_id` (属性)

进程 ID

**类型**: int | None

---

## WindowDriver

窗口操作

### 方法

#### `maximize()`

最大化窗口

**返回**: self

---

#### `minimize()`

最小化窗口

**返回**: self

---

#### `restore()`

恢复窗口

**返回**: self

---

#### `close()`

关闭窗口

**返回**: self

---

#### `set_focus()`

设置焦点

**返回**: self

---

## Locator

元素定位器

### 类方法

#### `by_id(value, control_type=None, timeout=10)`

通过 AutomationID 定位

**参数**:
- `value`: AutomationID
- `control_type`: 控件类型 (可选)
- `timeout`: 超时时间 (秒)

**返回**: Locator 实例

---

#### `by_name(value, control_type=None, timeout=10)`

通过 Name 定位

**参数**:
- `value`: Name
- `control_type`: 控件类型
- `timeout`: 超时时间

**返回**: Locator 实例

---

#### `by_class_name(value, control_type=None, timeout=10)`

通过类名定位

---

#### `by_xpath(value, timeout=10)`

通过 XPath 定位

---

### 实例方法

#### `to_dict()`

转换为字典

**返回**: dict

**示例**:
```python
locator_dict = locator.to_dict()
# {'type': 'name', 'value': 'btn_login', ...}
```

---

#### `from_yaml(data)`

从 YAML 数据创建

**参数**:
- `data`: YAML 数据字典

**返回**: Locator 实例

---

## SearchEngine

元素搜索引擎

### 方法

#### `find(locator)`

查找元素

**参数**:
- `locator`: 定位器

**返回**: 元素对象

**异常**: ElementNotFoundError

---

#### `exists(locator, timeout=0)`

检查元素是否存在

**参数**:
- `locator`: 定位器
- `timeout`: 超时时间 (0=立即返回)

**返回**: bool

---

#### `find_all(locator)`

查找所有匹配元素

**参数**:
- `locator`: 定位器

**返回**: 元素列表

---

## SmartWait

智能等待

### 方法

#### `wait_until(condition, timeout=10, interval=0.5)`

等待直到条件满足

**参数**:
- `condition`: 等待条件
- `timeout`: 超时时间
- `interval`: 轮询间隔

**返回**: self

**异常**: TimeoutError

---

#### `wait_visible(locator, timeout=10)`

等待元素可见

---

#### `wait_clickable(locator, timeout=10)`

等待元素可点击

---

#### `wait_exists(locator, timeout=10)`

等待元素存在

---

**Core API 完整参考**
