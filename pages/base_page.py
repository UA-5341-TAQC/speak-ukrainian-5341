from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base import Base
from pages.components.header_component import HeaderComponent
from pages.types import Locator


class BasePage(Base):
    """Base class for all pages."""

    success_message: Locator = (
        By.CSS_SELECTOR,
        "div.ant-message-success span:not(.anticon)",
    )
    error_message: Locator = (
        By.CSS_SELECTOR,
        "div.ant-message-error span:not(.anticon)",
    )

    HEADER_ROOT: Locator = (By.CSS_SELECTOR, "header.header")

    def __init__(self, driver: WebDriver):
        """Initialize the base page with a WebDriver."""
        super().__init__(driver)

    @property
    def header(self) -> HeaderComponent:
        """Get HeaderComponent instance for the site header."""
        root = self._find_element(self.HEADER_ROOT)
        return HeaderComponent(root)

    def get_success_message_text(self) -> str:
        """Get the text of the global success toast message."""
        return self._get_text(self.success_message)

    def get_error_message_text(self) -> str:
        """Get the text of the global error toast message."""
        return self._get_text(self.error_message)
