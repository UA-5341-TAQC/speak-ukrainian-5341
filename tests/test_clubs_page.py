"""Automated test for TC-27: Club's Catalog - Club search (positive)."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage


@allure.feature("Clubs")
@allure.story("Club search")
@pytest.mark.parametrize("query", ["театр", "ТЕАТР", "ТеаТр"])
@allure.title("TC-27: Verify that the user can find a club by name")
def test_club_search_positive(driver: WebDriver, query: str) -> None:
    """Verify that the user can find a club by name."""
    home_page = HomePage(driver).open().wait_loaded()

    with allure.step("Step 1: Click 'Гуртки' in the site header"):
        clubs_page = home_page.header.click_clubs()
        assert clubs_page.get_clubs_count() > 0

    with allure.step(f"Step 2: Search for '{query}' and wait for results"):
        clubs_page.header_lower.search_club(query)
        clubs_page.header_lower.click_search()
        clubs_page.wait_for_search_results_contain(query)

        club_cards = clubs_page.get_club_cards()
        assert len(club_cards) > 0, f"Search displays no results for query '{query}'"

    with allure.step("Step 3: Verify search keyword is present in club cards"):
        expected_keyword = query.lower()
        for card in club_cards:
            title = card.title().lower()
            description = card.description().lower()
            categories = [cat.lower() for cat in card.categories()]

            match_found = (
                expected_keyword in title
                or expected_keyword in description
                or any(expected_keyword in cat for cat in categories)
            )

            assert match_found, (
                f"Resource block does not contain '{expected_keyword}' for query '{query}'.\n"
                f"Title: {title}\nDescription: {description}\nVisible Categories: {categories}"
            )
