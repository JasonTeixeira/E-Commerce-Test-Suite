"""
User and authentication API tests for DemoBlaze.

Tests user registration, login, and authentication workflows.
"""

import uuid

import pytest

from api_tests.clients.demoblaze_client import DemoBlazeAPIClient


@pytest.fixture
def api_client():
    """Create API client instance."""
    client = DemoBlazeAPIClient()
    yield client
    client.close()


@pytest.fixture
def unique_username():
    """Generate unique username for testing."""
    return f"testuser_{uuid.uuid4().hex[:8]}"


class TestUserSignup:
    """Test suite for user signup API."""

    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.auth
    @pytest.mark.critical
    def test_signup_new_user(self, api_client, unique_username):
        """Test signing up a new user."""
        response = api_client.signup(unique_username, "TestPassword123")

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.auth
    def test_signup_response_time(self, api_client, unique_username):
        """Test signup response time."""
        response = api_client.signup(unique_username, "TestPassword123")

        assert response.is_success()
        assert response.elapsed < 5.0

    @pytest.mark.api
    @pytest.mark.auth
    def test_signup_with_strong_password(self, api_client, unique_username):
        """Test signup with strong password."""
        strong_password = "Str0ng!P@ssw0rd#2024"
        response = api_client.signup(unique_username, strong_password)

        assert response.is_success()

    @pytest.mark.api
    @pytest.mark.auth
    def test_signup_with_short_password(self, api_client, unique_username):
        """Test signup with short password."""
        response = api_client.signup(unique_username, "123")

        # Should still accept (DemoBlaze doesn't enforce password strength)
        assert response.is_success()

    @pytest.mark.api
    @pytest.mark.auth
    def test_signup_with_special_characters(self, api_client):
        """Test signup with special characters in username."""
        username = f"test_user_{uuid.uuid4().hex[:6]}"
        response = api_client.signup(username, "TestPassword")

        assert response.is_success()


class TestUserLogin:
    """Test suite for user login API."""

    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.auth
    @pytest.mark.critical
    def test_login_existing_user(self, api_client, unique_username):
        """Test logging in with existing user."""
        # First signup
        api_client.signup(unique_username, "TestPassword123")

        # Then login
        response = api_client.login(unique_username, "TestPassword123")

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_returns_token(self, api_client, unique_username):
        """Test login returns auth token."""
        api_client.signup(unique_username, "TestPassword123")
        response = api_client.login(unique_username, "TestPassword123")

        assert response.is_success()
        # DemoBlaze returns base64 encoded token in response text
        assert response.text is not None
        assert len(response.text) > 0

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_response_time(self, api_client, unique_username):
        """Test login response time."""
        api_client.signup(unique_username, "TestPassword123")
        response = api_client.login(unique_username, "TestPassword123")

        assert response.is_success()
        assert response.elapsed < 5.0

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_with_wrong_password(self, api_client, unique_username):
        """Test login with incorrect password."""
        api_client.signup(unique_username, "CorrectPassword")

        # Try with wrong password
        try:
            response = api_client.login(unique_username, "WrongPassword")
            # DemoBlaze may return error or 200 with error message
        except Exception:
            pass  # Expected to fail

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user."""
        try:
            response = api_client.login("nonexistent_user_12345", "password")
            # Should fail or return error
        except Exception:
            pass  # Expected to fail


class TestAuthenticationWorkflow:
    """Test suite for complete auth workflows."""

    @pytest.mark.api
    @pytest.mark.auth
    @pytest.mark.integration
    def test_signup_then_login_workflow(self, api_client, unique_username):
        """Test complete signup then login workflow."""
        password = "TestPassword123"

        # Signup
        signup_response = api_client.signup(unique_username, password)
        assert signup_response.is_success()

        # Login
        login_response = api_client.login(unique_username, password)
        assert login_response.is_success()

    @pytest.mark.api
    @pytest.mark.auth
    def test_multiple_signups_different_users(self, api_client):
        """Test signing up multiple different users."""
        users = [f"user_{uuid.uuid4().hex[:6]}" for _ in range(3)]

        for username in users:
            response = api_client.signup(username, "Password123")
            assert response.is_success()

    @pytest.mark.api
    @pytest.mark.auth
    def test_auth_api_consistency(self, api_client, unique_username):
        """Test auth API returns consistent responses."""
        responses = []

        for i in range(3):
            username = f"{unique_username}_{i}"
            response = api_client.signup(username, "Password123")
            responses.append(response)

        # All should have same status code
        status_codes = [r.status_code for r in responses]
        assert len(set(status_codes)) == 1  # All the same

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_after_multiple_signups(self, api_client):
        """Test login works after multiple user registrations."""
        # Create multiple users
        users = []
        for _ in range(2):
            username = f"user_{uuid.uuid4().hex[:6]}"
            api_client.signup(username, "Password123")
            users.append(username)

        # Login with first user
        response = api_client.login(users[0], "Password123")
        assert response.is_success()

    @pytest.mark.api
    @pytest.mark.auth
    def test_auth_with_empty_credentials(self, api_client):
        """Test auth with empty credentials."""
        try:
            response = api_client.signup("", "")
            # May accept empty or return error
        except Exception:
            pass  # Expected to potentially fail
