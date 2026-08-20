"""Test suite for verifying navigation to the Clubs page (TC-38)."""

from __future__ import annotations

import allure
import pytest

from data.config import Config
from pages.home_page import HomePage
from pages.clubs_page import ClubPage


@allure.feature("Home Page Navigation")
class TestHomePageClubsNavigation:
    """Test suite for verifying navigation to the Clubs page (TC-38)."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Open home page before each test."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-38")
    @allure.title(
        "TC-38: Verify navigation to the Clubs page from the homepage"
    )
    @allure.description(
        "Verify navigation from the homepage to the Clubs page via the 'Всі гуртки' "
        "button and individual club category cards ('Спортивні секції', 'Танці, хореографія', 'Студії раннього розвитку')."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_verify_clubs_navigation_and_categories(self, driver) -> None:
        home_page = HomePage(driver)

        with allure.step(
            "Step 1 & 2: Scroll to and click 'Всі гуртки' button"
        ):
            home_page._scroll_into_view(home_page.ALL_CLUBS_BUTTON)
            clubs_page: ClubPage = home_page.click_all_clubs_button()

            assert clubs_page.get_current_url().endswith("/clubs"), (
                f"Expected URL to end with '/clubs', but got '{driver.current_url}'"
            )

        with allure.step(
            "Step 3: Navigate back to the homepage using browser back"
        ):
            driver.back()

            home_page.wait.until(
                lambda _: not driver.current_url.rstrip("/").endswith("/clubs")
            )

            assert not driver.current_url.rstrip("/").endswith("/clubs"), (
                "User should return to the homepage"
            )

        with allure.step(
            "Step 4 & 5: Scroll to categories and click the first category card ('Спортивні секції')"
        ):
            home_page._scroll_into_view(home_page.CONTENT_CARDS)
            card_1 = home_page.get_content_card_by_title("Спортивні секції")
            card_1.click()

            assert clubs_page.get_current_url().endswith("/clubs"), (
                "User should be redirected to the Clubs page"
            )

        with allure.step("Step 6: Navigate back to the homepage"):
            driver.back()

            home_page.wait.until(
                lambda _: not driver.current_url.rstrip("/").endswith("/clubs")
            )

        with allure.step(
            "Step 7 & 8: Click the second category card ('Танці, хореографія')"
        ):
            home_page._scroll_into_view(home_page.CONTENT_CARDS)
            card_2 = home_page.get_content_card_by_title("Танці, хореографія")
            card_2.click()

            assert "/clubs" in driver.current_url, (
                "User should be redirected to the Clubs page"
            )

        with allure.step("Step 8 (cont.): Navigate back to the homepage"):
            driver.back()

            home_page.wait.until(
                lambda _: not driver.current_url.rstrip("/").endswith("/clubs")
            )

        with allure.step(
            "Step 9: Click the third category card ('Студії раннього розвитку')"
        ):
            home_page._scroll_into_view(home_page.CONTENT_CARDS)
            card_3 = home_page.get_content_card_by_title("Студії раннього розвитку")
            card_3.click()

            assert "/clubs" in driver.current_url, (
                "User should be redirected to the Clubs page with the selected category"
            )
