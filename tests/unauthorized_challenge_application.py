"""Test suite for verifying unauthorized user challenge application restrictions (TC-16)."""

from __future__ import annotations

import allure
import pytest

from data.config import Config
from pages.challenge_page import ChallengePage
from pages.components.header_component import HeaderComponent


@allure.feature("Challenge")
class TestUnauthorizedChallengeApplication:
    """Test suite for verifying challenge application restrictions."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Open home page before each test."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-16")
    @allure.title(
        "TC-16: Unauthorized user cannot apply to the challenge "
        "using 'Записатись на челендж' button"
    )
    @allure.description(
        "Verify that an unauthorized user cannot apply to the challenge "
        "and the disabled registration button displays the appropriate tooltip."
    )
    @allure.label("owner", "Svitlana Kovalova")
    @pytest.mark.regression
    def test_unauthorized_user_cannot_apply_to_challenge(self, driver) -> None:
        """Verify unauthorized user cannot apply to the challenge."""

        header = HeaderComponent(driver)
        challenge_page = ChallengePage(driver)

        with allure.step("Step 1: Click the 'Челендж' from the top menu"):
            header.click_challenge()

        with allure.step(
            "Step 2: Select 'Мовомаратон' from the dropdown menu and click it"
        ):
            dropdown = header.get_challenge_dropdown()
            dropdown.click_language_marathon()

            challenge_page.wait.until(
                lambda _: "/challenges/" in driver.current_url
            ), "Challenge page is not opened"

        with allure.step(
            "Step 3: Scroll down to the end of the challenge description "
            "block and verify button and tooltip"
        ):
            challenge_page._scroll_into_view(
                challenge_page.CTA_BUTTON
            )

            cta_component = challenge_page.get_visible_cta_button()

            assert not cta_component.is_enabled(), (
                "The 'Записатися на челендж' button should be inactive "
                "and not clickable for unauthorized users"
            )

        with allure.step(
            "Step 4: Hover over the disabled 'Записатись на челендж' "
            "button and verify the tooltip"
        ):
            challenge_page.hover_over_cta_button()

            tooltip_text = challenge_page.get_cta_tooltip_text()

            assert tooltip_text == (
                "Ця функціональність доступна тільки користувачу"
            ), (
                f"Unexpected tooltip text: '{tooltip_text}'"
            )
