<<<<<<< HEAD
"""Page object for the News Details page on the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage
from pages.components.news_card_component import NewsCardComponent
from pages.components.social_buttons import SocialButtons
from pages.types import Locator


class NewsDetailsPage(BasePage):
    """Page object representing the detailed view of a single news article."""

    NEWS_MAJOR_TITLE: Locator = (By.ID, "major-title")
    NEWS_BANNER_IMAGE: Locator = (By.CSS_SELECTOR, ".news-page .image")
    NEWS_CONTENT_TITLE: Locator = (By.CSS_SELECTOR, ".content-title #title")
    NEWS_CONTENT_DATE: Locator = (By.CSS_SELECTOR, ".content-title #date")
    NEWS_DESCRIPTION: Locator = (By.ID, "description")

    NEWS_CAROUSEL_TITLE: Locator = (By.CSS_SELECTOR, ".other-news .title")
    NEWS_CAROUSEL_LEFT_ARROW: Locator = (
        By.CSS_SELECTOR, ".other-news .anticon-arrow-left",
    )
    NEWS_CAROUSEL_RIGHT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".other-news .news-carousel-block > .anticon-arrow-right.arrow",
    )
    NEWS_ACTIVE_SLIDE_CARDS: Locator = (
        By.CSS_SELECTOR,
        ".other-news .slick-slide.slick-active .carousel-item",
    )

    SOCIAL_SECTION_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        ".social-info .social-media",
    )

    def __init__(self, driver: WebDriver) -> None:
        """Initialize NewsDetailsPage with generic sub-components."""
        super().__init__(driver)

    @allure.step("Open news details page (id={news_id})")
    def open(self, news_id: int = 27) -> "NewsDetailsPage":
        """Open the news details page for a specific news article by ID."""
        from data.config import Config
        self.driver.get(f"{Config.BASE_UI_URL}/news/{news_id}")
        return self

    @allure.step("Scroll to 'Наші контакти' block")
    def scroll_to_contacts(self) -> "NewsDetailsPage":
        """Scroll the contacts section into view."""
        self._scroll_into_view(self.SOCIAL_SECTION_CONTAINER)
        return self

    @property
    @allure.step("Access Social Buttons component")
    def social_buttons(self) -> SocialButtons:
        """Get the SocialButtons sub-component instance."""
        section = self._wait_visible(self.SOCIAL_SECTION_CONTAINER)
        return SocialButtons(section)

    @allure.step("Get major news title text")
    def get_news_major_title_text(self) -> str:
        """Get the title text from the main banner image."""
        return self._find_element(self.NEWS_MAJOR_TITLE).text.strip()

    @allure.step("Get main news content title text")
    def get_news_content_title_text(self) -> str:
        """Get article title text inside the main content section."""
        return self._find_element(self.NEWS_CONTENT_TITLE).text.strip()

    @allure.step("Get news publication date text")
    def get_news_publication_date_text(self) -> str:
        """Get article publication date text."""
        return self._find_element(self.NEWS_CONTENT_DATE).text.strip()

    @allure.step("Get news full description text")
    def get_news_description_text(self) -> str:
        """Get full article text content."""
        return self._find_element(self.NEWS_DESCRIPTION).text.strip()

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
        return [NewsCardComponent(el) for el in elements]
=======
"""Page object for the News Details page on the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage
from pages.components.news_card_component import NewsCardComponent
from pages.components.social_buttons import SocialButtons
from pages.types import Locator


