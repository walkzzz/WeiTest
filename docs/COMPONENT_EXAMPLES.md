# 组件使用示例大全

本文档提供 AutoTestMe-NG 所有 UI 组件的完整使用示例。

---

## 📋 目录

1. [基础组件](#1-基础组件)
2. [选择类组件](#2-选择类组件)
3. [容器类组件](#3-容器类组件)
4. [高级组件](#4-高级组件)

---

## 1. 基础组件

### 1.1 Button - 按钮

```python
from engine.component import Button
from core.finder.locator import ByID

# 创建按钮组件
btn = Button(page, ByID("btn_login"))

# 基本操作
btn.click()                    # 单击
btn.double_click()             # 双击
btn.right_click()              # 右键

# 状态检查
btn.is_enabled()               # 是否可用
btn.is_visible()               # 是否可见
btn.get_text()                 # 获取文本

# 等待操作
btn.wait_clickable(timeout=10)    # 等待可点击
btn.wait_visible(timeout=5)       # 等待可见

# 链式调用
btn.wait_clickable().click()
```

### 1.2 TextInput - 输入框

```python
from engine.component import TextInput

# 创建输入框组件
input_box = TextInput(page, ByID("txt_username"))

# 基本操作
input_box.type("admin")             # 输入文本
input_box.clear()                   # 清空
input_box.set_value("password123")  # 设置值

# 获取值
value = input_box.value             # 获取当前值
text = input_box.get_text()         # 获取显示文本

# 状态检查
input_box.is_enabled()
input_box.is_visible()
input_box.is_editable()

# 特殊操作
input_box.send_keys("{TAB}")        # 发送特殊键
input_box.select_all()              # 全选
input_box.copy()                    # 复制
input_box.paste("text")             # 粘贴
```

### 1.3 CheckBox - 复选框

```python
from engine.component import CheckBox

# 创建复选框组件
chk = CheckBox(page, ByID("chk_remember"))

# 基本操作
chk.check()                         # 勾选
chk.uncheck()                       # 取消勾选
chk.toggle()                        # 切换状态

# 状态检查
is_checked = chk.is_checked()       # 是否已勾选
is_enabled = chk.is_enabled()       # 是否可用

# 等待操作
chk.wait_checked(timeout=5)         # 等待勾选
chk.wait_unchecked(timeout=5)       # 等待未勾选

# 使用示例
if not chk.is_checked():
    chk.check()
```

### 1.4 Label - 标签

```python
from engine.component import Label

# 创建标签组件
label = Label(page, ByID("lbl_title"))

# 获取文本
text = label.text                   # 标签文本
raw_text = label.get_text()         # 原始文本

# 状态检查
label.is_visible()
label.is_enabled()

# 验证文本
from engine.assertion import Assert
Assert.that(label.text).contains("欢迎")
```

---

## 2. 选择类组件

### 2.1 ComboBox - 下拉框

```python
from engine.component import ComboBox

# 创建下拉框组件
combo = ComboBox(page, ByID("combo_city"))

# 选择选项
combo.select("北京")                # 按文本选择
combo.select_by_index(0)            # 按索引选择
combo.select_by_value("beijing")    # 按值选择

# 获取选项
options = combo.options             # 所有选项
selected = combo.selected_value     # 已选值
selected_index = combo.selected_index  # 已选索引

# 状态检查
combo.is_enabled()
combo.is_expanded()                 # 是否展开

# 等待操作
combo.wait_for_option("上海", timeout=5)

# 遍历选项
for option in combo.options:
    print(f"选项：{option}")
```

### 2.2 RadioButton - 单选按钮

```python
from engine.component import RadioButton

# 创建单选按钮组件
radio = RadioButton(page, ByID("radio_male"))

# 选择
radio.select()                      # 选中

# 状态检查
is_selected = radio.is_selected()   # 是否已选中
group = radio.get_group()           # 获取组名

# 获取组内所有选项
group_options = radio.get_group_options()
for option in group_options:
    print(f"组选项：{option}")

# 使用示例
# 选择性别
male = RadioButton(page, ByID("radio_male"))
female = RadioButton(page, ByID("radio_female"))

male.select()  # 选择男性
```

### 2.3 ListBox - 列表框

```python
from engine.component import ListBox

# 创建列表框组件
listbox = ListBox(page, ByID("list_items"))

# 选择
listbox.select("项目 1")            # 按文本选择
listbox.select_by_index(0)          # 按索引选择

# 多选
listbox.select_multiple(["项目 1", "项目 2"])

# 获取选项
items = listbox.items               # 所有项
selected = listbox.selected_items   # 已选项
count = listbox.count()             # 项目数量

# 检查
exists = listbox.item_exists("项目 3")
is_selected = listbox.is_selected("项目 1")

# 遍历
for item in listbox.items:
    print(f"列表项：{item}")
```

### 2.4 TabControl - 选项卡

```python
from engine.component import TabControl

# 创建选项卡组件
tab = TabControl(page, ByID("tab_main"))

# 选择选项卡
tab.select_tab(0)                   # 按索引选择
tab.select_tab("设置")              # 按名称选择

# 获取信息
selected = tab.get_selected_tab()   # 已选选项卡
selected_index = tab.get_selected_index()
tab_count = tab.get_tab_count()     # 选项卡数量

# 检查
exists = tab.tab_exists("高级")
all_tabs = tab.get_all_tabs()       # 所有选项卡名称

# 等待
tab.wait_for_tab("帮助", timeout=5)

# 使用示例
# 切换到设置选项卡
if tab.tab_exists("设置"):
    tab.select_tab("设置")
```

---

## 3. 容器类组件

### 3.1 TreeView - 树形视图

```python
from engine.component import TreeView

# 创建树形视图组件
tree = TreeView(page, ByID("tree_files"))

# 展开/折叠
tree.expand_node("文档")            # 展开节点
tree.collapse_node("文档")          # 折叠节点
tree.expand_all()                   # 展开所有

# 选择
tree.select_node("文档/报告.docx")  # 按路径选择

# 获取信息
selected = tree.get_selected_node()
children = tree.get_children("文档")
all_nodes = tree.get_all_nodes()

# 检查
exists = tree.node_exists("文档/报告.docx")
is_expanded = tree.is_node_expanded("文档")

# 遍历节点
for node in tree.get_all_nodes():
    print(f"节点：{node}")
```

### 3.2 Menu - 菜单

```python
from engine.component import Menu

# 创建菜单组件
menu = Menu(page, ByName("应用程序菜单"))

# 选择菜单项
menu.select_menu_item("文件", "新建")  # 选择子菜单
menu.select_menu_item("编辑", "复制", "全部")  # 三级菜单

# 获取菜单项
items = menu.get_menu_items()
file_items = menu.get_menu_items("文件")

# 检查
exists = menu.menu_item_exists("帮助", "关于")
is_enabled = menu.is_menu_item_enabled("文件", "保存")

# 使用示例
# 文件 → 保存
menu.select_menu_item("文件", "保存")

# 编辑 → 复制 → 全部
menu.select_menu_item("编辑", "复制", "全部")
```

### 3.3 DataGrid - 数据表格

```python
from engine.component import DataGrid

# 创建数据表格组件
grid = DataGrid(page, ByID("grid_users"))

# 选择行
grid.select_row(0)                  # 选择第一行
grid.select_row_by_text("张三")     # 按文本选择

# 获取数据
row = grid.get_row(0)               # 获取行数据
cell = grid.get_cell(0, "姓名")     # 获取单元格
all_data = grid.get_all_rows()      # 所有行数据

# 行数
row_count = grid.row_count()

# 排序
grid.sort_by_column("姓名")         # 按列排序
grid.sort_by_column("年龄", ascending=False)

# 过滤
grid.filter("部门", "技术部")       # 过滤数据

# 搜索
row_index = grid.search_column("姓名", "张三")

# 使用示例
# 获取所有用户
for row in grid.get_all_rows():
    print(f"用户：{row['姓名']}, 部门：{row['部门']}")

# 查找并选择特定用户
index = grid.search_column("姓名", "李四")
if index >= 0:
    grid.select_row(index)
```

### 3.4 Table - 表格

```python
from engine.component import Table

# 创建表格组件
table = Table(page, ByID("table_data"))

# 获取数据
cell = table.get_cell(0, 0)         # 获取单元格 (行，列)
row = table.get_row(0)              # 获取整行
column = table.get_column(0)        # 获取整列

# 行列数
rows = table.row_count()
cols = table.column_count()

# 表头
headers = table.get_headers()

# 使用示例
for i in range(table.row_count()):
    for j in range(table.column_count()):
        print(table.get_cell(i, j))
```

---

## 4. 高级组件

### 3.1 ProgressBar - 进度条

```python
from engine.component import ProgressBar

# 创建进度条组件
progress = ProgressBar(page, ByID("progress_download"))

# 获取进度
value = progress.get_progress()     # 当前进度 (0-100)
min_val = progress.get_min()        # 最小值
max_val = progress.get_max()        # 最大值

# 状态
is_complete = progress.is_complete()  # 是否完成
state = progress.get_state()          # 状态 (正常/错误/暂停)

# 等待
progress.wait_for_completion(timeout=60)

# 使用示例
# 等待下载完成
progress.wait_for_completion(timeout=120)

if progress.is_complete():
    print("下载完成!")
```

### 4.2 组件组合使用示例

#### 示例 1: 登录流程

```python
from engine.component import Button, TextInput, CheckBox
from engine.assertion import Assert

# 页面对象
class LoginPage:
    def __init__(self, page):
        self.username = TextInput(page, ByID("txt_username"))
        self.password = TextInput(page, ByID("txt_password"))
        self.remember = CheckBox(page, ByID("chk_remember"))
        self.login_btn = Button(page, ByID("btn_login"))
    
    def login(self, user: str, pwd: str, remember: bool = False):
        """执行登录"""
        self.username.clear()
        self.username.type(user)
        
        self.password.clear()
        self.password.type(pwd)
        
        if remember:
            self.remember.check()
        else:
            self.remember.uncheck()
        
        self.login_btn.click()
        
        # 验证
        Assert.ui(self.login_btn).should_be_visible()

# 使用
login_page = LoginPage(page)
login_page.login("admin", "password123", remember=True)
```

#### 示例 2: 数据录入流程

```python
from engine.component import (
    TextInput, ComboBox, DatePicker,
    Button, DataGrid, Label
)

class DataEntryPage:
    def __init__(self, page):
        self.name_input = TextInput(page, ByID("txt_name"))
        self.department = ComboBox(page, ByID("combo_dept"))
        self.position = TextInput(page, ByID("txt_position"))
        self.save_btn = Button(page, ByID("btn_save"))
        self.message = Label(page, ByID("lbl_message"))
        self.grid = DataGrid(page, ByID("grid_employees"))
    
    def add_employee(self, name: str, dept: str, position: str):
        """添加员工"""
        # 填写表单
        self.name_input.type(name)
        self.department.select(dept)
        self.position.type(position)
        
        # 保存
        self.save_btn.click()
        
        # 验证成功消息
        Assert.ui(self.message).text_should_contain("成功")
        
        # 验证数据已添加
        assert self.grid.row_count() > 0

# 使用
entry_page = DataEntryPage(page)
entry_page.add_employee("张三", "技术部", "工程师")
```

#### 示例 3: 文件管理流程

```python
from engine.component import TreeView, Menu, Button

class FileManagerPage:
    def __init__(self, page):
        self.tree = TreeView(page, ByID("tree_files"))
        self.menu = Menu(page, ByName("菜单"))
        self.new_btn = Button(page, ByID("btn_new"))
    
    def create_file(self, folder: str, filename: str):
        """创建文件"""
        # 展开文件夹
        self.tree.expand_node(folder)
        
        # 选择文件夹
        self.tree.select_node(folder)
        
        # 菜单操作：文件 → 新建
        self.menu.select_menu_item("文件", "新建")
        
        # 或点击新建按钮
        self.new_btn.click()
        
        # 输入文件名
        # ... (使用 Input 组件)

# 使用
file_page = FileManagerPage(page)
file_page.create_file("文档", "新文档.txt")
```

---

## 5. 断言示例

### 5.1 基础断言

```python
from engine.assertion import Assert

# 基本断言
Assert.that(value).is_not_none()
Assert.that(text).contains("expected")
Assert.that(number).equals(100)

# 链式断言
(Assert.that(title, "窗口标题")
    .is_not_none()
    .contains("Login")
    .length_greater_than(5))
```

### 5.2 UI 断言

```python
from engine.assertion import Assert

# 元素存在性
Assert.ui(page, ByID("btn_login")).should_exist()
Assert.ui(page, ByID("btn_login")).should_not_exist()

# 可见性
Assert.ui(page, ByID("btn_login")).should_be_visible()

# 可用性
Assert.ui(page, ByID("btn_login")).should_be_enabled()

# 文本断言
Assert.ui(page, ByID("lbl_title")).text_should_equal("欢迎")
Assert.ui(page, ByID("lbl_title")).text_should_contain("欢迎")
```

---

## 6. 最佳实践

### 6.1 组件封装

```python
# 推荐：将常用操作封装为方法
class LoginPage:
    def __init__(self, page):
        self.username = TextInput(page, ByID("txt_username"))
        self.password = TextInput(page, ByID("txt_password"))
        self.login_btn = Button(page, ByID("btn_login"))
    
    def login(self, user: str, pwd: str):
        """封装登录流程"""
        self.username.type(user)
        self.password.type(pwd)
        self.login_btn.click()

# 使用
login_page.login("admin", "123456")
```

### 6.2 等待策略

```python
# 推荐：操作前等待元素就绪
btn = Button(page, ByID("btn_submit"))
btn.wait_clickable(timeout=10)  # 等待可点击
btn.click()

# 推荐：使用显式等待
from core.waiter import WaitCondition
page.wait_element(locator, "visible", timeout=5)
```

### 6.3 错误处理

```python
from core.exceptions import ElementNotFoundError

try:
    btn = Button(page, ByID("btn_not_exist"))
    btn.click()
except ElementNotFoundError:
    print("元素未找到，记录截图")
    page.take_screenshot("error.png")
```

---

**最后更新**: 2026-03-28  
**版本**: v2.0.0
