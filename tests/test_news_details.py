"""Tests for the News Details page on the Speak Ukrainian website."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.news_details_page import NewsDetailsPage


@allure.title("TC-24 Verify carousel navigation using left and right arrows")
def test_news_details_carousel_navigation_arrows(driver: WebDriver) -> None:
    """Verify that 'Інші новини' carousel can be navigated using arrows."""
    news_page = NewsDetailsPage(driver)

    with allure.step("Precondition: Open News details page"):
        news_page.open(27)

    with allure.step("1. Scroll down to 'Інші новини' block"):
        news_page.scroll_to_carousel()

    with allure.step("2. Note the title of the first visible card"):
        initial_cards = news_page.get_active_carousel_cards()
        assert len(initial_cards) > 0, "No active cards found in the carousel"
        initial_first_card_title = initial_cards[0].get_title()

    with allure.step("3. Click the Right Navigation Arrow"):
        news_page.click_carousel_next()

    with allure.step("4. Verify displayed cards update"):
        news_page.wait_until_first_card_title_changes(initial_first_card_title)

    with allure.step("5. Click the Left Navigation Arrow"):
        news_page.click_carousel_prev()

    with allure.step("6. Verify return to initial state"):
        news_page.wait_until_first_card_title_equals(initial_first_card_title)

    with allure.step("7. Repeat rapid arrow navigation (stress check)"):
        news_page.click_carousel_next()
        news_page.click_carousel_prev()
        news_page.wait_until_first_card_title_equals(initial_first_card_title)
