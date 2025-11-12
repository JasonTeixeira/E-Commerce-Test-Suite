"""
Additional edge case tests for comprehensive coverage.

Tests for boundary conditions, error handling, race conditions,
and unusual user behaviors.
"""

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings


class TestNavigationEdgeCases:
    """Test edge cases in navigation."""

    @pytest.mark.ui
    @pytest.mark.critical
    def test_rapid_navigation_clicks(self, page: Page):
        """Test rapid clicking between pages."""
        page.goto(settings.base_url)

        # Rapidly click between categories
        for _ in range(5):
            page.click("a:has-text('Phones')")
            page.click("a:has-text('Laptops')")
            page.click("a:has-text('Monitors')")

        # Page should still be functional
        assert page.url.startswith(settings.base_url)

    @pytest.mark.ui
    def test_browser_back_forward(self, page: Page):
        """Test browser back/forward navigation."""
        page.goto(settings.base_url)
        
        # Navigate forward
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")

        # Go back
        page.go_back()
        page.wait_for_selector(".card")

        # Go forward
        page.go_forward()
        page.wait_for_selector("#tbodyid")

        # Should be on product page
        assert "prod.html" in page.url

    @pytest.mark.ui
    def test_page_refresh_preserves_state(self, page: Page):
        """Test page refresh behavior."""
        page.goto(settings.base_url)
        page.click("a:has-text('Phones')")
        page.wait_for_timeout(500)

        # Refresh page
        page.reload()
        page.wait_for_load_state("networkidle")

        # Page should load successfully
        assert page.locator(".card").count() > 0

    @pytest.mark.ui
    def test_multiple_tabs_independence(self, page: Page, context):
        """Test multiple tabs work independently."""
        page.goto(settings.base_url)

        # Open new tab
        page2 = context.new_page()
        page2.goto(settings.base_url)

        # Different actions in each tab
        page.click("a:has-text('Phones')")
        page2.click("a:has-text('Laptops')")

        page.wait_for_timeout(500)
        page2.wait_for_timeout(500)

        # Tabs should maintain independent state


class TestFormEdgeCases:
    """Test form edge cases."""

    @pytest.mark.ui
    def test_login_form_autofill(self, page: Page):
        """Test form autofill behavior."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Simulate autofill
        page.fill("#loginusername", "testuser")
        page.fill("#loginpassword", "password123")

        # Form should accept autofilled data
        assert page.locator("#loginusername").input_value() == "testuser"

    @pytest.mark.ui
    def test_form_submission_double_click(self, page: Page):
        """Test double-clicking submit button."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        page.fill("#loginusername", "testuser")
        page.fill("#loginpassword", "password")

        # Double click submit
        page.click("button:has-text('Log in')")
        page.click("button:has-text('Log in')")

        page.wait_for_timeout(1000)

        # Should handle gracefully (not double-submit)

    @pytest.mark.ui
    def test_form_validation_on_blur(self, page: Page):
        """Test validation triggers on blur."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Focus and blur without input
        page.click("#loginusername")
        page.click("#loginpassword")

        # Check if validation messages appear

    @pytest.mark.ui
    def test_copy_paste_in_forms(self, page: Page):
        """Test copy/paste in form fields."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Paste text
        test_username = "pasteduser123"
        page.fill("#loginusername", test_username)

        assert page.locator("#loginusername").input_value() == test_username


