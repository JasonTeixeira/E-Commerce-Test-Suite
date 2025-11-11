"""
Base API client for REST API testing.

Provides common HTTP methods with retry logic, logging,
authentication, and comprehensive error handling.
"""

import time
from typing import Any, Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class APIResponse:
    """Wrapper for API response with convenient methods."""

    def __init__(self, response: requests.Response):
        """Initialize API response wrapper."""
        self.response = response
        self.status_code = response.status_code
        self.headers = dict(response.headers)
        self.url = response.url
        self.request_method = response.request.method
        self.elapsed = response.elapsed.total_seconds()

        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None

        self.text = response.text

    def is_success(self) -> bool:
        """Check if response is successful (2xx)."""
        return 200 <= self.status_code < 300

    def is_client_error(self) -> bool:
        """Check if response is client error (4xx)."""
        return 400 <= self.status_code < 500

    def is_server_error(self) -> bool:
        """Check if response is server error (5xx)."""
        return 500 <= self.status_code < 600

    def __repr__(self) -> str:
        """String representation of response."""
        return f"<APIResponse [{self.status_code}] {self.request_method} {self.url}>"


class BaseAPIClient:
    """Base API client with common HTTP methods."""

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.

        Args:
            base_url: Base URL for API requests
        """
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.api_timeout
        self.retry_count = settings.api_retry_count
        self.retry_delay = settings.api_retry_delay

        self.session = self._create_session()
        self.default_headers = settings.get_api_headers()

        logger.info(f"Initialized API client for: {self.base_url}")

    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry strategy.

        Returns:
            Configured requests session
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retry_count,
            backoff_factor=self.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.

        Args:
            endpoint: API endpoint

        Returns:
            Full URL
        """
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _merge_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Merge custom headers with default headers.

        Args:
            headers: Custom headers

        Returns:
            Merged headers dictionary
        """
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details."""
        logger.info(f"API Request: {method} {url}")
        if kwargs.get("params"):
            logger.debug(f"Query params: {kwargs['params']}")
        if kwargs.get("json"):
            logger.debug(f"JSON body: {kwargs['json']}")

    def _log_response(self, response: APIResponse) -> None:
        """Log response details."""
        logger.info(
            f"API Response: [{response.status_code}] "
            f"{response.request_method} {response.url} "
            f"({response.elapsed:.2f}s)"
        )
        if response.json_data:
            logger.debug(f"Response data: {response.json_data}")

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """
        Handle and wrap response.

        Args:
            response: Raw requests response

        Returns:
            Wrapped APIResponse

        Raises:
            requests.HTTPError: If response indicates error
        """
        api_response = APIResponse(response)
        self._log_response(api_response)

        # Raise for HTTP errors
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response body: {api_response.text}")
            raise

        return api_response

    # ========================================
    # HTTP Methods
    # ========================================

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> APIResponse:
        """
        Send GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Custom headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout

        self._log_request("GET", url, params=params, headers=headers)

        response = self.session.get(
            url, params=params, headers=headers, timeout=timeout, **kwargs
        )

        return self._handle_response(response)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> APIResponse:
        """
        Send POST request.

        Args:
            endpoint: API endpoint
            json: JSON data
            data: Form data
            headers: Custom headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout

        self._log_request("POST", url, json=json, data=data, headers=headers)

        response = self.session.post(
            url, json=json, data=data, headers=headers, timeout=timeout, **kwargs
        )

        return self._handle_response(response)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> APIResponse:
        """
        Send PUT request.

        Args:
            endpoint: API endpoint
            json: JSON data
            data: Form data
            headers: Custom headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout

        self._log_request("PUT", url, json=json, data=data, headers=headers)

        response = self.session.put(
            url, json=json, data=data, headers=headers, timeout=timeout, **kwargs
        )

        return self._handle_response(response)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> APIResponse:
        """
        Send DELETE request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Custom headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout

        self._log_request("DELETE", url, params=params, headers=headers)

        response = self.session.delete(
            url, params=params, headers=headers, timeout=timeout, **kwargs
        )

        return self._handle_response(response)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> APIResponse:
        """
        Send PATCH request.

        Args:
            endpoint: API endpoint
            json: JSON data
            data: Form data
            headers: Custom headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            APIResponse object
        """
        url = self._build_url(endpoint)
        headers = self._merge_headers(headers)
        timeout = timeout or self.timeout

        self._log_request("PATCH", url, json=json, data=data, headers=headers)

        response = self.session.patch(
            url, json=json, data=data, headers=headers, timeout=timeout, **kwargs
        )

        return self._handle_response(response)

    # ========================================
    # Utility Methods
    # ========================================

    def close(self) -> None:
        """Close session."""
        self.session.close()
        logger.info("API client session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
