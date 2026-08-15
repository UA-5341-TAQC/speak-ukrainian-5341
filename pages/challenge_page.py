"""Page object for the second Speak Ukrainian challenge."""

from urllib.parse import urljoin

import allure
from components.social_buttons import SocialButtons
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.challenge_cta_button import ChallengeCtaButton
from pages.components.challenge_video_card import ChallengeVideoCard
from pages.types import Locator


class ChallengePage(BasePage):
    """Represent a Speak Ukrainian challenge page."""

    TITLE: Locator = (By.CSS_SELECTOR, ".banner .title")
    DESCRIPTION_PARAGRAPHS: Locator = (
        By.XPATH,
        "//div[contains(@class, 'challenge-description')]/p[normalize-space()]",
    )
    CONTENT_TITLE: Locator = (
        By.CSS_SELECTOR,
        ".challenge-description h1",
    )
    CTA_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.apply-button",
    )
    CTA_BUTTON_WRAPPER: Locator = (
        By.CSS_SELECTOR,
        ".full-width.button-box > span",
    )
    CTA_TOOLTIP: Locator = (
        By.CSS_SELECTOR,
        ".ant-tooltip-inner[role='tooltip']",
    )
    VIDEO_CARDS: Locator = (
        By.XPATH,
        "//button[normalize-space()='Записатись на челендж']",
    )
    SOCIAL_BUTTONS: Locator = (
        By.CSS_SELECTOR,
        ".social-info",
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
        return self._find_element(self.TITLE).text

    @allure.step("Get challenge description paragraphs")
    def get_description_paragraphs(self) -> list[str]:
        """Return challenge description paragraphs."""
        return [
            element.text.strip()
            for element in self.driver.find_elements(
                *self.DESCRIPTION_PARAGRAPHS
            )
        ]

    @allure.step("Get challenge content title")
    def get_content_title(self) -> str:
        """Return the main challenge content title."""
        return self._find_element(self.CONTENT_TITLE).text.strip()

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

    @allure.step("Get challenge registration button component (visible)")
    def get_visible_cta_button(self) -> ChallengeCtaButton:
        """Return the challenge registration button component using visibility wait."""
        return ChallengeCtaButton(
            self._wait_visible(self.CTA_BUTTON)
        )

    @allure.step("Get challenge registration button wrapper")
    def get_cta_button_wrapper(self):
        """Return the wrapper of the disabled registration button."""
        return self._wait_visible(self.CTA_BUTTON_WRAPPER)

    @allure.step("Get registration button tooltip text")
    def get_cta_tooltip_text(self) -> str:
        """Return the visible tooltip text for the registration button."""
        return self._wait_visible(self.CTA_TOOLTIP).text.strip()

    @allure.step("Hover over registration button")
    def hover_over_cta_button(self) -> None:
        """Hover over the registration button wrapper to trigger tooltip."""
        wrapper = self._wait_visible(self.CTA_BUTTON_WRAPPER)

        self.driver.execute_script(
            """
            const element = arguments[0];
            const rect = element.getBoundingClientRect();

            ['mouseover', 'mouseenter', 'mousemove'].forEach(eventName => {
                element.dispatchEvent(new MouseEvent(eventName, {
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + rect.width / 2,
                    clientY: rect.top + rect.height / 2
                }));
            });
            """,
            wrapper,
        )

    @allure.step("Get social buttons component")
    def get_social_buttons(self) -> SocialButtons:
        """Return social buttons component."""
        return SocialButtons(
            self._wait_visible(self.SOCIAL_BUTTONS)
        )
