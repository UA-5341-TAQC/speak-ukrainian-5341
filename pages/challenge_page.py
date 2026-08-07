"""Page object for the second Speak Ukrainian challenge."""

from urllib.parse import urljoin

import allure
from selenium.webdriver.common.by import By

from data.config import Config
from pages.base_page import BasePage
from pages.components.challenge_cta_button import ChallengeCtaButton
from pages.components.challenge_video_card import ChallengeVideoCard
from pages.types import Locator


class ChallengePage(BasePage):
    """Represent a Speak Ukrainian challenge page."""

    TITLE: Locator = (By.CSS_SELECTOR, ".banner .title")
    CTA_BUTTON: Locator = (By.XPATH, "//button[normalize-space()='Записатись на челендж']")
    VIDEO_CARDS: Locator = (
        By.XPATH,
        "//*[self::article or self::div][.//a[normalize-space()='Дивитися на YouTube']]",
    )

    @allure.step("Open challenge page")
    def open(self, challenge_id: int) -> None:
        """Navigate the browser to a challenge page.

        Args:
            challenge_id: Identifier of the challenge to open.
        """
        self.driver.get(urljoin(Config.BASE_UI_URL, f"challenges/{challenge_id}"))

    @allure.step("Get challenge page title")
    def get_title_text(self) -> str:
        """Return the title shown in the challenge banner."""
        return self._find_element(self.TITLE).text

    @allure.step("Get challenge registration button component")
    def get_cta_button(self) -> ChallengeCtaButton:
        """Return the challenge registration button component."""
        return ChallengeCtaButton(self._wait_clickable(self.CTA_BUTTON))

    @allure.step("Click challenge registration button")
    def click_cta_button(self) -> None:
        """Click the challenge registration call-to-action button."""
        self.get_cta_button().click()

    @allure.step("Get challenge webinar video cards")
    def get_video_cards(self) -> list[ChallengeVideoCard]:
        """Return all webinar video cards currently displayed on the page."""
        return [ChallengeVideoCard(card) for card in self.driver.find_elements(*self.VIDEO_CARDS)]
