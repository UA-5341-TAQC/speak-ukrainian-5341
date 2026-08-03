from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base


class BaseComponent(Base):
    """Base class for all components."""

    def __init__(self, root: WebElement):
        """Initialize the base component with a WebElement root."""
        super().__init__(root)
