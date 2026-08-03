"""Component Object Model (COM) / Modal class for the Registration window."""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.modals.base_modal import BaseModal


class SignUpModal(BaseModal):
    """COM / Modal representing the Registration modal window (Реєстрація).

    Domain facts:
        - Role radios: Відвідувач (default, checked) and Керівник.
        - Fields (all required): Прізвище, Ім'я, Телефон, Email, Пароль, Підтвердження паролю.
        - Submit button 'Зареєструватися' is disabled until the whole form is valid.
        - Third-party OAuth buttons available for Google and Facebook.
    """

    # --- LOCATORS ---
    MODAL_CONTENT: tuple[str, str] = (By.CSS_SELECTOR, "div.ant-modal-content")
    CLOSE_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, "button.ant-modal-close")
    MODAL_TITLE: tuple[str, str] = (
        By.CSS_SELECTOR,
        "div.registration-header, div.ant-modal-title",
    )

    # Role radios (clicking label wrapper in Ant Design is more reliable than hidden input)
    ROLE_USER_RADIO_LABEL: tuple[str, str] = (By.XPATH, "//label[.//input[@value='ROLE_USER']]")
    ROLE_MANAGER_RADIO_LABEL: tuple[str, str] = (
        By.XPATH,
        "//label[.//input[@value='ROLE_MANAGER']]",
    )
    ROLE_USER_RADIO_INPUT: tuple[str, str] = (By.CSS_SELECTOR, "input[value='ROLE_USER']")
    ROLE_MANAGER_RADIO_INPUT: tuple[str, str] = (By.CSS_SELECTOR, "input[value='ROLE_MANAGER']")

    # Form inputs
    LAST_NAME_INPUT: tuple[str, str] = (By.ID, "lastName")
    FIRST_NAME_INPUT: tuple[str, str] = (By.ID, "firstName")
    PHONE_INPUT: tuple[str, str] = (By.ID, "phone")
    EMAIL_INPUT: tuple[str, str] = (By.ID, "email")
    PASSWORD_INPUT: tuple[str, str] = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT: tuple[str, str] = (By.ID, "confirm")

    # Submit button
    SUBMIT_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, "button.registration-button")

    # OAuth login links
    GOOGLE_OAUTH_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, "a[href*='authorize/google']")
    FACEBOOK_OAUTH_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, "a[href*='authorize/facebook']")

    # Validation errors
    FIELD_ERROR_MESSAGES: tuple[str, str] = (By.CSS_SELECTOR, "div.ant-form-item-explain-error")

    @allure.step("Check if Registration modal is displayed")
    def is_displayed(self) -> bool:
        """Check if the registration modal window is visible on screen."""
        elements = self.driver.find_elements(*self.MODAL_CONTENT)
        return len(elements) > 0 and elements[0].is_displayed()

    @allure.step("Select role: Відвідувач (ROLE_USER)")
    def select_visitor_role(self) -> SignUpModal:
        """Select the 'Відвідувач' role radio button."""
        self.driver.find_element(*self.ROLE_USER_RADIO_LABEL).click()
        return self

    @allure.step("Select role: Керівник (ROLE_MANAGER)")
    def select_manager_role(self) -> SignUpModal:
        """Select the 'Керівник' role radio button."""
        self.driver.find_element(*self.ROLE_MANAGER_RADIO_LABEL).click()
        return self

    @allure.step("Check if 'Відвідувач' role is selected")
    def is_visitor_role_selected(self) -> bool:
        """Check whether 'Відвідувач' role is currently selected."""
        return self.driver.find_element(*self.ROLE_USER_RADIO_INPUT).is_selected()

    @allure.step("Check if 'Керівник' role is selected")
    def is_manager_role_selected(self) -> bool:
        """Check whether 'Керівник' role is currently selected."""
        return self.driver.find_element(*self.ROLE_MANAGER_RADIO_INPUT).is_selected()

    @allure.step("Enter Last Name (Прізвище): '{last_name}'")
    def enter_last_name(self, last_name: str) -> SignUpModal:
        """Type value into Last Name input field."""
        element = self.driver.find_element(*self.LAST_NAME_INPUT)
        element.clear()
        element.send_keys(last_name)
        return self

    @allure.step("Enter First Name (Ім'я): '{first_name}'")
    def enter_first_name(self, first_name: str) -> SignUpModal:
        """Type value into First Name input field."""
        element = self.driver.find_element(*self.FIRST_NAME_INPUT)
        element.clear()
        element.send_keys(first_name)
        return self

    @allure.step("Enter Phone (Телефон): '{phone}'")
    def enter_phone(self, phone: str) -> SignUpModal:
        """Type value into Phone input field (Ukrainian format e.g. +380991234567 or 0991234567)."""
        element = self.driver.find_element(*self.PHONE_INPUT)
        element.clear()
        element.send_keys(phone)
        return self

    @allure.step("Enter Email: '{email}'")
    def enter_email(self, email: str) -> SignUpModal:
        """Type value into Email input field."""
        element = self.driver.find_element(*self.EMAIL_INPUT)
        element.clear()
        element.send_keys(email)
        return self

    @allure.step("Enter Password (Пароль)")
    def enter_password(self, password: str) -> SignUpModal:
        """Type value into Password input field."""
        element = self.driver.find_element(*self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self

    @allure.step("Enter Confirm Password (Підтвердження паролю)")
    def enter_confirm_password(self, confirm_password: str) -> SignUpModal:
        """Type value into Confirm Password input field."""
        element = self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT)
        element.clear()
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
        if role.lower() == "manager" or role == "керівник":
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
        return self.driver.find_element(*self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Click Submit button ('Зареєструватися')")
    def click_submit(self) -> None:
        """Click the registration submit button."""
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    @allure.step("Click Close modal button (X)")
    def click_close_button(self) -> None:
        """Close the modal window by clicking the X button in top right."""
        self.driver.find_element(*self.CLOSE_BUTTON).click()

    @allure.step("Click Google OAuth registration link")
    def click_google_oauth(self) -> None:
        """Click the Google login/register button."""
        self.driver.find_element(*self.GOOGLE_OAUTH_BUTTON).click()

    @allure.step("Click Facebook OAuth registration link")
    def click_facebook_oauth(self) -> None:
        """Click the Facebook login/register button."""
        self.driver.find_element(*self.FACEBOOK_OAUTH_BUTTON).click()

    @allure.step("Get all displayed validation error messages in the form")
    def get_error_messages(self) -> list[str]:
        """Retrieve texts of all active client-side validation error messages."""
        elements: list[WebElement] = self.driver.find_elements(*self.FIELD_ERROR_MESSAGES)
        return [elem.text.strip() for elem in elements if elem.is_displayed()]
