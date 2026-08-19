"""Component Object Model (COM) / Modal class for the Sign In window."""

from __future__ import annotations

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class SignInModal(BaseModal):
    """COM / Modal representing the Sign In modal window (Увійти).

    Domain facts:
        - Fields: Email, Пароль.
        - Submit button 'Увійти' starts login process.
        - Third-party OAuth buttons available for Google and Facebook.
    """

    # --- LOCATORS ---
    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.ant-modal-content")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: Locator = (
        By.CSS_SELECTOR,
        "div.login-header, div.ant-modal-title",
    )

    # Form inputs
    EMAIL_INPUT: Locator = (By.ID, "basic_email")
    PASSWORD_INPUT: Locator = (By.ID, "basic_password")

    # Submit button and recovery
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button.login-button")
    FORGOT_PASSWORD_BUTTON: Locator = (By.CSS_SELECTOR, "a.restore-password-button")

    # OAuth login links
    GOOGLE_OAUTH_BUTTON: Locator = (By.CSS_SELECTOR, "a[href*='authorize/google']")
    FACEBOOK_OAUTH_BUTTON: Locator = (By.CSS_SELECTOR, "a[href*='authorize/facebook']")

    # Validation errors
    FIELD_ERROR_MESSAGES: Locator = (By.CSS_SELECTOR, "div.ant-form-item-explain-error")
    TOAST_ERROR_MESSAGE: Locator = (
        By.CSS_SELECTOR,
        "div.ant-message-custom-content.ant-message-error",
    )
    FIELD_ERROR_ICON: Locator = (
        By.CSS_SELECTOR,
        "div.ant-form-item.login-input.ant-form-item-has-error .ant-form-item-feedback-icon-error",
    )

    @allure.step("Check if Sign In modal is displayed")
    def is_displayed(self) -> bool:
        """Check if the sign-in modal window is visible on screen."""
        if self.root:
            return self.root.is_displayed()
        try:
            return self._wait_visible(self.MODAL_CONTENT).is_displayed()
        except TimeoutException:
            return False

    @allure.step("Enter Email: '{email}'")
    def enter_email(self, email: str) -> SignInModal:
        """Type value into Email input field with safe clear."""
        element = self._find_element(self.EMAIL_INPUT)
        self.clear(element)
        element.send_keys(email)
        return self

    @allure.step("Enter Password (Пароль)")
    def enter_password(self, password: str) -> SignInModal:
        """Type value into Password input field with safe clear."""
        element = self._find_element(self.PASSWORD_INPUT)
        self.clear(element)
        element.send_keys(password)
        return self

    @allure.step("Fill login form")
    def fill_login_form(self, email: str, password: str) -> SignInModal:
        """Fill both email and password fields in the sign in form."""
        self.enter_email(email)
        self.enter_password(password)
        return self

    @allure.step("Check if Submit button ('Увійти') is enabled")
    def is_submit_button_enabled(self) -> bool:
        """Verify whether the sign in submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click Submit button ('Увійти')")
    def click_submit(self) -> None:
        """Click the sign in submit button with explicit wait."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    @allure.step("Click 'Forgot password?' ('Забули пароль?') link")
    def click_forgot_password(self) -> None:
        """Click the forgot password link with explicit wait."""
        self._wait_clickable(self.FORGOT_PASSWORD_BUTTON).click()

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the X button in top right."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Click Google OAuth sign-in link")
    def click_google_oauth(self) -> None:
        """Click the Google sign-in button with explicit wait."""
        self._wait_clickable(self.GOOGLE_OAUTH_BUTTON).click()

    @allure.step("Click Facebook OAuth sign-in link")
    def click_facebook_oauth(self) -> None:
        """Click the Facebook sign-in button with explicit wait."""
        self._wait_clickable(self.FACEBOOK_OAUTH_BUTTON).click()

    @allure.step("Get all displayed validation error messages in the form")
    def get_error_messages(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages."""
        elements = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [elem.text.strip() for elem in elements if elem.is_displayed()]

    @allure.step("Wait for login toast error message to appear")
    def wait_for_login_error(self) -> str:
        """Wait until the login error toast notification appears and return its text."""
        try:
            return self.wait.until(
                lambda _: self._find_element(self.TOAST_ERROR_MESSAGE).text.strip() or False
            )
        except TimeoutException:
            return ""

    @allure.step("Get number of validation error icons")
    def get_validation_error_count(self) -> int:
        """Return the number of displayed validation error icons."""
        elements = self._find_elements(self.FIELD_ERROR_ICON)
        return sum(1 for element in elements if element.is_displayed())

    @allure.step("Wait for login toast error message to appear")
    def wait_for_login_error(self) -> str:
        """Wait until the login error toast notification appears and return its text."""
        try:
            return self.wait.until(
                lambda _: self._find_element(self.TOAST_ERROR_MESSAGE).text.strip() or False
            )
        except TimeoutException:
            return ""
