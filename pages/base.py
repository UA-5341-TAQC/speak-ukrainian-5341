"""Base class for all pages."""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Base:
    """Base class for all pages."""

    driver: WebDriver
    root: WebElement | None

    def __init__(self, context: WebDriver | WebElement):
        """Initialize the base page with a WebDriver or WebElement context."""
        if isinstance(context, WebDriver):
            self.driver = context
            self.root = None
        if isinstance(context, WebElement):
            self.root = context
            self.driver = context.parent
