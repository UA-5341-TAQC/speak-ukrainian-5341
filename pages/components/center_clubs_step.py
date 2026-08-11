from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class CenterClubsStep(BaseComponent):
    """Page object for the Center Clubs step of the Add Center modal."""

    MODAL_TITLE: Locator = (By.CSS_SELECTOR, "div.modal-title")
    CHOOSE_CLUBS_LABEL: Locator = (By.CSS_SELECTOR, "span.ant-typography")
    CLUBS_LIST: Locator = (By.ID, "clubs")

    BACK_BUTTON: Locator = (By.CSS_SELECTOR, "button.prev-btn")
    NEXT_BUTTON: Locator = (By.CSS_SELECTOR, "button.finish-btn")

    @allure.step("Get modal title text")
    def get_title(self) -> str:
        """Return the modal title text."""
        return self._find_element(self.MODAL_TITLE).text.strip()


    @allure.step("Get choose clubs label text")
    def get_choose_clubs_label(self) -> str:
        """Return the choose clubs label text."""
        return self._find_element(self.CHOOSE_CLUBS_LABEL).text.strip()


    @allure.step("Check if clubs list is displayed")
    def is_clubs_list_displayed(self) -> bool:
        """Check whether the clubs list is visible."""
        return self._find_element(self.CLUBS_LIST).is_displayed()


    @allure.step("Click Back button")
    def click_back(self) -> None:
        """Click the Back button."""
        self._wait_clickable(self.BACK_BUTTON).click()


    @allure.step("Click Next button")
    def click_next(self) -> None:
        """Click the Next button."""
        self._wait_clickable(self.NEXT_BUTTON).click()


    @allure.step("Check if Back button is enabled")
    def is_back_button_enabled(self) -> bool:
        """Check whether the Back button is enabled."""
        return self._find_element(self.BACK_BUTTON).is_enabled()


    @allure.step("Check if Next button is enabled")
    def is_next_button_enabled(self) -> bool:
        """Check whether the Next button is enabled."""
        return self._find_element(self.NEXT_BUTTON).is_enabled()
