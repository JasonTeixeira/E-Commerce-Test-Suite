"""
Product detail page tests for DemoBlaze.

Tests product information display, add to cart functionality,
and product page interactions.
"""

import pytest
from playwright.sync_api import Page

from ui_tests.pages.home_page import HomePage
from ui_tests.pages.product_detail_page import ProductDetailPage


class TestProductDetailPage:
    """Test suite for product detail page display."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.products
    def test_product_detail_page_loads(self, page: Page):
        """Test product detail page loads successfully."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_on_product_detail_page()

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_name_is_displayed(self, page: Page):
        """Test product name is displayed on detail page."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_name = product_detail.get_product_name()

        assert product_name is not None
        assert len(product_name) > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_price_is_displayed(self, page: Page):
        """Test product price is displayed on detail page."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        product_price = product_detail.get_product_price()

        assert product_price is not None
        assert len(product_price) > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_description_is_displayed(self, page: Page):
        """Test product description is displayed on detail page."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        description = product_detail.get_product_description()

        assert description is not None
        assert len(description) > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_image_is_visible(self, page: Page):
        """Test product image is visible on detail page."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_product_image_visible()

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_image_has_src(self, page: Page):
        """Test product image has valid source URL."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        image_src = product_detail.get_product_image_src()

        assert image_src is not None
        assert len(image_src) > 0
        assert image_src.startswith("http")

    @pytest.mark.ui
    @pytest.mark.products
    def test_all_product_information_present(self, page: Page):
        """Test all product information elements are present."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.has_product_information()


class TestProductPricing:
    """Test suite for product pricing."""

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_price_format(self, page: Page):
        """Test product price has correct format with $ symbol."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.verify_product_price_format()

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_price_is_positive(self, page: Page):
        """Test product price is a positive number."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.verify_product_price_is_positive()

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_price_value_extraction(self, page: Page):
        """Test extracting numeric price value."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        price_value = product_detail.get_product_price_value()

        assert isinstance(price_value, float)
        assert price_value > 0
        assert price_value < 10000  # Reasonable max price


class TestAddToCart:
    """Test suite for add to cart functionality."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.cart
    def test_add_to_cart_button_visible(self, page: Page):
        """Test add to cart button is visible on product detail page."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_add_to_cart_button_visible()

    @pytest.mark.ui
    @pytest.mark.cart
    def test_click_add_to_cart_button(self, page: Page):
        """Test clicking add to cart button."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        alert_text = product_detail.add_to_cart_and_get_alert_text()

        assert alert_text is not None
        assert len(alert_text) > 0

    @pytest.mark.ui
    @pytest.mark.cart
    def test_add_to_cart_success_message(self, page: Page):
        """Test successful add to cart shows success message."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        alert_text = product_detail.add_to_cart_and_get_alert_text()

        assert "added" in alert_text.lower() or "success" in alert_text.lower()


class TestProductNavigation:
    """Test suite for navigation on product detail page."""

    @pytest.mark.ui
    @pytest.mark.products
    def test_navigate_back_to_home(self, page: Page):
        """Test navigating back to homepage from product detail."""
        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_on_product_detail_page()

        product_detail.go_to_home()
        assert home.verify_on_homepage()

    @pytest.mark.ui
    @pytest.mark.products
    def test_multiple_product_views(self, page: Page):
        """Test viewing multiple products sequentially."""
        home = HomePage(page).open()

        # View first product
        home.click_product_by_index(0)
        product_detail = ProductDetailPage(page)
        first_product_name = product_detail.get_product_name()

        # Go back and view second product
        product_detail.go_to_home()
        home.click_product_by_index(1)
        second_product_name = product_detail.get_product_name()

        # Verify different products
        assert first_product_name != second_product_name


class TestProductDetailResponsive:
    """Test suite for responsive product detail page."""

    @pytest.mark.ui
    @pytest.mark.products
    @pytest.mark.mobile
    def test_product_detail_mobile_view(self, page: Page):
        """Test product detail page on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})

        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_on_product_detail_page()
        assert product_detail.has_product_information()

    @pytest.mark.ui
    @pytest.mark.products
    @pytest.mark.tablet
    def test_product_detail_tablet_view(self, page: Page):
        """Test product detail page on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})

        home = HomePage(page).open()
        home.click_product_by_index(0)

        product_detail = ProductDetailPage(page)
        assert product_detail.is_on_product_detail_page()
        assert product_detail.has_product_information()
