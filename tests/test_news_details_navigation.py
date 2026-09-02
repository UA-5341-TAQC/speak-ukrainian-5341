"""TC-07: Navigation to the News details page."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage


@allure.feature("News navigation")
@allure.title("TC-07: Navigation to the News details page")
def test_navigation_to_news_details_page(driver: WebDriver) -> None:
    """Verify opening a news article from the list and returning back to the News page."""
    home_page = HomePage(driver).open()

    with allure.step("Click the 'Новини' menu item"):
        home_page.header.click_news()
        news_page = NewsPage(driver)
        news_page.wait_loaded()
        news_list_url = driver.current_url

    with allure.step("Click the first news title or image"):
        first_card = news_page.get_news_list().get_first_card()
        first_card.open()
        details_page = NewsDetailsPage(driver)

    assert details_page.is_title_displayed()
    assert details_page.is_date_displayed()
    assert details_page.is_description_displayed()

    with allure.step("Click the browser Back button"):
        driver.back()
        news_page.wait_loaded()
        assert driver.current_url == news_list_url