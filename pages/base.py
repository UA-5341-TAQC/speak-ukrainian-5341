"""Base class for all pages and components."""

import platform
import time
from typing import Literal

from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data.config import Config
from pages.types import Locator


class Base:
    """Base class for all pages and component objects."""

    driver: WebDriver
    root: WebElement | None

    def __init__(self, context: WebDriver | WebElement) -> None:
        """Initialize the base page with a WebDriver or WebElement context."""
        if isinstance(context, WebDriver):
            self.driver = context
            self.root = None
        elif isinstance(context, WebElement):
            self.root = context
            self.driver = context.parent
        else:
            raise TypeError(f"Invalid context type: {type(context)}")

    def get_current_url(self) -> str:
        """Return the current browser URL, normalized without a trailing slash."""
        return self.driver.current_url.rstrip("/")

    def get_base_url(self) -> str:
        """Return the configured base UI URL without a trailing slash."""
        return Config.BASE_UI_URL.rstrip("/")

    @property
    def _target(self) -> WebDriver | WebElement:
        """Return current context (root WebElement if inside component, else driver)."""
        return self.root if self.root is not None else self.driver

    @property
    def wait(self) -> WebDriverWait[WebDriver]:
        """Return a WebDriverWait instance bound to the active context."""
        return WebDriverWait(
            self.driver,
            Config.EXPLICIT_WAIT,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
                ElementNotInteractableException,
            ),
        )

    def _format_locator(self, locator: Locator) -> Locator:
        """Ensure XPath starts with dot when searching within root context."""
        by, value = locator
        if self.root is not None and by == By.XPATH and value.startswith("//"):
            return (by, "." + value)
        return locator

    def _find_element(self, locator: Locator, from_driver: bool = False) -> WebElement:
        """Find a single element within the current context."""
        target = self._target if not from_driver else self.driver
        return target.find_element(*self._format_locator(locator))

    def _find_elements(self, locator: Locator) -> list[WebElement]:
        """Find all matching elements within the current context."""
        return self._target.find_elements(*self._format_locator(locator))

    def _wait_present(self, locator: Locator) -> WebElement:
        """Wait until an element exists in the active context DOM."""
        return self.wait.until(lambda _: self._find_element(locator))

    def _wait_visible(self, locator: Locator) -> WebElement:
        """Wait until an element is visible within the active context."""

        def _predicate(_: object) -> WebElement | Literal[False]:
            try:
                element = self._find_element(locator)
                return element if element.is_displayed() else False
            except Exception:
                return False

        return self.wait.until(_predicate)

    def _wait_clickable(self, locator: Locator, from_driver: bool = False) -> WebElement:
        """Wait until an element is clickable within the active context."""

        def _predicate(_: object) -> WebElement | Literal[False]:
            try:
                element = self._find_element(locator, from_driver)
                return element if (element.is_displayed() and element.is_enabled()) else False
            except Exception:
                return False

        return self.wait.until(_predicate)

    def _wait_for_url(self, url: str) -> None:
        """Wait until the browser's current URL (ignoring a trailing slash) equals the given URL.

        Args:
            url: The expected URL.
        """
        self.wait.until(lambda d: d.current_url.rstrip("/") == url.rstrip("/"))

    def _scroll_into_view(self, locator: Locator) -> WebElement:
        """Scroll the element matching the locator into view and return it."""
        element = self._wait_present(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )
        return element

    def _get_text(self, locator: Locator) -> str:
        """Wait for an element to be visible and return its text.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The text content of the element.
        """
        return self._wait_visible(locator).text

    def _click(self, locator: Locator) -> None:
        """Wait for an element to be clickable and click it.

        Args:
            locator: Selenium locator of the element.
        """
        self._wait_clickable(locator).click()

    def _fill_input(self, locator: Locator, text: str) -> None:
        """Wait for an input element to be visible, clear it reliably, and enter text.

        Args:
            locator: Selenium locator of the input element.
            text: Text to enter into the input.
        """
        element = self._wait_visible(locator)
        cmd_ctrl = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        element.send_keys(cmd_ctrl + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)

    def _clear(self, element: WebElement) -> None:
        """Clear an input element."""
        element.clear()

    def clear(self, element: WebElement) -> None:
        """Clear an input element using Ctrl+A and Backspace."""
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)

    def _wait_clickable_from_driver(self, locator: Locator) -> WebElement:
        """Wait until an element is clickable using the driver context."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def get_wait(self, timeout: int = 5) -> WebDriverWait[WebDriver]:
        """Get a WebDriverWait instance with the specified timeout."""
        return WebDriverWait(self.driver, timeout)

    @staticmethod
    def _type_slowly(element: WebElement, text: str, delay: float = 0.05) -> None:
        """Type text one character at a time, pausing between keystrokes."""
        for char in text:
            element.send_keys(char)
            time.sleep(delay)
