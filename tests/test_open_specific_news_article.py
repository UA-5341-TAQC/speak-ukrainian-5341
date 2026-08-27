"""TC-18: Opening a specific news article from the News page."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.news_details_page import NewsDetailsPage
from pages.news_page import NewsPage

NEWS_TITLE = 'Новий курс "Єдині": почніть літо із переходу на українську'
NEWS_ID = 27
EXPECTED_DATE = "28.05.2023"
EXPECTED_DESCRIPTION_FIRST_PARAGRAPH = "Проєкт «Єдині» допоможе вашим друзям перейти на українську!"
EXPECTED_IMAGE_FILENAME = "14_course_registrationpost.jpg"

@allure.feature("News")
@allure.title("TC-18: Opening a specific news article from the News page")
def test_open_specific_news_article(driver: WebDriver) -> None:
    """Verify that opening a news card leads to the correct, fully rendered details page."""
    news_page = NewsPage(driver).open()
    expected_news_url = f"{news_page.get_base_url()}/news/{NEWS_ID}"

    with allure.step("Review available news cards on the page"):
        cards = news_page.get_news_list().get_cards()
        assert len(cards) > 0

    with allure.step(f"Find the required news card: '{NEWS_TITLE}'"):
        target_card = None
        for card in cards:
            if card.get_title() == NEWS_TITLE:
                target_card = card
                break

        assert target_card is not None, f"News card with title '{NEWS_TITLE}' was not found."

    with allure.step("Click the 'Детальніше' button on the selected news card"):
        target_card.click_details()

    news_details_page = NewsDetailsPage(driver)

    with allure.step("Verify the opened URL"):
        news_details_page.wait_for_current_url(expected_news_url)
        assert driver.current_url.rstrip("/") == expected_news_url

    with allure.step("Verify news title on the opened page"):
        news_details_page.wait_for_article_title(NEWS_TITLE)
        assert news_details_page.get_news_major_title_text() == NEWS_TITLE

    with allure.step("Verify the main news image is displayed correctly"):
        assert news_details_page.is_banner_image_available()
        assert EXPECTED_IMAGE_FILENAME in news_details_page.get_banner_image_url()
        width, height = news_details_page.get_banner_image_size()
        assert width > 0 and height > 0


    assert news_details_page.get_news_publication_date_text() == EXPECTED_DATE

    description = news_details_page.get_news_description_text()
    assert description.startswith(EXPECTED_DESCRIPTION_FIRST_PARAGRAPH)

    with allure.step("Scroll through the article description"):
        news_details_page.scroll_to_contacts()
        assert news_details_page.is_description_displayed()

    with allure.step("Refresh the page and verify content remains correct"):
        driver.refresh()
        news_details_page.wait_for_article_title(NEWS_TITLE)

        assert driver.current_url.rstrip("/") == expected_news_url
        assert news_details_page.get_news_major_title_text() == NEWS_TITLE
        assert news_details_page.is_banner_image_available()
        assert news_details_page.get_news_publication_date_text() == EXPECTED_DATE
        assert news_details_page.get_news_description_text().startswith(EXPECTED_DESCRIPTION_FIRST_PARAGRAPH)