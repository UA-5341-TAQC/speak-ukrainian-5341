"""Test suite for verifying Catalog Club's Location functionality (TC-10)."""

from __future__ import annotations

import allure
import pytest

from data.config import Config
from pages.clubs_page import ClubPage
from pages.home_page import HomePage


@allure.feature("Clubs Catalog")
class TestCatalogClubLocation:
    """Test suite for verifying club locations on the map."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Open home page before each test."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-10")
    @allure.title("TC-10: Catalog: Club's Location")
    @allure.description(
        "Verify that the map modal displays clubs according "
        "to the selected city and category."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_catalog_club_location(self, driver) -> None:
        home_page = HomePage(driver)

        with allure.step("Step 1: Open 'Гуртки' catalog"):
            home_page.header.click_clubs()

            club_page = ClubPage(driver)
            club_page.wait_loaded()

            clubs_count = club_page.get_clubs_count()

            assert 0 < clubs_count <= 8, (
                f"Expected from 1 to 8 clubs on the catalog page, "
                f"but got {clubs_count}"
            )

        with allure.step("Step 2: Open map and verify Kyiv is selected by default"):
            map_modal = club_page.open_map_modal()

            assert map_modal.is_displayed(), "Map modal should be displayed"

            assert map_modal.get_selected_city() == "Київ", (
                "Kyiv should be selected by default"
            )

            assert map_modal.get_clubs_count() > 0, (
                "Sidebar should display clubs for Kyiv by default"
            )

        with allure.step("Step 3: Select city 'Харків'"):
            map_modal.select_city("Харків")

            assert map_modal.get_selected_city() == "Харків", (
                "Kharkiv should be selected"
            )

            assert map_modal.get_clubs_count() > 0, (
                "Sidebar should contain clubs located in Kharkiv"
            )

            kharkiv_pins = map_modal.get_pins_count()

            assert kharkiv_pins > 0, (
                "Location pins should be displayed for Kharkiv"
            )

        with allure.step("Step 4: Select city 'Полтава'"):
            map_modal.select_city("Полтава")

            assert map_modal.get_selected_city() == "Полтава", (
                "Poltava should be selected"
            )

            no_results_message = map_modal.get_no_results_text()

            assert "Нічого не знайдено" in no_results_message, (
                f"Expected 'Нічого не знайдено' message, "
                f"but got '{no_results_message}'"
            )

        with allure.step("Step 5: Select 'Всі міста'"):
            map_modal.select_city("Всі міста")

            assert map_modal.get_selected_city() == "Всі міста", (
                "'Всі міста' should be selected"
            )

            all_cities_clubs_count = map_modal.get_clubs_count()

            assert all_cities_clubs_count > 0, (
                "Sidebar should display clubs when 'Всі міста' is selected"
            )

        with allure.step("Step 6: Select category 'Спортивні секції'"):
            map_modal.select_category("Спортивні секції")

            assert map_modal.get_selected_category() == "Спортивні секції", (
                "'Спортивні секції' should be selected"
            )

            assert map_modal.get_clubs_count() > 0, (
                "Sidebar should contain clubs of 'Спортивні секції' category"
            )

