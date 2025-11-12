"""
Visual regression tests for DemoBlaze.

Tests for visual consistency across browsers, viewports,
and page states using screenshot comparison.
"""

import pytest
from playwright.sync_api import Page

from config.settings import settings
from visual.utils.screenshot_compare import ScreenshotCompare


@pytest.fixture
def screenshot_compare():
    """Create screenshot comparison utility."""
    return ScreenshotCompare()


class TestPageVisualRegression:
    """Test visual consistency of full pages."""

    @pytest.mark.visual
    @pytest.mark.ui
    def test_homepage_visual_desktop(self, page: Page, screenshot_compare):
        """Test homepage visual consistency on desktop."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        screenshot_path = "visual/temp/homepage_desktop.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "homepage_desktop", threshold=0.05
        )

        assert is_similar, f"Homepage visual regression detected: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.mobile
    def test_homepage_visual_mobile(self, page: Page, screenshot_compare):
        """Test homepage visual consistency on mobile."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        screenshot_path = "visual/temp/homepage_mobile.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "homepage_mobile", threshold=0.05
        )

        assert is_similar, f"Mobile homepage regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.tablet
    def test_homepage_visual_tablet(self, page: Page, screenshot_compare):
        """Test homepage visual consistency on tablet."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        screenshot_path = "visual/temp/homepage_tablet.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "homepage_tablet", threshold=0.05
        )

        assert is_similar, f"Tablet homepage regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_product_page_visual(self, page: Page, screenshot_compare):
        """Test product detail page visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        # Click first product
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")

        screenshot_path = "visual/temp/product_page.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "product_page", threshold=0.05
        )

        assert is_similar, f"Product page regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_cart_page_visual(self, page: Page, screenshot_compare):
        """Test cart page visual consistency."""
        page.goto(settings.base_url)
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        screenshot_path = "visual/temp/cart_page.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "cart_page", threshold=0.05
        )

        assert is_similar, f"Cart page regression: {diff:.2%} difference"


class TestComponentVisualRegression:
    """Test visual consistency of components."""

    @pytest.mark.visual
    @pytest.mark.ui
    def test_navbar_visual(self, page: Page, screenshot_compare):
        """Test navbar visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        navbar = page.locator("nav.navbar")
        screenshot_path = "visual/temp/navbar.png"
        navbar.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "navbar", threshold=0.03
        )

        assert is_similar, f"Navbar regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_product_card_visual(self, page: Page, screenshot_compare):
        """Test product card visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        card = page.locator(".card").first
        screenshot_path = "visual/temp/product_card.png"
        card.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "product_card", threshold=0.03
        )

        assert is_similar, f"Product card regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_footer_visual(self, page: Page, screenshot_compare):
        """Test footer visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        footer = page.locator("#fotcont")
        screenshot_path = "visual/temp/footer.png"
        footer.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "footer", threshold=0.03
        )

        assert is_similar, f"Footer regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_category_sidebar_visual(self, page: Page, screenshot_compare):
        """Test category sidebar visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        sidebar = page.locator("#cat")
        screenshot_path = "visual/temp/sidebar.png"
        sidebar.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "sidebar", threshold=0.03
        )

        assert is_similar, f"Sidebar regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_carousel_visual(self, page: Page, screenshot_compare):
        """Test carousel visual consistency."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        carousel = page.locator("#carouselExampleIndicators")
        screenshot_path = "visual/temp/carousel.png"
        carousel.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "carousel", threshold=0.05
        )

        assert is_similar, f"Carousel regression: {diff:.2%} difference"


class TestModalVisualRegression:
    """Test modal visual consistency."""

    @pytest.mark.visual
    @pytest.mark.ui
    def test_login_modal_visual(self, page: Page, screenshot_compare):
        """Test login modal visual consistency."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        modal = page.locator("#logInModal")
        screenshot_path = "visual/temp/login_modal.png"
        modal.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "login_modal", threshold=0.03
        )

        assert is_similar, f"Login modal regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_signup_modal_visual(self, page: Page, screenshot_compare):
        """Test signup modal visual consistency."""
        page.goto(settings.base_url)
        page.click("#signin2")
        page.wait_for_selector("#signInModal", state="visible")

        modal = page.locator("#signInModal")
        screenshot_path = "visual/temp/signup_modal.png"
        modal.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "signup_modal", threshold=0.03
        )

        assert is_similar, f"Signup modal regression: {diff:.2%} difference"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_checkout_modal_visual(self, page: Page, screenshot_compare):
        """Test checkout modal visual consistency."""
        page.goto(settings.base_url)
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")
        page.click("button:has-text('Place Order')")
        page.wait_for_selector("#orderModal", state="visible")

        modal = page.locator("#orderModal")
        screenshot_path = "visual/temp/checkout_modal.png"
        modal.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "checkout_modal", threshold=0.03
        )

        assert is_similar, f"Checkout modal regression: {diff:.2%} difference"


