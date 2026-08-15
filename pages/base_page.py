import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

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

    @allure.step("Refresh the browser page")
    def refresh(self) -> None:
        """Refresh the current browser page."""
        self.driver.refresh()
    @property
    def header(self) -> HeaderComponent:
        """Get the header component."""
        header_element = self._find_element(self.HEADER_ROOT)
        return HeaderComponent(header_element)

    def get_success_message_text(self) -> str:
        """Get the text of the global success toast message."""
        return self._get_text(self.success_message)

    def get_error_message_text(self) -> str:
        """Get the text of the global error toast message."""
        return self._get_text(self.error_message)

    def get_wait(self, timeout: int = 5) -> WebDriverWait:
        """Get a WebDriverWait instance with the specified timeout."""
        return WebDriverWait(self.driver, timeout)

    def scroll_to_element(self, locator: Locator) -> None:
        """Scroll the specified element into view."""
        element = self._wait_visible(locator)
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'nearest'
            });
            """,
            element,
        )
