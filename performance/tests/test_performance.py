"""
Performance benchmark tests for DemoBlaze.

Tests response times, throughput, and performance metrics
for critical user journeys and API endpoints.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from api_tests.clients.demoblaze_client import DemoBlazeAPIClient
from config.settings import settings


@pytest.fixture
def api_client():
    """Create API client for performance testing."""
    client = DemoBlazeAPIClient()
    yield client
    client.close()


class TestAPIPerformance:
    """Performance tests for API endpoints."""

    @pytest.mark.performance
    @pytest.mark.api
    def test_products_api_response_time(self, api_client):
        """Test products API responds within threshold."""
        start = time.time()
        response = api_client.get_products()
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 2.0, f"API took {elapsed:.2f}s (threshold: 2.0s)"

    @pytest.mark.performance
    @pytest.mark.api
    def test_products_api_avg_response_time(self, api_client):
        """Test average response time over multiple requests."""
        times = []

        for _ in range(10):
            start = time.time()
            response = api_client.get_products()
            elapsed = time.time() - start
            times.append(elapsed)
            assert response.is_success()

        avg_time = sum(times) / len(times)
        assert avg_time < 2.0, f"Average: {avg_time:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_login_api_performance(self, api_client):
        """Test login API performance."""
        # Create test user first
        import uuid
        username = f"perftest_{uuid.uuid4().hex[:8]}"
        api_client.signup(username, "Password123")

        start = time.time()
        response = api_client.login(username, "Password123")
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 2.0, f"Login took {elapsed:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_cart_operations_performance(self, api_client):
        """Test cart operations complete quickly."""
        import uuid
        cookie = f"perftest_{uuid.uuid4().hex}"

        # Add to cart
        start = time.time()
        response = api_client.add_to_cart(1, cookie)
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 2.0, f"Add to cart took {elapsed:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_concurrent_api_requests(self, api_client):
        """Test API handles concurrent requests."""
        def make_request():
            response = api_client.get_products()
            return response.is_success()

        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [f.result() for f in as_completed(futures)]
        elapsed = time.time() - start

        assert all(results), "Some requests failed"
        assert elapsed < 10.0, f"20 concurrent requests took {elapsed:.2f}s"


class TestResponseTimeConsistency:
    """Test response time consistency."""

    @pytest.mark.performance
    @pytest.mark.api
    def test_response_time_variance(self, api_client):
        """Test response times don't vary wildly."""
        times = []

        for _ in range(10):
            start = time.time()
            api_client.get_products()
            elapsed = time.time() - start
            times.append(elapsed)

        avg = sum(times) / len(times)
        variance = sum((t - avg) ** 2 for t in times) / len(times)
        std_dev = variance ** 0.5

        # Standard deviation should be reasonable
        assert std_dev < 1.0, f"High variance: {std_dev:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_no_performance_degradation(self, api_client):
        """Test performance doesn't degrade over time."""
        first_batch = []
        second_batch = []

        # First batch
        for _ in range(5):
            start = time.time()
            api_client.get_products()
            first_batch.append(time.time() - start)

        time.sleep(1)

        # Second batch
        for _ in range(5):
            start = time.time()
            api_client.get_products()
            second_batch.append(time.time() - start)

        avg_first = sum(first_batch) / len(first_batch)
        avg_second = sum(second_batch) / len(second_batch)

        # Second batch shouldn't be significantly slower
        assert avg_second <= avg_first * 1.5, "Performance degraded"


class TestThroughput:
    """Test API throughput."""

    @pytest.mark.performance
    @pytest.mark.api
    @pytest.mark.slow
    def test_requests_per_second(self, api_client):
        """Test API can handle minimum requests per second."""
        request_count = 20
        start = time.time()

        for _ in range(request_count):
            response = api_client.get_products()
            assert response.is_success()

        elapsed = time.time() - start
        rps = request_count / elapsed

        assert rps >= 5, f"Only {rps:.2f} req/s (target: 5)"

    @pytest.mark.performance
    @pytest.mark.api
    def test_api_handles_burst_traffic(self, api_client):
        """Test API handles burst of traffic."""
        def rapid_requests():
            for _ in range(5):
                api_client.get_products()

        start = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(rapid_requests) for _ in range(5)]
            [f.result() for f in as_completed(futures)]
        elapsed = time.time() - start

        # 25 total requests should complete in reasonable time
        assert elapsed < 15.0, f"Burst took {elapsed:.2f}s"


