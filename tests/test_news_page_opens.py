"""Test suite for verifying the News Page functionality."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage
from pages.news_page import NewsPage


@allure.feature("News Page")
class TestNewsPage:
    """Test cases for the News page."""

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver) -> None:
        """Precondition: Navigate to the home page before executing tests."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-06")
    @allure.title("TC-06: Verify that the News page opens")
    @allure.description(
        "Verify that clicking the 'Новини' menu item in the header navigates "
        "the user to the News page with valid URL, title, and article list."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_verify_news_page_opens(self, driver: WebDriver)->None:
        with allure.step("Step 1: Open the Speak Ukrainian home page"):
            home_page = HomePage(driver)

        with allure.step("Step 2: Click the 'Новини' menu item in header"):
            home_page.header.click_news()

        with allure.step("Step 3: Verify the page URL contains '/news'"):
            news_page = NewsPage(driver)
            news_page.wait_loaded()
            current_url = driver.current_url
            assert "/news" in current_url, (
                f"Expected URL to contain '/news', but got '{current_url}'"
            )

        with allure.step("Step 4: Verify that the news page title is displayed"):
            assert news_page.is_title_displayed(), "News page title should be visible"

        with allure.step("Step 5: Verify that the news list is displayed and contains cards"):
            news_list_component = news_page.get_news_list()
            assert news_list_component is not None, "News list component should be initialized"
            assert news_list_component.get_cards_count() > 0, "News list should contain at least one card"
