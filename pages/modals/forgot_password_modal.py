"""Component Object Model (COM) / Modal class for the Forgot Password window."""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class ForgotPasswordModal(BaseModal):
    """COM / Modal representing the Forgot Password modal window (Відновлення пароля).

    Domain facts:
        - Accessible from the SignInModal via the 'Забули пароль?' link.
        - Field: Email (with unique ID 'edit_email').
        - Submit button 'Відновити' triggers recovery process.
    """

    # --- LOCATORS ---
    # Scoped via edit_email to ensure isolation from underlying SignInModal in DOM
    MODAL_CONTENT: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')][.//input[@id='edit_email']]",
    )
    CLOSE_BUTTON: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')]"
        "[.//input[@id='edit_email']]//button[contains(@class, 'ant-modal-close')]",
    )
    MODAL_TITLE: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')][.//input[@id='edit_email']]"
        "//div[contains(@class, 'login-header') or contains(@class, 'ant-modal-title')]",
    )

    # Form inputs
    EMAIL_INPUT: Locator = (By.ID, "edit_email")

    # Submit button
    SUBMIT_BUTTON: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')][.//input[@id='edit_email']]"
        "//button[contains(@class, 'login-button') or contains(., 'Відновити')]",
    )

    # Validation errors
    FIELD_ERROR_MESSAGES: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal-content')][.//input[@id='edit_email']]"
        "//div[contains(@class, 'ant-form-item-explain-error')]",
    )

    @allure.step("Check if Forgot Password modal is displayed")
    def is_displayed(self) -> bool:
        """Check if the forgot password modal window is visible on screen."""
        if self.root:
            return self.root.is_displayed()
        return self._find_element(self.MODAL_CONTENT).is_displayed()

    @allure.step("Enter Email for password recovery: '{email}'")
    def enter_email(self, email: str) -> ForgotPasswordModal:
        """Type value into recovery Email input field with safe clear."""
        element = self._find_element(self.EMAIL_INPUT)
        self.clear(element)
        element.send_keys(email)
        return self

    @allure.step("Check if Submit button ('Відновити') is enabled")
    def is_submit_button_enabled(self) -> bool:
        """Verify whether the recovery submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click Submit button ('Відновити')")
    def click_submit(self) -> None:
        """Click the recovery submit button with explicit wait."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the X button in top right."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Get Forgot Password modal title text")
    def get_title_text(self) -> str:
        """Retrieve the trimmed text of the modal header."""
        return self._find_element(self.MODAL_TITLE).text.strip()

    @allure.step("Get all displayed validation error messages in recovery form")
    def get_error_messages(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages."""
        elements = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [elem.text.strip() for elem in elements if elem.is_displayed()]
