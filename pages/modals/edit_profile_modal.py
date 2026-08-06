"""Page object for the edit profile modal."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class EditProfileModal(BaseModal):
    """Page object representing the Edit Profile modal."""

    def __init__(self, driver: WebDriver):
        """Initialize the edit profile modal."""
        super().__init__(driver)

        self._modal_title: Locator = (By.CSS_SELECTOR, ".ant-modal-title")
        self._close_btn: Locator = (By.CSS_SELECTOR, ".ant-modal-close")

        self._role_visitor_btn: Locator = (
            By.XPATH,
            "//div[contains(@class, 'ant-modal-content')]//span[contains(text(), "
            "'Відвідувач')]/ancestor::div[contains(@class, 'ant-radio-button-wrapper') "
            "or contains(@class, 'role-btn')]",
        )
        self._role_manager_btn: Locator = (
            By.XPATH,
            "//div[contains(@class, 'ant-modal-content')]//span[contains(text(), "
            "'Керівник')]/ancestor::div[contains(@class, 'ant-radio-button-wrapper') "
            "or contains(@class, 'role-btn')]",
        )

        self._last_name_input: Locator = (By.ID, "edit_lastName")
        self._first_name_input: Locator = (By.ID, "edit_firstName")
        self._phone_input: Locator = (By.ID, "edit_phone")
        self._email_input: Locator = (By.ID, "edit_email")

        self._upload_photo_input: Locator = (
            By.CSS_SELECTOR,
            "input[type='file']#edit_urlLogo",
        )
        self._change_password_checkbox: Locator = (
            By.CSS_SELECTOR,
            "input.checkbox[type='checkbox']",
        )
        self._current_password_input: Locator = (By.ID, "edit_currentPassword")
        self._new_password_input: Locator = (By.ID, "edit_password")
        self._confirm_password_input: Locator = (By.ID, "edit_confirmPassword")

        self._save_changes_btn: Locator = (
            By.CSS_SELECTOR,
            ".ant-modal-footer button.ant-btn-primary, button[type='submit']",
        )

    @allure.step("Get modal title")
    def get_title(self) -> str:
        """Get the title of the modal."""
        return self._get_text(self._modal_title)

    @allure.step("Close Edit Profile modal")
    def close_modal(self) -> None:
        """Click the close button (X) of the modal."""
        self._click(self._close_btn)

    @allure.step("Select 'Visitor' role")
    def select_role_visitor(self) -> "EditProfileModal":
        """Select the 'Відвідувач' (Visitor) role."""
        self._click(self._role_visitor_btn)
        return self

    @allure.step("Select 'Manager' role")
    def select_role_manager(self) -> "EditProfileModal":
        """Select the 'Керівник' (Manager) role."""
        self._click(self._role_manager_btn)
        return self

    @allure.step("Set last name to '{text}'")
    def set_last_name(self, text: str) -> "EditProfileModal":
        """Fill in the last name (Прізвище) input."""
        self._fill_input(self._last_name_input, text)
        return self

    @allure.step("Set first name to '{text}'")
    def set_first_name(self, text: str) -> "EditProfileModal":
        """Fill in the first name (Ім'я) input."""
        self._fill_input(self._first_name_input, text)
        return self

    @allure.step("Set phone to '{phone}'")
    def set_phone(self, phone: str) -> "EditProfileModal":
        """Fill in the phone (Телефон) input."""
        self._fill_input(self._phone_input, phone)
        return self

    @allure.step("Get email")
    def get_email(self) -> str:
        """Get the value of the email input (read-only)."""
        return self._wait_visible(self._email_input).get_attribute("value") or ""

    @allure.step("Toggle 'Change Password' checkbox")
    def toggle_change_password(self) -> "EditProfileModal":
        """Click the 'Змінити пароль' checkbox."""
        self._click(self._change_password_checkbox)
        return self

    @allure.step("Set current password")
    def set_current_password(self, password: str) -> "EditProfileModal":
        """Fill in the current password."""
        self._fill_input(self._current_password_input, password)
        return self

    @allure.step("Set new password")
    def set_new_password(self, password: str) -> "EditProfileModal":
        """Fill in the new password."""
        self._fill_input(self._new_password_input, password)
        return self

    @allure.step("Confirm new password")
    def set_confirm_password(self, password: str) -> "EditProfileModal":
        """Fill in the confirm new password."""
        self._fill_input(self._confirm_password_input, password)
        return self

    @allure.step("Upload photo from '{file_path}'")
    def upload_photo(self, file_path: str) -> "EditProfileModal":
        """Upload a photo by sending the file path to the hidden file input."""
        self._find_element(self._upload_photo_input).send_keys(file_path)
        return self

    @allure.step("Click 'Save Changes' button")
    def save_changes(self) -> None:
        """Click the 'Зберегти зміни' button."""
        self._click(self._save_changes_btn)
