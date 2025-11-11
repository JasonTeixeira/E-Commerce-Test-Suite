"""
Base Page Object Model class.

Provides common functionality for all page objects including
element interactions, waits, and utility methods.
"""

from typing import List, Optional

from playwright.sync_api import Page, expect

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Base page object with common functionality for all pages."""

    def __init__(self, page: Page):
        """
        Initialize base page.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.base_url = settings.base_url
        self.timeout = settings.default_timeout

    # ========================================
    # Navigation Methods
    # ========================================

    def navigate_to(self, path: str = "") -> None:
        """
        Navigate to specific path.

        Args:
            path: URL path to navigate to
        """
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    def get_page_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def refresh(self) -> None:
        """Refresh the current page."""
        logger.info("Refreshing page")
        self.page.reload(wait_until="domcontentloaded")

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.page.go_back(wait_until="domcontentloaded")

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.page.go_forward(wait_until="domcontentloaded")

    # ========================================
    # Element Interaction Methods
    # ========================================

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click an element.

        Args:
            selector: Element selector
            timeout: Optional custom timeout
        """
        logger.debug(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout or self.timeout)

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Fill an input field.

        Args:
            selector: Element selector
            text: Text to fill
            timeout: Optional custom timeout
        """
        logger.debug(f"Filling '{selector}' with text")
        self.page.fill(selector, text, timeout=timeout or self.timeout)

    def type_text(
        self, selector: str, text: str, delay: int = 50, timeout: Optional[int] = None
    ) -> None:
        """
        Type text with delay (simulates human typing).

        Args:
            selector: Element selector
            text: Text to type
            delay: Delay between keystrokes in ms
            timeout: Optional custom timeout
        """
        logger.debug(f"Typing text into '{selector}'")
        self.page.type(selector, text, delay=delay, timeout=timeout or self.timeout)

    def select_option(
        self, selector: str, value: str, timeout: Optional[int] = None
    ) -> None:
        """
        Select option from dropdown.

        Args:
            selector: Select element selector
            value: Option value to select
            timeout: Optional custom timeout
        """
        logger.debug(f"Selecting option '{value}' from '{selector}'")
        self.page.select_option(selector, value, timeout=timeout or self.timeout)

    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Check a checkbox.

        Args:
            selector: Checkbox selector
            timeout: Optional custom timeout
        """
        logger.debug(f"Checking checkbox: {selector}")
        self.page.check(selector, timeout=timeout or self.timeout)

    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Uncheck a checkbox.

        Args:
            selector: Checkbox selector
            timeout: Optional custom timeout
        """
        logger.debug(f"Unchecking checkbox: {selector}")
        self.page.uncheck(selector, timeout=timeout or self.timeout)

    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over an element.

        Args:
            selector: Element selector
            timeout: Optional custom timeout
        """
        logger.debug(f"Hovering over: {selector}")
        self.page.hover(selector, timeout=timeout or self.timeout)

    def double_click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Double-click an element.

        Args:
            selector: Element selector
            timeout: Optional custom timeout
        """
        logger.debug(f"Double-clicking: {selector}")
        self.page.dblclick(selector, timeout=timeout or self.timeout)

    # ========================================
    # Element Query Methods
    # ========================================

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get element text content.

        Args:
            selector: Element selector
            timeout: Optional custom timeout

        Returns:
            Element text content
        """
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout or self.timeout)
        return element.inner_text()

    def get_attribute(
        self, selector: str, attribute: str, timeout: Optional[int] = None
    ) -> Optional[str]:
        """
        Get element attribute value.

        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Optional custom timeout

        Returns:
            Attribute value or None
        """
        element = self.page.locator(selector)
        element.wait_for(state="attached", timeout=timeout or self.timeout)
        return element.get_attribute(attribute)

    def get_value(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get input element value.

        Args:
            selector: Input element selector
            timeout: Optional custom timeout

        Returns:
            Input value
        """
        return self.get_attribute(selector, "value", timeout) or ""

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds

        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_hidden(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is hidden.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds

        Returns:
            True if hidden, False otherwise
        """
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
            return True
        except Exception:
            return False

    def is_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled.

        Args:
            selector: Element selector

        Returns:
            True if enabled, False otherwise
        """
        return self.page.locator(selector).is_enabled()

    def is_disabled(self, selector: str) -> bool:
        """
        Check if element is disabled.

        Args:
            selector: Element selector

        Returns:
            True if disabled, False otherwise
        """
        return self.page.locator(selector).is_disabled()

    def is_checked(self, selector: str) -> bool:
        """
        Check if checkbox/radio is checked.

        Args:
            selector: Element selector

        Returns:
            True if checked, False otherwise
        """
        return self.page.locator(selector).is_checked()

    def count_elements(self, selector: str) -> int:
        """
        Count number of elements matching selector.

        Args:
            selector: Element selector

        Returns:
            Number of matching elements
        """
        return self.page.locator(selector).count()

    # ========================================
    # Wait Methods
    # ========================================

    def wait_for_selector(
        self, selector: str, state: str = "visible", timeout: Optional[int] = None
    ) -> None:
        """
        Wait for element to reach specified state.

        Args:
            selector: Element selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Optional custom timeout
        """
        logger.debug(f"Waiting for '{selector}' to be {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout or self.timeout)

    def wait_for_url(self, url: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern.

        Args:
            url: URL pattern to wait for
            timeout: Optional custom timeout
        """
        logger.debug(f"Waiting for URL: {url}")
        self.page.wait_for_url(url, timeout=timeout or self.timeout)

    def wait_for_load_state(
        self, state: str = "load", timeout: Optional[int] = None
    ) -> None:
        """
        Wait for page load state.

        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Optional custom timeout
        """
        self.page.wait_for_load_state(state, timeout=timeout or self.timeout)

    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for specified timeout.

        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_timeout(timeout)

    # ========================================
    # Assertion Methods
    # ========================================

    def expect_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Assert element is visible.

        Args:
            selector: Element selector
            timeout: Optional custom timeout
        """
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout or self.timeout)

    def expect_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Assert element is hidden.

        Args:
            selector: Element selector
            timeout: Optional custom timeout
        """
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout or self.timeout)

    def expect_text(
        self, selector: str, text: str, timeout: Optional[int] = None
    ) -> None:
        """
        Assert element contains text.

        Args:
            selector: Element selector
            text: Expected text
            timeout: Optional custom timeout
        """
        expect(self.page.locator(selector)).to_contain_text(
            text, timeout=timeout or self.timeout
        )

    def expect_value(
        self, selector: str, value: str, timeout: Optional[int] = None
    ) -> None:
        """
        Assert input has value.

        Args:
            selector: Input selector
            value: Expected value
            timeout: Optional custom timeout
        """
        expect(self.page.locator(selector)).to_have_value(
            value, timeout=timeout or self.timeout
        )

    def expect_url(self, url: str, timeout: Optional[int] = None) -> None:
        """
        Assert page URL matches pattern.

        Args:
            url: Expected URL pattern
            timeout: Optional custom timeout
        """
        expect(self.page).to_have_url(url, timeout=timeout or self.timeout)

    def expect_title(self, title: str, timeout: Optional[int] = None) -> None:
        """
        Assert page title matches.

        Args:
            title: Expected title
            timeout: Optional custom timeout
        """
        expect(self.page).to_have_title(title, timeout=timeout or self.timeout)

    # ========================================
    # Screenshot Methods
    # ========================================

    def take_screenshot(self, path: str, full_page: bool = True) -> bytes:
        """
        Take screenshot of current page.

        Args:
            path: Path to save screenshot
            full_page: Whether to capture full page

        Returns:
            Screenshot bytes
        """
        logger.info(f"Taking screenshot: {path}")
        return self.page.screenshot(path=path, full_page=full_page)

    def take_element_screenshot(self, selector: str, path: str) -> bytes:
        """
        Take screenshot of specific element.

        Args:
            selector: Element selector
            path: Path to save screenshot

        Returns:
            Screenshot bytes
        """
        logger.info(f"Taking element screenshot: {selector}")
        return self.page.locator(selector).screenshot(path=path)

    # ========================================
    # JavaScript Methods
    # ========================================

    def execute_script(self, script: str, *args) -> any:
        """
        Execute JavaScript in page context.

        Args:
            script: JavaScript code
            *args: Arguments to pass to script

        Returns:
            Script return value
        """
        return self.page.evaluate(script, *args)

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll element into view.

        Args:
            selector: Element selector
        """
        self.page.locator(selector).scroll_into_view_if_needed()

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.execute_script("window.scrollTo(0, 0)")

    # ========================================
    # Utility Methods
    # ========================================

    def get_all_links(self) -> List[str]:
        """
        Get all links on the page.

        Returns:
            List of href attributes
        """
        return self.page.eval_on_selector_all("a[href]", "elements => elements.map(e => e.href)")

    def accept_alert(self) -> None:
        """Accept browser alert dialog."""
        self.page.on("dialog", lambda dialog: dialog.accept())

    def dismiss_alert(self) -> None:
        """Dismiss browser alert dialog."""
        self.page.on("dialog", lambda dialog: dialog.dismiss())

    def get_alert_text(self) -> Optional[str]:
        """Get alert dialog text."""
        alert_text = None

        def handle_dialog(dialog):
            nonlocal alert_text
            alert_text = dialog.message
            dialog.accept()

        self.page.on("dialog", handle_dialog)
        return alert_text
