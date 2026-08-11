import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class ChallengeRegistrationPage(BasePage):
    """Page object representing the 'Challenge UA' registration page."""

    BACK_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button.details-back")

    GOOGLE_FORM_CONTAINER: Locator = (
        By.CSS_SELECTOR,
        "div.google-form"
    )
    GOOGLE_FORM_IFRAME: Locator = (
        By.CSS_SELECTOR,
        "div.google-form iframe"
    )

    @allure.step("Check if Registration Challenge page is opened")
    def is_opened(self) -> bool:
        """Check whether the Registration Challenge page is opened."""
        return "/registration" in self.driver.current_url

    @allure.step("Check if Back button is displayed")
    def is_back_button_displayed(self) -> bool:
        """Check whether the Back button is visible."""
        return self._find_element(self.BACK_BUTTON).is_displayed()

    @allure.step("Check if Google Form container is displayed")
    def is_google_form_container_displayed(self) -> bool:
        """Check whether the Google Form container is visible."""
        return self._find_element(self.GOOGLE_FORM_CONTAINER).is_displayed()

    @allure.step("Check if Google Form iframe is displayed")
    def is_google_form_iframe_displayed(self) -> bool:
        """Check whether the Google Form iframe is visible."""
        return self._find_element(self.GOOGLE_FORM_IFRAME).is_displayed()

    @allure.step("Get Google Form iframe source URL")
    def get_google_form_src(self) -> str | None:
        """Return the Google Form iframe source URL."""
        return self._find_element(
            self.GOOGLE_FORM_IFRAME
        ).get_attribute("src")

    @allure.step("Check if Google Form iframe source URL is valid")
    def has_valid_google_form_src(self) -> bool:
        """Check whether the iframe contains a valid Google Forms URL."""
        src = self.get_google_form_src()

        return (
            src is not None
            and "docs.google.com/forms" in src
        )

    @allure.step("Click Back button")
    def click_back_button(self) -> None:
        """Click the Back button."""
        self._wait_clickable(self.BACK_BUTTON).click()
