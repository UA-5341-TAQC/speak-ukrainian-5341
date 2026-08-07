"""Component object for a challenge webinar video card."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class ChallengeVideoCard(BaseComponent):
    """Represent one webinar video card on a challenge page."""

    TITLE: Locator = (By.XPATH, ".//*[self::h2 or self::h3 or self::h4][1]")
    THUMBNAIL: Locator = (By.CSS_SELECTOR, "img")
    PLAY_BUTTON: Locator = (
        By.XPATH,
        ".//*[self::button or @role='button'][contains(@class, 'play') or .//*[name()='svg']]",
    )
    YOUTUBE_LINK: Locator = (By.XPATH, ".//a[normalize-space()='Дивитися на YouTube']")

    @allure.step("Get webinar video title")
    def get_title_text(self) -> str:
        """Return the webinar title."""
        return self._find_element(self.TITLE).text

    @allure.step("Click webinar play button")
    def click_play_button(self) -> None:
        """Start the webinar video."""
        self._find_element(self.PLAY_BUTTON).click()

    @allure.step("Open webinar on YouTube")
    def click_youtube_link(self) -> None:
        """Open the webinar on YouTube."""
        self._find_element(self.YOUTUBE_LINK).click()

    @allure.step("Check whether webinar thumbnail is loaded")
    def is_thumbnail_loaded(self) -> bool:
        """Return whether the video thumbnail is visible and has loaded pixels."""
        thumbnail = self._find_element(self.THUMBNAIL)
        natural_width = thumbnail.get_property("naturalWidth")
        return thumbnail.is_displayed() and isinstance(natural_width, int) and natural_width > 0
