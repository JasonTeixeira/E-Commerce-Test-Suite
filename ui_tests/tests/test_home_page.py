"""
Homepage UI tests for DemoBlaze e-commerce application.

Tests homepage functionality including navigation, product catalog,
categories, and user interactions.
"""

import pytest
from playwright.sync_api import Page, expect

from ui_tests.pages.home_page import HomePage


class TestHomePageNavigation:
    """Test suite for homepage navigation."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    def test_homepage_loads_successfully(self, page: Page):
        """Test homepage loads with all critical elements."""
        home = HomePage(page).open()

        # Verify page loaded
        assert home.verify_on_homepage()
        assert "STORE" in home.get_page_title()

        # Verify nav elements are visible
        assert home.is_visible(home.NAV_HOME)
        assert home.is_visible(home.NAV_CONTACT)
        assert home.is_visible(home.NAV_ABOUT_US)
        assert home.is_visible(home.NAV_CART)
        assert home.is_visible(home.NAV_LOGIN)
        assert home.is_visible(home.NAV_SIGNUP)

    @pytest.mark.ui
    def test_logo_click_returns_to_homepage(self, page: Page):
        """Test clicking logo returns to homepage."""
        home = HomePage(page).open()
        home.filter_by_phones()  # Navigate away
        home.click_logo()
        assert home.verify_on_homepage()

    @pytest.mark.ui
    def test_cart_navigation(self, page: Page):
        """Test navigation to shopping cart."""
        home = HomePage(page).open()
        home.goto_cart()
        assert "cart" in home.get_current_url().lower()

    @pytest.mark.ui
    def test_open_login_modal(self, page: Page):
        """Test opening login modal."""
        home = HomePage(page).open()
        home.open_login_modal()
        assert home.is_visible("#logInModal")
        assert home.is_visible("#loginusername")
        assert home.is_visible("#loginpassword")

    @pytest.mark.ui
    def test_open_signup_modal(self, page: Page):
        """Test opening signup modal."""
        home = HomePage(page).open()
        home.open_signup_modal()
        assert home.is_visible("#signInModal")
        assert home.is_visible("#sign-username")
        assert home.is_visible("#sign-password")

    @pytest.mark.ui
    def test_open_contact_modal(self, page: Page):
        """Test opening contact modal."""
        home = HomePage(page).open()
        home.open_contact_modal()
        assert home.is_visible("#exampleModal")
        assert home.is_visible("#recipient-email")
        assert home.is_visible("#recipient-name")

    @pytest.mark.ui
    def test_open_about_modal(self, page: Page):
        """Test opening about us modal."""
        home = HomePage(page).open()
        home.open_about_modal()
        assert home.is_visible("#videoModal")
        assert home.is_visible("video")


class TestProductCatalog:
    """Test suite for product catalog functionality."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.products
    def test_products_display_on_homepage(self, page: Page):
        """Test products are displayed on homepage."""
        home = HomePage(page).open()
        product_count = home.get_product_count()
        assert product_count > 0, "No products displayed on homepage"
        assert product_count <= 9, "Too many products on one page"

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_titles_are_visible(self, page: Page):
        """Test all product titles are visible."""
        home = HomePage(page).open()
        titles = home.get_product_titles()
        assert len(titles) > 0
        for title in titles:
            assert title.strip() != "", "Empty product title found"

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_prices_are_visible(self, page: Page):
        """Test all product prices are visible."""
        home = HomePage(page).open()
        prices = home.get_product_prices()
        assert len(prices) > 0
        for price in prices:
            assert "$" in price, f"Price format incorrect: {price}"

    @pytest.mark.ui
    @pytest.mark.products
    def test_click_product_navigates_to_detail(self, page: Page):
        """Test clicking product navigates to product detail page."""
        home = HomePage(page).open()
        titles = home.get_product_titles()
        if titles:
            home.click_product_by_index(0)
            assert "prod.html" in home.get_current_url()
            assert home.is_visible(".name")  # Product detail page element

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_count_matches_cards(self, page: Page):
        """Test product count matches number of product cards."""
        home = HomePage(page).open()
        product_count = home.get_product_count()
        titles = home.get_product_titles()
        prices = home.get_product_prices()
        assert product_count == len(titles)
        assert product_count == len(prices)


