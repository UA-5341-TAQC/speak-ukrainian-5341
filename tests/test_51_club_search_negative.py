"""Automated test for TC-51: Club's Catalog - Club search (negative)."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.clubs_page import ClubPage
from pages.home_page import HomePage


@allure.feature("Clubs")
@allure.story("Club search")
@pytest.mark.regression
def test_tc_51_club_search_negative(driver: WebDriver) -> None:
    """Verify that invalid search queries return no matching clubs."""
    driver.get(Config.BASE_UI_URL)

    home_page = HomePage(driver).wait_loaded()
    header = home_page.header
    header_lower = home_page.header_lower

    with allure.step("Step 1: Click 'Гуртки' in the site header"):
        header.click_clubs()

        clubs_page = ClubPage(driver).wait_loaded()

        assert clubs_page.get_clubs_count() > 0

    search_data = ("Тест", "12334", "!@$%&*)")

    for query in search_data:
        with allure.step(f"Enter '{query}' in the search field"):
            header_lower = clubs_page.header_lower
            header_lower.search_club(query)

        with allure.step(f"Search for '{query}'"):
            header_lower.click_search()

            assert clubs_page.is_no_results_message_displayed(), (
                f"Expected no-results message for search query '{query}'"
            )
