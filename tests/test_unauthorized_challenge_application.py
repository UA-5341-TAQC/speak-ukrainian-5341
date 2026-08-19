"""Test suite for verifying unauthorized user challenge application restrictions (TC-16)."""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage
from pages.challenge_page import ChallengePage


CHALLENGES = [
    "Єдині",
    "Клуб української мови Розмовляй",
    "Навчай українською челендж",
    "Мовомаратон",
    "Навчай українською",
]


@allure.feature("Challenge")
class TestUnauthorizedChallengeApplication:
    """Test suite for verifying challenge application restrictions."""

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver) -> None:
        """Open home page before each test."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-16")
    @allure.title(
        "TC-16: Unauthorized user cannot apply to the challenge "
        "using 'Записатися на челендж' button"
    )
    @allure.description(
        "Verify that an unauthorized user cannot apply to the selected "
        "challenge and the disabled registration button displays "
        "the appropriate tooltip."
    )
    @allure.label("owner", "Svitlana Kovalova")
    @pytest.mark.regression
    @pytest.mark.parametrize("challenge", CHALLENGES)
    def test_unauthorized_user_cannot_apply_to_challenge(
        self,
        driver: WebDriver,
        challenge: str,
    ) -> None:
        """Verify unauthorized user cannot apply to the selected challenge."""
        home_page = HomePage(driver)

        with allure.step("Step 1: Click the 'Челендж' from the top menu"):
            home_page.header.click_challenge()
            dropdown = home_page.header.get_challenge_dropdown()

        with allure.step(
            f"Step 2: Select '{challenge}' from the dropdown menu"
        ):
            dropdown.select_challenge(challenge)

            challenge_page = ChallengePage(driver)
            challenge_page.wait.until(
                lambda _: "/challenges/" in driver.current_url
            ), "Challenge page is not opened"

        with allure.step(
            "Step 3: Scroll to the 'Записатися на челендж' button"
        ):
            challenge_page._scroll_into_view(
                challenge_page.CTA_BUTTON
            )

            cta_component = challenge_page.get_visible_cta_button()

            assert not cta_component.is_enabled(), (
                f"The 'Записатися на челендж' button should be inactive "
                f"and not clickable for unauthorized user on "
                f"'{challenge}' challenge"
            )

        with allure.step(
            "Step 4: Hover over the disabled button and verify tooltip"
        ):
            challenge_page.hover_over_cta_button()

            tooltip_text = challenge_page.get_cta_tooltip_text()

            assert tooltip_text == (
                "Ця функціональність доступна тільки користувачу"
            ), (
                f"Unexpected tooltip text for '{challenge}': "
                f"'{tooltip_text}'"
            )
