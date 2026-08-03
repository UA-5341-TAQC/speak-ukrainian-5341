from selenium.webdriver.remote.webdriver import WebDriver

from pages.base import Base


class BasePage(Base):
    """Base class for all pages."""

    def __init__(self, driver: WebDriver):
        """Initialize the base page with a WebDriver."""
        super().__init__(driver)
