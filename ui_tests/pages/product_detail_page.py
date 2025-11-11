"""
Product Detail Page object for DemoBlaze.

Handles product detail page interactions including product information,
add to cart, and image gallery.
"""

from typing import Optional

from playwright.sync_api import Page

from ui_tests.pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductDetailPage(BasePage):
    """Product detail page object model."""

    # Product Information
    PRODUCT_NAME = ".name"
    PRODUCT_PRICE = ".price-container"
    PRODUCT_DESCRIPTION = "#more-information p"
    PRODUCT_IMAGE = ".item.active img"

    # Actions
    ADD_TO_CART_BUTTON = 'a[onclick="addToCart("]'
    HOME_LINK = ".navbar-brand"

    # Navigation
    BREADCRUMB_HOME = 'a[href="index.html"]'

    def __init__(self, page: Page):
        """Initialize Product Detail page."""
        super().__init__(page)

    # ========================================
    # Navigation Methods
    # ========================================

    def go_to_home(self) -> None:
        """Navigate back to homepage."""
        logger.info("Navigating to homepage")
        self.click(self.HOME_LINK)
        self.wait_for_load_state("networkidle")

    # ========================================
    # Product Information Methods
    # ========================================

    def get_product_name(self) -> str:
        """
        Get product name.

        Returns:
            Product name
        """
        name = self.get_text(self.PRODUCT_NAME)
        logger.debug(f"Product name: {name}")
        return name

    def get_product_price(self) -> str:
        """
        Get product price.

        Returns:
            Product price string
        """
        price = self.get_text(self.PRODUCT_PRICE)
        logger.debug(f"Product price: {price}")
        return price

    def get_product_price_value(self) -> float:
        """
        Get product price as float value.

        Returns:
            Product price as float
        """
        price_text = self.get_product_price()
        # Extract numeric value from price string like "$790 *includes tax"
        price_str = price_text.split()[0].replace("$", "").strip()
        return float(price_str)

    def get_product_description(self) -> str:
        """
        Get product description.

        Returns:
            Product description text
        """
        desc = self.get_text(self.PRODUCT_DESCRIPTION)
        logger.debug(f"Product description: {desc[:50]}...")
        return desc

    def is_product_image_visible(self) -> bool:
        """
        Check if product image is visible.

        Returns:
            True if image is visible
        """
        return self.is_visible(self.PRODUCT_IMAGE)

    def get_product_image_src(self) -> Optional[str]:
        """
        Get product image source URL.

        Returns:
            Image source URL
        """
        return self.get_attribute(self.PRODUCT_IMAGE, "src")

    # ========================================
    # Add to Cart Methods
    # ========================================

    def click_add_to_cart(self) -> "ProductDetailPage":
        """
        Click add to cart button.

        Returns:
            Self for method chaining
        """
        logger.info("Clicking add to cart button")
        self.click(self.ADD_TO_CART_BUTTON)
        return self

    def is_add_to_cart_button_visible(self) -> bool:
        """
        Check if add to cart button is visible.

        Returns:
            True if button is visible
        """
        return self.is_visible(self.ADD_TO_CART_BUTTON)

    def add_to_cart_and_accept_alert(self) -> "ProductDetailPage":
        """
        Add product to cart and accept success alert.

        Returns:
            Self for method chaining
        """
        logger.info("Adding product to cart")

        # Set up alert handler
        def handle_alert(dialog):
            logger.info(f"Alert: {dialog.message}")
            dialog.accept()

        self.page.on("dialog", handle_alert)
        self.click_add_to_cart()
        self.wait_for_timeout(1500)  # Wait for alert
        return self

    def add_to_cart_and_get_alert_text(self) -> Optional[str]:
        """
        Add product to cart and capture alert text.

        Returns:
            Alert message text
        """
        logger.info("Adding product to cart and capturing alert")
        alert_text = None

        def handle_alert(dialog):
            nonlocal alert_text
            alert_text = dialog.message
            logger.info(f"Alert captured: {alert_text}")
            dialog.accept()

        self.page.on("dialog", handle_alert)
        self.click_add_to_cart()
        self.wait_for_timeout(1500)
        return alert_text

    # ========================================
    # Verification Methods
    # ========================================

    def is_on_product_detail_page(self) -> bool:
        """
        Verify we're on product detail page.

        Returns:
            True if on product detail page
        """
        return (
            "prod.html" in self.get_current_url()
            and self.is_visible(self.PRODUCT_NAME)
            and self.is_visible(self.ADD_TO_CART_BUTTON)
        )

    def has_product_information(self) -> bool:
        """
        Check if all product information is displayed.

        Returns:
            True if name, price, and description are visible
        """
        return (
            self.is_visible(self.PRODUCT_NAME)
            and self.is_visible(self.PRODUCT_PRICE)
            and self.is_visible(self.PRODUCT_DESCRIPTION)
        )

    def verify_product_price_format(self) -> bool:
        """
        Verify product price has correct format.

        Returns:
            True if price contains $ symbol
        """
        price = self.get_product_price()
        return "$" in price

    def verify_product_price_is_positive(self) -> bool:
        """
        Verify product price is a positive number.

        Returns:
            True if price is positive
        """
        try:
            price_value = self.get_product_price_value()
            return price_value > 0
        except (ValueError, AttributeError):
            return False
