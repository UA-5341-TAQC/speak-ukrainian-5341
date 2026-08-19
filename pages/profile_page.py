"""Page object for the profile page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.footer_component import FooterComponent
from pages.modals.edit_profile_modal import EditProfileModal
from pages.profile_complaints_page import ProfileComplaintsPage
from pages.types import Locator


class ProfilePage(BasePage):
    """Page object representing the Speak Ukrainian profile page."""

    avatar_img: Locator = (
        By.CSS_SELECTOR,
        ".ant-layout-content .user-pic img, .ant-layout-content .ant-avatar img",
    )
    user_avatar: Locator = (By.CSS_SELECTOR, "span.user-avatar")
    first_last_name_text: Locator = (By.CSS_SELECTOR, ".user-name")
    role_text: Locator = (By.CSS_SELECTOR, ".user-role")
    phone_text: Locator = (By.CSS_SELECTOR, ".user-phone-data")
    email_text: Locator = (By.CSS_SELECTOR, ".user-email-data")
    edit_profile_btn: Locator = (
        By.CSS_SELECTOR,
        "div.edit-button button",
    )

    # Left hand navigation menu of the personal cabinet ('Особистий кабінет').
    complaints_menu_item: Locator = (
        By.CSS_SELECTOR,
        "ul.sider-profile a[href$='/complaints']",
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

    @allure.step("Get avatar source")
    def get_avatar_src(self) -> str | None:
        """Return the avatar image URL, or ``None`` when a default placeholder is shown.

        A user avatar without a set photo renders as an antd icon placeholder
        (no ``<img>`` element). Once a photo is uploaded it becomes an ``<img>``.
        This lets a test verify the avatar was not changed.
        """
        element = self._wait_visible(self.user_avatar)
        try:
            img = element.find_element(By.TAG_NAME, "img")
        except Exception:
            return None
        return img.get_attribute("src")

    @allure.step("Get avatar state")
    def get_avatar_state(self) -> str:
        """Return a stable representation of the avatar for before/after comparison.

        Returns the image ``src`` when a photo is set, or the literal string
        ``"default"`` for the placeholder avatar.
        """
        src = self.get_avatar_src()
        return src if src else "default"

    @allure.step("Open 'Скарги' page from the personal cabinet menu")
    def open_complaints(self) -> "ProfileComplaintsPage":
        """Click the 'Скарги' item in the left menu and return its page.

        Returns:
            An instance of ProfileComplaintsPage, already waited to load.
        """
        self._wait_clickable(self.complaints_menu_item).click()
        return ProfileComplaintsPage(self.driver).wait_loaded()

    @property
    def footer(self) -> FooterComponent:
        """Get the footer component."""
        root = self.driver.find_element(By.TAG_NAME, "body")
        return FooterComponent(root)
