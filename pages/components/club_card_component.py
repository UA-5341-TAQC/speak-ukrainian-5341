"""Club Card Component for the Speak Ukrainian website."""

from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from pages.club_details_page import ClubDetailsPage

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ClubCardComponent(BaseComponent):
    """Component for Single club card."""

    # locators
    TITLE: Locator = (By.CSS_SELECTOR, "div.name")
    CATEGORIES: Locator = (By.CSS_SELECTOR, "div.club-tags-box span-name")
    DESCRIPTION: Locator = (By.CSS_SELECTOR, "p.description")
    RATING: Locator = (By.CSS_SELECTOR, "ul.ant-rate")
    ADDRESS: Locator = (By.CSS_SELECTOR, "div.address")
    MORE_BUTTON: Locator = (By.CSS_SELECTOR, "a.ant-btn")

    @allure.step("Club Title")
    def title(self) -> str:
        """Return title."""
        return (self._find_element(self.TITLE).get_attribute("textContent") or "").strip()

    @allure.step("Club Categories")
    def categories(self) -> list[str]:
        """Return list of club categories."""
        elements = self._find_elements(self.CATEGORIES)
        return [(el.get_attribute("textContent") or "").strip() for el in elements]

    @allure.step("Club Description")
    def description(self) -> str:
        """Return club description."""
        return (self._find_element(self.DESCRIPTION).get_attribute("textContent") or "").strip()

    @allure.step("Club Address")
    def address(self) -> str:
        """Return club address."""
        return (self._find_element(self.ADDRESS).get_attribute("textContent") or "").strip()

    @allure.step("Click 'More information' button")
    def click_more_details(self) -> "ClubDetailsPage":
        """Click 'More information' button."""
        self._wait_clickable(self.MORE_BUTTON).click()
        from pages.club_details_page import ClubDetailsPage

        return ClubDetailsPage(self.driver)
