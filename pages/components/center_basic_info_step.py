"""Component Object for the Basic Information step of Add Center."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CenterBasicInfoStep(BaseComponent):
    """Represent the 'Основна інформація' step."""

    BASIC_FORM: Locator = (
        By.CSS_SELECTOR,
        "div.input-data form#basic",
    )
    CENTER_NAME_INPUT: Locator = (
        By.ID,
        "basic_name",
    )
    ADD_LOCATION_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.add-location-btn",
    )
    LOCATION_CHECKBOXES: Locator = (
        By.CSS_SELECTOR,
        "#basic_locations input[type='checkbox']",
    )
    NEXT_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.next-btn",
    )

    def __init__(self, root: WebElement):
        """Initialize the Basic Information step."""
        super().__init__(root)

    def wait_loaded(self) -> "CenterBasicInfoStep":
        """Wait until the Basic Information step is visible."""
        self._wait_visible(self.BASIC_FORM)
        return self

    @allure.step("Enter center name: {name}")
    def enter_center_name(self, name: str) -> None:
        """Enter the center name."""
        field = self._wait_visible(self.CENTER_NAME_INPUT)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(name)

    @allure.step("Open Add Location modal")
    def click_add_location(self) -> None:
        """Click the 'Додати локацію' button."""
        self._wait_clickable(self.ADD_LOCATION_BUTTON).click()

    @allure.step("Select the first available center location")
    def select_first_location(self) -> None:
        """Select the first available location checkbox."""
        try:
            checkboxes = self.wait.until(
                lambda _: self._find_elements(self.LOCATION_CHECKBOXES) or False
            )
        except Exception as e:
            raise AssertionError(
                "No center location checkboxes were found (Possible backend bug)."
            ) from e

        checkbox = checkboxes[0]
        if not checkbox.is_selected():
            checkbox.click()

    @allure.step("Go to the Contacts step")
    def click_next(self) -> None:
        """Go to the next Add Center step."""
        self._wait_clickable(self.NEXT_BUTTON).click()
