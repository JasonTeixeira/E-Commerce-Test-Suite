"""
Cart Page object for DemoBlaze shopping cart.

Handles cart interactions including viewing items, removing products,
and proceeding to checkout.
"""

from typing import List, Optional

from playwright.sync_api import Page

from ui_tests.pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Shopping cart page object model."""

    # Cart elements
    CART_TABLE = "#tbodyid"
    CART_ITEMS = "#tbodyid tr"
    CART_ITEM_TITLE = "td:nth-child(2)"
    CART_ITEM_PRICE = "td:nth-child(3)"
    CART_ITEM_DELETE = "a[onclick*='deleteItem']"

    # Total
    TOTAL_PRICE = "#totalp"

    # Actions
    PLACE_ORDER_BUTTON = 'button[data-target="#orderModal"]'
    CONTINUE_SHOPPING_LINK = 'a[href="index.html"]'

    # Order Modal
    ORDER_MODAL = "#orderModal"
    ORDER_NAME_INPUT = "#name"
    ORDER_COUNTRY_INPUT = "#country"
    ORDER_CITY_INPUT = "#city"
    ORDER_CARD_INPUT = "#card"
    ORDER_MONTH_INPUT = "#month"
    ORDER_YEAR_INPUT = "#year"
    ORDER_PURCHASE_BUTTON = 'button[onclick="purchaseOrder()"]'
    ORDER_CLOSE_BUTTON = "#orderModal .close"

    def __init__(self, page: Page):
        """Initialize Cart page."""
        super().__init__(page)
        self.page_path = "cart.html"

    def open(self) -> "CartPage":
        """
        Navigate to cart page.

        Returns:
            Self for method chaining
        """
        self.navigate_to(self.page_path)
        logger.info("Opened cart page")
        return self

    # ========================================
    # Cart Item Methods
    # ========================================

    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart.

        Returns:
            Number of cart items
        """
        count = self.count_elements(self.CART_ITEMS)
        logger.debug(f"Cart has {count} items")
        return count

    def get_cart_item_titles(self) -> List[str]:
        """
        Get titles of all items in cart.

        Returns:
            List of product titles
        """
        items = self.page.locator(self.CART_ITEMS).all()
        titles = []
        for item in items:
            title = item.locator(self.CART_ITEM_TITLE).inner_text()
            titles.append(title)
        logger.debug(f"Cart items: {titles}")
        return titles

    def get_cart_item_prices(self) -> List[str]:
        """
        Get prices of all items in cart.

        Returns:
            List of product prices
        """
        items = self.page.locator(self.CART_ITEMS).all()
        prices = []
        for item in items:
            price = item.locator(self.CART_ITEM_PRICE).inner_text()
            prices.append(price)
        logger.debug(f"Cart prices: {prices}")
        return prices

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if product is in cart.

        Args:
            product_name: Product name to check

        Returns:
            True if product is in cart
        """
        titles = self.get_cart_item_titles()
        return product_name in titles

    def remove_item_by_index(self, index: int) -> "CartPage":
        """
        Remove item from cart by index.

        Args:
            index: Index of item to remove (0-based)

        Returns:
            Self for method chaining
        """
        logger.info(f"Removing cart item at index {index}")
        items = self.page.locator(self.CART_ITEMS).all()
        if index < len(items):
            delete_button = items[index].locator(self.CART_ITEM_DELETE)
            delete_button.click()
            self.wait_for_timeout(1000)  # Wait for removal
        return self

    def remove_all_items(self) -> "CartPage":
        """
        Remove all items from cart.

        Returns:
            Self for method chaining
        """
        logger.info("Removing all items from cart")
        while self.get_cart_item_count() > 0:
            self.remove_item_by_index(0)
            self.wait_for_timeout(500)
        return self

    # ========================================
    # Total Price Methods
    # ========================================

    def get_total_price_text(self) -> str:
        """
        Get total price as text.

        Returns:
            Total price string
        """
        total = self.get_text(self.TOTAL_PRICE)
        logger.debug(f"Total price: {total}")
        return total

    def get_total_price_value(self) -> float:
        """
        Get total price as float value.

        Returns:
            Total price as float
        """
        total_text = self.get_total_price_text()
        return float(total_text)

    def calculate_expected_total(self) -> float:
        """
        Calculate expected total from item prices.

        Returns:
            Expected total price
        """
        prices = self.get_cart_item_prices()
        total = sum(float(price) for price in prices)
        logger.debug(f"Calculated total: {total}")
        return total

    def verify_total_matches_items(self) -> bool:
        """
        Verify total price matches sum of item prices.

        Returns:
            True if total is correct
        """
        expected = self.calculate_expected_total()
        actual = self.get_total_price_value()
        matches = expected == actual
        logger.debug(f"Total verification: expected={expected}, actual={actual}, matches={matches}")
        return matches

    # ========================================
    # Cart Actions
    # ========================================

    def click_place_order(self) -> "CartPage":
        """
        Click place order button.

        Returns:
            Self for method chaining
        """
        logger.info("Clicking place order button")
        self.click(self.PLACE_ORDER_BUTTON)
        self.wait_for_selector(self.ORDER_MODAL, state="visible")
        return self

    def is_place_order_button_visible(self) -> bool:
        """
        Check if place order button is visible.

        Returns:
            True if button is visible
        """
        return self.is_visible(self.PLACE_ORDER_BUTTON)

    def continue_shopping(self) -> None:
        """Navigate back to homepage."""
        logger.info("Continuing shopping")
        self.click(self.CONTINUE_SHOPPING_LINK)
        self.wait_for_load_state("networkidle")

    # ========================================
    # Order Modal Methods
    # ========================================

    def is_order_modal_open(self) -> bool:
        """
        Check if order modal is open.

        Returns:
            True if modal is visible
        """
        return self.is_visible(self.ORDER_MODAL, timeout=3000)

    def fill_order_form(
        self,
        name: str,
        country: str,
        city: str,
        card: str,
        month: str,
        year: str
    ) -> "CartPage":
        """
        Fill order form.

        Args:
            name: Customer name
            country: Country
            city: City
            card: Credit card number
            month: Expiration month
            year: Expiration year

        Returns:
            Self for method chaining
        """
        logger.info(f"Filling order form for {name}")
        self.fill(self.ORDER_NAME_INPUT, name)
        self.fill(self.ORDER_COUNTRY_INPUT, country)
        self.fill(self.ORDER_CITY_INPUT, city)
        self.fill(self.ORDER_CARD_INPUT, card)
        self.fill(self.ORDER_MONTH_INPUT, month)
        self.fill(self.ORDER_YEAR_INPUT, year)
        return self

    def click_purchase(self) -> "CartPage":
        """
        Click purchase button.

        Returns:
            Self for method chaining
        """
        logger.info("Clicking purchase button")
        self.click(self.ORDER_PURCHASE_BUTTON)
        return self

    def close_order_modal(self) -> "CartPage":
        """
        Close order modal.

        Returns:
            Self for method chaining
        """
        logger.info("Closing order modal")
        self.click(self.ORDER_CLOSE_BUTTON)
        self.wait_for_selector(self.ORDER_MODAL, state="hidden")
        return self

    # ========================================
    # Verification Methods
    # ========================================

    def is_on_cart_page(self) -> bool:
        """
        Verify we're on cart page.

        Returns:
            True if on cart page
        """
        return "cart" in self.get_current_url().lower()

    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty.

        Returns:
            True if cart has no items
        """
        return self.get_cart_item_count() == 0
