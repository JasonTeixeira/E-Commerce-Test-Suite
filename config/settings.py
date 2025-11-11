"""
Configuration settings manager for test execution.

Loads environment variables and provides centralized configuration
for all test types across the framework.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    """Global settings for test execution."""

    # ========================================
    # Application Under Test
    # ========================================
    base_url: str = Field(default="https://www.demoblaze.com", env="BASE_URL")
    api_base_url: str = Field(default="https://api.demoblaze.com", env="API_BASE_URL")

    # ========================================
    # Test Configuration
    # ========================================
    test_env: str = Field(default="staging", env="TEST_ENV")
    browser: str = Field(default="chromium", env="BROWSER")
    headless: bool = Field(default=True, env="HEADLESS")
    browser_width: int = Field(default=1920, env="BROWSER_WIDTH")
    browser_height: int = Field(default=1080, env="BROWSER_HEIGHT")

    # Parallel execution
    pytest_workers: int = Field(default=8, env="PYTEST_WORKERS")
    max_workers: int = Field(default=10, env="MAX_WORKERS")

    # Timeouts (in milliseconds)
    default_timeout: int = Field(default=30000, env="DEFAULT_TIMEOUT")
    navigation_timeout: int = Field(default=60000, env="NAVIGATION_TIMEOUT")
    action_timeout: int = Field(default=15000, env="ACTION_TIMEOUT")

    # ========================================
    # Test User Credentials
    # ========================================
    test_user_email: str = Field(default="testuser@example.com", env="TEST_USER_EMAIL")
    test_user_password: str = Field(default="Test@1234", env="TEST_USER_PASSWORD")
    test_admin_email: str = Field(default="admin@example.com", env="TEST_ADMIN_EMAIL")
    test_admin_password: str = Field(default="Admin@1234", env="TEST_ADMIN_PASSWORD")

    # ========================================
    # API Configuration
    # ========================================
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    api_retry_count: int = Field(default=3, env="API_RETRY_COUNT")
    api_retry_delay: int = Field(default=1, env="API_RETRY_DELAY")

    # ========================================
    # Performance Testing
    # ========================================
    locust_users: int = Field(default=100, env="LOCUST_USERS")
    locust_spawn_rate: int = Field(default=10, env="LOCUST_SPAWN_RATE")
    locust_run_time: str = Field(default="5m", env="LOCUST_RUN_TIME")

    # Performance thresholds
    max_response_time_ms: int = Field(default=2000, env="MAX_RESPONSE_TIME_MS")
    max_page_load_time_ms: int = Field(default=3000, env="MAX_PAGE_LOAD_TIME_MS")
    error_rate_threshold: float = Field(default=0.01, env="ERROR_RATE_THRESHOLD")

    # ========================================
    # Visual Regression Testing
    # ========================================
    visual_diff_threshold: float = Field(default=0.05, env="VISUAL_DIFF_THRESHOLD")
    screenshot_dir: Path = Field(default=Path("reports/screenshots"), env="SCREENSHOT_DIR")
    baseline_dir: Path = Field(
        default=Path("ui_tests/visual/baselines"), env="BASELINE_DIR"
    )

    # ========================================
    # Security Testing
    # ========================================
    zap_api_key: str = Field(default="", env="ZAP_API_KEY")
    zap_host: str = Field(default="localhost", env="ZAP_HOST")
    zap_port: int = Field(default=8080, env="ZAP_PORT")
    security_scan_timeout: int = Field(default=600, env="SECURITY_SCAN_TIMEOUT")

    # ========================================
    # Accessibility Testing
    # ========================================
    wcag_level: str = Field(default="AA", env="WCAG_LEVEL")
    a11y_rules_to_run: str = Field(
        default="wcag2a,wcag2aa,wcag21aa", env="A11Y_RULES_TO_RUN"
    )

    # ========================================
    # Database Configuration
    # ========================================
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="demoblaze_test", env="DB_NAME")
    db_user: str = Field(default="test_user", env="DB_USER")
    db_password: str = Field(default="test_password", env="DB_PASSWORD")

    # ========================================
    # Reporting Configuration
    # ========================================
    report_dir: Path = Field(default=Path("reports"), env="REPORT_DIR")
    html_report_dir: Path = Field(default=Path("reports/html"), env="HTML_REPORT_DIR")
    allure_results_dir: Path = Field(
        default=Path("reports/allure-results"), env="ALLURE_RESULTS_DIR"
    )
    coverage_dir: Path = Field(default=Path("reports/coverage"), env="COVERAGE_DIR")

    # ========================================
    # Logging Configuration
    # ========================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_dir: Path = Field(default=Path("logs"), env="LOG_DIR")
    log_file_max_bytes: int = Field(default=10485760, env="LOG_FILE_MAX_BYTES")
    log_backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")

    # ========================================
    # CI/CD Configuration
    # ========================================
    ci: bool = Field(default=False, env="CI")
    github_actions: bool = Field(default=False, env="GITHUB_ACTIONS")

    # Notifications
    slack_webhook_url: str = Field(default="", env="SLACK_WEBHOOK_URL")
    email_notifications_enabled: bool = Field(
        default=False, env="EMAIL_NOTIFICATIONS_ENABLED"
    )
    email_recipients: str = Field(default="", env="EMAIL_RECIPIENTS")

    # ========================================
    # Feature Flags
    # ========================================
    run_ui_tests: bool = Field(default=True, env="RUN_UI_TESTS")
    run_api_tests: bool = Field(default=True, env="RUN_API_TESTS")
    run_performance_tests: bool = Field(default=True, env="RUN_PERFORMANCE_TESTS")
    run_security_tests: bool = Field(default=True, env="RUN_SECURITY_TESTS")
    run_accessibility_tests: bool = Field(default=True, env="RUN_ACCESSIBILITY_TESTS")
    run_visual_tests: bool = Field(default=True, env="RUN_VISUAL_TESTS")
    run_integration_tests: bool = Field(default=True, env="RUN_INTEGRATION_TESTS")

    # Screenshot/video capture
    capture_screenshots: bool = Field(default=True, env="CAPTURE_SCREENSHOTS")
    capture_videos: bool = Field(default=False, env="CAPTURE_VIDEOS")
    video_on_failure_only: bool = Field(default=True, env="VIDEO_ON_FAILURE_ONLY")

    # ========================================
    # External Services
    # ========================================
    browserstack_username: str = Field(default="", env="BROWSERSTACK_USERNAME")
    browserstack_access_key: str = Field(default="", env="BROWSERSTACK_ACCESS_KEY")
    sauce_username: str = Field(default="", env="SAUCE_USERNAME")
    sauce_access_key: str = Field(default="", env="SAUCE_ACCESS_KEY")

    # ========================================
    # Advanced Configuration
    # ========================================
    pytest_rerun_failures: int = Field(default=2, env="PYTEST_RERUN_FAILURES")
    test_data_dir: Path = Field(default=Path("tests/data"), env="TEST_DATA_DIR")
    faker_locale: str = Field(default="en_US", env="FAKER_LOCALE")
    enable_mocks: bool = Field(default=False, env="ENABLE_MOCKS")
    mock_server_url: str = Field(default="http://localhost:8081", env="MOCK_SERVER_URL")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"

    def get_browser_dimensions(self) -> Dict[str, int]:
        """Get browser viewport dimensions."""
        return {"width": self.browser_width, "height": self.browser_height}

    def get_playwright_config(self) -> Dict[str, Any]:
        """Get Playwright-specific configuration."""
        return {
            "headless": self.headless,
            "viewport": self.get_browser_dimensions(),
            "slow_mo": 0 if self.ci else 50,
            "timeout": self.default_timeout,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }

    def get_api_headers(self) -> Dict[str, str]:
        """Get default API headers."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "E-Commerce-Test-Suite/1.0",
        }

    def get_database_url(self) -> str:
        """Get database connection URL."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def is_ci_environment(self) -> bool:
        """Check if running in CI environment."""
        return self.ci or self.github_actions or os.getenv("CI") == "true"

    def should_capture_video(self) -> bool:
        """Determine if videos should be captured."""
        if not self.capture_videos:
            return False
        return True

    def get_enabled_test_suites(self) -> List[str]:
        """Get list of enabled test suites."""
        suites = []
        if self.run_ui_tests:
            suites.append("ui")
        if self.run_api_tests:
            suites.append("api")
        if self.run_performance_tests:
            suites.append("performance")
        if self.run_security_tests:
            suites.append("security")
        if self.run_accessibility_tests:
            suites.append("accessibility")
        if self.run_visual_tests:
            suites.append("visual")
        if self.run_integration_tests:
            suites.append("integration")
        return suites

    def get_a11y_rules(self) -> List[str]:
        """Get accessibility rules as a list."""
        return [rule.strip() for rule in self.a11y_rules_to_run.split(",")]

    def create_directories(self) -> None:
        """Create necessary directories for reports and logs."""
        directories = [
            self.report_dir,
            self.html_report_dir,
            self.allure_results_dir,
            self.coverage_dir,
            self.log_dir,
            self.screenshot_dir,
            self.baseline_dir,
            self.test_data_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Create necessary directories on import
settings.create_directories()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


# Convenience functions
def get_base_url() -> str:
    """Get base URL for the application."""
    return settings.base_url


def get_api_base_url() -> str:
    """Get base URL for API."""
    return settings.api_base_url


def is_headless() -> bool:
    """Check if browser should run in headless mode."""
    return settings.headless


def is_ci() -> bool:
    """Check if running in CI environment."""
    return settings.is_ci_environment()
