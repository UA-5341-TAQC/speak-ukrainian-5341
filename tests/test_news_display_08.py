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

from data.config import Config
from pages.home_page import HomePage
from pages.news_page import NewsPage

@allure.title("TC-08: News card displays information in fields.")
def test_news_display_tc_38(driver:WebDriver):
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("1.Click the user icon in the site header."):
        home_page.header.click_news()
        news_page = NewsPage(driver)

        assert news_page.is_opened() == True

    with allure.step("2.Locate the first news card"):
        pass


        
