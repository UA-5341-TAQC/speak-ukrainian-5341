"""Component Object Model (COM) / Modal class for the Reset Password window."""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class ResetPasswordModal(BaseModal):
    """COM / Modal representing the Reset Password window (Зміна пароля).

    Domain facts:
        - Opened automatically when accessing verifyreset link with token/code.
        - Fields: New password ('edit_password') and Confirm password ('edit_new-password').
        - Submit button 'Змінити пароль' finalizes the password change.
    """

    # --- LOCATORS ---
    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.ant-modal-content")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: Locator = (
        By.XPATH,
        "//div[contains(@class, 'ant-modal')]//*[contains(text(), 'Відновлення паролю')]"
        " | //div[contains(@class, 'ant-modal-title')]",
    )

    # Form inputs
    NEW_PASSWORD_INPUT: Locator = (By.ID, "edit_password")
    CONFIRM_PASSWORD_INPUT: Locator = (By.ID, "edit_new-password")

    # Submit button
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button.submit-button")

    # Validation errors
    FIELD_ERROR_MESSAGES: Locator = (By.CSS_SELECTOR, "div.ant-form-item-explain-error")

    @allure.step("Check if Reset Password modal is displayed")
    def is_displayed(self) -> bool:
        """Check if the reset password modal window is visible on screen."""
        if self.root:
            return self.root.is_displayed()
        return self._find_element(self.MODAL_CONTENT).is_displayed()

    @allure.step("Enter New Password (Введіть новий пароль)")
    def enter_new_password(self, password: str) -> ResetPasswordModal:
        """Type value into New Password input field with safe clear."""
        element = self._find_element(self.NEW_PASSWORD_INPUT)
        self.clear(element)
        element.send_keys(password)
        return self

    @allure.step("Enter Confirm Password (Введіть новий пароль повторно)")
    def enter_confirm_password(self, password: str) -> ResetPasswordModal:
        """Type value into Confirm Password input field with safe clear."""
        element = self._find_element(self.CONFIRM_PASSWORD_INPUT)
        self.clear(element)
        element.send_keys(password)
        return self

    @allure.step("Fill reset password form")
    def fill_reset_form(self, new_password: str, confirm_password: str) -> ResetPasswordModal:
        """Fill both new password and confirmation fields."""
        self.enter_new_password(new_password)
        self.enter_confirm_password(confirm_password)
        return self

    @allure.step("Check if Submit button ('Змінити пароль') is enabled")
    def is_submit_button_enabled(self) -> bool:
        """Verify whether the reset password submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click Submit button ('Змінити пароль')")
    def click_submit(self) -> None:
        """Click the reset password submit button with explicit wait."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the X button in top right."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Get Reset Password modal title text")
    def get_title_text(self) -> str:
        """Retrieve the trimmed text of the modal header."""
        return self._find_element(self.MODAL_TITLE).text.strip()

    @allure.step("Get all displayed validation error messages in reset password form")
    def get_error_messages(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages."""
        elements = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [elem.text.strip() for elem in elements if elem.is_displayed()]
