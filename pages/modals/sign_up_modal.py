"""Component Object Model (COM) / Modal class for the Registration window."""

from __future__ import annotations

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class SignUpModal(BaseModal):
    """COM / Modal representing the Registration modal window (Реєстрація).

    Domain facts:
        - Role radios: Відвідувач (default, checked) and Керівник.
        - Fields (all required): Прізвище, Ім'я, Телефон, Email, Пароль, Підтвердження паролю.
        - Submit button 'Зареєструватися' is disabled until the whole form is valid.
        - Third-party OAuth buttons available for Google and Facebook.
    """

    # --- LOCATORS ---
    MODAL_CONTENT: Locator = (By.CSS_SELECTOR, "div.ant-modal-content")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: Locator = (
        By.CSS_SELECTOR,
        "div.registration-header, div.ant-modal-title",
    )

    # Role radios (clicking label wrapper in Ant Design is more reliable than hidden input)
    # Note: XPath starts with dot (.) to preserve COM encapsulation within self.root
    ROLE_USER_RADIO_LABEL: Locator = (By.XPATH, ".//label[.//input[@value='ROLE_USER']]")
    ROLE_MANAGER_RADIO_LABEL: Locator = (
        By.XPATH,
        ".//label[.//input[@value='ROLE_MANAGER']]",
    )
    ROLE_USER_RADIO_INPUT: Locator = (By.CSS_SELECTOR, "input[value='ROLE_USER']")
    ROLE_MANAGER_RADIO_INPUT: Locator = (By.CSS_SELECTOR, "input[value='ROLE_MANAGER']")

    # Form inputs
    LAST_NAME_INPUT: Locator = (By.ID, "lastName")
    FIRST_NAME_INPUT: Locator = (By.ID, "firstName")
    PHONE_INPUT: Locator = (By.ID, "phone")
    EMAIL_INPUT: Locator = (By.ID, "email")
    PASSWORD_INPUT: Locator = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT: Locator = (By.ID, "confirm")

    # Submit button
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button.registration-button")

    # OAuth login links
    GOOGLE_OAUTH_BUTTON: Locator = (By.CSS_SELECTOR, "a[href*='authorize/google']")
    FACEBOOK_OAUTH_BUTTON: Locator = (By.CSS_SELECTOR, "a[href*='authorize/facebook']")

    # Validation errors
    FIELD_ERROR_MESSAGES: Locator = (By.CSS_SELECTOR, "div.ant-form-item-explain-error")

    # Success icon for each field
    SUCCESS_ICON_LAST_NAME: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#lastName) .ant-form-item-feedback-icon-success",
    )

    SUCCESS_ICON_FIRST_NAME: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#firstName) .ant-form-item-feedback-icon-success",
    )

    SUCCESS_ICON_PHONE: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#phone) .ant-form-item-feedback-icon-success",
    )

    SUCCESS_ICON_EMAIL: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#email) .ant-form-item-feedback-icon-success",
    )

    SUCCESS_ICON_PASSWORD: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#password) .ant-form-item-feedback-icon-success",
    )

    SUCCESS_ICON_CONFIRM_PASSWORD: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#confirm) .ant-form-item-feedback-icon-success",
    )

    # Error icon for each field
    ERROR_ICON_LAST_NAME: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#lastName) .ant-form-item-feedback-icon-error",
    )

    ERROR_ICON_FIRST_NAME: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#firstName) .ant-form-item-feedback-icon-error",
    )

    ERROR_ICON_PHONE: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#phone) .ant-form-item-feedback-icon-error",
    )

    ERROR_ICON_EMAIL: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#email) .ant-form-item-feedback-icon-error",
    )

    ERROR_ICON_PASSWORD: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#password) .ant-form-item-feedback-icon-error",
    )

    ERROR_ICON_CONFIRM_PASSWORD: Locator = (
        By.CSS_SELECTOR,
        ".ant-form-item:has(#confirm) .ant-form-item-feedback-icon-error",
    )

    # Validation error for phone
    FIELD_ERROR_MESSAGES_PHONE: Locator = (
        By.XPATH,
        "//div[@id='phone_help']/div[@class='ant-form-item-explain-error']",
    )

    @allure.step("Check if Registration modal is displayed")
    def is_displayed(self) -> bool:
        """Check if the registration modal window is visible on screen."""
        return self._wait_visible(self.MODAL_CONTENT).is_displayed()

    @allure.step("Select role: Відвідувач (ROLE_USER)")
    def select_visitor_role(self) -> SignUpModal:
        """Select the 'Відвідувач' role radio button with explicit wait."""
        self._wait_clickable(self.ROLE_USER_RADIO_LABEL).click()
        return self

    @allure.step("Select role: Керівник (ROLE_MANAGER)")
    def select_manager_role(self) -> SignUpModal:
        """Select the 'Керівник' role radio button with explicit wait."""
        self._wait_clickable(self.ROLE_MANAGER_RADIO_LABEL).click()
        return self

    @allure.step("Check if 'Відвідувач' role is selected")
    def is_visitor_role_selected(self) -> bool:
        """Check whether 'Відвідувач' role is currently selected."""
        return self._find_element(self.ROLE_USER_RADIO_INPUT).is_selected()

    @allure.step("Check if 'Керівник' role is selected")
    def is_manager_role_selected(self) -> bool:
        """Check whether 'Керівник' role is currently selected."""
        return self._find_element(self.ROLE_MANAGER_RADIO_INPUT).is_selected()

    @allure.step("Enter Last Name (Прізвище): '{last_name}'")
    def enter_last_name(self, last_name: str) -> SignUpModal:
        """Type value into Last Name input field with React event safe clear."""
        element = self._find_element(self.LAST_NAME_INPUT)
        self.clear(element)
        element.send_keys(last_name)
        return self

    @allure.step("Enter First Name (Ім'я): '{first_name}'")
    def enter_first_name(self, first_name: str) -> SignUpModal:
        """Type value into First Name input field with React event safe clear."""
        element = self._find_element(self.FIRST_NAME_INPUT)
        self.clear(element)
        element.send_keys(first_name)
        return self

    @allure.step("Enter Phone (Телефон): '{phone}'")
    def enter_phone(self, phone: str) -> SignUpModal:
        """Type value into Phone input field (Ukrainian format e.g. 0991234567)."""
        element = self._find_element(self.PHONE_INPUT)
        self.clear(element)
        element.send_keys(phone)
        return self

    @allure.step("Enter Email: '{email}'")
    def enter_email(self, email: str) -> SignUpModal:
        """Type value into Email input field with React event safe clear."""
        element = self._find_element(self.EMAIL_INPUT)
        self.clear(element)
        element.send_keys(email)
        return self

    @allure.step("Enter Password (Пароль)")
    def enter_password(self, password: str) -> SignUpModal:
        """Type value into Password input field with React event safe clear."""
        element = self._find_element(self.PASSWORD_INPUT)
        self.clear(element)
        element.send_keys(password)
        return self

    @allure.step("Enter Confirm Password (Підтвердження паролю)")
    def enter_confirm_password(self, confirm_password: str) -> SignUpModal:
        """Type value into Confirm Password input field with React event safe clear."""
        element = self._find_element(self.CONFIRM_PASSWORD_INPUT)
        self.clear(element)
        element.send_keys(confirm_password)
        return self

    @allure.step("Fill full registration form (role: {role})")
    def fill_registration_form(
        self,
        last_name: str,
        first_name: str,
        phone: str,
        email: str,
        password: str,
        confirm_password: str,
        role: str = "user",
    ) -> SignUpModal:
        """Fill all fields in the registration form."""
        if role.lower() in ("manager", "керівник"):
            self.select_manager_role()
        else:
            self.select_visitor_role()

        self.enter_last_name(last_name)
        self.enter_first_name(first_name)
        self.enter_phone(phone)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        return self

    @allure.step("Check if Submit button ('Зареєструватися') is enabled")
    def is_submit_button_enabled(self) -> bool:
        """Verify whether the registration submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click Submit button ('Зареєструватися')")
    def click_submit(self) -> None:
        """Click the registration submit button with explicit wait."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the X button in top right."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Click Google OAuth registration link")
    def click_google_oauth(self) -> None:
        """Click the Google login/register button with explicit wait."""
        self._wait_clickable(self.GOOGLE_OAUTH_BUTTON).click()

    @allure.step("Click Facebook OAuth registration link")
    def click_facebook_oauth(self) -> None:
        """Click the Facebook login/register button with explicit wait."""
        self._wait_clickable(self.FACEBOOK_OAUTH_BUTTON).click()

    @allure.step("Get all displayed validation error messages in the form")
    def get_error_messages(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages."""
        elements = self._find_elements(self.FIELD_ERROR_MESSAGES)
        return [elem.text.strip() for elem in elements if elem.is_displayed()]

    @allure.step("Check whether successful icon for Last Name is visible")
    def is_successfull_icon_visible_last_name(self) -> bool:
        """Check if the successful icon for last name is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_LAST_NAME).is_displayed()

    @allure.step("Check whether successful icon for First Name is visible")
    def is_successfull_icon_visible_first_name(self) -> bool:
        """Check if the successful icon for first name is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_FIRST_NAME).is_displayed()

    @allure.step("Check whether successful icon for email is visible")
    def is_successfull_icon_visible_email(self) -> bool:
        """Check if the successful icon for email is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_EMAIL).is_displayed()

    @allure.step("Check whether successful icon for phone is visible")
    def is_successfull_icon_visible_phone(self) -> bool:
        """Check if the successful icon for phone is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_PHONE).is_displayed()

    @allure.step("Check whether successful icon for password is visible")
    def is_successfull_icon_visible_password(self) -> bool:
        """Check if the successful icon for password is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_PASSWORD).is_displayed()

    @allure.step("Check whether successful icon for confirm password is visible")
    def is_successfull_icon_visible_password_confirm(self) -> bool:
        """Check if the successful icon for password is visible on screen."""
        return self._wait_visible(self.SUCCESS_ICON_CONFIRM_PASSWORD).is_displayed()

    @allure.step("Check whether error icon for Last Name is visible")
    def is_error_icon_visible_last_name(self) -> bool:
        """Check if the error icon for last name is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_LAST_NAME).is_displayed()

    @allure.step("Check whether error icon for First Name is visible")
    def is_error_icon_visible_first_name(self) -> bool:
        """Check if the error icon for first name is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_FIRST_NAME).is_displayed()

    @allure.step("Check whether error icon for email is visible")
    def is_error_icon_visible_email(self) -> bool:
        """Check if the error icon for email is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_EMAIL).is_displayed()

    @allure.step("Check whether error icon for phone is visible")
    def is_error_icon_visible_phone(self) -> bool:
        """Check if the error icon for phone is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_PHONE).is_displayed()

    @allure.step("Check whether error icon for password is visible")
    def is_error_icon_visible_password(self) -> bool:
        """Check if the error icon for password is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_PASSWORD).is_displayed()

    @allure.step("Check whether error icon for confirm password is visible")
    def is_error_icon_visible_password_confirm(self) -> bool:
        """Check if the error icon for password is visible on screen."""
        return self._wait_visible(self.ERROR_ICON_CONFIRM_PASSWORD).is_displayed()

    @allure.step("Check whether validation error messages in the form for phone field is visible")
    def is_error_message_displayed_phone(self) -> bool:
        """Check if the error messages in the form for phone field is visible on screen."""
        return self._wait_visible(self.FIELD_ERROR_MESSAGES_PHONE).is_displayed()

    @allure.step("Get all displayed validation error messages in the form for phone field")
    def get_error_messages_phone(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages for phone field."""
        if self.is_error_message_displayed_phone():
            elements = self._find_elements(self.FIELD_ERROR_MESSAGES_PHONE)
            return [elem.text.strip() for elem in elements if elem.is_displayed()]
        else:
            return []

    @allure.step("Wait for validation error to appear")
    def wait_for_error_message(self, expected_error: str) -> None:
        """Wait until a specific validation error message is displayed."""

        def _is_error_present(_: object) -> bool:
            return expected_error in self.get_error_messages()

        self.wait.until(_is_error_present)

    @allure.step("Wait for submit button to become disabled")
    def wait_for_submit_button_disabled(self) -> None:
        """Wait until the submit button becomes disabled (handling React state delays)."""

        def _is_button_disabled(_: object) -> bool:
            return not self.is_submit_button_enabled()

        self.wait.until(_is_button_disabled)

    @allure.step("Type and clear a field")
    def type_and_clear(self, field_locator: Locator) -> SignUpModal:
        """Type a character then delete it."""
        element = self._find_element(field_locator)
        element.click()
        element.send_keys("a")
        element.send_keys(Keys.BACKSPACE)
        return self

    @allure.step("Wait for a specific validation error to appear")
    def wait_for_specific_error(self, expected_error: str) -> list[str]:
        """Wait until the expected error message appears among the displayed errors."""
        try:

            def _check_error(_: object) -> list[str]:
                return (
                    self.get_error_messages() if expected_error in self.get_error_messages() else []
                )

            result: list[str] = self.wait.until(_check_error)
            return result
        except TimeoutException:
            return self.get_error_messages() or []
