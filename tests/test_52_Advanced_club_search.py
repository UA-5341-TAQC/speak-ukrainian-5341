"""Automated test for TC-52: Advanced club search sorting."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.clubs_page import ClubPage
from pages.home_page import HomePage


@allure.feature("Clubs")
@allure.story("Advanced club search sorting")
@pytest.mark.regression
def test_tc_52_advanced_club_search_sorting(driver: WebDriver) -> None:
    """Verify alphabetical sorting in the advanced club search."""
    # Preconditions
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("Step 1: Click 'Гуртки' in the site header"):
        home_page.get_header().click_clubs()
        clubs_page = ClubPage(driver).wait_loaded()

        assert "/clubs" in driver.current_url
        assert clubs_page.get_clubs_count() > 0

    club_sort = clubs_page.sort()
    club_filters = clubs_page.filter()

    with allure.step("Step 2: Open advanced club search"):
        club_sort.toggle_advanced_search()

        assert club_sort.is_sort_visible()
        assert club_filters.is_sider_visible()

    with allure.step("Verify ascending sorting is selected by default"):
        assert club_sort.is_arrow_up_active()

    with allure.step("Step 3: Select sorting 'за алфавітом'"):
        club_sort.sort_by_alphabet()

        assert club_sort.get_actual_alphabet_direction() == "asc"

    with allure.step("Step 4: Change alphabetical sorting to descending"):
        club_sort.toggle_alphabet_sort_direction()

        assert club_sort.get_actual_alphabet_direction() == "desc"
        assert club_sort.is_arrow_down_active()

    with allure.step("Step 5: Change alphabetical sorting back to ascending"):
        club_sort.toggle_alphabet_sort_direction()

        assert club_sort.get_actual_alphabet_direction() == "asc"
        assert club_sort.is_arrow_up_active()

    with allure.step("Step 6: Select sorting 'за рейтингом'"):
        club_sort.sort_by_rate()

        assert club_sort.get_current_direction() == "asc"

    with allure.step("Step 7: Change rating sorting to descending"):
        club_sort.set_sort_direction_by_rating("desc")

        assert club_sort.get_current_direction() == "desc"
        assert club_sort.is_arrow_down_active()
