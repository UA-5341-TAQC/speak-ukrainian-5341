"""Test suite for verifying Marathon registration CTA functionality (TC-13)."""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.marathon_page import MarathonPage


@allure.feature("Language Marathon")
class TestMarathonRegistrationCTA:
    """Test suite for verifying 'Зареєструватись' CTA on the marathon page."""

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver) -> None:
        """Open marathon page before each test."""
        driver.get(f"{Config.BASE_UI_URL}/marathon")

    @allure.issue("TC-13")
    @allure.title(
        "TC-13: 'Зареєструватись' CTA opens registration page"
    )
    @allure.description(
        "Verify that the 'Зареєструватись' button is visible and enabled, "
        "opens the registration page, supports browser back navigation, "
        "and the registration page is accessible directly."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_marathon_registration_cta(self, driver: WebDriver) -> None:
        marathon_page = MarathonPage(driver)

        with allure.step(
            "Step 1: Wait for marathon page and verify registration button"
        ):

            button = marathon_page._wait_visible(
                marathon_page.REGISTER_BUTTON
            )

            assert button.is_displayed(), (
                "Registration button should be visible"
            )

            assert button.is_enabled(), (
                "Registration button should be enabled"
            )

            assert button.text.strip() == "Зареєструватись", (
                "Button should have text 'Зареєструватись'"
            )

        with allure.step(
            "Step 2: Scroll to and click 'Зареєструватись'"
        ):
            marathon_page._scroll_into_view(marathon_page.REGISTER_BUTTON)
            marathon_page.click_register()

        with allure.step(
            "Step 3: Verify navigation to registration page"
        ):
            marathon_page.wait.until(
                lambda _: "/marathon/registration" in driver.current_url
            )

            assert "/marathon/registration" in driver.current_url, (
                "User should be redirected to the registration page"
            )

        with allure.step(
            "Step 4: Verify registration page is loaded"
        ):
            assert driver.execute_script(
                "return document.readyState"
            ) == "complete", (
                "Registration page should be completely loaded"
            )

        with allure.step(
            "Step 5: Return to marathon page using browser back"
        ):
            driver.back()

            marathon_page.wait.until(
                lambda _: driver.current_url.rstrip("/").endswith("/marathon")
            )

            assert driver.current_url.rstrip("/").endswith("/marathon"), (
                "User should return to the marathon page"
            )

        with allure.step(
            "Step 6: Open registration page directly"
        ):
            driver.get(f"{Config.BASE_UI_URL}/marathon/registration")

            marathon_page.wait.until(
                lambda _: "/marathon/registration" in driver.current_url
            )

            assert "/marathon/registration" in driver.current_url, (
                "Registration page should be accessible directly"
            )

        with allure.step(
            "Step 7: Verify registration page loads from direct URL"
        ):
            assert driver.execute_script(
                "return document.readyState"
            ) == "complete", (
                "Registration page should be completely loaded "
                "when opened directly"
            )
