"""Base component class for all components in the application."""

from selenium.webdriver.remote.webelement import WebElement

from pages.base import Base


class BaseComponent(Base):
    """Base class for all component objects."""

    root: WebElement  # Type narrowing for mypy: root cannot be None in components

    def __init__(self, root: WebElement) -> None:
        """Initialize component with root element."""
        super().__init__(root)
        self.root = root  # Explicit assignment guarantees WebElement type for mypy
