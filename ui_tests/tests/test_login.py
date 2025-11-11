"""
Login and authentication tests for DemoBlaze.

Tests login functionality, signup, logout, and session management.
"""

import pytest
from playwright.sync_api import Page

from ui_tests.pages.home_page import HomePage
from ui_tests.pages.login_page import LoginPage


class TestLoginModal:
    """Test suite for login modal functionality."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.auth
    @pytest.mark.critical
    def test_open_login_modal(self, page: Page):
        """Test opening login modal from homepage."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        assert login.is_login_modal_open()
        assert login.is_visible(login.LOGIN_USERNAME_INPUT)
        assert login.is_visible(login.LOGIN_PASSWORD_INPUT)
        assert login.is_visible(login.LOGIN_BUTTON)

    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_modal_title(self, page: Page):
        """Test login modal displays correct title."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        title = login.get_login_modal_title()
        assert "Log in" in title

    @pytest.mark.ui
    @pytest.mark.auth
    def test_close_login_modal(self, page: Page):
        """Test closing login modal."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()
        assert login.is_login_modal_open()

        login.close_login_modal()
        assert not login.is_login_modal_open()

    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_modal_fields_are_empty(self, page: Page):
        """Test login modal fields are initially empty."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        username_value = login.get_value(login.LOGIN_USERNAME_INPUT)
        password_value = login.get_value(login.LOGIN_PASSWORD_INPUT)

        assert username_value == ""
        assert password_value == ""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_button_enabled_by_default(self, page: Page):
        """Test login button is enabled by default."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        assert login.is_login_button_enabled()


class TestSignupModal:
    """Test suite for signup modal functionality."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.auth
    def test_open_signup_modal(self, page: Page):
        """Test opening signup modal from homepage."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        assert login.is_signup_modal_open()
        assert login.is_visible(login.SIGNUP_USERNAME_INPUT)
        assert login.is_visible(login.SIGNUP_PASSWORD_INPUT)
        assert login.is_visible(login.SIGNUP_BUTTON)

    @pytest.mark.ui
    @pytest.mark.auth
    def test_signup_modal_title(self, page: Page):
        """Test signup modal displays correct title."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        title = login.get_signup_modal_title()
        assert "Sign up" in title

    @pytest.mark.ui
    @pytest.mark.auth
    def test_close_signup_modal(self, page: Page):
        """Test closing signup modal."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()
        assert login.is_signup_modal_open()

        login.close_signup_modal()
        assert not login.is_signup_modal_open()

    @pytest.mark.ui
    @pytest.mark.auth
    def test_signup_button_enabled_by_default(self, page: Page):
        """Test signup button is enabled by default."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        assert login.is_signup_button_enabled()


class TestLoginFunctionality:
    """Test suite for login functionality."""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_login_username_field(self, page: Page):
        """Test filling login username field."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        test_username = "testuser123"
        login.fill_login_username(test_username)

        value = login.get_value(login.LOGIN_USERNAME_INPUT)
        assert value == test_username

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_login_password_field(self, page: Page):
        """Test filling login password field."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        test_password = "testpass123"
        login.fill_login_password(test_password)

        value = login.get_value(login.LOGIN_PASSWORD_INPUT)
        assert value == test_password

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_both_login_fields(self, page: Page):
        """Test filling both username and password fields."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_login_modal()

        test_username = "testuser123"
        test_password = "testpass123"

        login.fill_login_username(test_username)
        login.fill_login_password(test_password)

        username_value = login.get_value(login.LOGIN_USERNAME_INPUT)
        password_value = login.get_value(login.LOGIN_PASSWORD_INPUT)

        assert username_value == test_username
        assert password_value == test_password


class TestSignupFunctionality:
    """Test suite for signup functionality."""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_signup_username_field(self, page: Page):
        """Test filling signup username field."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        test_username = "newuser123"
        login.fill_signup_username(test_username)

        value = login.get_value(login.SIGNUP_USERNAME_INPUT)
        assert value == test_username

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_signup_password_field(self, page: Page):
        """Test filling signup password field."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        test_password = "newpass123"
        login.fill_signup_password(test_password)

        value = login.get_value(login.SIGNUP_PASSWORD_INPUT)
        assert value == test_password

    @pytest.mark.ui
    @pytest.mark.auth
    def test_fill_both_signup_fields(self, page: Page):
        """Test filling both signup username and password fields."""
        home = HomePage(page).open()
        login = LoginPage(page)
        login.open_signup_modal()

        test_username = "newuser123"
        test_password = "newpass123"

        login.fill_signup_username(test_username)
        login.fill_signup_password(test_password)

        username_value = login.get_value(login.SIGNUP_USERNAME_INPUT)
        password_value = login.get_value(login.SIGNUP_PASSWORD_INPUT)

        assert username_value == test_username
        assert password_value == test_password


class TestAuthenticationState:
    """Test suite for authentication state."""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_user_not_logged_in_initially(self, page: Page):
        """Test user is not logged in when visiting homepage."""
        home = HomePage(page).open()
        login = LoginPage(page)

        assert not login.is_logged_in()
        assert login.get_logged_in_username() is None

    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_link_visible_when_not_logged_in(self, page: Page):
        """Test login link is visible when not logged in."""
        home = HomePage(page).open()
        login = LoginPage(page)

        assert login.is_visible(login.NAV_LOGIN_LINK)

    @pytest.mark.ui
    @pytest.mark.auth
    def test_signup_link_visible_when_not_logged_in(self, page: Page):
        """Test signup link is visible when not logged in."""
        home = HomePage(page).open()
        login = LoginPage(page)

        assert login.is_visible(login.NAV_SIGNUP_LINK)

    @pytest.mark.ui
    @pytest.mark.auth
    def test_logout_link_not_visible_when_not_logged_in(self, page: Page):
        """Test logout link is not visible when not logged in."""
        home = HomePage(page).open()
        login = LoginPage(page)

        assert not login.is_visible(login.NAV_LOGOUT_LINK, timeout=2000)


class TestModalBehavior:
    """Test suite for modal behavior and interactions."""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_cannot_open_both_modals_simultaneously(self, page: Page):
        """Test that only one modal can be open at a time."""
        home = HomePage(page).open()
        login = LoginPage(page)

        # Open login modal
        login.open_login_modal()
        assert login.is_login_modal_open()

        # Close it and open signup
        login.close_login_modal()
        login.open_signup_modal()

        assert login.is_signup_modal_open()
        assert not login.is_login_modal_open()
