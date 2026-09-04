"""TC-08: News card displays information in fields.

  Step 1  Click the Новини menu item                       -> News page is displayed
  Step 2  Locate the first news card                       -> News card is visible
  Step 3  Verify that the news image is displayed          -> Image is displayed
  Step 4  Verify that the news title is displayed          -> Title is displayed
  Step 5  Verify that the publication date is displayed    -> Publication date is displayed
  Step 6  Verify that the news card is clickable           -> User can open the news details page
"""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage
from pages.news_page import NewsPage

@allure.title("TC-08: News card displays information in fields.")
def test_news_display_tc_38(driver:WebDriver)-> None:
    home_page = HomePage(driver)


    home_page.header.click_news()
    news_page = NewsPage(driver)
    # Step 1. Click the Новини menu item
    assert news_page.is_opened() == True

    # Step 2. Locate the first news card
    news_card = news_page.get_news_list().get_first_card()
    assert news_card.is_visible() == True

    # Step 3. Verify that the news image is displayed
    assert news_card.is_image_displayed() == True

    # Step 4. Verify that the news image is displayed
    assert news_card.is_title_visible() == True

    # Step 5. Verify that the publication date is displayed
    assert news_card.is_date_visible() == True

    # Step 6. Verify that the news card is clickable
    excepted_url = news_card.get_details_href()
    news_card.click_details()

    assert driver.current_url == excepted_url
