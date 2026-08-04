"""Page object for the News Details page on the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from components.news_card_component import NewsCardComponent
from components.social_buttons import SocialButtons
from pages.base_page import BasePage

DEFAULT_TIMEOUT: int = 10


class NewsDetailsPage(BasePage):
    """Page object representing the detailed view of a single news article."""

    NEWS_MAJOR_TITLE: tuple[str, str] = (By.ID, "major-title")
    NEWS_BANNER_IMAGE: tuple[str, str] = (By.CSS_SELECTOR, ".news-page .image")
    NEWS_CONTENT_TITLE: tuple[str, str] = (By.CSS_SELECTOR, ".content-title #title")
    NEWS_CONTENT_DATE: tuple[str, str] = (By.CSS_SELECTOR, ".content-title #date")
    NEWS_DESCRIPTION: tuple[str, str] = (By.ID, "description")

    NEWS_CAROUSEL_TITLE: tuple[str, str] = (By.CSS_SELECTOR, ".other-news .title")
    NEWS_CAROUSEL_LEFT_ARROW: tuple[str, str] = (By.CSS_SELECTOR, ".other-news .anticon-arrow-left")
    NEWS_CAROUSEL_RIGHT_ARROW: tuple[str, str] = (By.CSS_SELECTOR, ".other-news .news-carousel-block > .anticon-arrow-right.arrow")
    NEWS_ACTIVE_SLIDE_CARDS: tuple[str, str] = (
        By.CSS_SELECTOR,
        ".other-news .slick-slide.slick-active .carousel-item",
    )

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize NewsDetailsPage with generic sub-components."""
        super().__init__(driver)
        self.wait = WebDriverWait(driver, timeout)

        self.social_buttons = SocialButtons(driver, timeout=timeout)


    @allure.step("Get major news title text")
    def get_news_major_title_text(self) -> str:
        """Get the title text from the main banner image."""
        return self._wait_visible(self.NEWS_MAJOR_TITLE).text.strip()

    @allure.step("Get main news content title text")
    def get_news_content_title_text(self) -> str:
        """Get article title text inside the main content section."""
        return self._wait_visible(self.NEWS_CONTENT_TITLE).text.strip()

    @allure.step("Get news publication date text")
    def get_news_publication_date_text(self) -> str:
        """Get article publication date text."""
        return self._wait_visible(self.NEWS_CONTENT_DATE).text.strip()

    @allure.step("Get news full description text")
    def get_news_description_text(self) -> str:
        """Get full article text content."""
        return self._wait_visible(self.NEWS_DESCRIPTION).text.strip()

    @allure.step("Click right arrow in news carousel")
    def click_carousel_next(self) -> None:
        """Click right navigation arrow in carousel."""
        self.wait.until(ec.element_to_be_clickable(self.NEWS_CAROUSEL_RIGHT_ARROW)).click()

    @allure.step("Click left arrow in news carousel")
    def click_carousel_prev(self) -> None:
        """Click left navigation arrow in carousel."""
        self.wait.until(ec.element_to_be_clickable(self.NEWS_CAROUSEL_LEFT_ARROW)).click()

    @allure.step("Get list of currently active news cards in carousel")
    def get_active_carousel_cards(self) -> list[NewsCardComponent]:
        """Find visible carousel slides and wrap them in NewsCardComponent instances."""
        elements = self.wait.until(
            ec.visibility_of_all_elements_located(self.NEWS_ACTIVE_SLIDE_CARDS)
        )
        return [NewsCardComponent(self.driver, root_element=el) for el in elements]

    def _wait_visible(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element located by locator becomes visible."""
        return self.wait.until(ec.visibility_of_element_located(locator))