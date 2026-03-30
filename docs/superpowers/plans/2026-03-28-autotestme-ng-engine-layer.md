# WeiTest Engine Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** 实现 WeiTest 框架的引擎层（Engine Layer），包括 Page 模块（Mixin 架构）、Component 组件库和 Assertion 断言引擎。

**Architecture:** Engine 层构建在 Core 层之上，提供 PageObject 模式实现、可复用的 UI 组件和流畅的断言 API。采用 Mixin 组合模式，避免深继承链。

**Tech Stack:** Python 3.9+, pywinauto 0.6.8+, pytest 7.4.0+

**Spec Reference:** `docs/superpowers/specs/2026-03-28-WeiTest-design.md` Section 4

**Prerequisites:** Core Layer 已完成（ApplicationDriver, WindowDriver, Locator, SearchEngine, SmartWait）

---

## File Structure

### Engine Layer Files to Create

```
engine/
├── __init__.py
├── page/
│   ├── __init__.py
│   ├── mixins/
│   │   ├── __init__.py
│   │   ├── application_mixin.py      # 应用管理 Mixin
│   │   ├── element_mixin.py          # 元素定位 Mixin
│   │   ├── action_mixin.py           # 操作 Mixin
│   │   └── screenshot_mixin.py       # 截图 Mixin
│   ├── base_page.py                  # BasePage（组合所有 Mixin）
│   └── yaml_page.py                  # YAML 驱动的页面对象
├── component/
│   ├── __init__.py
│   ├── button.py                     # 按钮组件
│   ├── input.py                      # 输入框组件
│   ├── combobox.py                   # 下拉框组件
│   ├── checkbox.py                   # 复选框组件
│   └── label.py                      # 标签组件
└── assertion/
    ├── __init__.py
    ├── base_assert.py                # 断言基类
    ├── ui_assert.py                  # UI 断言
    └── assertion_chain.py            # 链式断言
```

### Test Files to Create

```
tests/test_engine/
├── __init__.py
├── test_page/
│   ├── __init__.py
│   ├── test_base_page.py
│   └── test_yaml_page.py
├── test_component/
│   ├── __init__.py
│   ├── test_button.py
│   ├── test_input.py
│   └── test_checkbox.py
└── test_assertion/
    ├── __init__.py
    ├── test_ui_assert.py
    └── test_assertion_chain.py
```

---

## Implementation Tasks

### Task 1: Page 模块 - Mixin 基类

**Files:**
- Create: `engine/page/mixins/application_mixin.py`
- Create: `engine/page/mixins/element_mixin.py`
- Create: `engine/page/mixins/action_mixin.py`
- Create: `engine/page/mixins/screenshot_mixin.py`
- Create: `engine/page/base_page.py`
- Test: `tests/test_engine/test_page/test_base_page.py`

**Steps:**
1. 创建 engine/__init__.py
2. 创建 engine/page/__init__.py
3. 创建 engine/page/mixins/__init__.py
4. 创建 ApplicationMixin（应用启动/连接/关闭）
5. 创建 ElementMixin（元素查找/等待）
6. 创建 ActionMixin（点击/输入/选择）
7. 创建 ScreenshotMixin（截图功能）
8. 创建 BasePage 组合所有 Mixin
9. 创建单元测试
10. Commit

---

### Task 2: Page 模块 - YAML Page

**Files:**
- Create: `engine/page/yaml_page.py`
- Create: `framework/pages/login_page.yaml` (示例)
- Test: `tests/test_engine/test_page/test_yaml_page.py`

**Steps:**
1. 实现 YamlPage 类
2. 支持 YAML Schema 验证
3. 支持 from_yaml() 工厂方法
4. 创建示例 YAML 页面定义
5. 创建单元测试
6. Commit

---

### Task 3: Component 模块 - 基础组件

**Files:**
- Create: `engine/component/__init__.py`
- Create: `engine/component/button.py`
- Create: `engine/component/input.py`
- Create: `engine/component/label.py`
- Test: `tests/test_engine/test_component/test_button.py`
- Test: `tests/test_engine/test_component/test_input.py`

**Steps:**
1. 实现 Button 组件（点击/等待/文本）
2. 实现 TextInput 组件（输入/清空/获取值）
3. 实现 Label 组件（获取文本）
4. 创建单元测试
5. Commit

---

### Task 4: Component 模块 - 高级组件

**Files:**
- Create: `engine/component/combobox.py`
- Create: `engine/component/checkbox.py`
- Test: `tests/test_engine/test_component/test_combobox.py`
- Test: `tests/test_engine/test_component/test_checkbox.py`

**Steps:**
1. 实现 ComboBox 组件（选择/获取选项）
2. 实现 CheckBox 组件（勾选/取消勾选）
3. 创建单元测试
4. Commit

---

### Task 5: Assertion 模块 - 基础断言

**Files:**
- Create: `engine/assertion/__init__.py`
- Create: `engine/assertion/base_assert.py`
- Create: `engine/assertion/ui_assert.py`
- Test: `tests/test_engine/test_assertion/test_ui_assert.py`

**Steps:**
1. 实现 AssertionResult 类
2. 实现 BaseAssertion 抽象基类
3. 实现 UIAssertion（存在/可见/可用/文本断言）
4. 创建 Assert 快捷入口
5. 创建单元测试
6. Commit

---

### Task 6: Assertion 模块 - 链式断言

**Files:**
- Create: `engine/assertion/assertion_chain.py`
- Test: `tests/test_engine/test_assertion/test_assertion_chain.py`

**Steps:**
1. 实现 AssertionChain 类
2. 支持链式调用（is_not_none/contains/is_equal_to）
3. 集成到 Assert 快捷入口
4. 创建单元测试
5. Commit

---

### Task 7: Engine 层集成测试

**Files:**
- Create: `tests/test_engine/test_integration.py`
- Create: `framework/pages/login_page.yaml` (完整示例)
- Create: `framework/tests/ui/test_login_example.py` (完整示例)

**Steps:**
1. 创建完整的登录页面 YAML 定义
2. 创建基于 YAML 的登录测试示例
3. 测试 Page + Component + Assertion 集成
4. 验证端到端流程
5. Commit

---

## Testing Strategy

- **TDD**: 每个组件先写测试，再写实现
- **覆盖率**: Engine 层代码覆盖率目标 85%+
- **Mock 策略**: 使用 unittest.mock 模拟 pywinauto 对象
- **集成测试**: 验证模块间协作

---

## Commit Strategy

- **原子提交**: 每个任务一个提交
- **约定式提交**: 使用 `feat(engine/xxx): description` 格式
- **频繁提交**: 每个小功能完成后立即提交

---

## Success Criteria

- ✅ 所有 7 个任务完成
- ✅ 40+ 个单元测试通过
- ✅ 集成测试验证端到端流程
- ✅ 代码通过 mypy 类型检查
- ✅ 代码通过 ruff lint 检查
- ✅ 示例代码可运行

---

**Plan complete. Ready for execution.**
