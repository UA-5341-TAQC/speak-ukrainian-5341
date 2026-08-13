"""Component representing social media buttons and donation elements."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class SocialButtons(BaseComponent):
    """Encapsulates social media buttons and donation block component."""

    SOCIAL_SECTION_TITLE: Locator = (
        By.CSS_SELECTOR,
        ".social-media .text",
    )
    FACEBOOK_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".social-media a[href*='facebook.com']",
    )
    YOUTUBE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".social-media a[href*='youtube.com']",
    )
    INSTAGRAM_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".social-media a[href*='instagram.com']",
    )
    MAIL_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".social-media a[href^='mailto:']",
    )
    DONATE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        ".help-button .donate-button",
    )

    @allure.step("Get social media section title text")
    def get_social_section_title_text(self) -> str:
        """Get the title text of the social section."""
        return self._find_element(
            self.SOCIAL_SECTION_TITLE
        ).text

    @allure.step("Get Facebook link URL")
    def get_facebook_url(self) -> str:
        """Get the URL from the Facebook button."""
        return (
            self._find_element(self.FACEBOOK_BUTTON)
            .get_attribute("href")
            or ""
        )

    @allure.step("Click Facebook button")
    def click_facebook_button(self) -> None:
        """Click the Facebook social button."""
        self._find_element(self.FACEBOOK_BUTTON).click()

    @allure.step("Get YouTube link URL")
    def get_youtube_url(self) -> str:
        """Get the URL from the YouTube button."""
        return (
            self._find_element(self.YOUTUBE_BUTTON)
            .get_attribute("href")
            or ""
        )

    @allure.step("Click YouTube button")
    def click_youtube_button(self) -> None:
        """Click the YouTube social button."""
        self._find_element(self.YOUTUBE_BUTTON).click()

    @allure.step("Get Instagram link URL")
    def get_instagram_url(self) -> str:
        """Get the URL from the Instagram button."""
        return (
            self._find_element(self.INSTAGRAM_BUTTON)
            .get_attribute("href")
            or ""
        )

    @allure.step("Click Instagram button")
    def click_instagram_button(self) -> None:
        """Click the Instagram social button."""
        self._find_element(self.INSTAGRAM_BUTTON).click()

    @allure.step("Get email address from mailto link")
    def get_email_address(self) -> str:
        """Get the raw email address extracted from mailto link."""
        href = (
            self._find_element(self.MAIL_BUTTON)
            .get_attribute("href")
            or ""
        )
        return href.replace("mailto:", "")

    @allure.step("Get Donate button text")
    def get_donate_button_text(self) -> str:
        """Get text from the Donate button."""
        return self._find_element(self.DONATE_BUTTON).text

    @allure.step("Get Donate payment link URL")
    def get_donate_url(self) -> str:
        """Get payment URL from the Donate button."""
        return (
            self._find_element(self.DONATE_BUTTON)
            .find_element(By.XPATH, "..")
            .get_attribute("href")
            or ""
        )

    @allure.step("Click 'Donate' button")
    def click_donate_button(self) -> None:
        """Click the Donate button."""
        self._find_element(self.DONATE_BUTTON).click()

    @allure.step("Check if Donate button is displayed")
    def is_donate_button_displayed(self) -> bool:
        """Return whether the donate button is visible."""
        return self._find_element(
            self.DONATE_BUTTON
        ).is_displayed()

    @allure.step("Get Donate button cursor CSS value")
    def get_donate_button_cursor(self) -> str:
        """Return the donate button cursor CSS value."""
        return self._find_element(
            self.DONATE_BUTTON
        ).value_of_css_property("cursor")
