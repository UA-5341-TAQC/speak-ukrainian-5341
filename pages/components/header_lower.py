"""Module containing the HeaderLower component."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class HeaderLower(BaseComponent):
    """Component representing the lower part of the website header."""

    CITY_NAME: Locator = (
        By.CSS_SELECTOR,
        ".city-name",
    )

    SEARCH_INPUT: Locator = (
        By.CSS_SELECTOR,
        ".search-container input[role='combobox']",
    )

    SEARCH_ICON: Locator = (
        By.CSS_SELECTOR,
        ".search-icon-group .anticon-search",
    )

    ADVANCED_SEARCH_ICON: Locator = (
        By.CSS_SELECTOR,
        ".search-icon-group .anticon-control",
    )

    SHOW_MAP_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".show-map-button",
    )

    @allure.step("Get city name")
    def get_city_name(self) -> str:
        """Return the current city name."""
        return self._find_element(self.CITY_NAME).text

    @allure.step("Search for a club")
    def search_club(self, search_text: str) -> None:
        """Enter text into the club search field."""
        search_input = self._find_element(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(search_text)

    @allure.step("Click search")
    def click_search(self) -> None:
        """Click the search icon."""
        self._wait_clickable(self.SEARCH_ICON).click()

    @allure.step("Open advanced search")
    def click_advanced_search(self) -> None:
        """Open the advanced search."""
        self._wait_clickable(self.ADVANCED_SEARCH_ICON).click()

    @allure.step("Click 'Показати на мапі'")
    def click_show_map(self) -> None:
        """Click the 'Показати на мапі' button."""
        self._wait_clickable(self.SHOW_MAP_BUTTON).click()
