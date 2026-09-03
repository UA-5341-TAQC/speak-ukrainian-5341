"""Module containing the ChallengeDropdown component."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeDropdown(BaseComponent):
    """Component representing the Challenge dropdown menu."""

    UNIQUE_CHALLENGE_LINK: Locator = (
        By.CSS_SELECTOR,
       "a[href='/challenges/5']",
    )

    SPEAKING_CLUB_CHALLENGE_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href='/challenges/4']",
    )

    TEACH_UKRAINIAN_CHALLENGE_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href='/challenges/3']",
    )

    LANGUAGE_MARATHON_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href='/challenges/1']",
    )

    TEACH_UKRAINIAN_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href='/challenges/2']",
    )

    LEARN_UPD_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href*='/challenges/2']",
    )

    UNIQUE_UPD_LINK: Locator = (
        By.CSS_SELECTOR,
       "a[href*='/challenges/1']",
    )

    @allure.step("Click 'Єдині'")
    def click_unique_challenge(self) -> None:
        """Open the 'Єдині' challenge."""
        self._wait_clickable_from_driver(self.UNIQUE_CHALLENGE_LINK).click()


    @allure.step("Click 'Єдині', updated")
    def click_unique_upd_challenge(self) -> None:
        """Open the 'Єдині' challenge for updated page."""
        self._wait_clickable_from_driver(self.UNIQUE_UPD_LINK).click()

    @allure.step("Click 'Навчай', updated")
    def click_learn_upd_challenge(self) -> None:
        """Open the 'Навчай' challenge for updated page."""
        self._wait_clickable_from_driver(self.LEARN_UPD_LINK).click()

    @allure.step("Click 'Клуб української мови Розмовляй'")
    def click_speaking_club_challenge(self) -> None:
        """Open the 'Розмовляй' challenge."""
        self._wait_clickable_from_driver(
            self.SPEAKING_CLUB_CHALLENGE_LINK
        ).click()

    @allure.step("Click 'Навчай українською челендж'")
    def click_teach_ukrainian_challenge(self) -> None:
        """Open the 'Навчай українською челендж'."""
        self._wait_clickable_from_driver(
            self.TEACH_UKRAINIAN_CHALLENGE_LINK
        ).click()

    @allure.step("Click 'Мовомаратон'")
    def click_language_marathon(self) -> None:
        """Open the 'Мовомаратон' challenge."""
        self._wait_clickable_from_driver(self.LANGUAGE_MARATHON_LINK).click()

    @allure.step("Click 'Навчай українською'")
    def click_teach_ukrainian(self) -> None:
        """Open the 'Навчай українською' challenge."""
        self._wait_clickable_from_driver(self.TEACH_UKRAINIAN_LINK).click()

    def select_challenge(self, challenge: str) -> None:
        """Select a challenge by its name."""
        challenge_actions = {
            "Єдині": self.click_unique_challenge,
            "Клуб української мови Розмовляй":
                self.click_speaking_club_challenge,
            "Навчай українською челендж":
                self.click_teach_ukrainian_challenge,
            "Мовомаратон":
                self.click_language_marathon,
            "Навчай українською":
                self.click_teach_ukrainian,
        }

        if challenge not in challenge_actions:
            raise ValueError(
                f"Unknown challenge: {challenge}"
            )

        challenge_actions[challenge]()
