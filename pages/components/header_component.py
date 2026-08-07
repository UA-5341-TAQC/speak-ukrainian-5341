import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
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

    USER_PROFILE: Locator = (
        By.CSS_SELECTOR,
        ".nav-menu .user-profile",
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
