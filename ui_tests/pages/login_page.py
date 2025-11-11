"""
Login Page object for DemoBlaze authentication.

Handles login modal, signup modal, and authentication flows.
"""

from typing import Optional

from playwright.sync_api import Page

from ui_tests.pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Login page object model for authentication."""

    # Login Modal
    LOGIN_MODAL = "#logInModal"
    LOGIN_MODAL_TITLE = "#logInModalLabel"
    LOGIN_USERNAME_INPUT = "#loginusername"
    LOGIN_PASSWORD_INPUT = "#loginpassword"
    LOGIN_BUTTON = 'button[onclick="logIn()"]'
    LOGIN_CLOSE_BUTTON = "#logInModal .close"

    # Signup Modal
    SIGNUP_MODAL = "#signInModal"
    SIGNUP_MODAL_TITLE = "#signInModalLabel"
    SIGNUP_USERNAME_INPUT = "#sign-username"
    SIGNUP_PASSWORD_INPUT = "#sign-password"
    SIGNUP_BUTTON = 'button[onclick="register()"]'
    SIGNUP_CLOSE_BUTTON = "#signInModal .close"

    # Navigation
    NAV_LOGIN_LINK = "#login2"
    NAV_SIGNUP_LINK = "#signin2"
    NAV_LOGOUT_LINK = "#logout2"
    NAV_WELCOME_USER = "#nameofuser"

    def __init__(self, page: Page):
        """Initialize Login page."""
        super().__init__(page)

    # ========================================
    # Login Modal Actions
    # ========================================

    def open_login_modal(self) -> "LoginPage":
        """
        Open login modal.

        Returns:
            Self for method chaining
        """
        logger.info("Opening login modal")
        self.click(self.NAV_LOGIN_LINK)
        self.wait_for_selector(self.LOGIN_MODAL, state="visible")
        return self

    def close_login_modal(self) -> "LoginPage":
        """
        Close login modal.

        Returns:
            Self for method chaining
        """
        logger.info("Closing login modal")
        self.click(self.LOGIN_CLOSE_BUTTON)
        self.wait_for_selector(self.LOGIN_MODAL, state="hidden")
        return self

    def fill_login_username(self, username: str) -> "LoginPage":
        """
        Fill login username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        logger.info(f"Filling login username: {username}")
        self.fill(self.LOGIN_USERNAME_INPUT, username)
        return self

    def fill_login_password(self, password: str) -> "LoginPage":
        """
        Fill login password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        logger.info("Filling login password")
        self.fill(self.LOGIN_PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> "LoginPage":
        """
        Click login button.

        Returns:
            Self for method chaining
        """
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """
        Complete login flow.

        Args:
            username: Username for login
            password: Password for login

        Returns:
            Self for method chaining
        """
        logger.info(f"Logging in as: {username}")
        self.open_login_modal()
        self.fill_login_username(username)
        self.fill_login_password(password)
        self.click_login_button()
        self.wait_for_timeout(2000)  # Wait for login processing
        return self

    # ========================================
    # Signup Modal Actions
    # ========================================

    def open_signup_modal(self) -> "LoginPage":
        """
        Open signup modal.

        Returns:
            Self for method chaining
        """
        logger.info("Opening signup modal")
        self.click(self.NAV_SIGNUP_LINK)
        self.wait_for_selector(self.SIGNUP_MODAL, state="visible")
        return self

    def close_signup_modal(self) -> "LoginPage":
        """
        Close signup modal.

        Returns:
            Self for method chaining
        """
        logger.info("Closing signup modal")
        self.click(self.SIGNUP_CLOSE_BUTTON)
        self.wait_for_selector(self.SIGNUP_MODAL, state="hidden")
        return self

    def fill_signup_username(self, username: str) -> "LoginPage":
        """
        Fill signup username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        logger.info(f"Filling signup username: {username}")
        self.fill(self.SIGNUP_USERNAME_INPUT, username)
        return self

    def fill_signup_password(self, password: str) -> "LoginPage":
        """
        Fill signup password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        logger.info("Filling signup password")
        self.fill(self.SIGNUP_PASSWORD_INPUT, password)
        return self

    def click_signup_button(self) -> "LoginPage":
        """
        Click signup button.

        Returns:
            Self for method chaining
        """
        logger.info("Clicking signup button")
        self.click(self.SIGNUP_BUTTON)
        return self

    def signup(self, username: str, password: str) -> "LoginPage":
        """
        Complete signup flow.

        Args:
            username: Username for signup
            password: Password for signup

        Returns:
            Self for method chaining
        """
        logger.info(f"Signing up user: {username}")
        self.open_signup_modal()
        self.fill_signup_username(username)
        self.fill_signup_password(password)
        self.click_signup_button()
        self.wait_for_timeout(2000)  # Wait for signup processing
        return self

    # ========================================
    # Logout Actions
    # ========================================

    def logout(self) -> "LoginPage":
        """
        Logout current user.

        Returns:
            Self for method chaining
        """
        logger.info("Logging out user")
        if self.is_logged_in():
            self.click(self.NAV_LOGOUT_LINK)
            self.wait_for_selector(self.NAV_LOGIN_LINK, state="visible")
        return self

    # ========================================
    # Verification Methods
    # ========================================

    def is_login_modal_open(self) -> bool:
        """
        Check if login modal is open.

        Returns:
            True if login modal is visible
        """
        return self.is_visible(self.LOGIN_MODAL, timeout=3000)

    def is_signup_modal_open(self) -> bool:
        """
        Check if signup modal is open.

        Returns:
            True if signup modal is visible
        """
        return self.is_visible(self.SIGNUP_MODAL, timeout=3000)

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.

        Returns:
            True if user is logged in
        """
        return self.is_visible(self.NAV_WELCOME_USER, timeout=3000)

    def get_logged_in_username(self) -> Optional[str]:
        """
        Get logged in username.

        Returns:
            Username if logged in, None otherwise
        """
        if self.is_logged_in():
            text = self.get_text(self.NAV_WELCOME_USER)
            # Extract username from "Welcome username"
            return text.replace("Welcome", "").strip()
        return None

    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.

        Returns:
            True if button is enabled
        """
        return self.is_enabled(self.LOGIN_BUTTON)

    def is_signup_button_enabled(self) -> bool:
        """
        Check if signup button is enabled.

        Returns:
            True if button is enabled
        """
        return self.is_enabled(self.SIGNUP_BUTTON)

    def get_login_modal_title(self) -> str:
        """
        Get login modal title.

        Returns:
            Modal title text
        """
        return self.get_text(self.LOGIN_MODAL_TITLE)

    def get_signup_modal_title(self) -> str:
        """
        Get signup modal title.

        Returns:
            Modal title text
        """
        return self.get_text(self.SIGNUP_MODAL_TITLE)

    # ========================================
    # Alert Handling
    # ========================================

    def handle_alert_and_get_text(self) -> Optional[str]:
        """
        Handle browser alert and get text.

        Returns:
            Alert text if present
        """
        alert_text = None

        def handle_dialog(dialog):
            nonlocal alert_text
            alert_text = dialog.message
            logger.info(f"Alert captured: {alert_text}")
            dialog.accept()

        self.page.on("dialog", handle_dialog)
        return alert_text

    def expect_alert_with_text(self, expected_text: str, timeout: int = 5000) -> bool:
        """
        Wait for and verify alert with specific text.

        Args:
            expected_text: Expected alert text
            timeout: Timeout in milliseconds

        Returns:
            True if alert appears with expected text
        """
        alert_appeared = False
        alert_text = None

        def handle_dialog(dialog):
            nonlocal alert_appeared, alert_text
            alert_text = dialog.message
            alert_appeared = expected_text.lower() in alert_text.lower()
            logger.info(f"Alert appeared: {alert_text}")
            dialog.accept()

        self.page.on("dialog", handle_dialog)
        self.wait_for_timeout(timeout)
        return alert_appeared
