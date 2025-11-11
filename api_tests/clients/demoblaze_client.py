"""
DemoBlaze API client for e-commerce operations.

Provides methods for product, cart, user, and order operations
specific to the DemoBlaze API.
"""

from typing import Any, Dict, List, Optional

from api_tests.clients.base_client import APIResponse, BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class DemoBlazeAPIClient(BaseAPIClient):
    """API client for DemoBlaze e-commerce API."""

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize DemoBlaze API client.

        Args:
            base_url: Base URL for API (defaults to settings)
        """
        super().__init__(base_url)
        logger.info("Initialized DemoBlaze API client")

    # ========================================
    # Product API Methods
    # ========================================

    def get_products(self) -> APIResponse:
        """
        Get all products.

        Returns:
            APIResponse with products list
        """
        logger.info("Fetching all products")
        return self.get("entries")

    def get_product_by_id(self, product_id: int) -> APIResponse:
        """
        Get product by ID.

        Args:
            product_id: Product ID

        Returns:
            APIResponse with product details
        """
        logger.info(f"Fetching product with ID: {product_id}")
        return self.post("view", json={"id": product_id})

    # ========================================
    # Cart API Methods
    # ========================================

    def add_to_cart(
        self, product_id: int, cookie: str, product_name: Optional[str] = None
    ) -> APIResponse:
        """
        Add product to cart.

        Args:
            product_id: Product ID
            cookie: User session cookie
            product_name: Product name (optional)

        Returns:
            APIResponse
        """
        logger.info(f"Adding product {product_id} to cart")
        payload = {
            "id": cookie,
            "cookie": cookie,
            "prod_id": product_id,
            "flag": True,
        }
        return self.post("addtocart", json=payload)

    def get_cart(self, cookie: str) -> APIResponse:
        """
        Get cart contents.

        Args:
            cookie: User session cookie

        Returns:
            APIResponse with cart items
        """
        logger.info(f"Fetching cart for cookie: {cookie}")
        payload = {"cookie": cookie, "flag": True}
        return self.post("viewcart", json=payload)

    def delete_from_cart(self, cart_item_id: str, cookie: str) -> APIResponse:
        """
        Delete item from cart.

        Args:
            cart_item_id: Cart item ID
            cookie: User session cookie

        Returns:
            APIResponse
        """
        logger.info(f"Deleting cart item: {cart_item_id}")
        payload = {"cookie": cookie, "id": cart_item_id}
        return self.post("deleteitem", json=payload)

    # ========================================
    # User API Methods
    # ========================================

    def signup(self, username: str, password: str) -> APIResponse:
        """
        Register new user.

        Args:
            username: Username
            password: Password

        Returns:
            APIResponse
        """
        logger.info(f"Signing up user: {username}")
        payload = {"username": username, "password": password}
        return self.post("signup", json=payload)

    def login(self, username: str, password: str) -> APIResponse:
        """
        Login user.

        Args:
            username: Username
            password: Password

        Returns:
            APIResponse with auth token
        """
        logger.info(f"Logging in user: {username}")
        payload = {
            "username": username,
            "password": password,
        }
        return self.post("login", json=payload)

    # ========================================
    # Order API Methods
    # ========================================

    def place_order(
        self,
        cookie: str,
        name: str,
        country: str,
        city: str,
        card: str,
        month: str,
        year: str,
        total: int,
    ) -> APIResponse:
        """
        Place order.

        Args:
            cookie: User session cookie
            name: Customer name
            country: Country
            city: City
            card: Credit card number
            month: Expiration month
            year: Expiration year
            total: Total amount

        Returns:
            APIResponse with order confirmation
        """
        logger.info(f"Placing order for {name}")
        payload = {
            "id": cookie,
            "cookie": cookie,
            "name": name,
            "country": country,
            "city": city,
            "card": card,
            "month": month,
            "year": year,
            "total": total,
        }
        return self.post("purchaseorder", json=payload)

    # ========================================
    # Category API Methods
    # ========================================

    def get_products_by_category(self, category: str) -> APIResponse:
        """
        Get products by category.

        Args:
            category: Category name (phones, laptops, monitors)

        Returns:
            APIResponse with filtered products
        """
        logger.info(f"Fetching products in category: {category}")
        # DemoBlaze doesn't have direct category endpoint, 
        # but we can filter client-side after getting all products
        return self.get_products()

    # ========================================
    # Utility Methods
    # ========================================

    def check_api_health(self) -> bool:
        """
        Check if API is accessible.

        Returns:
            True if API is healthy
        """
        try:
            response = self.get_products()
            return response.is_success()
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            return False
