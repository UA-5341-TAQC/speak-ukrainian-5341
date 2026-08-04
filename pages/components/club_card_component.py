"""Club Card Component for the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ClubCardComponent(BaseComponent):
    """Component for Single club card."""

    #locators
    _TITLE: Locator = (By.CSS_SELECTOR, "div_name")
    _CATEGORIES: Locator = (By.CSS_SELECTOR, "div.club-tags-box span-name")
    _DESCRIPTION: Locator = (By.CSS_SELECTOR, "p.description")
    _RATING: Locator = (By.CSS_SELECTOR, "ul.ant-rate")
    _ADDRESS: Locator = (By.CSS_SELECTOR, "div.address")
    _MORE_BUTTON: Locator = (By.CSS_SELECTOR, "a.ant-btn")

    def __init__(self, root: WebElement) -> None:
        """Initialize the base component with a WebElement root."""
        super().__init__(root)


    @property
    @allure.step("Club Title")
    def title(self) -> str:
        """Return title."""
        return self._find_element(*self._TITLE).text.strip()

    @property
    @allure.step("Club Categories")
    def categories(self) -> list[str]:
        """Return list of club categories."""
        elements = self._find_element(*self._CATEGORIES)
        return [el.text.strip() for el in elements]

    @property
    @allure.step("Club Description")
    def description(self) -> str:
        """Return club description."""
        return self._find_element(*self._DESCRIPTION).text.strip()

    @property
    @allure.step("Club Address")
    def address(self) -> str:
        """Return club address."""
        return self._find_element(*self._ADDRESS).text.strip()

    @allure.step("Click 'More information' button")
    def click_more_details(self) -> None:
        """Click 'More information' button."""
        self._find_element(*self._MORE_BUTTON).click()


