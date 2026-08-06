"""Page object for the home page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.carousel import Carousel
from pages.components.home_content_card import HomeContentCard
from pages.types import Locator


class HomePage(BasePage):
    """Page object representing the Speak Ukrainian home page."""

    ALL_CLUBS_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".categories-header .more-button",
    )
    CATEGORIES_PREV_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".arrows-prev",
    )
    CATEGORIES_NEXT_ARROW: Locator = (
        By.CSS_SELECTOR,
        ".arrows-next",
    )
    CHALLENGE_LEARN_MORE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.flooded-button.materials-button",
    )
    SPEAKING_CLUB_LINK: Locator = (
        By.CSS_SELECTOR,
        "a[href='/speakingclub']",
    )
    BANNER_IMAGE: Locator = (
        By.CSS_SELECTOR,
        'a[href="https://www.facebook.com/events/2754499954695563"] img.banner-image',
    )

    CAROUSEL: Locator = (
        By.CSS_SELECTOR,
        ".about-carousel-block",
    )

    CONTENT_CARDS: Locator = (
        By.CSS_SELECTOR,
        ".primitive-card",
    )

    @allure.step("Click 'Всі гуртки' button")
    def click_all_clubs_button(self) -> None:
        """Click the 'Всі гуртки' button."""
        self._wait_clickable(self.ALL_CLUBS_BUTTON).click()

    @allure.step("Switch club categories to previous")
    def click_categories_prev_arrow(self) -> None:
        """Click the previous arrow of the categories carousel."""
        self._wait_clickable(self.CATEGORIES_PREV_ARROW).click()

    @allure.step("Switch club categories to next")
    def click_categories_next_arrow(self) -> None:
        """Click the next arrow of the categories carousel."""
        self._wait_clickable(self.CATEGORIES_NEXT_ARROW).click()

    @allure.step("Click 'Дізнатись більше' button in the challenge block")
    def click_challenge_learn_more_button(self) -> None:
        """Click the 'Дізнатись більше' button of the challenge block."""
        self._wait_clickable(self.CHALLENGE_LEARN_MORE_BUTTON).click()

    @allure.step("Click 'Розмовляй' speaking club link")
    def click_speaking_club_link(self) -> None:
        """Click the 'Розмовляй' speaking club link."""
        self._wait_clickable(self.SPEAKING_CLUB_LINK).click()

    @allure.step("Click initiative banner image")
    def click_banner_image(self) -> None:
        """Click the initiative banner image."""
        self._wait_clickable(self.BANNER_IMAGE).click()

    @allure.step("Get carousel")
    def get_carousel(self) -> Carousel:
        """Return the carousel component."""
        return Carousel(self._find_element(self.CAROUSEL))

    @allure.step("Get content cards")
    def get_content_cards(self) -> list[HomeContentCard]:
        """Return all home page content cards."""
        return [
            HomeContentCard(card)
            for card in self.driver.find_elements(*self.CONTENT_CARDS)
        ]
