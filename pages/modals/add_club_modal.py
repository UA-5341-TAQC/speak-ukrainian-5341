from __future__ import annotations

from typing import Literal

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class AddClubModal(BaseModal):
    """Page object for the Add Club modal window."""

    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.modal-add-club")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, "div.add-club-header")

    STEPS_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        "div.ant-steps.ant-steps-vertical"
    )

    STEP_BASIC_INFO_TITLE: Locator = (
        By.XPATH,
        ".//div[contains(@class,'ant-steps-item-title')][text()='Основна інформація']",
    )
    STEP_CONTACTS_TITLE: Locator = (
        By.XPATH,
        ".//div[contains(@class,'ant-steps-item-title')][text()='Контакти']",
    )
    STEP_DESCRIPTION_TITLE: Locator = (
        By.XPATH,
        ".//div[contains(@class,'ant-steps-item-title')][text()='Опис']",
    )

    ACTIVE_STEP_TITLE: Locator = (
        By.CSS_SELECTOR,
        ".ant-steps-item-active .ant-steps-item-title"
    )

    NEXT_STEP_BUTTON: Locator = (By.CSS_SELECTOR, "button.add-club-content-next")
    PREV_BUTTON: Locator = (By.CSS_SELECTOR, "button.add-club-content-prev")
    FINISH_BUTTON: Locator = (By.CSS_SELECTOR, "button.add-club-content-next")

    FIELD_ERROR_MESSAGES: Locator = (By.CSS_SELECTOR, "div.ant-form-item-explain-error")

    def is_opened(self) -> bool:
        """Check if the Add Club modal is currently opened."""
        return self._find_element(self.MODAL_CONTENT).is_displayed()

    @allure.step("Close Add Club modal")
    def close(self) -> None:
        """Close the Add Club modal by clicking the close button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Get active step title")
    def get_active_step(self) -> str:
        """Get the title of the currently active step in the Add Club modal."""

        def _title_ready(_: object) -> str | Literal[False]:
            text = self._find_element(self.ACTIVE_STEP_TITLE).text.strip()
            return text if text else False

        title = self.wait.until(_title_ready)
        allure.attach(title, "Active Step")
        return title

    @allure.step("Click 'Наступний крок' button")
    def click_next(self) -> None:
        """Click the 'Next Step' button in the Add Club modal."""
        self._wait_clickable(self.NEXT_STEP_BUTTON).click()

    @allure.step("Click 'Назад' button")
    def click_prev(self) -> None:
        """Click the 'Previous' button to return to Step 1."""
        self._wait_clickable(self.PREV_BUTTON).click()

    @allure.step("Click 'Завершити' button")
    def click_finish(self) -> None:
        """Submit the form and finish the wizard."""
        self._wait_clickable(self.FINISH_BUTTON).click()

    @allure.step("Check if 'Завершити' button is enabled")
    def is_finish_enabled(self) -> bool:
        """Verify whether the finish button is clickable."""
        return self._find_element(self.FINISH_BUTTON).is_enabled()

    @allure.step("Get currently displayed validation error messages")
    def get_errors(self) -> list[str]:
        """Get current validation error messages without waiting."""
        found = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [e.text.strip() for e in found if e.is_displayed()]

    @allure.step("Wait for {expected_count} validation error messages to appear")
    def wait_for_errors(self, expected_count: int) -> list[str]:
        """Wait until exactly expected_count error messages are visible, then return them."""

        def _errors_ready(_: object) -> list | Literal[False]:
            found = self._find_elements(self.FIELD_ERROR_MESSAGES)
            visible = [e.text.strip() for e in found if e.is_displayed()]
            return visible if len(visible) == expected_count else False

        try:
            return self.wait.until(_errors_ready)
        except TimeoutException:
            return self.get_errors()
