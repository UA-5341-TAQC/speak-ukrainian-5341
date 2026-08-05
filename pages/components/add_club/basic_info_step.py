from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.modals.add_club_modal import AddClubModal
from pages.types import Locator


class BasicInfoStep(AddClubModal):
    """Page object for the Basic Information step of the Add Club modal."""
    NAME_INPUT: Locator = (By.ID, "basic_name")

    CATEGORIES_CONTAINER: Locator = (By.ID, "basic_categories")

    @staticmethod
    def category_label(value: str) -> Locator:
        """Return a locator for the label of a category input based on its value."""
        return (
            By.XPATH,
            f".//label[.//input[@value='{value}']]"
        )

    @staticmethod
    def category_input(value: str) -> Locator:
        """Return a locator for the input of a category based on its value."""
        return (
            By.CSS_SELECTOR,
            f"input[value='{value}']"
        )

    AGE_FROM_INPUT: Locator = (By.ID, "basic_ageFrom")
    AGE_TO_INPUT: Locator = (By.ID, "basic_ageTo")

    CENTER_SELECT_SELECTOR: Locator = (
        By.CSS_SELECTOR,
        ".add-club-select .ant-select-selector"
    )

    CENTER_DROPDOWN: Locator = (
        By.CSS_SELECTOR,
        ".ant-select-dropdown"
    )

    CENTER_OPTIONS: Locator = (
        By.CSS_SELECTOR,
        ".ant-select-item-option"
    )

    @staticmethod
    def center_option(center_name: str) -> Locator:
        """Return locator for center dropdown option."""
        return (
            By.XPATH,
            (
                "//div[contains(@class,'ant-select-item-option-content') "
                f"and normalize-space()='{center_name}']"
            ),
        )

    @allure.step("Enter club name (Назва): '{name}'")
    def enter_name(self, name: str) -> BasicInfoStep:
        """Enter the club name in the name input field."""
        el = self._find_element(self.NAME_INPUT)
        self.clear(el)
        el.send_keys(name)
        return self

    @allure.step("Clear club name")
    def clear_name(self) -> BasicInfoStep:
        """Clear the club name input field."""
        self.clear(self._find_element(self.NAME_INPUT))
        return self

    @allure.step("Select category: {value}")
    def select_category(self, value: str) -> BasicInfoStep:
        """Select a category by its value."""
        self._wait_clickable(self.category_label(value)).click()
        return self

    @allure.step("Check if category '{value}' is selected")
    def is_category_selected(self, value: str) -> bool:
        """Check if a category is selected based on its value."""
        return self._find_element(self.category_input(value)).is_selected()

    @allure.step("Set age FROM: {age}")
    def set_age_from(self, age: int) -> BasicInfoStep:
        """Set the minimum age in the age FROM input field."""
        el = self._find_element(self.AGE_FROM_INPUT)
        self.clear(el)
        el.send_keys(str(age))
        return self

    @allure.step("Set age TO: {age}")
    def set_age_to(self, age: int) -> BasicInfoStep:
        """Set the maximum age in the age TO input field."""
        el = self._find_element(self.AGE_TO_INPUT)
        self.clear(el)
        el.send_keys(str(age))
        return self

    @allure.step("Set age range: {age_from} – {age_to} років")
    def set_age_range(self, age_from: int, age_to: int) -> BasicInfoStep:
        """Set the age range by specifying both minimum and maximum ages."""
        self.set_age_from(age_from)
        self.set_age_to(age_to)
        return self

    def clear_age_range(self):
        """Clear both age FROM and age TO input fields."""
        self.clear(self._find_element(self.AGE_FROM_INPUT))
        self.clear(self._find_element(self.AGE_TO_INPUT))

    @allure.step("Open center dropdown")
    def open_center_dropdown(self) -> BasicInfoStep:
        """Open the center selection dropdown."""
        self._wait_clickable(self.CENTER_SELECT_SELECTOR).click()
        return self

    @allure.step("Check if center dropdown is visible")
    def is_center_dropdown_visible(self) -> bool:
        """Check whether center dropdown is displayed."""
        return self._find_element(
            self.CENTER_DROPDOWN
        ).is_displayed()

    @allure.step("Select center by text: '{center_name}'")
    def select_center(self, center_name: str) -> BasicInfoStep:
        """Select a center from dropdown."""
        self.open_center_dropdown()

        self._wait_clickable(
            self.center_option(center_name)
        ).click()

        return self

    @allure.step("Fill Step 1 - Основна інформація")
    def fill(
        self,
        name: str,
        categories: list[str],
        age_from: int,
        age_to: int,
        center: str | None = None,
    ) -> BasicInfoStep:
        """Fill in the Basic Information step with the provided details."""
        self.enter_name(name)
        for cat in categories:
            self.select_category(cat)
        self.set_age_range(age_from, age_to)
        if center:
            self.select_center(center)
        return self