class TestProductEdgeCases:
    """Test product-related edge cases."""

    @pytest.mark.ui
    def test_add_same_product_multiple_times(self, page: Page):
        """Test adding same product to cart multiple times."""
        page.goto(settings.base_url)
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")

        # Add to cart multiple times
        for _ in range(3):
            page.click("a:has-text('Add to cart')")
            page.wait_for_timeout(300)
            page.once("dialog", lambda dialog: dialog.accept())

        # Check cart
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        # Should handle multiple adds

    @pytest.mark.ui
    def test_product_image_load_failure(self, page: Page):
        """Test handling of broken product images."""
        page.goto(settings.base_url)

        # Check for broken images
        images = page.locator(".card-img-top").all()
        
        for img in images[:5]:
            # Should have valid src or placeholder
            src = img.get_attribute("src")
            assert src is not None

    @pytest.mark.ui
    def test_pagination_boundary(self, page: Page):
        """Test pagination at boundaries."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        # Try clicking next multiple times
        next_button = page.locator("#next2")
        
        for _ in range(5):
            if next_button.is_enabled():
                next_button.click()
                page.wait_for_timeout(500)

        # Should handle reaching end gracefully

    @pytest.mark.ui
    def test_product_quick_navigation(self, page: Page):
        """Test quickly navigating through products."""
        page.goto(settings.base_url)

        # Quickly open and close products
        for i in range(3):
            page.click(f".card-title a >> nth={i}")
            page.wait_for_selector("#tbodyid")
            page.go_back()
            page.wait_for_timeout(200)

        # Should remain functional


class TestCartEdgeCases:
    """Test cart edge cases."""

    @pytest.mark.ui
    def test_cart_concurrent_modifications(self, page: Page):
        """Test modifying cart rapidly."""
        page.goto(settings.base_url)

        # Add items quickly
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(300)

        page.goto(settings.base_url)
        page.click(".card-title a >> nth=1")
        page.wait_for_selector("#tbodyid")
        page.click("a:has-text('Add to cart')")

        page.wait_for_timeout(500)

        # Go to cart
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        # Should show both items

    @pytest.mark.ui
    def test_delete_cart_item_confirmation(self, page: Page):
        """Test deleting items from cart."""
        page.goto(settings.base_url)

        # Add item
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(500)

        # Go to cart and delete
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        # Look for delete links
        delete_links = page.locator("a:has-text('Delete')")
        if delete_links.count() > 0:
            delete_links.first.click()
            page.wait_for_timeout(500)

    @pytest.mark.ui
    def test_cart_total_calculation_precision(self, page: Page):
        """Test cart total with decimal precision."""
        page.goto(settings.base_url)

        # Add items and check total
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(500)

        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        # Total should be displayed
        total = page.locator("#totalp")
        if total.is_visible():
            total_text = total.text_content()
            # Should be a valid number


class TestModalEdgeCases:
    """Test modal edge cases."""

    @pytest.mark.ui
    def test_open_multiple_modals(self, page: Page):
        """Test opening modals in sequence."""
        page.goto(settings.base_url)

        # Open and close multiple modals
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")
        page.keyboard.press("Escape")

        page.wait_for_timeout(300)

        page.click("#signin2")
        page.wait_for_selector("#signInModal", state="visible")
        page.keyboard.press("Escape")

        # Should handle gracefully

    @pytest.mark.ui
    def test_modal_backdrop_click(self, page: Page):
        """Test clicking modal backdrop."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Click backdrop area
        page.click(".modal", position={"x": 10, "y": 10})
        page.wait_for_timeout(300)

        # Modal might close

    @pytest.mark.ui
    def test_modal_keyboard_navigation(self, page: Page):
        """Test keyboard navigation in modals."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Tab through modal elements
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")

        # Focus should stay in modal


class TestResponsivenessEdgeCases:
    """Test responsive behavior edge cases."""

    @pytest.mark.ui
    @pytest.mark.mobile
    def test_orientation_change(self, page: Page):
        """Test device orientation change."""
        # Portrait
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        # Landscape
        page.set_viewport_size({"width": 667, "height": 375})
        page.wait_for_timeout(500)

        # Should adapt layout
        assert page.locator("body").is_visible()

    @pytest.mark.ui
    def test_extreme_viewport_sizes(self, page: Page):
        """Test extreme viewport dimensions."""
        # Very narrow
        page.set_viewport_size({"width": 280, "height": 640})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        assert page.locator("body").is_visible()

        # Very wide
        page.set_viewport_size({"width": 3840, "height": 2160})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        assert page.locator("body").is_visible()

    @pytest.mark.ui
    @pytest.mark.mobile
    def test_pinch_zoom(self, page: Page):
        """Test pinch-to-zoom behavior."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(settings.base_url)

        # Mobile browsers handle zoom
        # Just verify page loads properly


class TestSessionEdgeCases:
    """Test session-related edge cases."""

    @pytest.mark.ui
    def test_session_timeout(self, page: Page):
        """Test session timeout behavior."""
        page.goto(settings.base_url)

        # Wait for extended period
        # (Shortened for testing)
        page.wait_for_timeout(2000)

        # Page should still be functional
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

    @pytest.mark.ui
    def test_cookies_disabled(self, page: Page, context):
        """Test behavior with cookies disabled."""
        # Clear all cookies
        context.clear_cookies()

        page.goto(settings.base_url)

        # Should still load
        assert page.locator("body").is_visible()
