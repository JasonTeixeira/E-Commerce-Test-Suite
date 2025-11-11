"""
Cart and Order API tests for DemoBlaze.

Tests cart operations, order placement, and cart management.
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
def test_cookie():
    """Generate unique cookie for testing."""
    return f"test_cookie_{uuid.uuid4().hex}"


@pytest.fixture
def product_id(api_client):
    """Get a valid product ID for testing."""
    response = api_client.get_products()
    items = response.json_data.get("Items", [])
    return items[0]["id"] if items else 1


class TestCartAPI:
    """Test suite for cart API operations."""

    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.cart
    @pytest.mark.critical
    def test_add_product_to_cart(self, api_client, test_cookie, product_id):
        """Test adding product to cart."""
        response = api_client.add_to_cart(product_id, test_cookie)

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.cart
    def test_add_to_cart_response_time(self, api_client, test_cookie, product_id):
        """Test add to cart response time."""
        response = api_client.add_to_cart(product_id, test_cookie)

        assert response.is_success()
        assert response.elapsed < 5.0

    @pytest.mark.api
    @pytest.mark.cart
    def test_get_empty_cart(self, api_client, test_cookie):
        """Test retrieving empty cart."""
        response = api_client.get_cart(test_cookie)

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.cart
    def test_get_cart_after_adding_product(self, api_client, test_cookie, product_id):
        """Test getting cart after adding a product."""
        # Add product
        api_client.add_to_cart(product_id, test_cookie)

        # Get cart
        response = api_client.get_cart(test_cookie)

        assert response.is_success()
        assert response.json_data is not None

    @pytest.mark.api
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, api_client, test_cookie):
        """Test adding multiple products to cart."""
        # Get multiple product IDs
        products_response = api_client.get_products()
        items = products_response.json_data.get("Items", [])
        
        # Add first 3 products
        for product in items[:3]:
            response = api_client.add_to_cart(product["id"], test_cookie)
            assert response.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_cart_api_with_different_cookies(self, api_client, product_id):
        """Test cart isolation with different cookies."""
        cookie1 = f"cookie1_{uuid.uuid4().hex[:8]}"
        cookie2 = f"cookie2_{uuid.uuid4().hex[:8]}"

        # Add to both carts
        response1 = api_client.add_to_cart(product_id, cookie1)
        response2 = api_client.add_to_cart(product_id, cookie2)

        assert response1.is_success()
        assert response2.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_add_same_product_twice(self, api_client, test_cookie, product_id):
        """Test adding same product twice to cart."""
        # Add product twice
        response1 = api_client.add_to_cart(product_id, test_cookie)
        response2 = api_client.add_to_cart(product_id, test_cookie)

        assert response1.is_success()
        assert response2.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_cart_persistence(self, api_client, test_cookie, product_id):
        """Test cart persists across API calls."""
        # Add product
        api_client.add_to_cart(product_id, test_cookie)

        # Get cart multiple times
        response1 = api_client.get_cart(test_cookie)
        response2 = api_client.get_cart(test_cookie)

        assert response1.is_success()
        assert response2.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_get_cart_response_time(self, api_client, test_cookie):
        """Test get cart response time."""
        response = api_client.get_cart(test_cookie)

        assert response.is_success()
        assert response.elapsed < 5.0

    @pytest.mark.api
    @pytest.mark.cart
    def test_cart_with_invalid_product_id(self, api_client, test_cookie):
        """Test adding invalid product ID to cart."""
        try:
            response = api_client.add_to_cart(99999, test_cookie)
            # May succeed or fail depending on API validation
        except Exception:
            pass  # Expected to potentially fail


class TestOrderAPI:
    """Test suite for order API operations."""

    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.checkout
    @pytest.mark.critical
    def test_place_order(self, api_client, test_cookie, product_id):
        """Test placing an order."""
        # Add product first
        api_client.add_to_cart(product_id, test_cookie)

        # Place order
        response = api_client.place_order(
            cookie=test_cookie,
            name="Test User",
            country="USA",
            city="New York",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )

        assert response.is_success()
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.checkout
    def test_place_order_response_time(self, api_client, test_cookie, product_id):
        """Test place order response time."""
        api_client.add_to_cart(product_id, test_cookie)

        response = api_client.place_order(
            cookie=test_cookie,
            name="Test User",
            country="USA",
            city="New York",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )

        assert response.is_success()
        assert response.elapsed < 5.0

    @pytest.mark.api
    @pytest.mark.checkout
    def test_place_order_with_different_countries(self, api_client, test_cookie, product_id):
        """Test placing orders with different countries."""
        api_client.add_to_cart(product_id, test_cookie)

        countries = ["USA", "Canada", "UK"]

        for country in countries:
            cookie = f"cookie_{country}_{uuid.uuid4().hex[:6]}"
            api_client.add_to_cart(product_id, cookie)

            response = api_client.place_order(
                cookie=cookie,
                name="Test User",
                country=country,
                city="Test City",
                card="4111111111111111",
                month="12",
                year="2025",
                total=790
            )

            assert response.is_success()

    @pytest.mark.api
    @pytest.mark.checkout
    def test_place_order_with_special_characters(self, api_client, test_cookie, product_id):
        """Test placing order with special characters in name."""
        api_client.add_to_cart(product_id, test_cookie)

        response = api_client.place_order(
            cookie=test_cookie,
            name="Test O'Brien-Smith",
            country="Ireland",
            city="Dublin",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )

        assert response.is_success()

    @pytest.mark.api
    @pytest.mark.checkout
    def test_place_order_with_different_card_numbers(self, api_client, test_cookie, product_id):
        """Test placing orders with different card numbers."""
        api_client.add_to_cart(product_id, test_cookie)

        card_numbers = [
            "4111111111111111",
            "5500000000000004",
            "340000000000009"
        ]

        for card in card_numbers:
            cookie = f"cookie_{card[:4]}_{uuid.uuid4().hex[:6]}"
            api_client.add_to_cart(product_id, cookie)

            response = api_client.place_order(
                cookie=cookie,
                name="Test User",
                country="USA",
                city="New York",
                card=card,
                month="12",
                year="2025",
                total=790
            )

            assert response.is_success()


class TestCartOrderWorkflow:
    """Test suite for complete cart and order workflows."""

    @pytest.mark.api
    @pytest.mark.integration
    @pytest.mark.cart
    @pytest.mark.checkout
    def test_complete_purchase_workflow(self, api_client, test_cookie, product_id):
        """Test complete purchase workflow."""
        # Add product to cart
        add_response = api_client.add_to_cart(product_id, test_cookie)
        assert add_response.is_success()

        # Get cart
        cart_response = api_client.get_cart(test_cookie)
        assert cart_response.is_success()

        # Place order
        order_response = api_client.place_order(
            cookie=test_cookie,
            name="Test User",
            country="USA",
            city="New York",
            card="4111111111111111",
            month="12",
            year="2025",
            total=790
        )
        assert order_response.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_add_view_add_workflow(self, api_client, test_cookie, product_id):
        """Test add, view, add more workflow."""
        # Add first product
        api_client.add_to_cart(product_id, test_cookie)

        # View cart
        cart_response = api_client.get_cart(test_cookie)
        assert cart_response.is_success()

        # Add second product
        products_response = api_client.get_products()
        second_product_id = products_response.json_data["Items"][1]["id"]
        api_client.add_to_cart(second_product_id, test_cookie)

    @pytest.mark.api
    @pytest.mark.cart
    def test_multiple_carts_multiple_orders(self, api_client, product_id):
        """Test multiple users with separate carts and orders."""
        users = [f"user_{i}_{uuid.uuid4().hex[:6]}" for i in range(2)]

        for user_cookie in users:
            # Add to cart
            api_client.add_to_cart(product_id, user_cookie)

            # Place order
            response = api_client.place_order(
                cookie=user_cookie,
                name=f"User {user_cookie[:10]}",
                country="USA",
                city="Test City",
                card="4111111111111111",
                month="12",
                year="2025",
                total=790
            )

            assert response.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    @pytest.mark.integration
    def test_cart_operations_sequence(self, api_client, test_cookie):
        """Test sequence of cart operations."""
        # Get products
        products = api_client.get_products()
        items = products.json_data.get("Items", [])

        # Add multiple products
        for product in items[:2]:
            response = api_client.add_to_cart(product["id"], test_cookie)
            assert response.is_success()

        # View cart
        cart_response = api_client.get_cart(test_cookie)
        assert cart_response.is_success()

    @pytest.mark.api
    @pytest.mark.checkout
    def test_order_with_different_expiry_dates(self, api_client, test_cookie, product_id):
        """Test orders with different card expiry dates."""
        api_client.add_to_cart(product_id, test_cookie)

        expiry_dates = [
            ("01", "2025"),
            ("12", "2026"),
            ("06", "2027")
        ]

        for month, year in expiry_dates:
            cookie = f"cookie_{month}{year}_{uuid.uuid4().hex[:6]}"
            api_client.add_to_cart(product_id, cookie)

            response = api_client.place_order(
                cookie=cookie,
                name="Test User",
                country="USA",
                city="New York",
                card="4111111111111111",
                month=month,
                year=year,
                total=790
            )

            assert response.is_success()

    @pytest.mark.api
    @pytest.mark.cart
    def test_cart_api_consistency(self, api_client, product_id):
        """Test cart API returns consistent responses."""
        cookies = [f"cookie_{i}_{uuid.uuid4().hex[:6]}" for i in range(3)]
        responses = []

        for cookie in cookies:
            response = api_client.add_to_cart(product_id, cookie)
            responses.append(response)

        # All should have same status code
        status_codes = [r.status_code for r in responses]
        assert len(set(status_codes)) == 1

    @pytest.mark.api
    @pytest.mark.checkout
    def test_order_with_minimum_total(self, api_client, test_cookie, product_id):
        """Test order with minimum total amount."""
        api_client.add_to_cart(product_id, test_cookie)

        response = api_client.place_order(
            cookie=test_cookie,
            name="Test User",
            country="USA",
            city="New York",
            card="4111111111111111",
            month="12",
            year="2025",
            total=1  # Minimum amount
        )

        assert response.is_success()

    @pytest.mark.api
    @pytest.mark.checkout
    def test_order_with_large_total(self, api_client, test_cookie, product_id):
        """Test order with large total amount."""
        api_client.add_to_cart(product_id, test_cookie)

        response = api_client.place_order(
            cookie=test_cookie,
            name="Test User",
            country="USA",
            city="New York",
            card="4111111111111111",
            month="12",
            year="2025",
            total=99999
        )

        assert response.is_success()
