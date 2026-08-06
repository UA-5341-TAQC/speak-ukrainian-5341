from selenium.webdriver.remote.webdriver import WebDriver

from pages.base import Base


class BaseModal(Base):
    """Base class for all modals."""

    def __init__(self, driver: WebDriver):
        """Initialize the base modal with a WebDriver."""
        super().__init__(driver)
