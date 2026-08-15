"""Page object for the second Speak Ukrainian challenge."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.challenge_cta_button import ChallengeCtaButton
from pages.components.challenge_video_card import ChallengeVideoCard
from pages.types import Locator


class ChallengePage(BasePage):
    """Represent a Speak Ukrainian challenge page."""

    TITLE: Locator = (
        By.CSS_SELECTOR,
        ".banner .title",
    )

    CTA_BUTTON: Locator = (
        By.XPATH,
        "//button[normalize-space()='Записатись на челендж']",
    )

    VIDEO_CARDS: Locator = (
        By.CSS_SELECTOR,
        "div.challenge-description iframe.ql-video",
    )

    @allure.step("Scroll challenge registration button into view")
    def scroll_cta_button_into_view(self) -> None:
        """Scroll the registration button into the viewport."""
        self._scroll_into_view(self.CTA_BUTTON)

    @allure.step("Get challenge registration button bounding rect")
    def get_cta_button_rect(self) -> dict[str, float]:
        """Return the bounding rectangle of the registration button."""
        rect = self._wait_present(self.CTA_BUTTON).rect

        return {
            "top": float(rect["y"]),
            "bottom": float(rect["y"] + rect["height"]),
            "left": float(rect["x"]),
            "right": float(rect["x"] + rect["width"]),
        }

    @allure.step("Open challenge page")
    def open(self, challenge_id: int) -> None:
        """Navigate the browser to a challenge page.

        Args:
            challenge_id: Identifier of the challenge to open.
        """
        self.driver.get(f"{self.get_base_url()}/challenges/{challenge_id}")

    @allure.step("Get challenge page title")
    def get_title_text(self) -> str:
        """Return the title shown in the challenge banner."""
        return self._wait_visible(self.TITLE).text.strip()

    @allure.step("Get challenge registration button component")
    def get_cta_button(self) -> ChallengeCtaButton:
        """Return the challenge registration button component."""
        return ChallengeCtaButton(
            self._wait_clickable(self.CTA_BUTTON)
        )

    @allure.step("Click challenge registration button")
    def click_cta_button(self) -> None:
        """Click the challenge registration button."""
        self.get_cta_button().click()

    @allure.step("Wait for challenge webinar video cards")
    def wait_for_video_cards(self) -> list[ChallengeVideoCard]:
        """Wait until all video iframes are rendered."""
        self._wait_present(self.VIDEO_CARDS)

        return [
            ChallengeVideoCard(card)
            for card in self._find_elements(self.VIDEO_CARDS)
        ]

    @allure.step("Get challenge webinar video cards")
    def get_video_cards(self) -> list[ChallengeVideoCard]:
        """Return all currently displayed webinar video cards."""
        return [
            ChallengeVideoCard(card)
            for card in self._find_elements(self.VIDEO_CARDS)
        ]
