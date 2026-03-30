# WeiTest 文档索引

**框架版本**: v1.0  
**最后更新**: 2026-03-28

---

## 📚 文档分类

### 🚀 快速开始

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [README.md](../README.md) | 项目介绍和快速开始 | 所有用户 ⭐ |
| [USER_GUIDE.md](USER_GUIDE.md) | 详细使用指南 | 测试开发者 |
| [FAQ.md](FAQ.md) | 常见问题解答 | 所有用户 |

### 📖 开发指南

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | 最佳实践指南 | 测试开发者 ⭐ |
| [REMAINING_TASKS.md](REMAINING_TASKS.md) | 剩余任务和扩展方向 | 框架开发者 |

### 🔧 运维指南

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [CI_CD_SETUP_GUIDE.md](CI_CD_SETUP_GUIDE.md) | CI/CD 配置指南 | DevOps 工程师 ⭐ |
| [FINAL_SUMMARY.md](FINAL_SUMMARY.md) | 项目完成总结 | 项目经理 |

### 📊 测试报告

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [reports/TEST_REPORT.md](../reports/TEST_REPORT.md) | 初始测试报告 | QA 工程师 |
| [reports/TEST_OPTIMIZATION_REPORT.md](../reports/TEST_OPTIMIZATION_REPORT.md) | 测试优化报告 | QA 工程师 |
| [reports/CONFIG_MANAGER_OPTIMIZATION.md](../reports/CONFIG_MANAGER_OPTIMIZATION.md) | ConfigManager 优化报告 | 框架开发者 |

### 🏗️ 技术文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [superpowers/specs/2026-03-28-weitest-design.md](superpowers/specs/2026-03-28-weitest-design.md) | 框架设计文档 | 架构师 |
| [superpowers/plans/](superpowers/plans/) | 实施计划 | 开发者 |

---

## 🎯 按角色查找文档

### 新手用户
1. 📖 [README.md](../README.md) - 快速开始
2. 📖 [USER_GUIDE.md](USER_GUIDE.md) - 使用指南
3. 📖 [FAQ.md](FAQ.md) - 常见问题

### 测试开发者
1. 📖 [USER_GUIDE.md](USER_GUIDE.md) - 详细使用
2. 📖 [BEST_PRACTICES.md](BEST_PRACTICES.md) - 最佳实践
3. 📖 [FAQ.md](FAQ.md) - 问题解决

### DevOps 工程师
1. 📖 [CI_CD_SETUP_GUIDE.md](CI_CD_SETUP_GUIDE.md) - CI/CD 配置
2. 📖 [FINAL_SUMMARY.md](FINAL_SUMMARY.md) - 项目总结

### 框架开发者
1. 📖 [superpowers/specs/](superpowers/specs/) - 设计文档
2. 📖 [superpowers/plans/](superpowers/plans/) - 实施计划
3. 📖 [REMAINING_TASKS.md](REMAINING_TASKS.md) - 扩展方向
4. 📖 [reports/](../reports/) - 测试报告

---

## 📈 文档统计

| 类别 | 文档数 | 总行数 |
|------|-------|-------|
| **快速开始** | 3 | ~800 行 |
| **开发指南** | 2 | ~1,100 行 |
| **运维指南** | 2 | ~900 行 |
| **测试报告** | 3 | ~500 行 |
| **技术文档** | 4 | ~1,500 行 |
| **总计** | **14** | **~4,800 行** |

---

## 🔍 快速查找

### 安装问题
→ [FAQ.md - 安装与配置](FAQ.md#1-安装与配置)

### 编写测试
→ [USER_GUIDE.md - 快速开始](USER_GUIDE.md#快速开始)  
→ [BEST_PRACTICES.md - 测试编写](BEST_PRACTICES.md#2-测试编写)

### 组件使用
→ [USER_GUIDE.md - 使用组件](USER_GUIDE.md#使用组件)  
→ [BEST_PRACTICES.md - 组件使用](BEST_PRACTICES.md#3-组件使用)

### CI/CD 配置
→ [CI_CD_SETUP_GUIDE.md](CI_CD_SETUP_GUIDE.md)  
→ [FAQ.md - CI/CD 集成](FAQ.md#5-cicd-集成)

### 错误处理
→ [FAQ.md - 错误处理](FAQ.md#4-错误处理)  
→ [BEST_PRACTICES.md - 错误处理](BEST_PRACTICES.md#测试编写)

---

## 📞 支持资源

### 健康检查
```bash
python health_check.py
```

### 运行测试
```bash
# 所有测试
pytest -v

# 特定测试
pytest tests/test_engine/ -v

# 生成报告
pytest --alluredir=reports/allure-results -v
allure generate reports/allure-results -o reports/allure-report --clean
```

### 查看文档
```bash
# Windows
start docs\README.md

# Linux/Mac
open docs/README.md
```

---

## 📅 文档更新记录

| 日期 | 文档 | 更新内容 |
|------|------|---------|
| 2026-03-28 | FAQ.md | 新增 |
| 2026-03-28 | BEST_PRACTICES.md | 新增 |
| 2026-03-28 | CONFIG_MANAGER_OPTIMIZATION.md | 新增 |
| 2026-03-28 | TEST_OPTIMIZATION_REPORT.md | 更新 |
| 2026-03-28 | 所有文档 | 框架完成 |

---

## 🎯 文档完整度

| 文档类型 | 完整度 | 状态 |
|---------|-------|------|
| 快速开始 | 100% | ✅ 完成 |
| 开发指南 | 100% | ✅ 完成 |
| 运维指南 | 100% | ✅ 完成 |
| 测试报告 | 100% | ✅ 完成 |
| 技术文档 | 100% | ✅ 完成 |
| **总体** | **100%** | ✅ **完成** |

---

**文档维护**: AI Agent  
**最后审查**: 2026-03-28  
**状态**: ✅ 完整
