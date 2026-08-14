"""Page object for the Map modal window."""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class MapModal(BaseModal):
    """Page object for the Map modal window."""

    MODAL_CONTENT: Locator = (
        By.CSS_SELECTOR,
        "div.ant-modal-content, div.map-layout",
    )

    CLOSE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.ant-modal-close",
    )

    CITY_SELECT: Locator = (
        By.CSS_SELECTOR,
        "div.selectBlock div.ant-select:nth-child(1)",
    )

    CITY_SELECT_INPUT: Locator = (
        By.ID,
        "mapCitiesList",
    )

    CITY_SELECTED_ITEM: Locator = (
        By.CSS_SELECTOR,
        "div.selectBlock div.ant-select:nth-child(1) "
        "span.ant-select-selection-item",
    )

    CATEGORY_SELECT_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        "div.selectBlock div.ant-select:nth-child(2)",
    )

    CATEGORY_SELECTED_ITEM: Locator = (
        By.CSS_SELECTOR,
        "div.selectBlock div.ant-select:nth-child(2) "
        "span.ant-select-selection-item",
    )

    # Ant Design options
    ACTIVE_DROPDOWN_OPTIONS: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) "
        "div.ant-select-item-option",
    )

    CLUB_ITEMS: Locator = (
        By.CSS_SELECTOR,
        "div.clubList div.club-item",
    )

    CLUB_NAMES: Locator = (
        By.CSS_SELECTOR,
        "div.clubList div.club-item div.name",
    )

    NO_RESULTS_MESSAGE: Locator = (
        By.CSS_SELECTOR,
        "div.ant-empty-description span",
    )

    MAP_PINS: Locator = (
        By.CSS_SELECTOR,
        "div.map-layout img[src*='location.png']",
    )

    DROPDOWN_LIST_HOLDER: Locator = (
        By.CSS_SELECTOR,
        "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) "
        "div.rc-virtual-list-holder",
    )

    @staticmethod
    def get_city_locator(city_name: str) -> Locator:
        """Return XPath locator for a specific city option."""
        return (
            By.XPATH,
            "//div[contains(@class,'ant-select-dropdown') "
            "and not(contains(@class,'ant-select-dropdown-hidden'))]"
            "//div[contains(@class,'ant-select-item-option') "
            f"and (normalize-space(.)='{city_name}' or @title='{city_name}')]",
        )

    @staticmethod
    def get_all_cities_locator() -> Locator:
        """Return XPath locator for 'Всі міста' option."""
        return (
            By.XPATH,
            "//div[contains(@class,'ant-select-dropdown') "
            "and not(contains(@class,'ant-select-dropdown-hidden'))]"
            "//div[contains(@class,'ant-select-item-option') "
            "and (@title='Всі міста' or normalize-space(.)='Всі міста')]",
        )

    @staticmethod
    def get_category_locator(category_name: str) -> Locator:
        """Return XPath locator for a specific category option."""
        return (
            By.XPATH,
            "//div[contains(@class,'ant-select-dropdown') "
            "and not(contains(@class,'ant-select-dropdown-hidden'))]"
            "//div[contains(@class,'ant-select-item-option') "
            "and .//*[normalize-space(text())="
            f"'{category_name}'"
            "]]",
        )

    def is_displayed(self) -> bool:
        """Check whether the Map modal is displayed."""
        try:
            return self._wait_visible(self.MODAL_CONTENT).is_displayed()
        except Exception:
            return False

    @allure.step("Close Map modal")
    def close(self) -> None:
        """Close the Map modal."""
        self._wait_clickable(self.CLOSE_BUTTON).click()

    @allure.step("Select city: '{city_name}'")
    def select_city(self, city_name: str) -> MapModal:
        """Select city from city dropdown using explicit waits."""
        city_select = self._wait_clickable(self.CITY_SELECT)
        city_select.click()

        if city_name == "Всі міста":
            try:
                dropdown_list = self._wait_visible(self.DROPDOWN_LIST_HOLDER)
                self.driver.execute_script(
                    "arguments[0].scrollTop = 0;",
                    dropdown_list,
                )
            except Exception:
                pass

            option_locator = self.get_all_cities_locator()

        else:
            city_input = self._wait_visible(self.CITY_SELECT_INPUT)

            city_input.send_keys(Keys.CONTROL, "a")
            city_input.send_keys(Keys.BACKSPACE)
            city_input.send_keys(city_name)

            option_locator = self.get_city_locator(city_name)

        option = self.wait.until(
            EC.element_to_be_clickable(option_locator)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            option,
        )

        self.wait.until(
            lambda _: self.get_selected_city() == city_name
        )

        return self

    @allure.step("Select category: '{category_name}'")
    def select_category(self, category_name: str) -> MapModal:
        """Select category from category dropdown using explicit waits."""
        category_select = self._wait_clickable(self.CATEGORY_SELECT_CONTAINER)
        category_select.click()

        option_locator = self.get_category_locator(category_name)

        option = self.wait.until(
            EC.element_to_be_clickable(option_locator)
        )

        self.driver.execute_script("arguments[0].click();", option)

        self.wait.until(
            lambda _: self.get_selected_category() == category_name
        )

        return self

    @allure.step("Get selected city name")
    def get_selected_city(self) -> str:
        """Return selected city name."""
        return self._find_element(self.CITY_SELECTED_ITEM).text.strip()

    @allure.step("Get selected category name")
    def get_selected_category(self) -> str:
        """Return selected category name."""
        return self._find_element(self.CATEGORY_SELECTED_ITEM).text.strip()

    @allure.step("Get list of club names from map sidebar")
    def get_club_cards(self) -> list[str]:
        """Return names of clubs displayed in sidebar."""
        elements = self._find_elements(self.CLUB_NAMES)
        return [
            element.text.strip()
            for element in elements
            if element.text.strip()
        ]

    @allure.step("Get count of club items in map sidebar")
    def get_clubs_count(self) -> int:
        """Return number of clubs displayed in sidebar with wait."""
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(self.CLUB_ITEMS)
            )
        except Exception:
            pass

        return len(self._find_elements(self.CLUB_ITEMS))

    @allure.step("Get pins count on the map")
    def get_pins_count(self) -> int:
        """Return number of location markers displayed on map with wait."""
        try:
            self.wait.until(
                lambda _: len(self.driver.find_elements(*self.MAP_PINS)) > 0
            )
        except Exception:
            pass

        return len(self.driver.find_elements(*self.MAP_PINS))

    @allure.step("Get 'No results' message text")
    def get_no_results_text(self) -> str:
        """Wait for and return no-results message text."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
        )
        return element.text.strip()
