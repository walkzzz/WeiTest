# Components API - UI 组件库 API 参考

**版本**: 2.0.2

---

## Button - 按钮

### 方法

#### `click()`

单击按钮

**返回**: self

---

#### `double_click()`

双击按钮

**返回**: self

---

#### `right_click()`

右键点击

**返回**: self

---

#### `is_enabled()`

检查是否可用

**返回**: bool

---

#### `is_visible()`

检查是否可见

**返回**: bool

---

#### `get_text()`

获取按钮文本

**返回**: str

---

#### `wait_clickable(timeout=10)`

等待可点击状态

**返回**: self

---

## TextInput - 输入框

### 方法

#### `type(text)`

输入文本

**参数**:
- `text`: 要输入的文本

**返回**: self

---

#### `clear()`

清空输入框

**返回**: self

---

#### `set_value(value)`

设置值

**参数**:
- `value`: 值

**返回**: self

---

#### `value` (属性)

获取当前值

**类型**: str

---

#### `is_editable()`

检查是否可编辑

**返回**: bool

---

#### `send_keys(keys)`

发送特殊键

**参数**:
- `keys`: 特殊键 (如 {TAB}, {ENTER})

**返回**: self

---

## CheckBox - 复选框

### 方法

#### `check()`

勾选复选框

**返回**: self

---

#### `uncheck()`

取消勾选

**返回**: self

---

#### `toggle()`

切换状态

**返回**: self

---

#### `is_checked()`

检查是否已勾选

**返回**: bool

---

#### `wait_checked(timeout=5)`

等待勾选状态

**返回**: self

---

## ComboBox - 下拉框

### 方法

#### `select(text)`

按文本选择选项

**参数**:
- `text`: 选项文本

**返回**: self

---

#### `select_by_index(index)`

按索引选择

**参数**:
- `index`: 选项索引

**返回**: self

---

#### `select_by_value(value)`

按值选择

**参数**:
- `value`: 选项值

**返回**: self

---

#### `options` (属性)

获取所有选项

**类型**: list

---

#### `selected_value` (属性)

获取已选值

**类型**: str

---

## 其他组件

### Label

- `text` - 获取标签文本
- `is_visible()` - 检查可见性

### ListBox

- `select(item)` - 选择项
- `items` - 获取所有项
- `selected_items` - 获取已选项

### TabControl

- `select_tab(index_or_name)` - 选择选项卡
- `get_selected_tab()` - 获取已选选项卡
- `tab_exists(name)` - 检查选项卡是否存在

### TreeView

- `expand_node(path)` - 展开节点
- `select_node(path)` - 选择节点
- `node_exists(path)` - 检查节点是否存在

### Menu

- `select_menu_item(*path)` - 选择菜单项
- `get_menu_items(path)` - 获取菜单项

### DataGrid

- `select_row(index)` - 选择行
- `get_cell(row, column)` - 获取单元格
- `get_all_rows()` - 获取所有行
- `row_count()` - 行数

### ProgressBar

- `get_progress()` - 获取进度 (0-100)
- `is_complete()` - 检查是否完成
- `wait_for_completion(timeout=60)` - 等待完成

---

**Components API 完整参考**
