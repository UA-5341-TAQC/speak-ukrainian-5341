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

    @allure.step("Click 'Єдині'")
    def click_unique_challenge(self) -> None:
        """Open the 'Єдині' challenge."""
        self._wait_clickable(self.UNIQUE_CHALLENGE_LINK).click()

    @allure.step("Click 'Клуб української мови Розмовляй'")
    def click_speaking_club_challenge(self) -> None:
        """Open the 'Розмовляй' challenge."""
        self._wait_clickable(
            self.SPEAKING_CLUB_CHALLENGE_LINK
        ).click()

    @allure.step("Click 'Навчай українською челендж'")
    def click_teach_ukrainian_challenge(self) -> None:
        """Open the 'Навчай українською челендж'."""
        self._wait_clickable(
            self.TEACH_UKRAINIAN_CHALLENGE_LINK
        ).click()

    @allure.step("Click 'Мовомаратон'")
    def click_language_marathon(self) -> None:
        """Open the 'Мовомаратон' challenge."""
        self._wait_clickable(self.LANGUAGE_MARATHON_LINK).click()

    @allure.step("Click 'Навчай українською'")
    def click_teach_ukrainian(self) -> None:
        """Open the 'Навчай українською' challenge."""
        self._wait_clickable(self.TEACH_UKRAINIAN_LINK).click()
