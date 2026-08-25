import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base
from pages.components.header.header_component import HeaderComponent
from pages.components.header_lower import HeaderLower
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
    HEADER_LOWER_ROOT: Locator = (By.CSS_SELECTOR, ".lower-header-box")

    def __init__(self, driver: WebDriver):
        """Initialize the base page with a WebDriver."""
        super().__init__(driver)

    @allure.step("Refresh the browser page")
    def refresh(self) -> None:
        """Refresh the current browser page."""
        self.driver.refresh()

    def get_current_window_handle(self) -> str:
        """Get the current window handle."""
        return self.driver.current_window_handle

    def get_window_handles(self) -> list[str]:
        """Get all window handles."""
        return self.driver.window_handles

    @allure.step("Switch to window")
    def switch_to_window(self, window_handle: str) -> None:
        """Switch to the specified window handle."""
        self.driver.switch_to.window(window_handle)

    @allure.step("Wait for {expected_number_of_windows} windows to be opened")
    def wait_for_new_window(self, expected_number_of_windows: int) -> None:
        """Wait until the number of windows equals the expected number."""
        self.wait.until(EC.number_of_windows_to_be(expected_number_of_windows))

    @property
    def header(self) -> HeaderComponent:
        """Get the header component."""
        header_element = self._find_element(self.HEADER_ROOT)
        return HeaderComponent(header_element)

    @property
    def header_lower(self) -> HeaderLower:
        """Get the lower header component."""
        header_element = self._find_element(self.HEADER_LOWER_ROOT)
        return HeaderLower(header_element)

    def get_success_message_text(self) -> str:
        """Get the text of the global success toast message."""
        return self._get_text(self.success_message)

    def get_error_message_text(self) -> str:
        """Get the text of the global error toast message."""
        return self._get_text(self.error_message)
