"""Base class for all pages."""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data.config import Config
from pages.types import Locator


class Base:
    """Base class for all pages."""

    driver: WebDriver
    root: WebElement | None
    wait: WebDriverWait[WebDriver]

    def __init__(self, context: WebDriver | WebElement):
        """Initialize the base page with a WebDriver or WebElement context."""
        if isinstance(context, WebDriver):
            self.driver = context
            self.root = None
        if isinstance(context, WebElement):
            self.root = context
            self.driver = context.parent
        self.wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)

    def _find_element(self, locator: Locator) -> WebElement:
        """Find a single element within the page or component."""
        if self.root:
            return self.root.find_element(*locator)
        return self.driver.find_element(*locator)

    def _find_elements(self, locator: Locator) -> list[WebElement]:
        """Find all matching elements within the page or component."""
        if self.root:
            return self.root.find_elements(*locator)
        return self.driver.find_elements(*locator)

    def _wait_clickable(self, locator: Locator) -> WebElement:
        """Wait until an element matching the locator is clickable.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The clickable WebElement.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _wait_visible(self, locator: Locator) -> WebElement:
        """Wait until an element matching the locator is visible.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The visible WebElement.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _get_text(self, locator: Locator) -> str:
        """Wait for an element to be visible and return its text.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The text content of the element.
        """
        return self._wait_visible(locator).text

    def _clear(self, element: WebElement) -> None:
        """Clear an input element."""
        element.clear()

    def clear(self, element: WebElement) -> None:
        """Clear an input element using Ctrl+A and Backspace to trigger React events.

        Args:
            element: The WebElement input field to clear.
        """
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
