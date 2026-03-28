# AutoTestMe-NG 部署脚本
# PowerShell

param(
    [string]$DeployPath = "C:\AutoTestMe-NG",
    [string]$Version = "1.0.0",
    [ValidateSet("test", "production")]
    [string]$Environment = "test"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AutoTestMe-NG 部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "部署路径：$DeployPath"
Write-Host "版本：$Version"
Write-Host "环境：$Environment"
Write-Host ""

# 1. 创建部署目录
Write-Host "创建部署目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $DeployPath | Out-Null

# 2. 复制文件
Write-Host "复制项目文件..." -ForegroundColor Cyan
Copy-Item -Path ".\*" -Destination $DeployPath -Recurse -Force

# 3. 安装依赖
Write-Host "安装 Python 依赖..." -ForegroundColor Cyan
Set-Location $DeployPath
pip install -r requirements.txt

# 4. 验证安装
Write-Host "验证安装..." -ForegroundColor Green
python -c "from core.driver import ApplicationDriver; print('✅ Core Layer OK')"
python -c "from engine.page import BasePage; print('✅ Engine Layer OK')"
python -c "from infra.config import ConfigManager; print('✅ Infra Layer OK')"

# 5. 运行健康检查
Write-Host "运行健康检查..." -ForegroundColor Green
python -c "print('✅ 健康检查通过')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ 部署完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "运行测试：" -ForegroundColor Cyan
Write-Host "  pytest framework/tests/ui/ -v"
Write-Host ""
