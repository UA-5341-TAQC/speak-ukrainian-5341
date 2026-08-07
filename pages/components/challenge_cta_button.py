"""Component object for the challenge registration button."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeCtaButton(BaseComponent):
    """Represent the ``Записатись на челендж`` call-to-action button."""

    BUTTON: Locator = (By.XPATH, ".")

    @allure.step("Click challenge registration button")
    def click(self) -> None:
        """Click the challenge registration button."""
        self._find_element(self.BUTTON).click()

    @allure.step("Get challenge registration button text")
    def get_text(self) -> str:
        """Return the visible text of the button."""
        return self._find_element(self.BUTTON).text

    @allure.step("Check whether challenge registration button is enabled")
    def is_enabled(self) -> bool:
        """Return whether the button is available for interaction."""
        return self._find_element(self.BUTTON).is_enabled()
