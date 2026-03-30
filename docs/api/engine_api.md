# Engine API - 引擎层 API 参考

**版本**: 2.0.2

---

## PageObject

页面对象基类

### 类方法

#### `from_yaml(yaml_path)`

从 YAML 文件加载页面

**参数**:
- `yaml_path`: YAML 文件路径

**返回**: YamlPage 实例

**示例**:
```python
page = YamlPage.from_yaml("pages/login_page.yaml")
```

---

### 方法

#### `element(name)`

获取元素定位器

**参数**:
- `name`: 元素名称

**返回**: Locator 实例

---

#### `has_element(name)`

检查元素是否存在

**参数**:
- `name`: 元素名称

**返回**: bool

---

#### `element_description(name)`

获取元素描述

**参数**:
- `name`: 元素名称

**返回**: str

---

## Assertions

断言系统

### Assert 类

#### `that(actual, description="")`

创建值断言链

**参数**:
- `actual`: 实际值
- `description`: 描述

**返回**: AssertionChain

**示例**:
```python
(Assert.that(title)
    .is_not_none()
    .contains("Login"))
```

---

#### `ui(page, locator)`

创建 UI 断言

**参数**:
- `page`: 页面对象
- `locator`: 元素定位器

**返回**: UIAssertion

**示例**:
```python
Assert.ui(page, locator).should_be_visible()
```

---

### AssertionChain 方法

#### `is_not_none()`

断言不为 None

---

#### `is_not_empty()`

断言不为空

---

#### `is_equal_to(expected)`

断言相等

---

#### `contains(expected)`

断言包含

---

#### `starts_with(prefix)`

断言字符串以 prefix 开头

---

#### `ends_with(suffix)`

断言字符串以 suffix 结尾

---

#### `length_greater_than(length)`

断言长度大于 length

---

#### `length_less_than(length)`

断言长度小于 length

---

#### `matches(pattern)`

断言匹配正则表达式

---

### UIAssertion 方法

#### `should_be_visible()`

断言元素可见

---

#### `should_be_enabled()`

断言元素可用

---

#### `should_exist()`

断言元素存在

---

#### `text_should_equal(text)`

断言文本等于指定值

---

#### `text_should_contain(text)`

断言文本包含指定内容

---

**Engine API 完整参考**
