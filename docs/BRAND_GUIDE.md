# WeiTest - 微测试 品牌指南

**版本**: 2.0.1  
**创建日期**: 2026-03-30  
**状态**: 正式发布

---

## 🎯 品牌定位

### 品牌名称

```
中文名：微测试
英文名：WeiTest
简称：Wei
包名：wei-test
```

### 品牌口号

```
主口号：见微知著，质控无痕
副口号：于细微处见真章
英文口号：Small Details, Big Quality
```

### 品牌理念

```
微 = 
  • 细微 - 关注每一个细节
  • 微妙 - 洞察微妙的变化
  • 微光 - 照亮隐藏的 Bug
  • 微笑 - 让测试变得简单

我们相信：
- 最好的测试框架应该像显微镜一样，放大每一个细节
- 像探照灯一样，照亮每一个隐藏的问题
- 像守护者一样，保卫每一行代码的质量
```

---

## 🎨 视觉识别系统 (VIS)

### Logo 设计

#### 主 Logo
```
方案 A: 文字 Logo
┌──────────────────────┐
│   微 Test            │
│   WEITEST            │
└──────────────────────┘

方案 B: 图形 + 文字
┌──────────────────────┐
│   🔍 微              │
│   Wei Test           │
└──────────────────────┘

方案 C: 字母 Logo
┌──────────────────────┐
│      W               │
│   微测试             │
└──────────────────────┘
```

#### Logo 使用规范
- 最小尺寸：32px (高度)
- 安全边距：Logo 高度的 1/4
- 背景：白色或浅色优先

### 配色方案

```
主色调:
  • 微蓝：#1E3A8A (深蓝)
  • 微光：#06B6D4 (青色)
  
辅助色:
  • 点缀橙：#F97316
  • 成功绿：#10B981
  • 警告黄：#F59E0B
  • 错误红：#EF4444

中性色:
  • 纯白：#FFFFFF
  • 浅灰：#F3F4F6
  • 中灰：#6B7280
  • 深灰：#1F2937
  • 纯黑：#000000
```

### 字体规范

```
中文字体:
  • 首选：思源黑体
  • 备选：苹方、微软雅黑

英文字体:
  • 首选：Inter
  • 备选：SF Pro、Roboto

代码字体:
  • Fira Code
  • JetBrains Mono
```

---

## 📦 产品命名

### 包和模块

```python
# 安装包
pip install wei-test

# 导入模块
import wei
from wei import core, engine, infra

# 或使用子模块
from wei.core import ApplicationDriver
from wei.engine import Page, Component
from wei.infra import ConfigManager
```

### CLI 命令

```bash
# 主命令
wei <command> [options]

# 常用命令
wei init myproject          # 初始化项目
wei create page login       # 创建页面
wei create test test_login  # 创建测试
wei run tests/              # 运行测试
wei report                  # 生成报告
wei clean                   # 清理缓存
wei --version               # 查看版本
wei --help                  # 帮助信息
```

### 目录结构

```
myproject/
├── tests/                  # 测试用例
│   ├── test_login.py
│   └── test_example.py
├── pages/                  # 页面对象
│   ├── login_page.py
│   └── login_page.yaml
├── data/                   # 测试数据
├── reports/                # 测试报告
├── logs/                   # 日志文件
├── README.md
├── requirements.txt
└── pytest.ini
```

---

## 📝 文档规范

### 文档结构

```
docs/
├── getting-started.md      # 快速开始
├── tutorial/               # 教程
│   ├── installation.md
│   ├── first-test.md
│   └── advanced-usage.md
├── guides/                 # 指南
│   ├── page-object.md
│   ├── components.md
│   ├── assertions.md
│   └── best-practices.md
├── api/                    # API 参考
│   ├── core.md
│   ├── engine.md
│   └── infra.md
├── examples/               # 示例
│   ├── login-example.md
│   └── data-driven.md
└── faq.md                  # 常见问题
```

