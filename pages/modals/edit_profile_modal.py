"""Page object for the edit profile modal."""

import allure
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class EditProfileModal(BaseModal):
    """Page object representing the Edit Profile modal."""

    modal_title: Locator = (By.CSS_SELECTOR, "div.edit-header")
    close_btn: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

    role_visitor_btn: Locator = (
        By.CSS_SELECTOR,
        "#edit_roleName label.ant-radio-button-wrapper:nth-child(1)",
    )
    role_manager_btn: Locator = (
        By.CSS_SELECTOR,
        "#edit_roleName label.ant-radio-button-wrapper:nth-child(2)",
    )

    last_name_input: Locator = (By.ID, "edit_lastName")
    first_name_input: Locator = (By.ID, "edit_firstName")
    phone_input: Locator = (By.ID, "edit_phone")
    email_input: Locator = (By.ID, "edit_email")

    upload_photo_input: Locator = (
        By.CSS_SELECTOR,
        "input[type='file']#edit_urlLogo",
    )
    upload_photo_button: Locator = (
        By.CSS_SELECTOR,
        "div.ant-upload-select span.ant-upload[role='button']",
    )
    upload_photo_list_item: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content div.ant-upload-list div.ant-upload-list-item",
    )
    upload_photo_error_item: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content div.ant-upload-list-item.ant-upload-list-item-error",
    )
    photo_error_message: Locator = (
        By.CSS_SELECTOR,
        "div.ant-message-error span:not(.anticon)",
    )
    change_password_checkbox: Locator = (
        By.CSS_SELECTOR,
        "div.align-checkbox",
    )
    current_password_input: Locator = (By.ID, "edit_currentPassword")
    new_password_input: Locator = (By.ID, "edit_password")
    confirm_password_input: Locator = (By.ID, "edit_confirmPassword")

    save_changes_btn: Locator = (
        By.CSS_SELECTOR,
        "button.ant-btn[type='submit']",
    )
    phone_valid_icon: Locator = (
        By.CSS_SELECTOR,
        "input#edit_phone ~ span.ant-input-suffix span.anticon-check-circle",
    )

    # --- Last name (Прізвище) field validation ---
    last_name_error: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content "
        "div.ant-form-item:has(input#edit_lastName) "
        "div.ant-form-item-explain-error",
    )
    last_name_error_icon: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content "
        "div.ant-form-item:has(input#edit_lastName) "
        "span.ant-form-item-feedback-icon",
    )
    last_name_error_input: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content div.ant-form-item:has(input#edit_lastName).ant-form-item-has-error",
    )

    @allure.step("Get modal title")
    def get_title(self) -> str:
        """Get the title of the modal."""
        return self._get_text(self.modal_title)

    @allure.step("Check if Edit Profile modal is displayed")
    def is_displayed(self) -> bool:
        """Check whether the Edit Profile modal window is currently open."""
        return self._wait_visible(self.modal_title).is_displayed()

    @allure.step("Close Edit Profile modal")
    def close_modal(self) -> None:
        """Click the close button (X) of the modal."""
        self._click(self.close_btn)

    @allure.step("Select 'Visitor' role")
    def select_role_visitor(self) -> "EditProfileModal":
        """Select the 'Відвідувач' (Visitor) role."""
        self._click(self.role_visitor_btn)
        return self

    @allure.step("Select 'Manager' role")
    def select_role_manager(self) -> "EditProfileModal":
        """Select the 'Керівник' (Manager) role."""
        self._click(self.role_manager_btn)
        return self

    @allure.step("Set last name to '{text}'")
    def set_last_name(self, text: str) -> "EditProfileModal":
        """Fill in the last name (Прізвище) input."""
        self._fill_input(self.last_name_input, text)
        return self

    @allure.step("Set first name to '{text}'")
    def set_first_name(self, text: str) -> "EditProfileModal":
        """Fill in the first name (Ім'я) input."""
        self._fill_input(self.first_name_input, text)
        return self

    @allure.step("Set phone to '{phone}'")
    def set_phone(self, phone: str) -> "EditProfileModal":
        """Fill in the phone (Телефон) input."""
        self._fill_input(self.phone_input, phone)
        return self

    @allure.step("Get email")
    def get_email(self) -> str:
        """Get the value of the email input (read-only)."""
        return self._wait_visible(self.email_input).get_attribute("value") or ""

    @allure.step("Toggle 'Change Password' checkbox")
    def toggle_change_password(self) -> "EditProfileModal":
        """Click the 'Змінити пароль' checkbox."""
        self._click(self.change_password_checkbox)
        return self

    @allure.step("Set current password")
    def set_current_password(self, password: str) -> "EditProfileModal":
        """Fill in the current password."""
        self._fill_input(self.current_password_input, password)
        return self

    @allure.step("Set new password")
    def set_new_password(self, password: str) -> "EditProfileModal":
        """Fill in the new password."""
        self._fill_input(self.new_password_input, password)
        return self

    @allure.step("Confirm new password")
    def set_confirm_password(self, password: str) -> "EditProfileModal":
        """Fill in the confirm new password."""
        self._fill_input(self.confirm_password_input, password)
        return self

    @allure.step("Upload photo from '{file_path}'")
    def upload_photo(self, file_path: str) -> "EditProfileModal":
        """Upload a photo by sending the file path to the hidden file input."""
        self._find_element(self.upload_photo_input).send_keys(file_path)
        return self

    @allure.step("Click 'Завантажити фото' button")
    def click_upload_photo(self) -> "EditProfileModal":
        """Click the 'Завантажити фото' (upload photo) button.

        Note: the native OS file dialog cannot be automated by Selenium, so a
        real upload is performed with `upload_photo` (sending the file path to
        the hidden file input). This method is provided for completeness.
        """
        self._click(self.upload_photo_button)
        return self

    @allure.step("Get uploaded photo file names")
    def get_uploaded_file_names(self) -> list[str]:
        """Return the file names currently present in the photo upload list."""
        return [
            el.text.strip()
            for el in self._find_elements(self.upload_photo_list_item)
            if el.is_displayed()
        ]

    @allure.step("Check if an upload photo error state is shown")
    def is_photo_upload_error_displayed(self) -> bool:
        """Return whether the uploaded photo is in an error state.

        A rejected/unsupported upload is rendered by antd as a list item with
        the ``ant-upload-list-item-error`` class. Additionally an error toast
        may be shown via ``ant-message-error``.
        """
        error_items = [
            el for el in self._find_elements(self.upload_photo_error_item) if el.is_displayed()
        ]
        if error_items:
            return True
        toasts = [el for el in self._find_elements(self.photo_error_message) if el.is_displayed()]
        return bool(toasts)

    @allure.step("Get photo upload error text")
    def get_photo_upload_error_text(self) -> str:
        """Return the visible photo upload error message text, if any."""
        for el in self._find_elements(self.photo_error_message):
            if el.is_displayed() and el.text.strip():
                return el.text.strip()
        return ""

    @allure.step("Wait for the photo upload to settle")
    def wait_for_upload_settle(self) -> "EditProfileModal":
        """Wait until the uploaded file is rendered in the upload list.

        Uploading a file triggers an async request; the antd Upload component
        reflects the result (success or error) only after the request resolves.
        This helper waits for that settled state so assertions run against the
        final UI, not a transient "uploading" state.
        """
        self.wait.until(
            lambda _: bool(
                [el for el in self._find_elements(self.upload_photo_list_item) if el.is_displayed()]
            )
        )
        return self

    @allure.step("Click 'Save Changes' button")
    def save_changes(self) -> None:
        """Click the 'Зберегти зміни' button."""
        self._click(self.save_changes_btn)

    @allure.step("Get last name input value")
    def get_last_name_value(self) -> str:
        """Return the current value of the 'Прізвище' input field."""
        return self._wait_visible(self.last_name_input).get_attribute("value") or ""

    @allure.step("Remove focus from the Last Name field")
    def blur_last_name(self) -> "EditProfileModal":
        """Remove focus from the Last Name field by clicking the modal title.

        Clicking an element outside the input mimics a user moving focus away,
        which triggers the client-side blur validation of the field.
        """
        self._click(self.modal_title)
        return self

    @allure.step("Check if Last Name validation error is displayed")
    def is_last_name_error_displayed(self) -> bool:
        """Return whether the Last Name validation error message is visible."""
        elements = self._find_elements(self.last_name_error)
        return bool(elements) and any(el.is_displayed() for el in elements)

    @allure.step("Get Last Name validation error text")
    def get_last_name_error_text(self) -> str:
        """Return the text of the Last Name validation error message."""
        return self._wait_visible(self.last_name_error).text.strip()

    @allure.step("Check if Last Name error icon is displayed")
    def is_last_name_error_icon_displayed(self) -> bool:
        """Return whether the error icon inside the Last Name field is visible."""
        elements = self._find_elements(self.last_name_error_icon)
        return bool(elements) and any(el.is_displayed() for el in elements)

    @allure.step("Check if Last Name field has an error border")
    def has_last_name_error_border(self) -> bool:
        """Return whether the Last Name input is styled with the error status."""
        elements = self._find_elements(self.last_name_error_input)
        return bool(elements) and any(el.is_displayed() for el in elements)

    @allure.step("Check if 'Save Changes' button is enabled")
    def is_save_changes_enabled(self) -> bool:
        """Return whether the 'Зберегти зміни' button is enabled (no disabled attr)."""
        return self._wait_visible(self.save_changes_btn).is_enabled()
    @allure.step("Check if phone valid icon is displayed")
    def is_phone_valid_icon_displayed(self) -> bool:
        """Check if the phone valid icon is displayed."""
        return self._wait_visible(self.phone_valid_icon).is_displayed()
