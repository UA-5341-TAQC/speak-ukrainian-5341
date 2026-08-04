"""Base class for all pages."""

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

    def _wait_clickable(self, locator: Locator) -> WebElement:
        """Wait until an element matching the locator is clickable.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The clickable WebElement.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))
