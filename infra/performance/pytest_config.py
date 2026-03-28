"""Performance Configuration - pytest configuration for parallel execution and retry"""

# pytest.ini 配置内容
PYTEST_INI_CONTENT = """
[pytest]
# 基础配置
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short

# 并行测试执行
# -n auto: 自动检测 CPU 核心数
# -n 4: 使用 4 个进程
addopts = -n auto

# 失败重试
# --reruns 2: 失败后重试 2 次
# --reruns-delay 2: 重试间隔 2 秒
addopts = --reruns 2 --reruns-delay 2

# 超时控制
# --timeout 300: 每个测试超时 300 秒
addopts = --timeout 300

# 标记选择
# -m smoke: 只运行冒烟测试
# -m "not slow": 跳过慢速测试
markers =
    smoke: 冒烟测试（核心功能，快速验证）
    regression: 回归测试（完整功能验证）
    slow: 慢速测试（>10 秒）
    ui: UI 测试
    unit: 单元测试
    integration: 集成测试

# 日志配置
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# 覆盖率配置
addopts = --cov=core --cov=engine --cov=infra --cov-report=html --cov-report=xml

# Allure 配置
addopts = --alluredir=reports/allure-results
"""

# conftest.py 配置内容
CONFTEST_PY_CONTENT = """
"""Pytest configuration and fixtures"""

import pytest
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="测试环境 (test/dev/prod)"
    )
    
    parser.addoption(
        "--retry-flaky",
        action="store_true",
        default=False,
        help="重试失败测试"
    )
    
    parser.addoption(
        "--parallel",
        action="store_true",
        default=True,
        help="并行执行测试"
    )


@pytest.fixture(scope="session")
def env(request):
    """获取测试环境"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    """加载环境配置"""
    from infra.config.enhanced_config import EnhancedConfigManager
    
    manager = EnhancedConfigManager("framework/data")
    return manager.load_with_env("env.yaml")


@pytest.fixture(autouse=True)
def setup_logging():
    """自动设置日志"""
    from infra.logging.logger import Logger
    
    logger = Logger("TestExecution")
    logger.info("测试开始")
    
    yield
    
    logger.info("测试结束")


# 自动重试失败测试
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """修改测试项集合"""
    if config.getoption("--retry-flaky"):
        for item in items:
            # 为 UI 测试添加重试标记
            if "ui" in item.keywords:
                item.add_marker(
                    pytest.mark.flaky(reruns=3, reruns_delay=2)
                )


# 超时配置
@pytest.fixture(autouse=True)
def timeout_setup():
    """设置测试超时"""
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("测试超时")
    
    # 设置 300 秒超时
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(300)
    
    yield
    
    signal.alarm(0)  # 取消超时


# 失败截图
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    if call.failed:
        # 尝试截图
        try:
            import pyautogui
            from pathlib import Path
            
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成截图文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = screenshot_dir / filename
            
            # 截图
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            print(f"\\n📸 失败截图已保存：{filepath}")
        except Exception as e:
            print(f"\\n⚠️  截图失败：{e}")
"""

# 并行测试执行脚本
RUN_PARALLEL_TESTS_BAT = """@echo off
REM 并行执行测试

echo ========================================
echo AutoTestMe-NG 并行测试执行
echo ========================================

REM 检测 CPU 核心数
echo 检测系统配置...
wmic cpu get NumberOfCores

REM 安装依赖
echo 安装测试依赖...
pip install pytest-xdist pytest-rerunfailures pytest-timeout

REM 执行并行测试
echo 开始并行测试执行...
pytest -n auto --reruns 2 --reruns-delay 2 --timeout 300 -v

echo ========================================
echo 测试执行完成
echo ========================================

pause
"""

# 测试执行报告生成脚本
GENERATE_REPORT_BAT = """@echo off
REM 生成测试报告

echo ========================================
echo 生成测试报告
echo ========================================

REM 生成 Allure 报告
echo 生成 Allure 报告...
allure generate reports/allure-results -o reports/allure-report --clean

REM 生成覆盖率报告
echo 生成覆盖率报告...
coverage html

REM 打开报告
echo 打开报告...
start reports/allure-report/index.html
start htmlcov/index.html

echo ========================================
echo 报告生成完成
echo ========================================

pause
"""
