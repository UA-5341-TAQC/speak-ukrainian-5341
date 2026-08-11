"""Component representing a carousel item."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CarouselItem(BaseComponent):
    """Component representing a carousel slide."""

    TITLE: Locator = (
        By.CSS_SELECTOR,
        ".label",
    )

    DESCRIPTION: Locator = (
        By.CSS_SELECTOR,
        ".description",
    )

    DETAILS_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".details-button",
    )

    LINK: Locator = (
        By.CSS_SELECTOR,
        "a",
    )

    @allure.step("Get carousel item title")
    def get_title(self) -> str:
        """Return the title of the carousel item."""
        return self._find_element(self.TITLE).text

    @allure.step("Get carousel item description")
    def get_description(self) -> str:
        """Return the description of the carousel item."""
        return self._find_element(self.DESCRIPTION).text

    @allure.step("Get carousel item link")
    def get_link(self) -> str:
        """Return the link of the carousel item."""
        return self._find_element(self.LINK).get_attribute("href") or ""

    @allure.step("Click 'Детальніше' button")
    def click_details_button(self) -> None:
        """Click the 'Детальніше' button."""
        self._wait_clickable(self.DETAILS_BUTTON).click()
