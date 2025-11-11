"""
Shopping cart tests for DemoBlaze.

Tests cart functionality including adding/removing items,
price calculations, and checkout process.
"""

import pytest
from playwright.sync_api import Page

from ui_tests.pages.cart_page import CartPage
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.product_detail_page import ProductDetailPage


class TestCartPage:
    """Test suite for cart page basic functionality."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.cart
    def test_navigate_to_cart(self, page: Page):
        """Test navigating to cart page."""
        home = HomePage(page).open()
        home.goto_cart()

        cart = CartPage(page)
        assert cart.is_on_cart_page()

    @pytest.mark.ui
    @pytest.mark.cart
    def test_empty_cart_displays(self, page: Page):
        """Test empty cart page displays correctly."""
        cart = CartPage(page).open()
        assert cart.is_on_cart_page()

    @pytest.mark.ui
    @pytest.mark.cart
    def test_place_order_button_visible(self, page: Page):
        """Test place order button is visible on cart page."""
        cart = CartPage(page).open()
        assert cart.is_place_order_button_visible()


class TestAddToCart:
    """Test suite for adding items to cart."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.cart
    def test_add_single_item_to_cart(self, page: Page):
        """Test adding a single item to cart."""
        # Add product to cart
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_name = product_detail.get_product_name()
        product_detail.add_to_cart_and_accept_alert()

        # Verify in cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 1
        assert cart.is_product_in_cart(product_name)

    @pytest.mark.ui
    @pytest.mark.cart
    def test_add_multiple_items_to_cart(self, page: Page):
        """Test adding multiple different items to cart."""
        home = HomePage(page).open()

        # Add first product
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Add second product
        product_detail.go_to_home()
        home.click_product_by_index(1)
        product_detail.add_to_cart_and_accept_alert()

        # Verify cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 2

    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_preserves_items_across_navigation(self, page: Page):
        """Test cart items persist when navigating away."""
        # Add item
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_name = product_detail.get_product_name()
        product_detail.add_to_cart_and_accept_alert()

        # Navigate away and back
        product_detail.go_to_home()
        cart = CartPage(page).open()

        # Verify item still in cart
        assert cart.get_cart_item_count() == 1
        assert cart.is_product_in_cart(product_name)


class TestCartItems:
    """Test suite for cart item display and management."""

    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_shows_product_titles(self, page: Page):
        """Test cart displays product titles."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        titles = cart.get_cart_item_titles()

        assert len(titles) > 0
        assert all(len(title) > 0 for title in titles)

    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_shows_product_prices(self, page: Page):
        """Test cart displays product prices."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        prices = cart.get_cart_item_prices()

        assert len(prices) > 0
        assert all(len(price) > 0 for price in prices)

    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_item_count_matches_items(self, page: Page):
        """Test cart item count matches actual items."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        count = cart.get_cart_item_count()
        titles = cart.get_cart_item_titles()

        assert count == len(titles)


class TestRemoveFromCart:
    """Test suite for removing items from cart."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.cart
    def test_remove_single_item_from_cart(self, page: Page):
        """Test removing a single item from cart."""
        # Add item
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Remove item
        cart = CartPage(page).open()
        initial_count = cart.get_cart_item_count()
        cart.remove_item_by_index(0)

        assert cart.get_cart_item_count() == initial_count - 1

    @pytest.mark.ui
    @pytest.mark.cart
    def test_remove_multiple_items(self, page: Page):
        """Test removing multiple items from cart."""
        # Add multiple items
        home = HomePage(page).open()

        for i in range(2):
            home.click_product_by_index(i)
            product_detail = ProductDetailPage(page)
            product_detail.add_to_cart_and_accept_alert()
            product_detail.go_to_home()

        # Remove all items
        cart = CartPage(page).open()
        cart.remove_all_items()

        assert cart.is_cart_empty()

    @pytest.mark.ui
    @pytest.mark.cart
    def test_cart_empty_after_removal(self, page: Page):
        """Test cart shows as empty after removing all items."""
        # Add and remove
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        cart.remove_all_items()

        assert cart.is_cart_empty()
        assert cart.get_cart_item_count() == 0


class TestCartPricing:
    """Test suite for cart price calculations."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.cart
    def test_cart_displays_total_price(self, page: Page):
        """Test cart displays total price."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        total = cart.get_total_price_text()

        assert total is not None
        assert len(total) > 0

    @pytest.mark.ui
    @pytest.mark.cart
    def test_total_price_is_numeric(self, page: Page):
        """Test total price can be parsed as number."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        total_value = cart.get_total_price_value()

        assert isinstance(total_value, float)
        assert total_value > 0

    @pytest.mark.ui
    @pytest.mark.cart
    def test_total_updates_after_adding_items(self, page: Page):
        """Test total price updates when adding items."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        initial_total = cart.get_total_price_value()

        # Add another item
        cart.continue_shopping()
        home.click_product_by_index(1)
        product_detail.add_to_cart_and_accept_alert()

        cart.open()
        new_total = cart.get_total_price_value()

        assert new_total > initial_total


class TestPlaceOrder:
    """Test suite for place order functionality."""

    @pytest.mark.ui
    @pytest.mark.cart
    @pytest.mark.checkout
    def test_place_order_opens_modal(self, page: Page):
        """Test place order button opens order modal."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        cart.click_place_order()

        assert cart.is_order_modal_open()

    @pytest.mark.ui
    @pytest.mark.cart
    @pytest.mark.checkout
    def test_order_modal_has_form_fields(self, page: Page):
        """Test order modal displays all form fields."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        cart.click_place_order()

        assert cart.is_visible(cart.ORDER_NAME_INPUT)
        assert cart.is_visible(cart.ORDER_COUNTRY_INPUT)
        assert cart.is_visible(cart.ORDER_CITY_INPUT)
        assert cart.is_visible(cart.ORDER_CARD_INPUT)
        assert cart.is_visible(cart.ORDER_MONTH_INPUT)
        assert cart.is_visible(cart.ORDER_YEAR_INPUT)

    @pytest.mark.ui
    @pytest.mark.cart
    @pytest.mark.checkout
    def test_close_order_modal(self, page: Page):
        """Test closing order modal."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        cart = CartPage(page).open()
        cart.click_place_order()
        assert cart.is_order_modal_open()

        cart.close_order_modal()
        assert not cart.is_order_modal_open()


class TestCartNavigation:
    """Test suite for cart page navigation."""

    @pytest.mark.ui
    @pytest.mark.cart
    def test_continue_shopping_from_cart(self, page: Page):
        """Test continue shopping returns to homepage."""
        cart = CartPage(page).open()
        cart.continue_shopping()

        home = HomePage(page)
        assert home.verify_on_homepage()
