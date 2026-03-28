# CI/CD 配置指南

本指南介绍如何配置和使用 AutoTestMe-NG 的 CI/CD 管道。

---

## 📋 目录

1. [GitHub Actions 配置](#1-github-actions-配置)
2. [本地测试](#2-本地测试)
3. [代码质量检查](#3-代码质量检查)
4. [测试报告](#4-测试报告)
5. [发布流程](#5-发布流程)

---

## 1. GitHub Actions 配置

### 1.1 工作流文件

项目已包含完整的 GitHub Actions 配置：

```yaml
.github/workflows/ci.yml
```

### 1.2 触发条件

工作流在以下情况下触发：

- **Push**: 推送到 `main` 或 `develop` 分支
- **Pull Request**: 针对 `main` 分支的 PR
- **定时任务**: 工作日早上 8 点自动运行

### 1.3 测试矩阵

```yaml
strategy:
  matrix:
    os: [windows-latest]
    python-version: ['3.9', '3.10', '3.11']
```

支持多个 Python 版本并行测试。

---

## 2. 本地测试

### 2.1 运行所有测试

```bash
pytest tests/ -v --tb=short
```

### 2.2 并行测试

```bash
pytest tests/ -n auto -v
```

### 2.3 带覆盖率报告

```bash
pytest tests/ --cov=core --cov=engine --cov=infra --cov-report=html
```

### 2.4 失败重试

```bash
pytest tests/ --reruns 2 --reruns-delay 2
```

---

## 3. 代码质量检查

### 3.1 Lint 检查（Ruff）

```bash
ruff check . --statistics
```

### 3.2 类型检查（Mypy）

```bash
mypy core engine infra --ignore-missing-imports
```

### 3.3 格式化检查（Black）

```bash
black --check .
```

---

## 4. 测试报告

### 4.1 HTML 报告

```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

### 4.2 Allure 报告

```bash
# 生成报告数据
pytest tests/ --alluredir=reports/allure-results

# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

### 4.3 覆盖率报告

```bash
# HTML 格式
pytest tests/ --cov=core --cov=engine --cov=infra --cov-report=html

# XML 格式（用于 CI/CD）
pytest tests/ --cov=core --cov=engine --cov=infra --cov-report=xml

# 查看覆盖率摘要
pytest tests/ --cov=core --cov=engine --cov=infra --cov-report=term-missing
```

---

## 5. 发布流程

### 5.1 创建版本标签

```bash
# 创建版本标签
git tag -a v2.0.0 -m "AutoTestMe-NG v2.0.0"

# 推送标签
git push origin --tags
```

### 5.2 自动发布

推送标签后，GitHub Actions 会自动：

1. 构建 Python 包
2. 创建 GitHub Release
3. 发布到 PyPI

### 5.3 手动发布

```bash
# 构建包
python -m build

# 检查包
twine check dist/*

# 发布到 PyPI
twine upload dist/*
```

---

## 6. 环境变量配置

### 6.1 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

| Secret 名称 | 说明 |
|------------|------|
| `PYPI_API_TOKEN` | PyPI 发布令牌 |
| `CODECOV_TOKEN` | Codecov 上传令牌（可选） |

### 6.2 本地环境变量

```bash
# 设置测试环境变量
export ATM_TIMEOUT=60
export ATM_DEBUG=true
export ATM_ENVIRONMENT=test
```

---

## 7. 自定义 CI/CD

### 7.1 添加新的测试阶段

编辑 `.github/workflows/ci.yml`，在 `test` job 中添加新步骤：

```yaml
- name: Custom Test Stage
  run: |
    echo "Running custom tests"
    pytest tests/custom/ -v
```

### 7.2 添加新的触发条件

```yaml
on:
  push:
    tags:
      - 'v*'
```

### 7.3 添加部署步骤

```yaml
- name: Deploy to Server
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /path/to/project
      git pull
      pip install -r requirements.txt
      pytest tests/ -v
```

---

## 8. 故障排除

### 8.1 测试失败

查看测试日志：

```bash
# GitHub Actions
# 访问 Actions 标签页 → 选择失败的工作流 → 查看详细日志

# 本地
pytest tests/ -v --tb=long
```

### 8.2 覆盖率不足

```bash
# 查看未覆盖的代码行
pytest tests/ --cov=core --cov-report=term-missing
```

### 8.3 依赖安装失败

```bash
# 清除 pip 缓存
pip cache purge

# 重新安装
pip install -r requirements.txt --no-cache-dir
```

---

## 9. 最佳实践

### 9.1 测试标签使用

```python
@pytest.mark.smoke
def test_critical_function():
    """冒烟测试 - 核心功能"""
    pass

@pytest.mark.regression
def test_full_workflow():
    """回归测试 - 完整工作流"""
    pass

@pytest.mark.slow
def test_performance():
    """性能测试 - 运行时间较长"""
    pass
```

### 9.2 CI/CD 优化

- ✅ 使用缓存加速依赖安装
- ✅ 并行运行测试矩阵
- ✅ 失败测试自动重试
- ✅ 测试超时保护
- ✅ 自动上传测试报告和覆盖率

### 9.3 安全建议

- ✅ 不要在代码中硬编码密钥
- ✅ 使用 GitHub Secrets 管理敏感信息
- ✅ 定期更新依赖版本
- ✅ 审查第三方 Actions 权限

---

## 10. 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [pytest 文档](https://docs.pytest.org/)
- [Codecov 文档](https://docs.codecov.com/)
- [Allure 文档](https://docs.qameta.io/allure/)

---

**最后更新**: 2026-03-28  
**版本**: v2.0.0
