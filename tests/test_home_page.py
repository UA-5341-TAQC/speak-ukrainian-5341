"""Tests for the homepage navigation and elements."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage


@allure.title("TC-50 Verify challenge and event banner navigation on the homepage")
@pytest.mark.smoke
def test_homepage_challenge_and_banner_navigation(driver: WebDriver) -> None:
    """Verify challenge and event banner navigation on the homepage."""
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("1. Scroll down to the 'Навчай українською' challenge section"):
        home_page.scroll_to_challenge_section()
        assert home_page.is_challenge_section_displayed(), "Challenge section is not displayed"

    with allure.step("2. Click the 'Дізнатися більше' button"):
        home_page.click_challenge_learn_more_button()
        assert "/challenge" in driver.current_url, "User was not redirected to the challenge page"

    with allure.step("3. Navigate back to the homepage"):
        driver.back()
        assert driver.current_url.rstrip("/") == Config.BASE_UI_URL.rstrip("/"), "Homepage is not displayed after navigating back"

    with allure.step("4. Scroll down to the event banner section"):
        home_page.scroll_to_event_banner()
        assert home_page.is_banner_image_displayed(), "Event banner is not displayed"

    with allure.step("5. Click the event banner"):
        home_page.click_banner_image()
        assert len(driver.window_handles) > 1, "A new tab was not opened"
        driver.switch_to.window(driver.window_handles[-1])
        assert "facebook.com/events/" in driver.current_url, "The URL is not a Facebook event page"
