"""Test suite for verifying task carousel navigation on the Marathon page (TC-11)."""

from __future__ import annotations

from urllib.parse import urljoin
import allure
import pytest

from data.config import Config
from pages.marathon_page import MarathonPage


@allure.feature("Language Marathon")
class TestMarathonTaskCarousel:
    """Test suite for verifying carousel navigation via arrows and pagination dots."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Open the marathon page and scroll to tasks before each test."""
        driver.get(f"{Config.BASE_UI_URL}/marathon")

    @allure.issue("TC-11")
    @allure.title("TC-11: Task carousel navigation via arrows and pagination dots")
    @allure.description(
        "Verify that users can navigate through the 30 language marathon tasks "
        "using next/previous arrows and pagination dots."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_task_carousel_navigation(self, driver) -> None:
        marathon_page = MarathonPage(driver)

        with allure.step("Step 1 & 4: Verify task cards are displayed on page 1"):
            titles = marathon_page.get_visible_task_titles()
            assert len(titles) >= 2, f"Expected at least 2 visible task cards, got {len(titles)}"
            assert "Крок 1. Оточіть себе українською мовою" in titles
            assert "Крок 2. Подбайте про свою мотивацію" in titles

        with allure.step("Step 2 & 3: Count pagination dots and check active dot"):
            dot_count = marathon_page.get_pagination_dot_count()
            assert dot_count == 10, f"Expected 10 pagination dots, got {dot_count}"
            assert marathon_page.get_active_dot_index() == 1, "Dot 1 should be active by default"

        with allure.step("Step 5: Click the right arrow once"):
            marathon_page.click_next()
            assert marathon_page.get_active_dot_index() == 2, "Dot 2 should become active"

        with allure.step("Step 6: Click the left arrow once"):
            marathon_page.click_prev()
            assert marathon_page.get_active_dot_index() == 1, "Dot 1 should become active again"

        with allure.step("Step 7: Click left arrow while on page 1 (boundary check)"):
            marathon_page.click_prev()
            assert marathon_page.get_active_dot_index() == 1, "Carousel should stay on page 1"

        with allure.step("Step 8: Click last pagination dot (10)"):
            marathon_page.click_dot(10)
            assert marathon_page.get_active_dot_index() == 10, "Dot 10 should become active"
            titles = marathon_page.get_visible_task_titles()
            assert "Крок 30. Відчуйте себе переможцями!" in titles

        with allure.step("Step 9: Click right arrow while on page 10 (boundary check)"):
            marathon_page.click_next()
            assert marathon_page.get_active_dot_index() == 10, "Carousel should stay on page 10"

        with allure.step("Step 10: Click pagination dot 1"):
            marathon_page.click_dot(1)
            assert marathon_page.get_active_dot_index() == 1, "Dot 1 should be active"

        with allure.step("Step 11: Click pagination dot 5"):
            marathon_page.click_dot(5)
            assert marathon_page.get_active_dot_index() == 5, "Dot 5 should be active"

        with allure.step("Step 12: Click last pagination dot (10) again"):
            marathon_page.click_dot(10)
            assert marathon_page.get_active_dot_index() == 10, "Dot 10 should be active"
