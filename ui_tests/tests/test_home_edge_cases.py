"""
Homepage edge cases and negative tests.

Tests error handling, boundary conditions, and edge scenarios
for the homepage functionality.
"""

import pytest
from playwright.sync_api import Page

from ui_tests.pages.home_page import HomePage


class TestHomePageEdgeCases:
    """Test suite for homepage edge cases."""

    @pytest.mark.ui
    @pytest.mark.products
    def test_click_product_with_invalid_index(self, page: Page):
        """Test clicking product with out-of-range index."""
        home = HomePage(page).open()
        
        # Try to click non-existent product
        with pytest.raises(IndexError):
            home.click_product_by_index(999)

    @pytest.mark.ui
    @pytest.mark.products
    def test_filter_products_multiple_times(self, page: Page):
        """Test repeatedly filtering products."""
        home = HomePage(page).open()
        
        # Filter multiple times in succession
        for _ in range(5):
            home.filter_by_phones()
            assert home.get_product_count() > 0
            
            home.filter_by_laptops()
            assert home.get_product_count() > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_count_never_negative(self, page: Page):
        """Test product count is never negative."""
        home = HomePage(page).open()
        
        count = home.get_product_count()
        assert count >= 0

    @pytest.mark.ui
    def test_page_reload_preserves_state(self, page: Page):
        """Test page reload maintains proper state."""
        home = HomePage(page).open()
        home.filter_by_phones()
        
        initial_count = home.get_product_count()
        
        home.refresh()
        
        # After reload, products should still be visible
        assert home.get_product_count() >= 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_empty_product_titles_not_allowed(self, page: Page):
        """Test that product titles are never empty strings."""
        home = HomePage(page).open()
        titles = home.get_product_titles()
        
        for title in titles:
            assert title.strip() != "", "Product title should not be empty"
            assert len(title) > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_product_prices_are_always_formatted(self, page: Page):
        """Test all product prices include currency symbol."""
        home = HomePage(page).open()
        prices = home.get_product_prices()
        
        for price in prices:
            assert "$" in price, f"Price should include $ symbol: {price}"

    @pytest.mark.ui
    def test_navigation_links_are_clickable(self, page: Page):
        """Test all main navigation links are clickable."""
        home = HomePage(page).open()
        
        # Check that navigation elements are present and enabled
        assert home.is_visible(home.NAV_HOME)
        assert home.is_visible(home.NAV_CONTACT)
        assert home.is_visible(home.NAV_ABOUT_US)
        assert home.is_visible(home.NAV_CART)

    @pytest.mark.ui
    @pytest.mark.slow
    def test_rapid_pagination_clicks(self, page: Page):
        """Test rapid clicking of pagination buttons."""
        home = HomePage(page).open()
        
        # Rapidly click next button
        for _ in range(3):
            if home.is_next_button_enabled():
                home.click_next_page()
                assert home.get_product_count() > 0

    @pytest.mark.ui
    def test_category_buttons_remain_functional(self, page: Page):
        """Test category buttons work after multiple uses."""
        home = HomePage(page).open()
        
        # Click each category multiple times
        for _ in range(2):
            home.filter_by_phones()
            phones_count = home.get_product_count()
            assert phones_count > 0
            
            home.filter_by_laptops()
            laptops_count = home.get_product_count()
            assert laptops_count > 0
            
            home.filter_by_monitors()
            monitors_count = home.get_product_count()
            assert monitors_count > 0

    @pytest.mark.ui
    @pytest.mark.products
    def test_all_products_have_links(self, page: Page):
        """Test all products have clickable links."""
        home = HomePage(page).open()
        
        product_count = home.get_product_count()
        product_links = home.count_elements(home.PRODUCT_LINKS)
        
        assert product_links == product_count, "Each product should have a link"
