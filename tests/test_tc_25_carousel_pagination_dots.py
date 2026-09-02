"""Tests for TC-25 — 'Інші новини' carousel pagination dots on the News Details page."""

from __future__ import annotations

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.news_details_page import NewsDetailsPage


@allure.title("TC-25 Verify carousel pagination dots functionality")
def test_news_details_carousel_pagination_dots(driver: WebDriver) -> None:
    """Verify that the 'Інші новини' carousel can be navigated via pagination dots.

    Steps:
        1. Open a news article and scroll down to the 'Інші новини' block.
        2. Confirm pagination dots are visible and the first dot is active.
        3. Click the second dot.
        4. Verify the active dot transferred to the second dot and the
           displayed news cards belong to group 2.
        5. Click another (non-adjacent) dot.
        6. Verify the active dot transferred to the clicked dot and only
           one dot is active at a time.
    """
    news_page = NewsDetailsPage(driver)

    with allure.step("1. Scroll down to the 'Інші новини' block"):
        news_page.open(27)
        news_page.scroll_to_carousel()

    with allure.step("2. Verify default active dot status"):
        assert news_page.get_other_news_dots_count() >= 2, (
            "Expected at least 2 pagination dots under the carousel"
        )
        assert news_page.get_other_news_active_dot_index() == 1, (
            "First pagination dot should be active by default"
        )
        initial_first_card_title = news_page.get_active_carousel_cards()[0].get_title()

    with allure.step("3. Click on the second pagination dot"):
        news_page.click_other_news_dot(2)

    with allure.step("4. Verify content and active dot state"):
        assert news_page.get_other_news_active_dot_index() == 2, (
            "Second dot should become active"
        )
        assert (
            news_page.get_other_news_active_dot_count() == 1
        ), "Only one pagination dot should be active at a time"
        new_first_card_title = news_page.get_active_carousel_cards()[0].get_title()
        assert new_first_card_title != initial_first_card_title, (
            "Displayed news cards should change to match group 2"
        )

    with allure.step("5. Click on another (last) pagination dot"):
        last_index = news_page.get_other_news_dots_count()
        news_page.click_other_news_dot(last_index)

    with allure.step("6. Verify active state transfers to the selected dot"):
        assert news_page.get_other_news_active_dot_index() == last_index, (
            "Active dot should transfer to the clicked dot"
        )
        assert news_page.get_other_news_active_dot_count() == 1, (
            "Only one pagination dot should be active at a time"
        )
