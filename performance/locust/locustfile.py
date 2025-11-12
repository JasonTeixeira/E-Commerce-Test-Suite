"""
Locust performance test suite for DemoBlaze.

Load testing scenarios covering homepage, products, cart,
and complete user workflows under various load conditions.
"""

import random
import uuid
from locust import HttpUser, TaskSet, between, task

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowsingBehavior(TaskSet):
    """User behavior for browsing products."""

    @task(5)
    def view_homepage(self):
        """Load homepage."""
        with self.client.get("/", catch_response=True, name="Homepage") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def view_products_api(self):
        """Get products via API."""
        with self.client.post(
            "/entries",
            catch_response=True,
            name="Get Products API"
        ) as response:
            if response.status_code == 200 and "Items" in response.text:
                response.success()
            else:
                response.failure("Failed to get products")

    @task(2)
    def view_product_detail(self):
        """View product detail page."""
        product_id = random.randint(1, 9)
        with self.client.get(
            f"/prod.html?idp_={product_id}",
            catch_response=True,
            name="Product Detail"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Product {product_id} failed")


class ShoppingBehavior(TaskSet):
    """User behavior for shopping and checkout."""

    def on_start(self):
        """Initialize shopping session."""
        self.cookie = f"locust_{uuid.uuid4().hex}"
        self.cart_items = []

    @task(4)
    def add_to_cart(self):
        """Add product to cart via API."""
        product_id = random.randint(1, 9)
        
        payload = {
            "id": self.cookie,
            "cookie": self.cookie,
            "prod_id": product_id,
            "flag": True
        }

        with self.client.post(
            "/addtocart",
            json=payload,
            catch_response=True,
            name="Add to Cart"
        ) as response:
            if response.status_code == 200:
                self.cart_items.append(product_id)
                response.success()
            else:
                response.failure("Failed to add to cart")

    @task(2)
    def view_cart(self):
        """View shopping cart."""
        with self.client.get(
            "/cart.html",
            catch_response=True,
            name="View Cart"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failed to load cart")

    @task(2)
    def get_cart_api(self):
        """Get cart contents via API."""
        payload = {"cookie": self.cookie, "flag": True}

        with self.client.post(
            "/viewcart",
            json=payload,
            catch_response=True,
            name="Get Cart API"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failed to get cart")

    @task(1)
    def place_order(self):
        """Place order via API."""
        if not self.cart_items:
            return

        payload = {
            "id": self.cookie,
            "cookie": self.cookie,
            "name": "Locust User",
            "country": "USA",
            "city": "Test City",
            "card": "4111111111111111",
            "month": "12",
            "year": "2025",
            "total": 790
        }

        with self.client.post(
            "/purchaseorder",
            json=payload,
            catch_response=True,
            name="Place Order"
        ) as response:
            if response.status_code == 200:
                response.success()
                self.cart_items = []
            else:
                response.failure("Failed to place order")


class AuthenticationBehavior(TaskSet):
    """User behavior for authentication."""

    @task(2)
    def signup(self):
        """Signup new user via API."""
        username = f"user_{uuid.uuid4().hex[:8]}"
        payload = {
            "username": username,
            "password": "TestPassword123"
        }

        with self.client.post(
            "/signup",
            json=payload,
            catch_response=True,
            name="Signup"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Signup failed")

    @task(3)
    def login_existing(self):
        """Login with predefined test user."""
        payload = {
            "username": settings.test_user_email,
            "password": settings.test_user_password
        }

        with self.client.post(
            "/login",
            json=payload,
            catch_response=True,
            name="Login"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Login failed")


class DemoBlazeUser(HttpUser):
    """
    Simulated user for DemoBlaze e-commerce site.
    
    Represents a typical user with mixed behavior patterns.
    """
    
    host = settings.base_url
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    tasks = {
        BrowsingBehavior: 5,      # 50% browsing
        ShoppingBehavior: 3,       # 30% shopping
        AuthenticationBehavior: 2  # 20% auth
    }


class BrowsingUser(HttpUser):
    """User that only browses products."""
    
    host = settings.base_url
    wait_time = between(0.5, 2)
    tasks = [BrowsingBehavior]


class ShoppingUser(HttpUser):
    """User that actively shops and completes purchases."""
    
    host = settings.base_url
    wait_time = between(1, 4)
    tasks = [ShoppingBehavior]


class FastUser(HttpUser):
    """User with minimal wait time (stress testing)."""
    
    host = settings.base_url
    wait_time = between(0.1, 0.5)
    tasks = [BrowsingBehavior]


class RealisticUser(HttpUser):
    """User with realistic browsing patterns and delays."""
    
    host = settings.base_url
    wait_time = between(3, 8)
    tasks = {
        BrowsingBehavior: 6,
        ShoppingBehavior: 3,
        AuthenticationBehavior: 1
    }