class TestEndpointPerformance:
    """Test individual endpoint performance."""

    @pytest.mark.performance
    @pytest.mark.api
    def test_signup_endpoint_performance(self, api_client):
        """Test signup endpoint performance."""
        import uuid
        username = f"perftest_{uuid.uuid4().hex[:8]}"

        start = time.time()
        response = api_client.signup(username, "Password123")
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 2.0

    @pytest.mark.performance
    @pytest.mark.api
    def test_cart_view_performance(self, api_client):
        """Test cart viewing performance."""
        import uuid
        cookie = f"perftest_{uuid.uuid4().hex}"

        start = time.time()
        response = api_client.get_cart(cookie)
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 2.0

    @pytest.mark.performance
    @pytest.mark.api
    def test_order_placement_performance(self, api_client):
        """Test order placement performance."""
        import uuid
        cookie = f"perftest_{uuid.uuid4().hex}"

        # Add item first
        api_client.add_to_cart(1, cookie)

        start = time.time()
        response = api_client.place_order(
            cookie=cookie,
            name="Perf Test",
            country="USA",
            city="Test",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )
        elapsed = time.time() - start

        assert response.is_success()
        assert elapsed < 3.0  # Order might take slightly longer


class TestLoadScenarios:
    """Test various load scenarios."""

    @pytest.mark.performance
    @pytest.mark.slow
    def test_sequential_user_journey_performance(self, api_client):
        """Test complete user journey performance."""
        import uuid
        username = f"perftest_{uuid.uuid4().hex[:8]}"
        cookie = uuid.uuid4().hex

        start = time.time()

        # Signup
        api_client.signup(username, "Password123")

        # Login
        api_client.login(username, "Password123")

        # Browse products
        api_client.get_products()

        # Add to cart
        api_client.add_to_cart(1, cookie)

        # View cart
        api_client.get_cart(cookie)

        # Place order
        api_client.place_order(
            cookie=cookie,
            name="Perf Test",
            country="USA",
            city="Test",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )

        elapsed = time.time() - start

        # Complete journey should be under 15 seconds
        assert elapsed < 15.0, f"Journey took {elapsed:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_repeated_operations_performance(self, api_client):
        """Test repeated operations don't slow down."""
        times = []

        for i in range(10):
            start = time.time()
            response = api_client.get_products()
            elapsed = time.time() - start
            times.append(elapsed)
            assert response.is_success()

        # First and last should be similar
        first_three = sum(times[:3]) / 3
        last_three = sum(times[-3:]) / 3

        assert last_three <= first_three * 1.5


class TestPerformanceMetrics:
    """Test performance metrics and thresholds."""

    @pytest.mark.performance
    @pytest.mark.api
    def test_p95_response_time(self, api_client):
        """Test 95th percentile response time."""
        times = []

        for _ in range(20):
            start = time.time()
            api_client.get_products()
            times.append(time.time() - start)

        times.sort()
        p95 = times[int(len(times) * 0.95)]

        assert p95 < 3.0, f"P95: {p95:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_p99_response_time(self, api_client):
        """Test 99th percentile response time."""
        times = []

        for _ in range(20):
            start = time.time()
            api_client.get_products()
            times.append(time.time() - start)

        times.sort()
        p99 = times[int(len(times) * 0.99)]

        assert p99 < 5.0, f"P99: {p99:.2f}s"

    @pytest.mark.performance
    @pytest.mark.api
    def test_api_success_rate_under_load(self, api_client):
        """Test API maintains high success rate under load."""
        successes = 0
        total = 50

        for _ in range(total):
            try:
                response = api_client.get_products()
                if response.is_success():
                    successes += 1
            except Exception:
                pass

        success_rate = successes / total
        assert success_rate >= 0.95, f"Success rate: {success_rate:.2%}"

    @pytest.mark.performance
    @pytest.mark.api
    def test_error_rate_threshold(self, api_client):
        """Test error rate stays below threshold."""
        errors = 0
        total = 30

        for _ in range(total):
            try:
                response = api_client.get_products()
                if not response.is_success():
                    errors += 1
            except Exception:
                errors += 1

        error_rate = errors / total
        assert error_rate <= settings.error_rate_threshold
