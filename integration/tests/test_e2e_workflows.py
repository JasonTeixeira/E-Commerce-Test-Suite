"""
End-to-end integration workflow tests.

Tests complete user journeys from browsing to checkout,
simulating real user interactions across multiple pages.
"""

import pytest
from playwright.sync_api import Page

from ui_tests.pages.cart_page import CartPage
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.product_detail_page import ProductDetailPage


class TestCompleteShoppingWorkflow:
    """Test suite for complete shopping workflows."""

    @pytest.mark.smoke
    @pytest.mark.integration
    @pytest.mark.critical
    def test_browse_add_to_cart_checkout_flow(self, page: Page):
        """Test complete flow: browse → add to cart → checkout."""
        # Browse products
        home = HomePage(page).open()
        assert home.verify_on_homepage()

        # View product
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_name = product_detail.get_product_name()
        assert product_detail.is_on_product_detail_page()

        # Add to cart
        product_detail.add_to_cart_and_accept_alert()

        # Go to cart
        cart = CartPage(page).open()
        assert cart.is_on_cart_page()
        assert cart.is_product_in_cart(product_name)

        # Place order
        cart.click_place_order()
        assert cart.is_order_modal_open()

    @pytest.mark.integration
    def test_multi_product_shopping_journey(self, page: Page):
        """Test adding multiple products and completing checkout."""
        home = HomePage(page).open()

        # Add first product
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        first_product = product_detail.get_product_name()
        product_detail.add_to_cart_and_accept_alert()

        # Add second product
        product_detail.go_to_home()
        home.click_product_by_index(1)
        second_product = product_detail.get_product_name()
        product_detail.add_to_cart_and_accept_alert()

        # Verify both in cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 2
        assert cart.is_product_in_cart(first_product)
        assert cart.is_product_in_cart(second_product)

    @pytest.mark.integration
    def test_category_filter_to_purchase(self, page: Page):
        """Test filtering by category then purchasing."""
        home = HomePage(page).open()

        # Filter by category
        home.filter_by_laptops()
        assert home.get_product_count() > 0

        # Select product from filtered results
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Navigate to cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 1

    @pytest.mark.integration
    def test_navigation_across_all_pages(self, page: Page):
        """Test navigating through all main pages."""
        # Start at home
        home = HomePage(page).open()
        assert home.verify_on_homepage()

        # Go to product detail
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        assert product_detail.is_on_product_detail_page()

        # Add to cart and navigate
        product_detail.add_to_cart_and_accept_alert()
        cart = CartPage(page).open()
        assert cart.is_on_cart_page()

        # Return home
        cart.continue_shopping()
        assert home.verify_on_homepage()


class TestProductBrowsingWorkflows:
    """Test suite for product browsing workflows."""

    @pytest.mark.integration
    @pytest.mark.products
    def test_browse_multiple_products_sequentially(self, page: Page):
        """Test viewing multiple products one after another."""
        home = HomePage(page).open()
        product_names = []

        # View 3 different products
        for i in range(3):
            home.click_product_by_index(i)
            product_detail = ProductDetailPage(page)
            product_name = product_detail.get_product_name()
            product_names.append(product_name)
            product_detail.go_to_home()

        # Verify all products were different
        assert len(set(product_names)) == 3

    @pytest.mark.integration
    @pytest.mark.products
    def test_filter_and_browse_workflow(self, page: Page):
        """Test filtering categories and browsing products."""
        home = HomePage(page).open()

        # Filter by phones
        home.filter_by_phones()
        phone_count = home.get_product_count()

        # Filter by laptops
        home.filter_by_laptops()
        laptop_count = home.get_product_count()

        # Both categories should have products
        assert phone_count > 0
        assert laptop_count > 0

    @pytest.mark.integration
    @pytest.mark.products
    def test_pagination_and_product_viewing(self, page: Page):
        """Test paginating through products and viewing details."""
        home = HomePage(page).open()

        # Get product from first page
        first_page_products = home.get_product_titles()

        # Navigate to next page
        if home.is_next_button_enabled():
            home.click_next_page()
            second_page_products = home.get_product_titles()

            # Verify different products on different pages
            assert first_page_products != second_page_products


