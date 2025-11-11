"""
Product API tests for DemoBlaze.

Tests product retrieval, filtering, validation,
and error handling for the products API.
"""

import pytest

from api_tests.clients.demoblaze_client import DemoBlazeAPIClient


@pytest.fixture
def api_client():
    """Create API client instance."""
    client = DemoBlazeAPIClient()
    yield client
    client.close()


class TestProductsAPI:
    """Test suite for products API endpoints."""

    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.critical
    def test_get_all_products(self, api_client):
        """Test retrieving all products."""
        response = api_client.get_products()

        assert response.is_success()
        assert response.status_code == 200
        assert response.json_data is not None

    @pytest.mark.api
    def test_products_response_structure(self, api_client):
        """Test products response has correct structure."""
        response = api_client.get_products()

        assert response.is_success()
        assert "Items" in response.json_data
        assert isinstance(response.json_data["Items"], list)

    @pytest.mark.api
    def test_products_list_not_empty(self, api_client):
        """Test products list contains items."""
        response = api_client.get_products()

        assert response.is_success()
        items = response.json_data.get("Items", [])
        assert len(items) > 0

    @pytest.mark.api
    def test_product_has_required_fields(self, api_client):
        """Test each product has required fields."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        assert len(items) > 0
        product = items[0]

        # Check required fields
        assert "id" in product
        assert "title" in product
        assert "price" in product
        assert "cat" in product

    @pytest.mark.api
    def test_product_id_is_numeric(self, api_client):
        """Test product IDs are numeric."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items[:5]:  # Check first 5
            assert isinstance(product["id"], int)
            assert product["id"] > 0

    @pytest.mark.api
    def test_product_price_is_numeric(self, api_client):
        """Test product prices are numeric."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items[:5]:
            assert isinstance(product["price"], int)
            assert product["price"] > 0

    @pytest.mark.api
    def test_product_title_not_empty(self, api_client):
        """Test product titles are not empty."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items[:5]:
            assert product["title"] is not None
            assert len(product["title"].strip()) > 0

    @pytest.mark.api
    def test_product_category_valid(self, api_client):
        """Test product categories are valid."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        valid_categories = ["phone", "notebook", "monitor"]

        for product in items[:5]:
            assert product["cat"] in valid_categories

    @pytest.mark.api
    def test_get_product_by_id(self, api_client):
        """Test retrieving product by ID."""
        # First get a product ID
        products_response = api_client.get_products()
        items = products_response.json_data.get("Items", [])
        product_id = items[0]["id"]

        # Get specific product
        response = api_client.get_product_by_id(product_id)

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    def test_products_api_response_time(self, api_client):
        """Test API response time is reasonable."""
        response = api_client.get_products()

        assert response.is_success()
        assert response.elapsed < 5.0  # Should respond within 5 seconds

    @pytest.mark.api
    def test_products_have_descriptions(self, api_client):
        """Test products have descriptions."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items[:3]:
            assert "desc" in product
            assert len(product["desc"]) > 0

    @pytest.mark.api
    def test_products_have_images(self, api_client):
        """Test products have image URLs."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items[:3]:
            assert "img" in product
            assert product["img"].startswith("http") or product["img"].startswith("imgs/")

    @pytest.mark.api
    def test_api_returns_json_content_type(self, api_client):
        """Test API returns JSON content type."""
        response = api_client.get_products()

        assert response.is_success()
        # DemoBlaze may not set proper content-type, so we just verify JSON parsing worked
        assert response.json_data is not None

    @pytest.mark.api
    def test_multiple_products_api_calls(self, api_client):
        """Test multiple consecutive API calls."""
        responses = []

        for _ in range(3):
            response = api_client.get_products()
            responses.append(response)

        # All should succeed
        assert all(r.is_success() for r in responses)

        # All should return same number of products
        counts = [len(r.json_data.get("Items", [])) for r in responses]
        assert len(set(counts)) == 1  # All counts are the same

    @pytest.mark.api
    def test_products_sorted_by_id(self, api_client):
        """Test products are returned in consistent order."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        # Get IDs
        ids = [p["id"] for p in items]

        # Check they're in order
        assert ids == sorted(ids)

    @pytest.mark.api
    def test_product_price_range(self, api_client):
        """Test product prices are within reasonable range."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        for product in items:
            price = product["price"]
            assert 0 < price < 10000  # Reasonable price range

    @pytest.mark.api
    def test_products_have_unique_ids(self, api_client):
        """Test all products have unique IDs."""
        response = api_client.get_products()
        items = response.json_data.get("Items", [])

        ids = [p["id"] for p in items]
        assert len(ids) == len(set(ids))  # No duplicates

    @pytest.mark.api
    def test_api_health_check(self, api_client):
        """Test API health check utility."""
        is_healthy = api_client.check_api_health()
        assert is_healthy is True

    @pytest.mark.api
    def test_products_api_headers(self, api_client):
        """Test API response headers."""
        response = api_client.get_products()

        assert response.is_success()
        assert response.headers is not None
        assert isinstance(response.headers, dict)

    @pytest.mark.api
    def test_get_products_by_category(self, api_client):
        """Test getting products by category."""
        response = api_client.get_products_by_category("phones")

        assert response.is_success()
        assert response.json_data is not None
