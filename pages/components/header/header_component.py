"""Module containing the HeaderComponent class for interacting with the website header."""

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from pages.clubs_page import ClubPage

from pages.components.base_component import BaseComponent
from pages.components.challenges_dropdown import ChallengeDropdown
from pages.components.header.user_profile_menu import UserProfileMenu
from pages.types import Locator


class HeaderComponent(BaseComponent):
    """Component representing the website header."""

    LOGO: Locator = (
        By.CSS_SELECTOR,
        ".left-side-menu .logo",
    )

    CLUBS_LINK: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu a[href='/clubs']",
    )

    CHALLENGE_MENU: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu .challenge-text",
    )

    CHALLENGE_DROPDOWN: Locator = (
        By.CSS_SELECTOR,
        ".ant-menu-submenu-popup",
    )

    NEWS_LINK: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu a[href='/news']",
    )

    ABOUT_LINK: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu a[href='/about']",
    )

    SERVICES_LINK: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu a[href='/service']",
    )

    CITY_SELECTOR: Locator = (
        By.CSS_SELECTOR,
        ".right-side-menu .ant-dropdown-trigger.city",
    )

    ADD_CLUB_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.add-club-button",
    )

    USER_PROFILE: Locator = (
        By.CSS_SELECTOR,
        ".right-side-menu .user-profile",
    )
    USER_DROPDOWN_MENU_ROOT: Locator = (
        By.CSS_SELECTOR,
        "ul.ant-dropdown-menu.ant-dropdown-menu-root",
    )

    @allure.step("Click logo")
    def click_logo(self) -> None:
        """Click the website logo."""
        self._wait_clickable(self.LOGO).click()

    @allure.step("Click 'Гуртки'")
    def click_clubs(self) -> "ClubPage":
        """Click the 'Гуртки' menu item."""
        self._wait_clickable(self.CLUBS_LINK).click()
        from pages.clubs_page import ClubPage

        return ClubPage(self.driver).wait_loaded()

    @allure.step("Open 'Челендж' menu")
    def click_challenge(self) -> ChallengeDropdown:
        """Open the Challenge dropdown."""
        self._wait_clickable(self.CHALLENGE_MENU).click()
        dropdown_element = self.wait.until(
            lambda driver: driver.find_element(*self.CHALLENGE_DROPDOWN)
        )
        return ChallengeDropdown(dropdown_element)

    @allure.step("Click 'Новини'")
    def click_news(self) -> None:
        """Click the 'Новини' menu item."""
        self._wait_clickable(self.NEWS_LINK).click()

    @allure.step("Click 'Про нас'")
    def click_about(self) -> None:
        """Click the 'Про нас' menu item."""
        self._wait_clickable(self.ABOUT_LINK).click()

    @allure.step("Click 'Послуги українською'")
    def click_services(self) -> None:
        """Click the 'Послуги українською' menu item."""
        self._wait_clickable(self.SERVICES_LINK).click()

    @allure.step("Open user profile menu")
    def click_user_profile(self) -> UserProfileMenu:
        """Open the user profile dropdown."""
        self._wait_clickable(self.USER_PROFILE).click()
        user_profile_menu_root = self._find_element(self.USER_DROPDOWN_MENU_ROOT, from_driver=True)
        return UserProfileMenu(user_profile_menu_root)

    @allure.step("Check whether the user is signed in")
    def is_logged_in(self) -> bool:
        """Return whether the current session is authenticated.

        A signed-in user menu contains the 'Вийти' (log out) item, which is
        only rendered when an access token exists. The dropdown is rendered at
        the document root, so it is searched on the driver scope.
        """
        self.click_user_profile()
        try:
            self.wait.until(lambda _: self.driver.find_element(*self.CHALLENGE_DROPDOWN))
            return True
        except Exception:
            return False

    @allure.step("Return whether challenge dropdown menu is displayed.")
    def is_challenge_dropdown_visibile(self) -> bool:
        """Return whether challenge dropdown menu is displayed."""
        try:
            self.wait.until(lambda _: self.driver.find_element(*self.CHALLENGE_DROPDOWN))
            return True
        except Exception:
            return False
