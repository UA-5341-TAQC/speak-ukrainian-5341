"""Base component class for all components in the application."""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base
from pages.types import Locator


class BaseComponent(Base):
    """Base class for all component objects."""

    def __init__(self, root: WebElement):
        """Initialize component with root element."""
        super().__init__(root)

    def _wait_present(self, locator: Locator) -> WebElement:
        """Wait until an element exists inside this component root."""
        return self.wait.until(lambda _: self.root.find_element(*locator))

    def _wait_visible(self, locator: Locator) -> WebElement:
        """Wait until an element inside this component root is visible."""
        return self.wait.until(
            lambda driver: EC.visibility_of(self.root.find_element(*locator))(driver)
        )

    def _wait_clickable(self, locator: Locator) -> WebElement:
        """Wait until an element inside this component root is clickable."""
        return self.wait.until(
            lambda driver: EC.element_to_be_clickable(self.root.find_element(*locator))(driver)
        )
