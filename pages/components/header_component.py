"""Module containing the HeaderComponent class for interacting with the website header."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.components.challenges_dropdown import ChallengeDropdown
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
        "[id$='challenge_ONE-popup']",
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

    USER_DROPDOWN_MENU: Locator = (
        By.CSS_SELECTOR,
        "ul.ant-dropdown-menu.ant-dropdown-menu-root",
    )

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

    @allure.step("Click logo")
    def click_logo(self) -> None:
        """Click the website logo."""
        self._wait_clickable(self.LOGO).click()

    @allure.step("Click 'Гуртки'")
    def click_clubs(self) -> None:
        """Click the 'Гуртки' menu item."""
        self._wait_clickable(self.CLUBS_LINK).click()

    @allure.step("Open 'Челендж' menu")
    def click_challenge(self) -> None:
        """Open the Challenge dropdown."""
        self._wait_clickable(self.CHALLENGE_MENU).click()

    @allure.step("Get Challenge dropdown")
    def get_challenge_dropdown(self) -> ChallengeDropdown:
        """Return the Challenge dropdown component."""
        root = self._wait_clickable(
            self.CHALLENGE_DROPDOWN,
            from_driver=True,
        )
        return ChallengeDropdown(root)

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
    def click_user_profile(self) -> None:
        """Open the user profile dropdown."""
        self._wait_clickable(self.USER_PROFILE).click()

    @allure.step("Click 'Додати гурток' in user menu")
    def click_add_club_menu_item(self) -> None:
        """Click the 'Додати гурток' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.ADD_CLUB_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Додати центр' in user menu")
    def click_add_centre_menu_item(self) -> None:
        """Click the 'Додати центр' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.ADD_CENTRE_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Пошук сертифікатів' in user menu")
    def click_search_certificates_menu_item(self) -> None:
        """Click the 'Пошук сертифікатів' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.SEARCH_CERTIFICATES_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Особистий кабінет' in user menu")
    def click_profile_menu_item(self) -> None:
        """Click the 'Особистий кабінет' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.PROFILE_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Вийти' in user menu")
    def click_logout_menu_item(self) -> None:
        """Click the logout item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.LOGOUT_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Увійти' in user menu")
    def click_login_menu_item(self) -> None:
        """Click the 'Увійти' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.LOGIN_MENU_ITEM, from_driver=True).click()

    @allure.step("Click 'Зареєструватися' in user menu")
    def click_register_menu_item(self) -> None:
        """Click the 'Зареєструватися' item in the user dropdown."""
        self.click_user_profile()
        self._wait_clickable(self.REGISTER_MENU_ITEM, from_driver=True).click()

    @allure.step("Check whether the user is signed in")
    def is_logged_in(self) -> bool:
        """Return whether the current session is authenticated.

        A signed-in user menu contains the 'Вийти' (log out) item, which is
        only rendered when an access token exists. The dropdown is rendered at
        the document root, so it is searched on the driver scope.
        """
        self.click_user_profile()
        try:
            self.wait.until(lambda _: self.driver.find_element(*self.LOGOUT_MENU_ITEM))
            return True
        except Exception:
            return False
