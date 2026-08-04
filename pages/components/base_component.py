from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base
from pages.types import Locator


class BaseComponent(Base):
    """Base class for all components."""

    def __init__(self, root: WebElement):
        """Initialize the base component with a WebElement root."""
        super().__init__(root)

    def _find_elements(self, locator: Locator) -> list[WebElement]:
        """Find all elements matching locator inside this component root."""
        return self.root.find_elements(*locator)

    # дані функції є в base.py але можуть некоректно працювати для Component Object.
    # WebDriverWait передає в EC  driver. А потрібно self.root.

    def _wait_present(self, locator: Locator) -> WebElement:
        """Wait until an element exists inside this component root."""

        def element_is_present(_driver):
            try:
                return self.root.find_element(*locator)
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        return self.wait.until(element_is_present)

    def _wait_visible(self, locator: Locator) -> WebElement:
        """Wait until an element inside this component root is visible."""

        def element_is_visible(_driver):
            try:
                element = self.root.find_element(*locator)
                return element if element.is_displayed() else False
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        return self.wait.until(element_is_visible)

    def _wait_clickable(self, locator: Locator) -> WebElement:
        """Wait until an element inside this component is visible and enabled."""

        def element_is_clickable(_driver):
            try:
                element = self.root.find_element(*locator)
                if element.is_displayed() and element.is_enabled():
                    return element
                return False
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        return self.wait.until(element_is_clickable)
