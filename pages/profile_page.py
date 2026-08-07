"""Page object for the profile page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.modals.edit_profile_modal import EditProfileModal
from pages.components.footer_component import FooterComponent
from pages.types import Locator


class ProfilePage(BasePage):
    """Page object representing the Speak Ukrainian profile page."""

    avatar_img: Locator = (
        By.CSS_SELECTOR,
        ".ant-layout-content .user-pic img, .ant-layout-content .ant-avatar img",
    )
    first_last_name_text: Locator = (By.CSS_SELECTOR, ".user-name")
    role_text: Locator = (By.CSS_SELECTOR, ".user-role")
    phone_text: Locator = (By.CSS_SELECTOR, ".user-phone-data")
    email_text: Locator = (By.CSS_SELECTOR, ".user-email-data")
    edit_profile_btn: Locator = (
        By.CSS_SELECTOR,
        "div.edit-button button",
    )

    @allure.step("Click 'Edit Profile' button")
    def click_edit_profile(self) -> "EditProfileModal":
        """Click the edit profile button.

        Returns:
            An instance of EditProfileModal.
        """
        self._wait_clickable(self.edit_profile_btn).click()
        return EditProfileModal(self.driver)

    @allure.step("Get user name")
    def get_user_name(self) -> str:
        """Get the user's first and last name."""
        return self._get_text(self.first_last_name_text)

    @allure.step("Get user role")
    def get_user_role(self) -> str:
        """Get the user's role."""
        return self._get_text(self.role_text)

    @allure.step("Get user phone")
    def get_user_phone(self) -> str:
        """Get the user's phone number."""
        return self._get_text(self.phone_text)

    @allure.step("Get user email")
    def get_user_email(self) -> str:
        """Get the user's email."""
        return self._get_text(self.email_text)

    @allure.step("Check if avatar is visible")
    def is_avatar_visible(self) -> bool:
        """Check if the user's avatar is visible."""
        return self._wait_visible(self.avatar_img).is_displayed()

    @property
    def footer(self) -> FooterComponent:
        """Get the footer component."""
        root = self.driver.find_element(By.TAG_NAME, "body")
        return FooterComponent(root)
