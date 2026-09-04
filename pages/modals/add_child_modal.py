"""Add child modal, opened from the enroll to club modal."""

import allure
from selenium.webdriver.common.by import By

from pages.modals.base_modal import BaseModal
from pages.types import Locator


class AddChildModal(BaseModal):
    """Modal for adding a new child."""

    # Modal container and header
    MODAL_DIALOG: Locator = (By.CSS_SELECTOR, "div.add-child-modal")
    MODAL_TITLE: Locator = (By.CSS_SELECTOR, "div.ant-modal-title")
    CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, "button.ant-modal-close")

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

    def is_modal_displayed(self) -> bool:
        """Check if the modal is open."""
        return self._find_element(self.MODAL_DIALOG).is_displayed()

    def wait_for_visible(self) -> "AddChildModal":
        """Wait until the modal dialog becomes visible.

        Returns:
            The modal instance for chaining.
        """
        self._wait_visible(self.MODAL_DIALOG)
        return self

    def is_modal_title_displayed(self) -> bool:
        """Check if the "Додати дитину" title is visible."""
        return self._find_element(self.MODAL_TITLE).is_displayed()

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

    def close_modal(self) -> None:
        """Close the modal via x button."""
        self._wait_clickable(self.CLOSE_BUTTON).click()
