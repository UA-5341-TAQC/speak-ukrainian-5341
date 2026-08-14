"""Automated test for TC-40 'Verify "Детальніше" button opens the selected news article'."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.news_details_page import NewsDetailsPage


def test_news_details_other_news_navigation(driver: WebDriver) -> None:
    """Verify opening another news article from the 'Інші новини' section."""
    news_details = NewsDetailsPage(driver)
    # Precondition: the news details page of article 27 is opened.
    news_details.open_article("27")

    with allure.step("1. Scroll down to the 'Інші новини' block"):
        news_details.scroll_to_other_news()
        assert news_details.get_other_news_title() == "Інші новини"
        target = news_details.get_active_carousel_cards()[0]
        expected_title = target.get_title()
        assert expected_title, "Selected card title is not visible"
        assert target.get_details_text() == "Детальніше"

    target_url = target.get_details_href()
    assert target_url, "The selected card has no details link"

    with allure.step("2. Click the 'Детальніше' button on the selected card"):
        target.click_details()

    with allure.step("3. Verify page URL update"):
        news_details.wait_for_current_url(target_url)
        assert "/news/" in driver.current_url

    with allure.step("4. Verify opened article content"):
        news_details.wait_for_article_title(expected_title)
        assert news_details.get_news_major_title_text() == expected_title

    with allure.step("5. Refresh the browser page"):
        news_details.refresh()
        news_details.wait_for_current_url(target_url)
        news_details.wait_for_article_title(expected_title)
        assert news_details.get_news_major_title_text() == expected_title
