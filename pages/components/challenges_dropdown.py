"""Module containing the ChallengeDropdown component."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeDropdown(BaseComponent):
    """Component representing the Challenge dropdown menu."""

    TEACH_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href*='/challenges/2']",
    )

    HISTORICAL_CHALLENGE_2026_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href*='/challenges/13']",
    )

    UPDATED_HISTORICAL_CHALLENGE_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href*='/challenges/15']",
    )

    UNIQUE_CHALLENGE_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href*='/challenges/1']",
    )

    @allure.step("Click 'Навчайся'")
    def click_teach(self) -> None:
        """Open the 'Навчайся' challenge."""
        self._wait_clickable_from_driver(self.TEACH_LINK).click()

    @allure.step("Click 'Історичний челендж 2026'")
    def click_historical_challenge_2026(self) -> None:
        """Open the 'Історичний челендж 2026'."""
        self._wait_clickable_from_driver(
            self.HISTORICAL_CHALLENGE_2026_LINK
        ).click()

    @allure.step("Click 'Оновлений історичний челендж'")
    def click_updated_historical_challenge(self) -> None:
        """Open the 'Оновлений історичний челендж'."""
        self._wait_clickable_from_driver(
            self.UPDATED_HISTORICAL_CHALLENGE_LINK
        ).click()

    @allure.step("Click 'Єдині'")
    def click_unique_challenge(self) -> None:
        """Open the 'Єдині' challenge."""
        self._wait_clickable_from_driver(self.UNIQUE_CHALLENGE_LINK).click()

    def select_challenge(self, challenge: str) -> None:
        """Select a challenge by its name using JavaScript click to prevent interception."""
        challenge_links = {
            "Навчайся": self.TEACH_LINK,
            "Історичний челендж 2026": self.HISTORICAL_CHALLENGE_2026_LINK,
            "Оновлений історичний челендж": self.UPDATED_HISTORICAL_CHALLENGE_LINK,
            "Єдині": self.UNIQUE_CHALLENGE_LINK,
        }

        if challenge not in challenge_links:
            raise ValueError(
                f"Unknown challenge: {challenge}"
            )

        locator = challenge_links[challenge]
        element = self._wait_clickable_from_driver(locator)

        with allure.step(f"Click '{challenge}' challenge link via JavaScript"):
            self.driver.execute_script("arguments[0].click();", element)
