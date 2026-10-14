"""Add child modal, opened from the enroll to club modal."""

import allure
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class AddChildModal(BaseModal):
    """Modal for adding a new child."""

    # Modal container
    MODAL_DIALOG: Locator = (By.CSS_SELECTOR, "div.add-child-modal")

    # Form fields
    FIRST_NAME_FIELD: Locator = (By.CSS_SELECTOR, "#add-child_firstName")
    LAST_NAME_FIELD: Locator = (By.CSS_SELECTOR, "#add-child_lastName")
    AGE_FIELD: Locator = (By.CSS_SELECTOR, "#add-child_age")

    # "Стать" radio buttons
    BOY_RADIO_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#add-child_gender input[type='radio'][value='MALE']",
    )  # noqa: E501
    GIRL_RADIO_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#add-child_gender input[type='radio'][value='FEMALE']",
    )  # noqa: E501

    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "#add-child button.submit-button")

    @allure.step("Enter first name: '{text}'")
    def enter_first_name(self, text: str) -> None:
        """Enter text into the first name field."""
        field = self._find_element(self.FIRST_NAME_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(text)

    @allure.step("Enter last name: '{text}'")
    def enter_last_name(self, text: str) -> None:
        """Enter text into the last name field."""
        field = self._find_element(self.LAST_NAME_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(text)

    @allure.step("Enter age: '{age}'")
    def enter_age(self, age: str) -> None:
        """Enter text into the age field."""
        field = self._find_element(self.AGE_FIELD)
        field.click()
        self.clear(field)
        field.send_keys(age)

    @allure.step('Select "Хлопчик" gender')
    def select_boy(self) -> None:
        """Select the "Хлопчик" gender radio button."""
        self._find_element(self.BOY_RADIO_BUTTON).click()

    @allure.step('Select "Дівчинка" gender')
    def select_girl(self) -> None:
        """Select the "Дівчинка" gender radio button."""
        self._find_element(self.GIRL_RADIO_BUTTON).click()

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    def click_submit(self) -> None:
        """Click the submit button to add the child."""
        self._wait_clickable(self.SUBMIT_BUTTON).click()
