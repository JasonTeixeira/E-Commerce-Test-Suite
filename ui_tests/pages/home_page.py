"""
Home Page object for DemoBlaze e-commerce application.

Handles homepage elements including navigation, product catalog,
categories, and featured products.
"""

from typing import List, Optional

from playwright.sync_api import Page

from ui_tests.pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Home page object model."""

    # Page elements
    LOGO = "#narvbarx"
    NAV_HOME = 'a[href="index.html"]'
    NAV_CONTACT = 'a[data-target="#exampleModal"]'
    NAV_ABOUT_US = 'a[data-target="#videoModal"]'
    NAV_CART = "#cartur"
    NAV_LOGIN = "#login2"
    NAV_SIGNUP = "#signin2"
    NAV_LOGOUT = "#logout2"
    NAV_USER_NAME = "#nameofuser"

    # Category filters
    CATEGORIES = "#cat"
    CATEGORY_PHONES = 'a:text("Phones")'
    CATEGORY_LAPTOPS = 'a:text("Laptops")'
    CATEGORY_MONITORS = 'a:text("Monitors")'

    # Product list
    PRODUCTS_CONTAINER = "#tbodyid"
    PRODUCT_CARDS = ".card"
    PRODUCT_TITLES = ".card-title"
    PRODUCT_PRICES = ".card-block h5"
    PRODUCT_DESCRIPTIONS = ".card-block p"
    PRODUCT_LINKS = ".hrefch"

    # Pagination
    PREV_BUTTON = "#prev2"
    NEXT_BUTTON = "#next2"

    # Carousel
    CAROUSEL = "#carouselExampleIndicators"
    CAROUSEL_CONTROLS = ".carousel-control-next, .carousel-control-prev"

    def __init__(self, page: Page):
        """Initialize Home page."""
        super().__init__(page)
        self.page_path = ""

    def open(self) -> "HomePage":
        """
        Navigate to home page.

        Returns:
            Self for method chaining
        """
        self.navigate_to(self.page_path)
        logger.info("Opened home page")
        return self

    # ========================================
    # Navigation Actions
    # ========================================

    def click_logo(self) -> "HomePage":
        """Click site logo."""
        self.click(self.LOGO)
        return self

    def goto_cart(self) -> None:
        """Navigate to shopping cart."""
        logger.info("Navigating to cart")
        self.click(self.NAV_CART)
        self.wait_for_load_state("networkidle")

    def open_login_modal(self) -> None:
        """Open login modal dialog."""
        logger.info("Opening login modal")
        self.click(self.NAV_LOGIN)
        self.wait_for_selector("#logInModal .modal-content", state="visible")

    def open_signup_modal(self) -> None:
        """Open signup modal dialog."""
        logger.info("Opening signup modal")
        self.click(self.NAV_SIGNUP)
        self.wait_for_selector("#signInModal .modal-content", state="visible")

    def open_contact_modal(self) -> None:
        """Open contact modal dialog."""
        logger.info("Opening contact modal")
        self.click(self.NAV_CONTACT)
        self.wait_for_selector("#exampleModal .modal-content", state="visible")

    def open_about_modal(self) -> None:
        """Open about us modal dialog."""
        logger.info("Opening about us modal")
        self.click(self.NAV_ABOUT_US)
        self.wait_for_selector("#videoModal .modal-content", state="visible")

    def logout(self) -> "HomePage":
        """
        Logout user.

        Returns:
            Self for method chaining
        """
        logger.info("Logging out user")
        self.click(self.NAV_LOGOUT)
        self.wait_for_selector(self.NAV_LOGIN, state="visible")
        return self

    # ========================================
    # Category Filtering
    # ========================================

    def filter_by_phones(self) -> "HomePage":
        """
        Filter products by Phones category.

        Returns:
            Self for method chaining
        """
        logger.info("Filtering by Phones category")
        self.click(self.CATEGORY_PHONES)
        self.wait_for_load_state("networkidle")
        return self

    def filter_by_laptops(self) -> "HomePage":
        """
        Filter products by Laptops category.

        Returns:
            Self for method chaining
        """
        logger.info("Filtering by Laptops category")
        self.click(self.CATEGORY_LAPTOPS)
        self.wait_for_load_state("networkidle")
        return self

    def filter_by_monitors(self) -> "HomePage":
        """
        Filter products by Monitors category.

        Returns:
            Self for method chaining
        """
        logger.info("Filtering by Monitors category")
        self.click(self.CATEGORY_MONITORS)
        self.wait_for_load_state("networkidle")
        return self

    # ========================================
    # Product Interaction
    # ========================================

    def get_product_count(self) -> int:
        """
        Get number of products displayed.

        Returns:
            Number of products
        """
        count = self.count_elements(self.PRODUCT_CARDS)
        logger.debug(f"Found {count} products")
        return count

    def get_product_titles(self) -> List[str]:
        """
        Get all product titles on current page.

        Returns:
            List of product titles
        """
        titles = self.page.locator(self.PRODUCT_TITLES).all_inner_texts()
        logger.debug(f"Retrieved {len(titles)} product titles")
        return titles

    def get_product_prices(self) -> List[str]:
        """
        Get all product prices on current page.

        Returns:
            List of product prices
        """
        prices = self.page.locator(self.PRODUCT_PRICES).all_inner_texts()
        logger.debug(f"Retrieved {len(prices)} product prices")
        return prices

    def click_product_by_name(self, product_name: str) -> None:
        """
        Click on product by name.

        Args:
            product_name: Name of the product to click
        """
        logger.info(f"Clicking on product: {product_name}")
        self.click(f'a:text("{product_name}")')
        self.wait_for_load_state("networkidle")

    def click_product_by_index(self, index: int) -> None:
        """
        Click on product by index (0-based).

        Args:
            index: Product index to click
        """
        logger.info(f"Clicking on product at index: {index}")
        products = self.page.locator(self.PRODUCT_LINKS).all()
        if index < len(products):
            products[index].click()
            self.wait_for_load_state("networkidle")
        else:
            raise IndexError(f"Product index {index} out of range")

    def is_product_visible(self, product_name: str) -> bool:
        """
        Check if product with given name is visible.

        Args:
            product_name: Product name to check

        Returns:
            True if product is visible
        """
        return self.is_visible(f'a:text("{product_name}")', timeout=3000)

    # ========================================
    # Pagination
    # ========================================

    def click_next_page(self) -> "HomePage":
        """
        Navigate to next page of products.

        Returns:
            Self for method chaining
        """
        logger.info("Navigating to next page")
        self.click(self.NEXT_BUTTON)
        self.wait_for_load_state("networkidle")
        return self

    def click_previous_page(self) -> "HomePage":
        """
        Navigate to previous page of products.

        Returns:
            Self for method chaining
        """
        logger.info("Navigating to previous page")
        self.click(self.PREV_BUTTON)
        self.wait_for_load_state("networkidle")
        return self

    def is_next_button_enabled(self) -> bool:
        """Check if next button is enabled."""
        return self.is_visible(self.NEXT_BUTTON)

    def is_previous_button_enabled(self) -> bool:
        """Check if previous button is enabled."""
        return self.is_visible(self.PREV_BUTTON)

    # ========================================
    # Verification Methods
    # ========================================

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.

        Returns:
            True if user is logged in
        """
        return self.is_visible(self.NAV_USER_NAME, timeout=3000)

    def get_logged_in_username(self) -> Optional[str]:
        """
        Get logged in username.

        Returns:
            Username if logged in, None otherwise
        """
        if self.is_logged_in():
            text = self.get_text(self.NAV_USER_NAME)
            # Extract username from "Welcome username"
            return text.replace("Welcome", "").strip()
        return None

    def is_login_button_visible(self) -> bool:
        """Check if login button is visible."""
        return self.is_visible(self.NAV_LOGIN, timeout=3000)

    def is_signup_button_visible(self) -> bool:
        """Check if signup button is visible."""
        return self.is_visible(self.NAV_SIGNUP, timeout=3000)

    def is_logout_button_visible(self) -> bool:
        """Check if logout button is visible."""
        return self.is_visible(self.NAV_LOGOUT, timeout=3000)

    def verify_on_homepage(self) -> bool:
        """
        Verify user is on homepage.

        Returns:
            True if on homepage
        """
        return (
            self.base_url in self.get_current_url()
            and self.is_visible(self.PRODUCTS_CONTAINER)
        )
