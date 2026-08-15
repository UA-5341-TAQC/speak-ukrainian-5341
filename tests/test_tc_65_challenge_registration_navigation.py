"""Automated test for TC-65: Challenge registration navigation."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.challenge_page import ChallengePage
from pages.challenge_registration_page import ChallengeRegistrationPage
from pages.home_page import HomePage


@allure.title(
    'TC-65 User can register for the “Клуб української мови "Розмовляй" challenge'
)
@allure.feature("Challenge")
@allure.story("Speaking club challenge registration")
@pytest.mark.regression
def test_tc_65_speaking_club_challenge_registration(
    authenticated_driver: WebDriver,
) -> None: 
    """Verify navigation to the registration form for the 'Розмовляй' challenge."""
    driver = authenticated_driver
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("Step 1: Open the 'Челендж' dropdown menu"):
        home_page.header.click_challenge()
        challenge_dropdown = home_page.header.get_challenge_dropdown()

    with allure.step("Step 2: Open the 'Клуб української мови Розмовляй' challenge"):
        challenge_dropdown.click_speaking_club_challenge()

        challenge_page = ChallengePage(driver)
        challenge_page.wait.until(
            lambda current_driver: "/challenges/4" in current_driver.current_url
        )

        assert "/challenges/4" in driver.current_url, (
            "Expected the 'Розмовляй' challenge page to be opened."
        )

        assert challenge_page.get_title_text(), (
            "Expected the challenge page title to be displayed."
        )

    with allure.step("Step 3: Verify the challenge registration button is available"):
        challenge_page.scroll_cta_button_into_view()
        cta_button = challenge_page.get_cta_button()

        assert cta_button.is_enabled(), (
            "Expected the challenge registration button to be enabled."
        )

        assert cta_button.get_text() == "Записатись на челендж", (
            "Unexpected challenge registration button text."
        )

    with allure.step("Step 4: Open the challenge registration page"):
        challenge_page.click_cta_button()

        registration_page = ChallengeRegistrationPage(driver)

        registration_page.wait.until(
            lambda current_driver: "/registration" in current_driver.current_url,
            message=(
                "Expected result: The registration page should open after clicking "
                "'Записатись на челендж'. "
                f"Actual URL: {driver.current_url}"
            ),
        )

        assert registration_page.is_opened(), (
            "Expected the challenge registration page to be opened."
        )

    with allure.step("Step 5: Verify the Google registration form is displayed"):
        assert registration_page.is_google_form_container_displayed(), (
            "Expected the Google Form container to be displayed."
        )

        assert registration_page.is_google_form_iframe_displayed(), (
            "Expected the Google Form iframe to be displayed."
        )

        assert registration_page.has_valid_google_form_src(), (
            "Expected the registration iframe to contain a valid Google Forms URL."
        )

    # TC-65 step 5 is not automated yet because the current Page Objects
    # do not contain methods for interacting with the Google Form inside
    # the iframe or for verifying the final success message.

    # Type: Positive / Functional
    # Current execution status: Failed
    # Reason: application defect на Step 4.