class TestCartManagementWorkflows:
    """Test suite for cart management workflows."""

    @pytest.mark.integration
    @pytest.mark.cart
    def test_add_remove_add_workflow(self, page: Page):
        """Test adding item, removing it, then adding again."""
        # Add product
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_name = product_detail.get_product_name()
        product_detail.add_to_cart_and_accept_alert()

        # Remove from cart
        cart = CartPage(page).open()
        assert cart.is_product_in_cart(product_name)
        cart.remove_item_by_index(0)
        assert cart.is_cart_empty()

        # Add again
        cart.continue_shopping()
        home.click_product_by_index(0)
        product_detail.add_to_cart_and_accept_alert()

        # Verify in cart
        cart.open()
        assert cart.get_cart_item_count() == 1

    @pytest.mark.integration
    @pytest.mark.cart
    def test_build_cart_incrementally(self, page: Page):
        """Test building cart by adding products one at a time."""
        home = HomePage(page).open()
        expected_count = 0

        # Add 3 products incrementally
        for i in range(3):
            home.click_product_by_index(i)
            product_detail = ProductDetailPage(page)
            product_detail.add_to_cart_and_accept_alert()
            expected_count += 1

            # Check cart after each addition
            cart = CartPage(page).open()
            assert cart.get_cart_item_count() == expected_count

            # Continue shopping
            cart.continue_shopping()

    @pytest.mark.integration
    @pytest.mark.cart
    def test_empty_cart_workflow(self, page: Page):
        """Test completely emptying a cart with multiple items."""
        home = HomePage(page).open()

        # Add multiple products
        for i in range(2):
            home.click_product_by_index(i)
            product_detail = ProductDetailPage(page)
            product_detail.add_to_cart_and_accept_alert()
            product_detail.go_to_home()

        # Empty cart
        cart = CartPage(page).open()
        initial_count = cart.get_cart_item_count()
        assert initial_count == 2

        cart.remove_all_items()
        assert cart.is_cart_empty()


class TestCategoryBasedWorkflows:
    """Test suite for category-based shopping workflows."""

    @pytest.mark.integration
    @pytest.mark.products
    def test_shop_phones_category(self, page: Page):
        """Test complete workflow for phones category."""
        home = HomePage(page).open()

        # Filter by phones
        home.filter_by_phones()
        assert home.get_product_count() > 0

        # Select and purchase phone
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Verify in cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 1

    @pytest.mark.integration
    @pytest.mark.products
    def test_shop_laptops_category(self, page: Page):
        """Test complete workflow for laptops category."""
        home = HomePage(page).open()

        # Filter by laptops
        home.filter_by_laptops()
        assert home.get_product_count() > 0

        # Select and purchase laptop
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Verify in cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 1

    @pytest.mark.integration
    @pytest.mark.products
    def test_mixed_category_shopping(self, page: Page):
        """Test shopping across multiple categories."""
        home = HomePage(page).open()

        # Buy from phones
        home.filter_by_phones()
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        product_detail.add_to_cart_and_accept_alert()

        # Buy from laptops
        product_detail.go_to_home()
        home.filter_by_laptops()
        home.click_product_by_index(0)
        product_detail.add_to_cart_and_accept_alert()

        # Verify mixed cart
        cart = CartPage(page).open()
        assert cart.get_cart_item_count() == 2


class TestPriceVerificationWorkflows:
    """Test suite for price verification workflows."""

    @pytest.mark.integration
    @pytest.mark.cart
    def test_price_consistency_product_to_cart(self, page: Page):
        """Test price remains consistent from product page to cart."""
        # Get price from product page
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_price = product_detail.get_product_price_value()
        product_detail.add_to_cart_and_accept_alert()

        # Get price from cart
        cart = CartPage(page).open()
        cart_prices = cart.get_cart_item_prices()

        # Verify price matches
        assert len(cart_prices) == 1
        assert float(cart_prices[0]) == product_price

    @pytest.mark.integration
    @pytest.mark.cart
    @pytest.mark.slow
    def test_total_calculation_workflow(self, page: Page):
        """Test cart total calculation with multiple items."""
        home = HomePage(page).open()
        prices = []

        # Add 2 products and track prices
        for i in range(2):
            home.click_product_by_index(i)
            product_detail = ProductDetailPage(page)
            price = product_detail.get_product_price_value()
            prices.append(price)
            product_detail.add_to_cart_and_accept_alert()
            product_detail.go_to_home()

        # Verify cart total
        cart = CartPage(page).open()
        cart_total = cart.get_total_price_value()
        expected_total = sum(prices)

        assert cart_total == expected_total
