"""Page object for the home page of the Speak Ukrainian website."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

DEFAULT_TIMEOUT: int = 10


class HomePage(BasePage):
    """Page object representing the Speak Ukrainian home page."""

    ALL_CLUBS_BUTTON: tuple[str, str] = (
    By.CSS_SELECTOR,
    "a[href='/clubs'] button",
    )
    CATEGORIES_PREV_ARROW: tuple[str, str] = (By.CSS_SELECTOR, ".arrows-prev")
    CATEGORIES_NEXT_ARROW: tuple[str, str] = (By.CSS_SELECTOR, ".arrows-next")
    CHALLENGE_LEARN_MORE_BUTTON: tuple[str, str] = (
        By.CSS_SELECTOR,
        "button.flooded-button.materials-button",
    )
    SPEAKING_CLUB_LINK: tuple[str, str] = (
        By.CSS_SELECTOR,
        "a[href='/speakingclub']",
    )
    BANNER_IMAGE: tuple[str, str] = (
        By.CSS_SELECTOR,
        'a[href="https://www.facebook.com/events/2754499954695563"] img.banner-image',
    )

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize the home page.

        Args:
            driver: Selenium WebDriver instance.
            timeout: Maximum time in seconds to wait for elements.
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Switch club categories to previous")
    def click_categories_prev_arrow(self) -> None:
        """Click the previous arrow of the categories carousel."""
        self._click_clickable(self.CATEGORIES_PREV_ARROW)

    @allure.step("Switch club categories to next")
    def click_categories_next_arrow(self) -> None:
        """Click the next arrow of the categories carousel."""
        self._click_clickable(self.CATEGORIES_NEXT_ARROW)

    @allure.step("Перемкнути напрями гуртків на попередні")
    def click_categories_prev_arrow(self) -> None:
        """Click the previous arrow of the categories carousel."""
        self._click_clickable(self.CATEGORIES_PREV_ARROW)

    @allure.step("Click 'Дізнатись більше' button in the challenge block")
    def click_challenge_learn_more_button(self) -> None:
        """Click the 'Learn more' button of the challenge block."""
        self._click_clickable(self.CHALLENGE_LEARN_MORE_BUTTON)

    @allure.step("Click 'Розмовляй' speaking club link")
    def click_speaking_club_link(self) -> None:
        """Click the speaking club 'Розмовляй' link."""
        self._click_clickable(self.SPEAKING_CLUB_LINK)

    @allure.step("Click initiative banner image")
    def click_banner_image(self) -> None:
        """Click the initiative banner image."""
        self._click_clickable(self.BANNER_IMAGE)

    @allure.step("Click 'Всі гуртки' button")
    def click_all_clubs_button(self) -> None:
        """Click the 'Всі гуртки' button."""
        self._click_clickable(self.ALL_CLUBS_BUTTON)    

    def _wait_clickable(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element matching the locator is clickable.

        Args:
            locator: Selenium locator of the element.

        Returns:
            The clickable WebElement.
        """
        return self.wait.until(ec.element_to_be_clickable(locator))

    def _click_clickable(self, locator: tuple[str, str]) -> None:
        """Wait for an element to become clickable and click it.

        Args:
            locator: Selenium locator of the element.
        """
        element = self._wait_clickable(locator)
        element.click()
