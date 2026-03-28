# Pytest Configuration and Fixtures

import pytest
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--env", action="store", default="test", help="Test environment (test/dev/prod)"
    )

    parser.addoption("--retry-flaky", action="store_true", default=False, help="Retry failed tests")


@pytest.fixture(scope="session")
def env(request):
    """Get test environment"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    """Load environment configuration"""
    from infra.config.enhanced_config import EnhancedConfigManager

    manager = EnhancedConfigManager("framework/data")
    return manager.load_with_env("env.yaml")


@pytest.fixture(autouse=True)
def setup_logging():
    """Auto setup logging"""
    from infra.logging.structured_logger import get_logger

    logger = get_logger("TestExecution", "reports/logs")
    logger.info("Test started")

    yield

    logger.info("Test completed")
