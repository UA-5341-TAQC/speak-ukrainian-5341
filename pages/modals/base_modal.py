"""Base Component Object Model (COM) class for all modal dialogs."""

from __future__ import annotations

import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base
from pages.types import Locator


class BaseModal(Base):
    """Base Component Object Model (COM) representing an Ant Design modal dialog.

    Encapsulates common structure and behaviors shared by all modals across
    the application:
        - Common container, backdrop (mask), close button, and title locators.
        - Visibility and display status checks.
        - Title retrieval and visibility verification.
        - Dismissal via close button (X), backdrop click, or Escape key.
        - Explicit synchronization for animations and modal disappearance.
    """

    # --- COMMON MODAL LOCATORS ---
    MODAL_CONTAINER: Locator = (By.CSS_SELECTOR, "div.ant-modal")
    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.ant-modal-content")
    MODAL_MASK: Locator = (By.CSS_SELECTOR, "div.ant-modal-mask")
    MODAL_WRAP: Locator = (By.CSS_SELECTOR, "div.ant-modal-wrap")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, "div.ant-modal-title")

    def __init__(self, context: WebDriver | WebElement) -> None:
        """Initialize the base modal with a WebDriver or WebElement context."""
        super().__init__(context)

    def _get_modal_root_locator(self) -> Locator:
        """Resolve the active content or container locator for this modal."""
        for attr in ("MODAL_CONTENT", "MODAL_DIALOG", "MODAL_CONTAINER"):
            if hasattr(self, attr):
                val = getattr(self, attr)
                if isinstance(val, tuple) and len(val) == 2:
                    return (val[0], str(val[1]))
        return self.MODAL_CONTENT

    # --- DISPLAY & VISIBILITY ---

    @allure.step("Check if modal is displayed")
    def is_displayed(self) -> bool:
        """Check whether the modal window is currently visible on screen."""
        if self.root is not None:
            try:
                return bool(self.root.is_displayed())
            except (TimeoutException, NoSuchElementException):
                return False
        try:
            return bool(self._wait_visible(self._get_modal_root_locator()).is_displayed())
        except (TimeoutException, NoSuchElementException):
            return False

    def is_modal_displayed(self) -> bool:
        """Alias for is_displayed for backward compatibility."""
        return bool(self.is_displayed())

    @allure.step("Wait until modal is visible")
    def wait_for_visible(self) -> BaseModal:
        """Wait until the modal dialog becomes visible."""
        self._wait_visible(self._get_modal_root_locator())
        return self

    @allure.step("Wait for backdrop mask to become visible")
    def wait_for_backdrop(self) -> BaseModal:
        """Wait until the modal backdrop mask (div.ant-modal-mask) is visible."""
        self._wait_visible(self.MODAL_MASK)
        return self

    @allure.step("Wait until modal is closed and disappeared")
    def wait_for_closed(self) -> BaseModal:
        """Wait until the modal container and backdrop mask disappear from the DOM."""
        self.wait.until(EC.invisibility_of_element_located(self._get_modal_root_locator()))
        try:
            self.wait.until(EC.invisibility_of_element_located(self.MODAL_MASK))
        except TimeoutException:
            pass
        return self

    # --- TITLE METHODS ---

    @allure.step("Get modal title text")
    def get_title_text(self) -> str:
        """Retrieve the trimmed text of the modal header."""
        return str(self._get_text(self.MODAL_TITLE).strip())

    def get_title(self) -> str:
        """Alias for get_title_text for backward compatibility."""
        return str(self.get_title_text())

    @allure.step("Check if modal title is displayed")
    def is_title_displayed(self) -> bool:
        """Check whether the modal title header is currently visible."""
        try:
            return bool(self._find_element(self.MODAL_TITLE).is_displayed())
        except (TimeoutException, NoSuchElementException):
            return False

    def is_modal_title_displayed(self) -> bool:
        """Alias for is_title_displayed for backward compatibility."""
        return bool(self.is_title_displayed())

    # --- DISMISSAL / CLOSE METHODS ---

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the close button (X)."""
        self._click(self.CLOSE_BUTTON)

    def close_modal(self) -> None:
        """Alias for click_close_button for backward compatibility."""
        self.click_close_button()

    @allure.step("Close modal by clicking outside on backdrop wrap")
    def close_by_backdrop_click(self) -> None:
        """Close the modal by clicking on the outer backdrop wrap area."""
        wrap = self._wait_clickable(self.MODAL_WRAP)
        ActionChains(self.driver).move_to_element_with_offset(wrap, 10, 10).click().perform()

    @allure.step("Close modal by pressing Escape key")
    def close_by_escape(self) -> None:
        """Close the modal by sending the Escape key."""
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