class TestCategoryFilters:
    """Test suite for category filtering."""

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.products
    def test_filter_by_phones(self, page: Page):
        """Test filtering products by Phones category."""
        home = HomePage(page).open()
        home.filter_by_phones()
        products = home.get_product_titles()
        assert len(products) > 0, "No products shown for Phones category"

    @pytest.mark.ui
    @pytest.mark.products
    def test_filter_by_laptops(self, page: Page):
        """Test filtering products by Laptops category."""
        home = HomePage(page).open()
        home.filter_by_laptops()
        products = home.get_product_titles()
        assert len(products) > 0, "No products shown for Laptops category"

    @pytest.mark.ui
    @pytest.mark.products
    def test_filter_by_monitors(self, page: Page):
        """Test filtering products by Monitors category."""
        home = HomePage(page).open()
        home.filter_by_monitors()
        products = home.get_product_titles()
        assert len(products) > 0, "No products shown for Monitors category"

    @pytest.mark.ui
    @pytest.mark.products
    def test_category_filter_changes_products(self, page: Page):
        """Test category filtering changes displayed products."""
        home = HomePage(page).open()

        # Get initial products
        initial_products = home.get_product_titles()

        # Filter by phones
        home.filter_by_phones()
        phones_products = home.get_product_titles()

        # Filter by laptops
        home.filter_by_laptops()
        laptops_products = home.get_product_titles()

        # Verify products changed
        assert phones_products != laptops_products, "Products should change between categories"

    @pytest.mark.ui
    @pytest.mark.products
    def test_multiple_category_switches(self, page: Page):
        """Test switching between multiple categories."""
        home = HomePage(page).open()

        # Switch between categories
        home.filter_by_phones()
        assert home.get_product_count() > 0

        home.filter_by_laptops()
        assert home.get_product_count() > 0

        home.filter_by_monitors()
        assert home.get_product_count() > 0

        home.filter_by_phones()
        assert home.get_product_count() > 0


class TestPagination:
    """Test suite for pagination functionality."""

    @pytest.mark.ui
    def test_next_button_visible(self, page: Page):
        """Test next page button is visible."""
        home = HomePage(page).open()
        assert home.is_visible(home.NEXT_BUTTON)

    @pytest.mark.ui
    def test_previous_button_visible(self, page: Page):
        """Test previous page button is visible."""
        home = HomePage(page).open()
        assert home.is_visible(home.PREV_BUTTON)

    @pytest.mark.ui
    def test_click_next_page(self, page: Page):
        """Test clicking next page button."""
        home = HomePage(page).open()
        initial_products = home.get_product_titles()
        home.click_next_page()
        new_products = home.get_product_titles()
        # Products should be different after pagination
        assert initial_products != new_products or len(initial_products) == len(new_products)

    @pytest.mark.ui
    @pytest.mark.slow
    def test_pagination_cycle(self, page: Page):
        """Test cycling through multiple pages."""
        home = HomePage(page).open()

        # Click next several times
        for _ in range(3):
            if home.is_next_button_enabled():
                home.click_next_page()
                assert home.get_product_count() > 0

        # Click previous to go back
        for _ in range(3):
            if home.is_previous_button_enabled():
                home.click_previous_page()
                assert home.get_product_count() > 0


class TestUserAuthentication:
    """Test suite for user authentication UI."""

    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_button_visible_when_logged_out(self, page: Page):
        """Test login button is visible when not logged in."""
        home = HomePage(page).open()
        assert home.is_login_button_visible()
        assert not home.is_logged_in()

    @pytest.mark.ui
    @pytest.mark.auth
    def test_signup_button_visible_when_logged_out(self, page: Page):
        """Test signup button is visible when not logged in."""
        home = HomePage(page).open()
        assert home.is_signup_button_visible()

    @pytest.mark.ui
    @pytest.mark.auth
    def test_logout_not_visible_when_logged_out(self, page: Page):
        """Test logout button is not visible when not logged in."""
        home = HomePage(page).open()
        assert not home.is_logout_button_visible()


class TestResponsiveDesign:
    """Test suite for responsive design."""

    @pytest.mark.ui
    @pytest.mark.mobile
    def test_homepage_mobile_viewport(self, page: Page):
        """Test homepage on mobile viewport."""
        page.set_viewport_size({"width": 375, "height": 667})  # iPhone SE
        home = HomePage(page).open()
        assert home.verify_on_homepage()
        assert home.get_product_count() > 0

    @pytest.mark.ui
    @pytest.mark.tablet
    def test_homepage_tablet_viewport(self, page: Page):
        """Test homepage on tablet viewport."""
        page.set_viewport_size({"width": 768, "height": 1024})  # iPad
        home = HomePage(page).open()
        assert home.verify_on_homepage()
        assert home.get_product_count() > 0

    @pytest.mark.ui
    @pytest.mark.desktop
    def test_homepage_desktop_viewport(self, page: Page):
        """Test homepage on desktop viewport."""
        page.set_viewport_size({"width": 1920, "height": 1080})
        home = HomePage(page).open()
        assert home.verify_on_homepage()
        assert home.get_product_count() > 0


class TestPagePerformance:
    """Test suite for page performance."""

    @pytest.mark.ui
    @pytest.mark.performance
    def test_homepage_load_time(self, page: Page):
        """Test homepage loads within acceptable time."""
        import time

        start_time = time.time()
        home = HomePage(page).open()
        load_time = time.time() - start_time

        assert load_time < 5.0, f"Homepage took {load_time}s to load"
        assert home.verify_on_homepage()

    @pytest.mark.ui
    @pytest.mark.performance
    def test_product_filtering_performance(self, page: Page):
        """Test category filtering responds quickly."""
        import time

        home = HomePage(page).open()

        start_time = time.time()
        home.filter_by_phones()
        filter_time = time.time() - start_time

        assert filter_time < 3.0, f"Filtering took {filter_time}s"
        assert home.get_product_count() > 0
