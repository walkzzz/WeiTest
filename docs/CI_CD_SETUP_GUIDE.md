# WeiTest CI/CD 配置指南

本文档详细说明如何配置 Jenkins 和 GitHub Actions 用于 WeiTest 自动化测试。

---

## 目录

1. [Jenkins 配置](#1-jenkins-配置)
2. [GitHub Actions 配置](#2-github-actions-配置)
3. [部署脚本使用](#3-部署脚本使用)
4. [故障排除](#4-故障排除)

---

## 1. Jenkins 配置

### 1.1 前置要求

- Jenkins 服务器（Windows 环境）
- Python 3.9+ 已安装
- Git 已安装
- Allure 已安装（可选，用于报告生成）

### 1.2 Jenkins 插件安装

登录 Jenkins，安装以下插件：

1. **Pipeline** - Pipeline 支持
2. **Allure Jenkins Plugin** - Allure 报告集成
3. **GitHub Integration Plugin** - GitHub 集成
4. **Email Extension Plugin** - 邮件通知
5. **Build Timeout Plugin** - 构建超时控制

**安装方法**：
```
系统管理 → 管理插件 → 可选插件 → 搜索并安装上述插件
```

### 1.3 创建 Jenkins 任务

#### 步骤 1: 创建新任务

```
1. 点击 "新建任务" (New Item)
2. 输入任务名称：WeiTest
3. 选择 "Pipeline" 类型
4. 点击 "确定"
```

#### 步骤 2: 配置源码管理

```
1. 选择 "Git"
2. Repository URL: 
   - GitHub: https://github.com/your-org/weitest.git
   - 本地 Git: file:///D:/Work/Trae/weitest
3. Branch: */master (或 main)
4. Credentials: 添加 Git 凭据（如需要）
```

#### 步骤 3: 配置构建触发器

**选项 A: Git 推送触发**
```
1. 勾选 "轮询 SCM" (Poll SCM)
2. 调度表：H/5 * * * * (每 5 分钟检查)
```

**选项 B: 定时触发**
```
1. 勾选 "构建触发器" → "定时构建"
2. 调度表：0 8 * * 1-5 (工作日早上 8 点)
```

**选项 C: Webhook 触发（推荐）**
```
1. 勾选 "GitHub hook trigger for GITScm polling"
2. 在 GitHub 仓库配置 Webhook:
   - Payload URL: http://your-jenkins-url/github-webhook/
   - Content type: application/json
   - Trigger: Push events
```

#### 步骤 4: 配置 Pipeline

**选项 A: 使用 SCM 中的 Jenkinsfile**
```
1. 选择 "Pipeline script from SCM"
2. Script Path: infra/ci/Jenkinsfile
```

**选项 B: 直接粘贴 Pipeline 脚本**
```
1. 选择 "Pipeline script"
2. 粘贴 infra/ci/Jenkinsfile 内容
```

#### 步骤 5: 配置邮件通知

```
系统管理 → 系统设置 → Extended E-mail Notification

SMTP 服务器：smtp.your-company.com
端口：587
发件人：jenkins@your-company.com
认证：用户名/密码
```

### 1.4 Windows Agent 配置

由于 WeiTest 是 Windows UI 自动化框架，需要配置 Windows 节点：

#### 创建 Windows Agent

```
1. 系统管理 → 节点管理 → 新节点
2. 节点名称：windows-ui-agent
3. 节点类型：Permanent Agent
4. 配置：
   - 远程根目录：C:\Jenkins\agent
   - 标签：windows ui-testing
   - 启动方法：Launch agent via Java Web Start
   - 使用率：尽可能使用此节点
   - 环境变量：
     * PYTHON_HOME=C:\Python39
     * PATH=%PYTHON_HOME%;%PATH%
```

#### Windows Agent 要求

- **操作系统**: Windows 10/11 或 Windows Server 2019+
- **Python**: 3.9+
- **屏幕分辨率**: 1920x1080+ (UI 测试需要)
- **屏幕锁定**: 必须保持解锁状态
- **用户权限**: 需要 GUI 交互权限

### 1.5 Allure 报告配置

#### 安装 Allure

```powershell
# 使用 Chocolatey
choco install allure

# 或手动安装
# 1. 下载：https://github.com/allure-framework/allure2/releases
# 2. 解压到 C:\tools\allure
# 3. 添加环境变量：ALLURE_HOME=C:\tools\allure
# 4. 添加 PATH: %ALLURE_HOME%\bin
```

#### Jenkins 配置 Allure

```
1. 系统管理 → 全局工具配置
2. Allure Commandline → 添加 Allure
3. 名称：allure
4. 路径：C:\tools\allure\bin
```

### 1.6 完整 Pipeline 示例

```groovy
// infra/ci/Jenkinsfile

pipeline {
    agent {
        label 'windows-ui-agent'  // 使用 Windows Agent
    }
    
    environment {
        PYTHON_VERSION = '3.9'
        PROJECT_NAME = 'WeiTest'
        REPORT_DIR = 'reports'
        ALLURE_RESULTS = 'reports/allure-results'
        LOG_DIR = 'logs'
        PYTHONPATH = '.'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 60, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }
    
    triggers {
        // Git 推送触发
        pollSCM('H/5 * * * *')
        // 定时触发
        cron('0 8 * * 1-5')
    }
    
    stages {
        stage('📥 Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    echo "当前提交：${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('🛠️ Environment Setup') {
            steps {
                bat '''
                    python --version
                    mkdir -p %REPORT_DIR%
                    mkdir -p %ALLURE_RESULTS%
                    mkdir -p %LOG_DIR%
                '''
            }
        }
        
        stage('📦 Install Dependencies') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install allure-pytest
                '''
            }
        }
        
        stage('🔍 Code Quality') {
            parallel {
                stage('Type Check') {
                    steps {
                        bat 'mypy core/ engine/ --ignore-missing-imports'
                    }
                }
                stage('Lint Check') {
                    steps {
                        bat 'ruff check src/ framework/ tests/'
                    }
                }
            }
        }
        
        stage('🧪 Run Tests') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        bat '''
                            pytest tests/test_core/ -v 
                                --alluredir=%ALLURE_RESULTS%/unit
                                --html=%REPORT_DIR%/unit-report.html
                                --tb=short
                        '''
                    }
                }
                
                stage('UI Tests') {
                    steps {
                        bat '''
                            pytest framework/tests/ui/ -v 
                                --alluredir=%ALLURE_RESULTS%/ui
                                --html=%REPORT_DIR%/ui-report.html
                                --tb=short
                        '''
                    }
                }
            }
        }
        
        stage('📊 Generate Reports') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${ALLURE_RESULTS}"]]
                ])
            }
        }
        
        stage('📁 Archive Artifacts') {
            steps {
                archiveArtifacts(
                    artifacts: '''
                        ${REPORT_DIR}/*.html
                        ${LOG_DIR}/**/*.log
                    ''',
                    allowEmptyArchive: true
                )
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            emailext(
                to: '${env.CHANGE_AUTHOR_EMAIL}',
                subject: "✅ [SUCCESS] ${env.PROJECT_NAME} - Build #${env.BUILD_NUMBER}",
                body: """
                    <html>
                    <body>
                    <h2>✅ 构建成功</h2>
                    <p>项目：${env.PROJECT_NAME}</p>
                    <p>构建号：#${env.BUILD_NUMBER}</p>
                    <p><a href="${env.BUILD_URL}">查看构建详情</a></p>
                    </body>
                    </html>
                """,
                mimeType: 'text/html'
            )
        }
        failure {
            emailext(
                to: '${env.CHANGE_AUTHOR_EMAIL}',
                subject: "❌ [FAILURE] ${env.PROJECT_NAME} - Build #${env.BUILD_NUMBER}",
                body: """
                    <html>
                    <body>
                    <h2>❌ 构建失败</h2>
                    <p>请查看构建日志</p>
                    <p><a href="${env.BUILD_URL}console">查看控制台输出</a></p>
                    </body>
                    </html>
                """,
                mimeType: 'text/html',
                attachLog: true
            )
        }
    }
}
```

---

## 2. GitHub Actions 配置

### 2.1 自动配置

项目已包含 GitHub Actions 工作流文件：`.github/workflows/ci.yml`

### 2.2 推送到 GitHub

#### 步骤 1: 创建 GitHub 仓库

```bash
# GitHub 上创建新仓库
# 访问：https://github.com/new
# 仓库名：weitest
```

#### 步骤 2: 添加远程仓库

```bash
cd D:\Work\Trae\weitest

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/weitest.git

# 验证
git remote -v
```

#### 步骤 3: 推送代码

```bash
# 推送到 GitHub
git push -u origin master

# 或推送到 main 分支
git push -u origin main
```

#### 步骤 4: 配置 GitHub Secrets（如需要）

如果需要使用 Codecov 或其他服务：

```
1. GitHub 仓库 → Settings → Secrets and variables → Actions
2. 添加 Secrets:
   - CODECOV_TOKEN: 你的 Codecov 令牌
```

### 2.3 查看工作流

推送后，GitHub Actions 会自动触发：

```
1. 访问：https://github.com/YOUR_USERNAME/weitest/actions
2. 查看工作流运行状态
3. 查看测试报告和覆盖率
```

### 2.4 自定义工作流

编辑 `.github/workflows/ci.yml` 自定义：

```yaml
name: WeiTest CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    # 自定义定时触发
    - cron: '0 8 * * 1-5'  # 工作日早上 8 点

jobs:
  test:
    runs-on: windows-latest
    
    strategy:
      matrix:
        # 自定义 Python 版本
        python-version: ['3.9', '3.10', '3.11']
    
    # ... 其余配置
```

---

## 3. 部署脚本使用

### 3.1 Windows 部署

使用 PowerShell 部署脚本：

```powershell
# 基本部署
.\infra\ci\deploy.ps1

# 指定部署路径
.\infra\ci\deploy.ps1 -DeployPath "C:\WeiTest"

# 指定环境
.\infra\ci\deploy.ps1 -Environment "production"

# 指定版本
.\infra\ci\deploy.ps1 -Version "1.0.0"
```

### 3.2 部署参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| DeployPath | 部署路径 | C:\WeiTest |
| Version | 版本号 | 1.0.0 |
| Environment | 环境 (test/production) | test |

### 3.3 部署后验证

```powershell
# 运行健康检查
python health_check.py

# 运行测试
pytest framework/tests/ui/ -v
```

---

## 4. 故障排除

### 4.1 Jenkins 常见问题

#### 问题 1: Windows Agent 无法连接

**解决方案**：
```
1. 检查 Java Web Start 是否运行
2. 检查防火墙设置
3. 重启 Jenkins Agent 服务
```

#### 问题 2: UI 测试失败（屏幕锁定）

**解决方案**：
```
1. 确保 Windows Agent 屏幕保持解锁
2. 使用自动登录配置
3. 或使用虚拟显示锁禁用工具
```

#### 问题 3: Allure 报告未生成

**解决方案**：
```
1. 检查 Allure 是否安装：allure --version
2. 检查 Jenkins 全局工具配置
3. 检查 pytest --alluredir 参数
```

### 4.2 GitHub Actions 常见问题

#### 问题 1: 工作流未触发

**解决方案**：
```
1. 检查 .github/workflows/ci.yml 语法
2. 检查分支名称是否匹配
3. 查看 Actions 日志
```

#### 问题 2: Windows 运行器 UI 测试失败

**说明**：GitHub-hosted runners 不支持 UI 自动化测试

**解决方案**：
```yaml
# 使用自托管运行器
jobs:
  test:
    runs-on: [self-hosted, windows, ui-testing]
```

### 4.3 日志位置

| 组件 | 日志位置 |
|------|----------|
| Jenkins | JENKINS_HOME/jobs/WeiTest/builds/*/log |
| GitHub Actions | GitHub → Actions → 工作流运行 → 查看日志 |
| 测试日志 | logs/*.log |
| 测试报告 | reports/*.html |

---

## 5. 最佳实践

### 5.1 Jenkins

- ✅ 使用专用 Windows Agent 运行 UI 测试
- ✅ 配置构建超时（60 分钟）
- ✅ 启用邮件通知
- ✅ 保留最近 30 个构建
- ✅ 使用 Pipeline 即代码

### 5.2 GitHub Actions

- ✅ 多 Python 版本测试
- ✅ 使用矩阵构建
- ✅ 缓存依赖加速构建
- ✅ 上传测试产物
- ✅ 集成 Codecov

### 5.3 一般建议

- ✅ 在 PR 合并前运行测试
- ✅ 定时运行完整测试套件
- ✅ 失败时自动通知
- ✅ 保留测试报告和日志
- ✅ 定期清理旧构建

---

## 6. 联系支持

如有问题，请联系：

- 项目文档：`docs/USER_GUIDE.md`
- 健康检查：`python health_check.py`
- CI/CD 配置：`infra/ci/Jenkinsfile`

---

**配置完成！现在可以开始使用 CI/CD 自动化测试了！** 🚀
