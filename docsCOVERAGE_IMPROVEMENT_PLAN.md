# WeiTest 测试覆盖率提升计划

**当前覆盖率**: 40%  
**目标覆盖率**: 80%+  
**日期**: 2026-03-30

---

## 📊 当前覆盖率分析

### 按模块统计

| 模块 | 覆盖率 | 状态 | 需要提升 |
|------|--------|------|---------|
| **Core Layer** | 65% | ⚠️ 中等 | +15% |
| **Engine Layer** | 35% | ❌ 低 | +45% |
| **Infra Layer** | 55% | ⚠️ 中等 | +25% |

### 覆盖率低的模块 (<50%)

#### Engine Layer (需重点改进)
- advanced_assertions.py: 0% (137 行)
- ui_assert.py: 31% (59 行)
- base_assert.py: 48% (31 行)
- data_grid.py: 24% (119 行)
- list_box.py: 22% (117 行)
- tree_view.py: 15% (146 行)
- menu.py: 26% (62 行)
- progress_bar.py: 27% (52 行)
- radio_button.py: 27% (113 行)
- tab_control.py: 33% (66 行)
- table.py: 24% (63 行)

#### Core Layer
- plugin/base.py: 51% (187 行)
- plugin/registry.py: 47% (59 行)
- waiter/custom_conditions.py: 46% (63 行)

#### Infra Layer
- reporting/reporter.py: 23% (106 行)
- reporting/screenshot_on_failure.py: 25% (71 行)

---

## 🎯 提升策略

### 短期 (1-2 周) - 达到 60%

1. **补充组件测试** (+15%)
   - Button, TextInput 已有 100%
   - 补充 CheckBox, ComboBox, Label 测试
   - 目标：所有基础组件 80%+

2. **补充断言测试** (+10%)
   - 高级断言方法测试
   - UI 断言完整测试
   - 目标：断言模块 90%+

3. **补充配置测试** (+5%)
   - ConfigEncryption 完整测试
   - ConfigValidator 完整测试
   - 目标：配置模块 90%+

### 中期 (2-4 周) - 达到 75%

4. **复杂组件测试** (+10%)
   - DataGrid, ListBox, TreeView
   - Menu, TabControl, ProgressBar
   - 目标：复杂组件 70%+

5. **插件系统测试** (+5%)
   - Plugin 基类测试
   - PluginManager 完整测试
   - 目标：插件系统 80%+

### 长期 (1-2 月) - 达到 80%+

6. **高级功能测试** (+5%)
   - 图像识别模块
   - YAML 生成器/加载器
   - 报告系统完整测试

---

## 📝 优先级排序

### P0 - 立即实施 (提升 15%)

1. ✅ 基础组件测试 (CheckBox, ComboBox, Label)
2. ✅ 断言方法完整测试
3. ✅ 配置加密和验证测试

### P1 - 本周实施 (提升 20%)

4. 复杂组件核心功能测试
5. 插件系统基本测试
6. 等待条件完整测试

### P2 - 本月实施 (提升 15%)

7. 图像识别模块测试
8. YAML 模块测试
9. 报告系统完整测试
10. Page Mixin 完整测试

---

## 📈 预期进展

```
当前：40%
  ↓ P0 (+15%)
55%
  ↓ P1 (+20%)
75%
  ↓ P2 (+15%)
90% ✨
```

---

## 🔧 实施建议

### 1. 使用 pytest-cov

```bash
# 运行测试并查看覆盖率
pytest tests/ --cov=core --cov=engine --cov=infra --cov-report=term-missing

# 生成 HTML 报告
pytest tests/ --cov-report=html

# 查看未覆盖的代码行
pytest tests/ --cov-report=term-missing
```

### 2. 针对低覆盖率模块编写测试

```python
# 示例：测试 ComboBox
def test_combobox_select():
    from engine.component import ComboBox
    
    mock_page = Mock()
    combo = ComboBox(mock_page, locator)
    
    # 测试所有公共方法
    combo.select("option")
    combo.select_by_index(0)
    assert combo.selected_value is not None
```

### 3. 设置覆盖率阈值

```ini
# pytest.ini
[tool.coverage.run]
branch = true

[tool.coverage.report]
fail_under = 80
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
```

---

## 📊 成功标准

| 标准 | 目标 | 当前 | 状态 |
|------|------|------|------|
| 整体覆盖率 | 80%+ | 40% | ❌ |
| Core Layer | 80%+ | 65% | ⚠️ |
| Engine Layer | 80%+ | 35% | ❌ |
| Infra Layer | 80%+ | 55% | ⚠️ |
| 低覆盖率模块 | <10 个 | 20+ 个 | ❌ |

---

**提升计划**: 2-4 周达到 80%+  
**负责人**: AI Agent  
**状态**: 进行中

