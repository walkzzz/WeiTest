# WeiTest v2.0 安装指南

**版本**: 2.0.1  
**更新日期**: 2026-03-30

---

## 🚀 快速安装

### 方法一：一键安装（推荐）

```bash
cd E:\Huawei\WeiTest
pip install -r requirements.txt
```

### 方法二：从 PyPI 安装

```bash
pip install wei-test
```

---

## 📦 分步安装

### 1. 核心依赖

```bash
# UI 自动化核心
pip install pywinauto>=0.6.8

# 测试框架
pip install pytest>=7.4.0
pip install pytest-html>=4.0.0

# YAML 支持
pip install pyyaml>=6.0.1
```

### 2. 可选功能

#### 图像识别
```bash
# 基础图像识别
pip install opencv-python>=4.7.0
pip install pyautogui>=0.9.53
pip install pillow>=10.0.0

# 图像相似度 (SSIM)
pip install scikit-image>=0.21.0
```

#### 高级功能
```bash
# 配置加密
pip install cryptography>=41.0.0

# 数据生成
pip install faker>=18.0.0

# 类型检查
pip install mypy>=1.0.0
```

### 3. 测试增强工具

```bash
# 并行测试执行
pip install pytest-xdist>=3.0.0

# 失败自动重试
pip install pytest-rerunfailures>=12.0.0

# 测试超时控制
pip install pytest-timeout>=2.2.0

# 覆盖率报告
pip install pytest-cov>=4.1.0

# Allure 报告
pip install allure-pytest>=2.13.0

# 代码质量工具
pip install ruff>=0.1.0
pip install black>=23.0.0
```

---

## ✅ 验证安装

### 检查 WeiTest 版本

```bash
# 使用 CLI 工具
wei --version

# 或使用 Python
python -c "import wei; print(wei.__version__)"
```

### 运行测试验证

```bash
# 运行示例测试
cd E:\Huawei\WeiTest
pytest tests/ -v --tb=short
```

### 检查依赖

```bash
# 检查所有依赖
pip list | findstr /i "wei pytest pywinauto pyyaml"

# 或使用 pip check
pip check
```

---

## 🔧 故障排除

### 问题 1: opencv-python 安装失败

**解决方案**：
```bash
# 方法 1: 使用预编译 wheel
pip install opencv-python --only-binary :all:

# 方法 2: 使用国内镜像
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: pywinauto 无法导入

**解决方案**：
```bash
# 重新安装 pywinauto
pip uninstall pywinauto
pip install pywinauto --force-reinstall
```

### 问题 3: wei 命令找不到

**解决方案**：
```bash
# 确保已安装包
pip install wei-test

# 检查 PATH 环境变量
# 或直接用 python 运行
python -m wei.cli --help
```

---

## 💻 环境要求

### 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10/11 |
| Python 版本 | 3.9, 3.10, 3.11 |
| 内存 | 最少 4GB |
| 磁盘空间 | 最少 500MB |

### 可选：被测试应用

- 任何 Windows 桌面应用
- Win32 应用
- WPF 应用
- WinForms 应用

---

## 📚 下一步

安装完成后：

1. 📖 阅读 [快速开始](QUICKSTART.md)
2. 📚 查看 [用户指南](docs/USER_GUIDE.md)
3. 💻 运行示例测试
4. 🎯 创建你的第一个测试

---

## 🆘 获取帮助

- 📖 [完整文档](docs/README_DOCS.md)
- 🐛 [问题反馈](https://github.com/wei-test/wei-test/issues)
- 💬 [社区讨论](https://github.com/wei-test/wei-test/discussions)
- 📧 邮件：support@wei-test.dev

---

**安装愉快！** 🎉

**WeiTest - 见微知著，质控无痕**
