"""Module containing the UserMenuComponent for the avatar dropdown in the header."""

from typing import Literal

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator

# Ant Design keeps closed dropdowns in the DOM, so every menu lookup is scoped to the
# visible one. The menu itself is rendered at the document root, outside the header.
VISIBLE_DROPDOWN = "div.ant-dropdown:not(.ant-dropdown-hidden)"


class UserMenuComponent(BaseComponent):
    """Component representing the user menu behind the header avatar.

    Domain facts:
        - The component root is the `.user-profile` dropdown trigger; the menu is portalled to
          the document root, so its items are searched on the driver rather than on the root.
        - The avatar class tells the auth state without opening the menu: `avatarIfNotLogin`
          for a guest, `avatarIfLogin` for a signed-in user.
        - Guest menu: Зареєструватися, Увійти.
        - Signed-in menu: Додати гурток, Додати центр, Пошук сертифікатів, Особистий кабінет,
          Вийти.
        - An admin (ROLE_ADMIN) additionally gets the Контент, Локації, Гуртки and Сторінка
          submenus - use `has_item` for those instead of a method per entry.
    """

    AVATAR: Locator = (By.CSS_SELECTOR, "span.ant-avatar")
    MENU: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} ul.ant-dropdown-menu-root")
    MENU_ITEMS: Locator = (
        By.CSS_SELECTOR,
        f"{VISIBLE_DROPDOWN} ul.ant-dropdown-menu-root > li[data-menu-id]",
    )

    REGISTER_ITEM: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-register']")
    LOGIN_ITEM: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-login']")
    ADD_CLUB_ITEM: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-add_club']")
    ADD_CENTRE_ITEM: Locator = (
        By.CSS_SELECTOR,
        f"{VISIBLE_DROPDOWN} li[data-menu-id$='-add_centre']",
    )
    SEARCH_CERTIFICATES_ITEM: Locator = (
        By.CSS_SELECTOR,
        f"{VISIBLE_DROPDOWN} li[data-menu-id$='-search_certificates']",
    )
    PROFILE_ITEM: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-profile']")
    LOGOUT_ITEM: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-logout']")

    def __init__(self, root: WebElement) -> None:
        """Initialize the component with the `.user-profile` dropdown trigger as root."""
        super().__init__(root)
        self.trigger = root

    @allure.step("Open the user menu")
    def open(self) -> None:
        """Open the dropdown and wait for its items, unless it is already open."""
        if not self.is_open():
            self.trigger.click()
        self._wait_menu(self.MENU)

    @allure.step("Check whether the user menu is open")
    def is_open(self) -> bool:
        """Return whether the dropdown is currently expanded."""
        classes = self.trigger.get_attribute("class") or ""
        return "ant-dropdown-open" in classes

    @allure.step("Check whether the user is signed in")
    def is_logged_in(self) -> bool:
        """Return whether the session is authenticated, judged by the avatar class."""
        classes = self._find_element(self.AVATAR).get_attribute("class") or ""
        return "avatarIfLogin" in classes

    @allure.step("Get user menu item labels")
    def get_item_labels(self) -> list[str]:
        """Return the labels of the items currently rendered in the menu."""
        self.open()
        return [item.text.strip() for item in self.driver.find_elements(*self.MENU_ITEMS)]

    @allure.step("Check whether the user menu contains the '{key}' item")
    def has_item(self, key: str) -> bool:
        """Check whether the menu contains an item with the given menu key.

        Args:
            key: The Ant Design menu key, e.g. 'logout' or 'users'.

        Returns:
            True if an item with that key is rendered in the menu.
        """
        self.open()
        locator: Locator = (By.CSS_SELECTOR, f"{VISIBLE_DROPDOWN} li[data-menu-id$='-{key}']")
        return len(self.driver.find_elements(*locator)) > 0

    @allure.step("Click 'Зареєструватися' in the user menu")
    def click_register(self) -> None:
        """Open the registration modal."""
        self._click_item(self.REGISTER_ITEM)

    @allure.step("Click 'Увійти' in the user menu")
    def click_login(self) -> None:
        """Open the sign-in modal."""
        self._click_item(self.LOGIN_ITEM)

    @allure.step("Click 'Додати гурток' in the user menu")
    def click_add_club(self) -> None:
        """Open the 'Додати гурток' modal."""
        self._click_item(self.ADD_CLUB_ITEM)

    @allure.step("Click 'Додати центр' in the user menu")
    def click_add_centre(self) -> None:
        """Open the 'Додати центр' modal."""
        self._click_item(self.ADD_CENTRE_ITEM)

    @allure.step("Click 'Пошук сертифікатів' in the user menu")
    def click_search_certificates(self) -> None:
        """Open the certificate search page."""
        self._click_item(self.SEARCH_CERTIFICATES_ITEM)

    @allure.step("Click 'Особистий кабінет' in the user menu")
    def click_profile(self) -> None:
        """Open the personal profile page."""
        self._click_item(self.PROFILE_ITEM)

    @allure.step("Click 'Вийти' in the user menu")
    def click_logout(self) -> None:
        """Sign the current user out."""
        self._click_item(self.LOGOUT_ITEM)

    def _click_item(self, locator: Locator) -> None:
        """Open the menu and click one of its items.

        Args:
            locator: Locator of the menu item.
        """
        self.open()
        self._wait_menu(locator).click()

    def _wait_menu(self, locator: Locator) -> WebElement:
        """Wait until an element of the dropdown is visible and return it.

        The inherited `_wait_*` helpers search within the root element, which here is the
        trigger; the menu is rendered at the document root, so it is searched on the driver.

        Args:
            locator: Locator of the element inside the dropdown.

        Returns:
            The visible WebElement.
        """

        def _predicate(_: object) -> WebElement | Literal[False]:
            element = self.driver.find_element(*locator)
            return element if element.is_displayed() else False

        return self.wait.until(_predicate)
