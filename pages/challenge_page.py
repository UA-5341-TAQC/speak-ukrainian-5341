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
