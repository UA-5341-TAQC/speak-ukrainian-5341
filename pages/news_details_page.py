"""Page object for the News Details page on the Speak Ukrainian website."""

import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

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
    NEWS_PAGINATION_DOTS: Locator = (
        By.CSS_SELECTOR,
        ".other-news .slick-dots li",
    )
    NEWS_ACTIVE_PAGINATION_DOT: Locator = (
        By.CSS_SELECTOR,
        ".other-news .slick-dots li.slick-active",
    )

    SOCIAL_SECTION_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        ".social-info",
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

    @allure.step("Scroll to 'Інші новини' carousel")
    def scroll_to_carousel(self) -> "NewsDetailsPage":
        """Scroll the other news carousel into view."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._scroll_into_view(self.NEWS_CAROUSEL_TITLE)
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
        self._wait_present((By.CSS_SELECTOR, ".news-carousel-block .slick-initialized"))
        self._click(self.NEWS_CAROUSEL_RIGHT_ARROW)

    @allure.step("Click left arrow in news carousel")
    def click_carousel_prev(self) -> None:
        """Click left navigation arrow in carousel."""
        self._click(self.NEWS_CAROUSEL_LEFT_ARROW)

    def _get_visible_carousel_cards(self) -> list[NewsCardComponent]:
        """Private helper to get currently visible cards without waiting or logging."""
        elements = self._find_elements(self.NEWS_ACTIVE_SLIDE_CARDS)
        return [NewsCardComponent(el) for el in elements if el.is_displayed()]

    @allure.step("Scroll to the 'Інші новини' block")
    def scroll_to_other_news(self) -> None:
        """Scroll the 'Інші новини' carousel into view."""
        self._scroll_into_view(self.NEWS_CAROUSEL_TITLE)

    @allure.step("Get the 'Інші новини' block title")
    def get_other_news_title(self) -> str:
        """Get the title text of the 'Інші новини' block."""
        return self._get_text(self.NEWS_CAROUSEL_TITLE).strip()

    @allure.step("Get the 'Інші новини' pagination dot count")
    def get_other_news_dots_count(self) -> int:
        """Return the number of pagination dots under the 'Інші новини' carousel."""
        self._wait_present(self.NEWS_PAGINATION_DOTS)
        return len(self._find_elements(self.NEWS_PAGINATION_DOTS))

    @allure.step("Get the index of the active 'Інші новини' pagination dot")
    def get_other_news_active_dot_index(self) -> int:
        """Return the 1-based index of the currently active pagination dot.

        Raises:
            ValueError: If no dot is marked active.
        """
        dots = self._find_elements(self.NEWS_PAGINATION_DOTS)
        for index, dot in enumerate(dots, start=1):
            if "slick-active" in (dot.get_attribute("class") or ""):
                return index
        raise ValueError("No active pagination dot found in the 'Інші новини' carousel.")

    @allure.step("Count active 'Інші новини' pagination dots")
    def get_other_news_active_dot_count(self) -> int:
        """Return how many dots currently have the slick-active class."""
        return len(self._find_elements(self.NEWS_ACTIVE_PAGINATION_DOT))

    @allure.step("Click the 'Інші новини' pagination dot at index {index}")
    def click_other_news_dot(self, index: int) -> None:
        """Click a pagination dot to jump the carousel to that group.

        Args:
            index: 1-based position of the dot to click.

        Raises:
            ValueError: If ``index`` is outside the available dot range.
        """
        dots = self._find_elements(self.NEWS_PAGINATION_DOTS)
        if not 1 <= index <= len(dots):
            raise ValueError(
                f"Dot index {index} out of range (1..{len(dots)}) for the 'Інші новини' carousel."
            )
        self._wait_clickable(self.NEWS_PAGINATION_DOTS)
        dots[index - 1].click()
        self.wait.until(lambda _: self.get_other_news_active_dot_index() == index)

    @allure.step("Get list of currently active news cards in carousel")
    def get_active_carousel_cards(self) -> list[NewsCardComponent]:
        """Find visible carousel slides and wrap them in NewsCardComponent instances."""
        self.wait.until(ec.visibility_of_all_elements_located(self.NEWS_ACTIVE_SLIDE_CARDS))
        return self._get_visible_carousel_cards()

    def _wait_for_first_card_title(self, title: str, expected_match: bool) -> None:
        """Helper to wait for the first card's title to match or differ from a target string."""

        def _predicate(_: object) -> bool:
            try:
                cards = self._get_visible_carousel_cards()
                if not cards:
                    return False
                title_el = cards[0].root.find_element(*NewsCardComponent.TITLE)
                card_title = title_el.text.strip()
                return bool((card_title == title) is expected_match)
            except Exception:
                return False

        self.wait.until(_predicate)

    def wait_until_first_card_title_changes(self, initial_title: str) -> None:
        """Wait until the first active card's title is different from the given title."""
        with allure.step("Wait for carousel cards to slide to next"):
            self._wait_for_first_card_title(initial_title, expected_match=False)

    def wait_until_first_card_title_equals(self, expected_title: str) -> None:
        """Wait until the first active card's title matches the given title."""
        with allure.step("Wait for carousel cards to slide to previous"):
            self._wait_for_first_card_title(expected_title, expected_match=True)

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

    @allure.step("Get main news image URL")
    def get_banner_image_url(self) -> str:
        """Return the URL of the banner image extracted from its CSS background-image."""
        image = self._wait_visible(self.NEWS_BANNER_IMAGE)
        style = image.value_of_css_property("background-image")

        match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
        return match.group(1) if match else ""

    @allure.step("Check if the main news image is displayed correctly")
    def is_banner_image_available(self) -> bool:
        """Verify the main banner image is visible and its background URL loads successfully."""
        image_url = self.get_banner_image_url()
        if not image_url:
            return False

        try:
            with urlopen(image_url, timeout=10) as response:
                return response.status == 200 and len(response.read()) > 0
        except (URLError, HTTPError):
            return False

    @allure.step("Get main news image container dimensions")
    def get_banner_image_size(self) -> tuple[int, int]:
        """Return the rendered (width, height) of the image container in pixels."""
        image = self._wait_visible(self.NEWS_BANNER_IMAGE)
        size = image.size
        return size["width"], size["height"]
