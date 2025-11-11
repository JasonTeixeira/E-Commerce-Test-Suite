"""
Root conftest.py for pytest configuration and global fixtures.

Provides shared fixtures and configuration for all test suites.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

# Add project root to Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


# ========================================
# Pytest Configuration Hooks
# ========================================


def pytest_configure(config):
    """Pytest configuration hook."""
    logger.info("=" * 80)
    logger.info("E-Commerce Test Suite - Starting Test Execution")
    logger.info("=" * 80)
    logger.info(f"Test Environment: {settings.test_env}")
    logger.info(f"Base URL: {settings.base_url}")
    logger.info(f"Browser: {settings.browser}")
    logger.info(f"Headless: {settings.headless}")
    logger.info(f"Parallel Workers: {settings.pytest_workers}")
    logger.info(f"CI Mode: {settings.is_ci_environment()}")
    logger.info("=" * 80)

    # Create report directories
    settings.create_directories()


def pytest_sessionfinish(session, exitstatus):
    """Pytest session finish hook."""
    logger.info("=" * 80)
    logger.info("Test Execution Completed")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 80)


def pytest_runtest_setup(item):
    """Hook called before each test."""
    logger.info(f"Running test: {item.nodeid}")


def pytest_runtest_makereport(item, call):
    """Hook to capture test results."""
    if call.when == "call":
        if call.excinfo is not None:
            logger.error(f"Test FAILED: {item.nodeid}")
        else:
            logger.info(f"Test PASSED: {item.nodeid}")


# ========================================
# Playwright Fixtures
# ========================================


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """
    Session-scoped Playwright instance.

    Yields:
        Playwright instance for the entire test session
    """
    with sync_playwright() as playwright:
        logger.info("Playwright instance started")
        yield playwright
        logger.info("Playwright instance closed")


@pytest.fixture(scope="session")
def browser_type_name() -> str:
    """Get browser type from settings."""
    return settings.browser


@pytest.fixture(scope="session")
def browser(
    playwright_instance: Playwright, browser_type_name: str
) -> Generator[Browser, None, None]:
    """
    Session-scoped browser instance.

    Args:
        playwright_instance: Playwright instance
        browser_type_name: Browser type (chromium, firefox, webkit)

    Yields:
        Browser instance
    """
    browser_type = getattr(playwright_instance, browser_type_name)
    browser_config = settings.get_playwright_config()

    browser_instance = browser_type.launch(**browser_config)
    logger.info(f"Browser launched: {browser_type_name}")

    yield browser_instance

    browser_instance.close()
    logger.info(f"Browser closed: {browser_type_name}")


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context.

    Args:
        browser: Browser instance

    Yields:
        Browser context
    """
    context = browser.new_context(
        viewport=settings.get_browser_dimensions(),
        record_video_dir=str(settings.report_dir / "videos")
        if settings.capture_videos
        else None,
    )

    yield context

    # Save video on failure if enabled
    if settings.video_on_failure_only:
        for page in context.pages:
            video = page.video
            if video:
                video_path = video.path()
                if video_path and not os.path.exists(str(video_path).replace(".webm", "_failure.webm")):
                    # Video is only kept for failures via pytest plugin
                    pass

    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page instance.

    Args:
        context: Browser context

    Yields:
        Page instance
    """
    page = context.new_page()
    page.set_default_timeout(settings.default_timeout)
    page.set_default_navigation_timeout(settings.navigation_timeout)

    yield page

    page.close()


# ========================================
# Screenshot Fixtures
# ========================================


@pytest.fixture
def screenshot_on_failure(request, page: Page):
    """Capture screenshot on test failure."""
    yield

    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_dir = settings.screenshot_dir / "failures"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

        page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ========================================
# Configuration Fixtures
# ========================================


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get base URL for the application."""
    return settings.base_url


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Get API base URL."""
    return settings.api_base_url


@pytest.fixture(scope="session")
def test_config() -> Dict:
    """Get test configuration."""
    return {
        "base_url": settings.base_url,
        "api_base_url": settings.api_base_url,
        "browser": settings.browser,
        "headless": settings.headless,
        "timeout": settings.default_timeout,
        "env": settings.test_env,
    }


# ========================================
# Test Data Fixtures
# ========================================


@pytest.fixture
def test_user_credentials() -> Dict[str, str]:
    """Get test user credentials."""
    return {
        "email": settings.test_user_email,
        "password": settings.test_user_password,
        "username": settings.test_user_email.split("@")[0],
    }


@pytest.fixture
def test_admin_credentials() -> Dict[str, str]:
    """Get admin user credentials."""
    return {
        "email": settings.test_admin_email,
        "password": settings.test_admin_password,
        "username": settings.test_admin_email.split("@")[0],
    }


# ========================================
# Utility Fixtures
# ========================================


@pytest.fixture
def timestamp() -> str:
    """Get current timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test information automatically."""
    logger.info(f"Starting: {request.node.nodeid}")
    yield
    logger.info(f"Finished: {request.node.nodeid}")


# ========================================
# Markers
# ========================================

pytest_plugins = []
