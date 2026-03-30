"""Pytest conftest - global fixtures and hooks"""

import pytest
import os
import webbrowser
from pathlib import Path
from datetime import datetime


# ========== Global Fixtures ==========


@pytest.fixture(scope="session")
def test_run_id():
    """生成测试运行 ID"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def report_dir(test_run_id):
    """测试报告目录"""
    report_path = Path("reports") / f"run_{test_run_id}"
    report_path.mkdir(parents=True, exist_ok=True)
    return report_path


@pytest.fixture(scope="function")
def screenshot_on_failure(request):
    """失败时自动截图"""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # 获取 page 对象并截图
        page = request.node.funcargs.get("page")
        if page and hasattr(page, "take_screenshot"):
            test_name = request.node.name.replace("/", "_").replace("\\", "_")
            filename = f"failure_{test_name}_{datetime.now().strftime('%H%M%S')}.png"
            try:
                page.take_screenshot(filename)
                print(f"\n  [SCREENSHOT] Saved: {filename}")
            except Exception as e:
                print(f"\n  [SCREENSHOT ERROR] {e}")


# ========== Hooks ==========


def pytest_collection_modifyitems(config, items):
    """测试收集后处理"""
    # 自动添加标记
    for item in items:
        # 根据路径添加标记
        if "smoke" in str(item.fspath):
            item.add_marker(pytest.mark.smoke)
        if "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行结果处理"""
    outcome = yield
    report = outcome.get_result()

    # 将报告存储到 item 中供 fixture 使用
    if report.when == "call":
        item.rep_call = report


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束后处理 - 自动打开报告"""
    yield

    # 自动打开 Allure 报告
    try:
        report_path = Path("reports/allure-report/index.html")
        if report_path.exists():
            print(f"\n{'=' * 60}")
            print(f"  测试完成！自动打开 Allure 报告...")
            print(f"  路径：{report_path.absolute()}")
            print(f"{'=' * 60}\n")
            webbrowser.open(f"file://{report_path.absolute()}")
    except Exception as e:
        print(f"\n[WARNING] 无法自动打开报告：{e}")

    # 打印测试摘要
    print(f"\n{'=' * 60}")
    print(f"  测试执行完成")
    print(f"  退出码：{exitstatus}")
    if exitstatus == 0:
        print(f"  状态：[PASS] 全部通过")
    else:
        print(f"  状态：[WARN] 部分失败")
    print(f"{'=' * 60}\n")


# ========== Worker ID for Parallel Execution ==========


@pytest.fixture(scope="session")
def worker_id(request):
    """获取并行测试 worker ID"""
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


# ========== Parallel-Safe Fixtures ==========


@pytest.fixture(scope="session")
def parallel_safe_tmp_dir(worker_id, tmp_path_factory):
    """并行安全的临时目录"""
    return tmp_path_factory.mktemp(f"tmp_{worker_id}")


# ========== Test History Tracking ==========


@pytest.fixture(scope="session")
def test_history_file():
    """测试历史文件路径"""
    history_dir = Path("reports/history")
    history_dir.mkdir(parents=True, exist_ok=True)
    return history_dir / "test_history.json"


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionstart(session):
    """测试会话开始时 - 记录历史信息"""
    yield

    # 记录测试开始时间
    import json

    history_file = Path("reports/history/test_history.json")

    history = {
        "start_time": datetime.now().isoformat(),
        "test_count": session.config.option.file_or_dir,
    }

    try:
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                all_history = json.load(f)
        else:
            all_history = []

        all_history.append(history)

        # 保留最近 100 次记录
        all_history = all_history[-100:]

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(all_history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARNING] 无法记录测试历史：{e}")
