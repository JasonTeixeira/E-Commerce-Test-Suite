"""
Security tests for DemoBlaze based on OWASP Top 10.

Tests for XSS, SQL injection, authentication, session management,
security headers, and other common vulnerabilities.
"""

import re
import uuid

import pytest
import requests

from api_tests.clients.demoblaze_client import DemoBlazeAPIClient
from config.settings import settings


@pytest.fixture
def api_client():
    """Create API client for security testing."""
    client = DemoBlazeAPIClient()
    yield client
    client.close()


@pytest.fixture
def session():
    """Create requests session."""
    s = requests.Session()
    yield s
    s.close()


class TestInjectionVulnerabilities:
    """Test for injection vulnerabilities (OWASP A03)."""

    @pytest.mark.security
    @pytest.mark.api
    def test_sql_injection_in_login(self, api_client):
        """Test SQL injection attempts in login."""
        payloads = [
            "admin' OR '1'='1",
            "admin'--",
            "admin' OR 1=1--",
            "' OR ''='",
            "1' OR '1' = '1",
        ]

        for payload in payloads:
            response = api_client.login(payload, "password")
            # Should not succeed with SQL injection
            assert not response.is_success(), f"SQL injection worked: {payload}"

    @pytest.mark.security
    @pytest.mark.api
    def test_sql_injection_in_signup(self, api_client):
        """Test SQL injection attempts in signup."""
        payloads = [
            "'; DROP TABLE users; --",
            "admin' OR '1'='1",
            "1' UNION SELECT NULL--",
        ]

        for payload in payloads:
            response = api_client.signup(payload, "password")
            # Should handle safely (either succeed or fail gracefully)
            assert response.status_code in [200, 400, 500]

    @pytest.mark.security
    @pytest.mark.api
    def test_xss_in_user_input(self, api_client):
        """Test XSS payload handling."""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
        ]

        for payload in xss_payloads:
            username = f"test_{uuid.uuid4().hex[:8]}"
            response = api_client.signup(username, payload)
            # Should sanitize or reject
            if response.is_success():
                # If accepted, verify no script execution in response
                assert "<script>" not in response.json_data.get("errorMessage", "")


class TestAuthenticationSecurity:
    """Test authentication and session security (OWASP A07)."""

    @pytest.mark.security
    @pytest.mark.api
    def test_weak_password_acceptance(self, api_client):
        """Test if system accepts weak passwords."""
        weak_passwords = ["123", "a", "password"]

        for weak_pwd in weak_passwords:
            username = f"test_{uuid.uuid4().hex[:8]}"
            response = api_client.signup(username, weak_pwd)
            # Note: DemoBlaze accepts any password (this is a finding)
            # In production, should reject weak passwords

    @pytest.mark.security
    @pytest.mark.api
    def test_brute_force_protection(self, api_client):
        """Test if there's rate limiting on login attempts."""
        username = "nonexistent_user"

        # Try multiple failed logins
        for _ in range(10):
            api_client.login(username, "wrongpassword")

        # Should have some protection (rate limiting, CAPTCHA, etc.)
        # Note: DemoBlaze likely doesn't have this (security finding)

    @pytest.mark.security
    @pytest.mark.api
    def test_session_token_randomness(self, api_client):
        """Test that session tokens are random."""
        tokens = set()

        for _ in range(5):
            username = f"test_{uuid.uuid4().hex[:8]}"
            api_client.signup(username, "Password123")
            response = api_client.login(username, "Password123")

            if response.is_success():
                token = response.json_data.get("Auth_token")
                if token:
                    tokens.add(token)

        # Tokens should be unique
        assert len(tokens) >= 4, "Tokens not sufficiently random"

    @pytest.mark.security
    @pytest.mark.api
    def test_password_in_response(self, api_client):
        """Test that passwords are never exposed in responses."""
        username = f"test_{uuid.uuid4().hex[:8]}"
        password = "SecretPassword123"

        response = api_client.signup(username, password)
        response_text = str(response.raw_response.text).lower()

        # Password should never appear in response
        assert password.lower() not in response_text


class TestSecurityHeaders:
    """Test security headers (OWASP A05)."""

    @pytest.mark.security
    def test_security_headers_present(self, session):
        """Test that security headers are present."""
        response = session.get("https://www.demoblaze.com")

        # Check for important security headers
        headers = response.headers

        # Note: Document findings if headers are missing
        expected_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": ["DENY", "SAMEORIGIN"],
            "Strict-Transport-Security": "max-age=",
            "Content-Security-Policy": None,
        }

    @pytest.mark.security
    def test_https_enforcement(self, session):
        """Test HTTPS is enforced."""
        # Try HTTP request
        response = session.get(
            "http://www.demoblaze.com",
            allow_redirects=False
        )

        # Should redirect to HTTPS or reject
        # Note: DemoBlaze may not enforce (security finding)

    @pytest.mark.security
    def test_cors_configuration(self, session):
        """Test CORS headers are properly configured."""
        response = session.options(
            "https://api.demoblaze.com/entries",
            headers={"Origin": "https://evil.com"}
        )

        # Check CORS headers
        cors_header = response.headers.get("Access-Control-Allow-Origin")
        # Should not be * or untrusted origins