class TestCrossBrowserVisualRegression:
    """Test visual consistency across browsers."""

    @pytest.mark.visual
    @pytest.mark.ui
    @pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
    def test_homepage_cross_browser(self, page: Page, screenshot_compare, browser_name):
        """Test homepage consistency across browsers."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        screenshot_path = f"visual/temp/homepage_{browser_name}.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, f"homepage_{browser_name}", threshold=0.08
        )

        # Higher threshold for cross-browser differences
        assert is_similar, f"{browser_name} visual diff: {diff:.2%}"

    @pytest.mark.visual
    @pytest.mark.ui
    @pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
    def test_login_modal_cross_browser(self, page: Page, screenshot_compare, browser_name):
        """Test login modal consistency across browsers."""
        page.goto(settings.base_url)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        modal = page.locator("#logInModal")
        screenshot_path = f"visual/temp/login_{browser_name}.png"
        modal.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, f"login_{browser_name}", threshold=0.08
        )

        assert is_similar, f"{browser_name} login modal diff: {diff:.2%}"


class TestResponsiveVisualRegression:
    """Test visual consistency across viewport sizes."""

    @pytest.mark.visual
    @pytest.mark.ui
    @pytest.mark.parametrize("width,height,name", [
        (320, 568, "iphone_se"),
        (375, 667, "iphone_8"),
        (414, 896, "iphone_11"),
        (768, 1024, "ipad"),
        (1024, 768, "ipad_landscape"),
        (1920, 1080, "desktop_hd"),
        (2560, 1440, "desktop_2k"),
    ])
    def test_homepage_responsive(self, page: Page, screenshot_compare, width, height, name):
        """Test homepage across different viewport sizes."""
        page.set_viewport_size({"width": width, "height": height})
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        screenshot_path = f"visual/temp/homepage_{name}.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, f"homepage_{name}", threshold=0.05
        )

        assert is_similar, f"{name} ({width}x{height}) diff: {diff:.2%}"


class TestStateVisualRegression:
    """Test visual consistency of different states."""

    @pytest.mark.visual
    @pytest.mark.ui
    def test_hover_state_product_card(self, page: Page, screenshot_compare):
        """Test product card hover state."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        card = page.locator(".card").first
        card.hover()
        page.wait_for_timeout(300)

        screenshot_path = "visual/temp/card_hover.png"
        card.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "card_hover", threshold=0.05
        )

        assert is_similar, f"Card hover state diff: {diff:.2%}"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_active_category_visual(self, page: Page, screenshot_compare):
        """Test active category visual state."""
        page.goto(settings.base_url)
        page.click("a:has-text('Phones')")
        page.wait_for_timeout(500)

        sidebar = page.locator("#cat")
        screenshot_path = "visual/temp/active_category.png"
        sidebar.screenshot(path=screenshot_path)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "active_category", threshold=0.05
        )

        assert is_similar, f"Active category state diff: {diff:.2%}"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_cart_with_items_visual(self, page: Page, screenshot_compare):
        """Test cart page with items."""
        page.goto(settings.base_url)
        page.wait_for_load_state("networkidle")

        # Add item to cart
        page.click(".card-title a >> nth=0")
        page.wait_for_selector("#tbodyid")
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(500)

        # Go to cart
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        screenshot_path = "visual/temp/cart_with_items.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "cart_with_items", threshold=0.05
        )

        assert is_similar, f"Cart with items diff: {diff:.2%}"

    @pytest.mark.visual
    @pytest.mark.ui
    def test_empty_cart_visual(self, page: Page, screenshot_compare):
        """Test empty cart visual state."""
        page.goto(settings.base_url)
        page.click("#cartur")
        page.wait_for_selector("#tbodyid")

        screenshot_path = "visual/temp/empty_cart.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "empty_cart", threshold=0.03
        )

        assert is_similar, f"Empty cart diff: {diff:.2%}"


class TestLoadingStateVisualRegression:
    """Test visual consistency during loading states."""

    @pytest.mark.visual
    @pytest.mark.ui
    def test_page_skeleton_visual(self, page: Page, screenshot_compare):
        """Test page loading skeleton/spinner."""
        page.goto(settings.base_url)
        # Capture immediately (might catch loading state)
        
        screenshot_path = "visual/temp/loading_state.png"
        page.screenshot(path=screenshot_path)

        # This test documents the loading state visual

    @pytest.mark.visual
    @pytest.mark.ui
    def test_modal_transition_visual(self, page: Page, screenshot_compare):
        """Test modal opening transition."""
        page.goto(settings.base_url)
        
        # Click and immediately capture
        page.click("#login2")
        page.wait_for_timeout(100)  # Mid-transition

        screenshot_path = "visual/temp/modal_transition.png"
        page.screenshot(path=screenshot_path)

        # Documents transition state


class TestDarkModeVisualRegression:
    """Test dark mode visual consistency (if supported)."""

    @pytest.mark.visual
    @pytest.mark.ui
    @pytest.mark.skip(reason="Dark mode not supported by DemoBlaze")
    def test_homepage_dark_mode(self, page: Page, screenshot_compare):
        """Test homepage in dark mode."""
        # Inject dark mode styles or toggle if supported
        page.goto(settings.base_url)
        
        screenshot_path = "visual/temp/homepage_dark.png"
        page.screenshot(path=screenshot_path, full_page=True)

        is_similar, diff, _ = screenshot_compare.compare_with_baseline(
            screenshot_path, "homepage_dark", threshold=0.05
        )

        assert is_similar, f"Dark mode diff: {diff:.2%}"