class NewsDetailsPage(BasePage):
    """Page object representing the detailed view of a single news article."""

    NEWS_MAJOR_TITLE: Locator = (By.ID, "major-title")
    NEWS_BANNER_IMAGE: Locator = (By.CSS_SELECTOR, ".news-page .image")
    NEWS_CONTENT_TITLE: Locator = (By.CSS_SELECTOR, ".content-title #title")
    NEWS_CONTENT_DATE: Locator = (By.CSS_SELECTOR, ".content-title #date")
    NEWS_DESCRIPTION: Locator = (By.ID, "description")

    NEWS_CAROUSEL_TITLE: Locator = (By.CSS_SELECTOR, ".other-news .title")
    NEWS_CAROUSEL_LEFT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".other-news .anticon-arrow-left",
    )
    NEWS_CAROUSEL_RIGHT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".other-news .news-carousel-block > .anticon-arrow-right.arrow",
    )
    NEWS_ACTIVE_SLIDE_CARDS: Locator = (
        By.CSS_SELECTOR,
        ".other-news .slick-slide.slick-active .carousel-item",
    )

    SOCIAL_SECTION_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        ".social-info .social-media",
    )

    @allure.step("Open news details page (id={news_id})")
    def open(self, news_id: int) -> "NewsDetailsPage":
        """Open the news details page for a specific news article by ID."""
        self.driver.get(f"{self.get_base_url()}/news/{news_id}")
        self._wait_visible(self.NEWS_MAJOR_TITLE)
        return self

    @allure.step("Scroll to 'Наші контакти' block")
    def scroll_to_contacts(self) -> "NewsDetailsPage":
        """Scroll the contacts section into view."""
        self._scroll_into_view(self.SOCIAL_SECTION_CONTAINER)
        return self

    @property
    @allure.step("Access Social Buttons component")
    def social_buttons(self) -> SocialButtons:
        """Get the SocialButtons sub-component instance."""
        section = self._wait_visible(self.SOCIAL_SECTION_CONTAINER)
        return SocialButtons(section)

    @allure.step("Get major news title text")
    def get_news_major_title_text(self) -> str:
        """Get the title text from the main banner image."""
        return self._find_element(self.NEWS_MAJOR_TITLE).text.strip()

    @allure.step("Wait until the visible article title matches the expected text")
    def wait_for_article_title(self, expected_title: str) -> None:
        """Wait until the article banner title equals the expected title.

        The banner title (#major-title) is the only visible article title on
        the details page; the title inside .content-title is rendered with
        display: none. Waiting on the text, not just presence, covers the
        SPA route transition after clicking a news card.
        """
        self.wait.until(
            lambda _: self._find_element(self.NEWS_MAJOR_TITLE).text.strip() == expected_title
        )

    @allure.step("Wait until the page URL equals the expected URL")
    def wait_for_current_url(self, expected_url: str) -> None:
        """Wait until the current URL matches the expected URL.

        The SPA updates the URL before the article content is rendered, so
        waiting on the URL alone is not enough; pair with
        `wait_for_article_title` when content readiness matters.
        """
        self.wait.until(lambda _: self.driver.current_url.rstrip("/") == expected_url.rstrip("/"))

    @allure.step("Get main news content title text")
    def get_news_content_title_text(self) -> str:
        """Get article title text inside the main content section."""
        return self._find_element(self.NEWS_CONTENT_TITLE).text.strip()

    @allure.step("Get news publication date text")
    def get_news_publication_date_text(self) -> str:
        """Get article publication date text."""
        return self._find_element(self.NEWS_CONTENT_DATE).text.strip()

    @allure.step("Get news full description text")
    def get_news_description_text(self) -> str:
        """Get full article text content."""
        return self._find_element(self.NEWS_DESCRIPTION).text.strip()

    @allure.step("Click right arrow in news carousel")
    def click_carousel_next(self) -> None:
        """Click right navigation arrow in carousel."""
        self.wait.until(ec.element_to_be_clickable(self.NEWS_CAROUSEL_RIGHT_ARROW)).click()

    @allure.step("Click left arrow in news carousel")
    def click_carousel_prev(self) -> None:
        """Click left navigation arrow in carousel."""
        self.wait.until(ec.element_to_be_clickable(self.NEWS_CAROUSEL_LEFT_ARROW)).click()

    @allure.step("Scroll to the 'Інші новини' block")
    def scroll_to_other_news(self) -> None:
        """Scroll the 'Інші новини' carousel into view."""
        self._scroll_into_view(self.NEWS_CAROUSEL_TITLE)

    @allure.step("Get the 'Інші новини' block title")
    def get_other_news_title(self) -> str:
        """Get the title text of the 'Інші новини' block."""
        return self._get_text(self.NEWS_CAROUSEL_TITLE).strip()

    @allure.step("Get list of currently active news cards in carousel")
    def get_active_carousel_cards(self) -> list[NewsCardComponent]:
        """Find visible carousel slides and wrap them in NewsCardComponent instances."""
        elements = self.wait.until(
            ec.visibility_of_all_elements_located(self.NEWS_ACTIVE_SLIDE_CARDS)
        )
        return [NewsCardComponent(el) for el in elements]

    @allure.step("Check if news title is displayed")
    def is_title_displayed(self) -> bool:
        """Check whether the article title is visible."""
        return self._wait_visible(self.NEWS_MAJOR_TITLE).is_displayed()

    @allure.step("Check if news publication date is displayed")
    def is_date_displayed(self) -> bool:
        """Check whether the article publication date is visible."""
        return self._wait_visible(self.NEWS_CONTENT_DATE).is_displayed()

    @allure.step("Check if news content is displayed")
    def is_description_displayed(self) -> bool:
        """Check whether the full article content is visible."""
        return self._wait_visible(self.NEWS_DESCRIPTION).is_displayed()
>>>>>>> main