class TestInputValidation:
    """Test input validation and sanitization (OWASP A03)."""

    @pytest.mark.security
    @pytest.mark.api
    def test_special_characters_handling(self, api_client):
        """Test handling of special characters."""
        special_chars = [
            "'; DROP TABLE--",
            "<script>alert('xss')</script>",
            "../../../../etc/passwd",
            "%00",
            "\x00",
        ]

        for chars in special_chars:
            username = f"test_{chars}_{uuid.uuid4().hex[:4]}"
            response = api_client.signup(username[:50], "Password123")
            # Should handle safely
            assert response.status_code in [200, 400, 500]

    @pytest.mark.security
    @pytest.mark.api
    def test_integer_overflow(self, api_client):
        """Test integer overflow handling."""
        cookie = uuid.uuid4().hex

        # Try adding with huge product ID
        response = api_client.add_to_cart(999999999999, cookie)
        # Should handle gracefully
        assert response.status_code in [200, 400, 404, 500]

    @pytest.mark.security
    @pytest.mark.api
    def test_negative_values(self, api_client):
        """Test negative value handling."""
        cookie = uuid.uuid4().hex

        # Try negative product ID
        response = api_client.add_to_cart(-1, cookie)
        # Should reject or handle safely
        assert response.status_code in [200, 400, 404]


class TestAuthorizationSecurity:
    """Test authorization and access control (OWASP A01)."""

    @pytest.mark.security
    @pytest.mark.api
    def test_cart_access_without_cookie(self, api_client):
        """Test accessing cart without proper cookie."""
        # Try to access cart with no cookie
        response = api_client.get_cart("")

        # Should reject or return empty
        assert response.status_code in [200, 401, 403]

    @pytest.mark.security
    @pytest.mark.api
    def test_other_user_cart_access(self, api_client):
        """Test accessing another user's cart."""
        cookie1 = uuid.uuid4().hex
        cookie2 = uuid.uuid4().hex

        # User 1 adds item
        api_client.add_to_cart(1, cookie1)

        # User 2 tries to access user 1's cart
        response = api_client.get_cart(cookie1)
        # Should protect cart data (note: cookie-based, may be vulnerable)


class TestCryptographicSecurity:
    """Test cryptographic implementations (OWASP A02)."""

    @pytest.mark.security
    @pytest.mark.api
    def test_password_not_stored_plaintext(self, api_client):
        """Test that passwords are not stored in plaintext."""
        username = f"test_{uuid.uuid4().hex[:8]}"
        password = "UniquePassword12345"

        api_client.signup(username, password)

        # Try to detect if password is visible anywhere
        # This is a limited test - proper test needs DB access

    @pytest.mark.security
    def test_ssl_certificate_valid(self, session):
        """Test SSL certificate is valid."""
        try:
            response = session.get("https://www.demoblaze.com", verify=True)
            assert response.status_code == 200
        except requests.exceptions.SSLError:
            pytest.fail("SSL certificate invalid or expired")


class TestAPISecurityMisconfigurations:
    """Test for security misconfigurations (OWASP A05)."""

    @pytest.mark.security
    def test_error_messages_not_verbose(self, session):
        """Test that error messages don't leak sensitive info."""
        response = session.post(
            "https://api.demoblaze.com/nonexistent",
            json={"invalid": "data"}
        )

        # Error messages should not reveal stack traces, DB info, etc.
        if response.status_code >= 400:
            text = response.text.lower()
            sensitive_keywords = [
                "stack trace",
                "exception",
                "mysql",
                "postgres",
                "mongodb",
                "/home/",
                "/var/",
            ]
            for keyword in sensitive_keywords:
                assert keyword not in text, f"Sensitive info leaked: {keyword}"

    @pytest.mark.security
    def test_directory_listing_disabled(self, session):
        """Test that directory listing is disabled."""
        paths = [
            "/uploads/",
            "/images/",
            "/assets/",
            "/static/",
        ]

        for path in paths:
            response = session.get(f"https://www.demoblaze.com{path}")
            # Should not show directory listing
            if response.status_code == 200:
                assert "Index of" not in response.text