### 代码示例规范

```python
# 好的示例 - 清晰、完整
from wei import Page
from wei.component import Button

class LoginPage(Page):
    def __init__(self):
        self.login_btn = Button(self, "btn_login")
    
    def login(self):
        self.login_btn.click()

# 使用示例
def test_login():
    page = LoginPage()
    page.login()
```

### 注释规范

```python
# 单行注释 - 简洁明了
btn.click()  # 点击登录按钮

# 多行注释 - 使用 docstring
def login(username, password):
    """
    执行登录操作
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        bool: 登录是否成功
    """
    pass
```

---

## 🗣️ 语调风格

### 文档语调

```
✓ 专业但不生硬
✓ 友好但不随意
✓ 清晰简洁
✓ 示例丰富
✓ 中文优先，英文友好

避免:
✗ 过于技术化的行话
✗ 冗长复杂的句子
✗ 模糊不清的描述
```

### 错误提示

```
好的错误提示:
"元素未找到：btn_login
请检查:
1. 元素 ID 是否正确
2. 页面是否已加载
3. 是否需要等待"

不好的错误提示:
"Error: Element not found"
```

### 社区交流

```
✓ 热情回答新手问题
✓ 鼓励分享最佳实践
✓ 建设性反馈
✓ 承认并快速修复问题
```

---

## 🌐 在线存在

### 官方网站

```
主站：wei-test.dev
文档：docs.wei-test.dev
博客：blog.wei-test.dev
Demo: demo.wei-test.dev
```

### 社交媒体

```
微信公众号：微测试框架
知乎：微测试框架
B 站：微测试框架
GitHub: github.com/wei-test
Twitter: @WeiTestFramework
```

### PyPI 页面

```
包名：wei-test
主页：https://wei-test.dev
文档：https://docs.wei-test.dev
源码：https://github.com/wei-test/wei-test
```

---

## 🎯 品牌传播

### 核心价值主张

```
1. 见微知著 - 关注细节，发现大问题
2. 简单易用 - 让测试变得简单
3. 强大灵活 - 满足各种测试需求
4. 开源开放 - 社区共建共享
```

### 目标受众

```
主要用户:
  • QA 工程师
  • 测试开发人员
  • 自动化测试工程师

次要用户:
  • 软件工程师
  • DevOps 工程师
  • 技术经理
```

### 差异化优势

```
vs 传统测试工具:
  • 更智能的等待机制
  • 更优雅的 API 设计
  • 更完善的文档

vs 竞品:
  • 中国文化底蕴
  • 更懂中国开发者
  • 更好的本地化支持
```

---

## 📊 品牌指标

### 成功指标

```
短期 (6 个月):
  • GitHub Stars: 1000+
  • PyPI 下载：10,000+/月
  • 社区用户：500+

中期 (1 年):
  • GitHub Stars: 5000+
  • PyPI 下载：50,000+/月
  • 企业用户：50+

长期 (2 年):
  • GitHub Stars: 10,000+
  • PyPI 下载：100,000+/月
  • 生态系统：100+ 插件
```

---

## 🔄 品牌演进

### 版本历史

```
v2.0.1 (2026-03-30):
  - 从 WeiTest 迁移到 WeiTest
  - 全新品牌形象
  - 完整文档体系
```

### 未来规划

```
v2.1:
  - Web 应用测试支持
  - AI 辅助测试

v3.0:
  - 云测试平台
  - 分布式测试
```

---

## 📞 联系方式

### 团队联系

```
商务：contact@wei-test.dev
技术：support@wei-test.dev
合作：partnership@wei-test.dev
```

### 社区支持

```
QQ 群：123456789
微信群：扫码加入
GitHub Issues: github.com/wei-test/wei-test/issues
```

---

**最后更新**: 2026-03-30  
**维护者**: WeiTest Team  
**许可**: CC BY 4.0
