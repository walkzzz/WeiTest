# AutoTestMe-NG v2.0 安装指南

## 1. 基础安装

```bash
cd E:\Huaweiutotestme-ng-v2.0
pip install -r requirements.txt
```

## 2. 分步安装（推荐）

### 核心依赖
```bash
pip install pywinauto>=0.6.8
pip install pytest>=7.4.0
pip install pytest-html>=4.0.0
```

### 可选功能
```bash
# 图像识别
pip install opencv-python pyautogui pillow

# 图像相似度 (SSIM)
pip install scikit-image

# 配置加密
pip install cryptography

# 数据生成
pip install faker
```

### 测试工具
```bash
# 并行测试
pip install pytest-xdist

# 失败重试
pip install pytest-rerunfailures

# 超时控制
pip install pytest-timeout

# 覆盖率
pip install pytest-cov

# Allure 报告
pip install allure-pytest
```

## 3. 验证安装

```bash
# 验证核心模块
python -c "from core.finder.locator import Locator; print('OK')"
python -c "from engine.component import *; print('OK')"

# 验证图像识别（如果已安装 opencv）
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

# 验证 pytest
pytest --version
```

## 4. 常见问题

### Q: cv2 导入失败？
A: 安装 opencv-python
```bash
pip install opencv-python
```

### Q: allure 命令不可用？
A: 安装 allure 命令行工具
```bash
# Windows (需要 scoop 或 chocolatey)
scoop install allure
# 或
choco install allure

# 或下载二进制文件
# https://github.com/allure-framework/allure2/releases
```

### Q: 并行测试不工作？
A: 确保安装了 pytest-xdist
```bash
pip install pytest-xdist
```

## 5. 完整依赖列表

详见：requirements.txt

---

**位置**: E:\Huaweiutotestme-ng-v2.0  
**版本**: v2.0.0
