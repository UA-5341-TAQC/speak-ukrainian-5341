"""Module containing the UserProfileMenu class for interacting with the user profile menu."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.modals.sign_in_modal import SignInModal
from pages.modals.sign_up_modal import SignUpModal
from pages.types import Locator


class UserProfileMenu(BaseComponent):
    """Component representing the user profile menu."""

    ADD_CLUB_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-add_club']",
    )

    ADD_CENTRE_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-add_centre']",
    )

    SEARCH_CERTIFICATES_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-search_certificates']",
    )

    PROFILE_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-profile']",
    )

    LOGOUT_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-logout'], li.ant-dropdown-menu-item-danger",
    )

    LOGIN_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-login']",
    )

    REGISTER_MENU_ITEM: Locator = (
        By.CSS_SELECTOR,
        "li[data-menu-id$='-register']",
    )

    @allure.step("Click 'Додати гурток' in user menu")
    def click_add_club_menu_item(self) -> None:
        """Click the 'Додати гурток' item in the user dropdown."""
        self._wait_clickable(self.ADD_CLUB_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Додати центр' in user menu")
    def click_add_centre_menu_item(self) -> None:
        """Click the 'Додати центр' item in the user dropdown."""
        self._wait_clickable(self.ADD_CENTRE_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Пошук сертифікатів' in user menu")
    def click_search_certificates_menu_item(self) -> None:
        """Click the 'Пошук сертифікатів' item in the user dropdown."""
        self._wait_clickable(self.SEARCH_CERTIFICATES_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Особистий кабінет' in user menu")
    def click_profile_menu_item(self) -> None:
        """Click the 'Особистий кабінет' item in the user dropdown."""
        self._wait_clickable(self.PROFILE_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Вийти' in user menu")
    def click_logout_menu_item(self) -> None:
        """Click the logout item in the user dropdown."""
        self._wait_clickable(self.LOGOUT_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Увійти' in user menu")
    def click_login(self) -> SignInModal:
        """Click the 'Увійти' item in the user dropdown."""
        self._wait_clickable(self.LOGIN_MENU_ITEM, from_driver=True).click()
        login_modal = SignInModal(self.driver)
        login_modal.is_displayed()
        return login_modal

    @allure.step("Click 'Зареєструватися' in user menu")
    def click_register(self) -> SignUpModal:
        """Click the 'Зареєструватися' item in the user dropdown."""
        self._wait_clickable(self.REGISTER_MENU_ITEM, from_driver=True).click()
        sign_up_modal = SignUpModal(self.driver)
        sign_up_modal.is_displayed()
        return sign_up_modal

    @allure.step("Check whether the user is signed in")
    def is_logged_in(self) -> bool:
        """Return whether the current session is authenticated.

        A signed-in user menu contains the 'Вийти' (log out) item, which is
        only rendered when an access token exists. The dropdown is rendered at
        the document root, so it is searched on the driver scope.
        """
        try:
            self.wait.until(lambda _: self.driver.find_element(*self.LOGOUT_MENU_ITEM))
            return True
        except Exception:
            return False

    @allure.step("Return whether user profile dropdown is displayed.")
    def is_visible(self) -> bool:
        """Return whether user profile dropdown is displayed."""
        try:
            return self.root.is_displayed()
        except Exception:
            return False
