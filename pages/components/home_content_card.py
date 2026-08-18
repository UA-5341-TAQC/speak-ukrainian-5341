"""Component representing a content card on the home page."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class HomeContentCard(BaseComponent):
    """Component representing a home page content card."""

    TITLE: Locator = (
        By.CSS_SELECTOR,
        ".name",
    )

    DESCRIPTION: Locator = (
        By.CSS_SELECTOR,
        ".description",
    )

    DETAILS: Locator = (
        By.CSS_SELECTOR,
        ".details",
    )

    LINK: Locator = (
        By.CSS_SELECTOR,
        "a.content",
    )

    @allure.step("Get card title")
    def get_title(self) -> str:
        """Return the title of the card."""
        return self._find_element(self.TITLE).text

    @allure.step("Get card description")
    def get_description(self) -> str:
        """Return the description of the card."""
        return self._find_element(self.DESCRIPTION).text

    @allure.step("Get card details text")
    def get_details_text(self) -> str:
        """Return the details text of the card."""
        return self._find_element(self.DETAILS).text

    @allure.step("Open content card")
    def click(self) -> None:
        """Click the card."""
        self._wait_clickable(self.LINK).click()

    @allure.step("Get card link")
    def get_link(self) -> str:
        """Return the card link href ("", when absent)."""
        return self._find_element(self.LINK).get_attribute("href") or ""
