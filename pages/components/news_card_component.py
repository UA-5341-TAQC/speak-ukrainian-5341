"""Component Object for one news card."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.components.base_component import BaseComponent
from pages.types import Locator


class NewsCardComponent(BaseComponent):
    """Represents one news item on the News list page."""

    IMAGE: Locator = (By.CSS_SELECTOR, "#newsImage")
    DATE: Locator = (By.CSS_SELECTOR, "#newsDate")
    TITLE: Locator = (By.CSS_SELECTOR, "#newsTitle")
    DETAILS_LINK: Locator = (By.CSS_SELECTOR, "#detailButton a")

    def __init__(self, root: WebElement):
        """Initialize the news card component with a WebElement root."""
        super().__init__(root)

    def get_title(self) -> str:
        """Return the news title."""
        return self._wait_visible(self.TITLE).text.strip()

    def get_date(self) -> str:
        """Return the publication date."""
        return self._wait_visible(self.DATE).text.strip()

    def get_details_text(self) -> str:
        """Return the text of the details link."""
        return self._wait_visible(self.DETAILS_LINK).text.strip()

    @allure.step("Check whether news image is displayed.")
    def is_image_displayed(self) -> bool:
        """Return True when the news image is visible."""
        return self._wait_visible(self.IMAGE).is_displayed()

    def get_image_background(self) -> str:
        """Return the CSS background-image value of the news image block."""
        return self._wait_visible(self.IMAGE).value_of_css_property("background-image")

    @allure.step("Open news card")
    def open(self) -> None:
        """Open this news item by clicking the card."""
        self.root.click()

    @allure.step("Get the details link URL")
    def get_details_href(self) -> str:
        """Return the absolute URL of the details link, normalized without a trailing slash."""
        href = self._wait_visible(self.DETAILS_LINK).get_attribute("href") or ""
        if href.startswith("/"):
            return f"{self.get_base_url()}{href}".rstrip("/")
        return href.rstrip("/")

    @allure.step("Open news details")
    def click_details(self) -> None:
        """Open this news item using the details link."""
        self._wait_clickable(self.DETAILS_LINK).click()

    @allure.step("Check if news card is visible")
    def is_visible(self) -> bool:
        """Check whether news card is displayed."""
        return self.root.is_displayed()

    @allure.step("Check whether title is displayed.")
    def is_title_visible(self)->bool:
        """Check whether title is displayed."""
        return self._wait_visible(self.TITLE).is_displayed()

    @allure.step("Check whether publication date is displayed")
    def is_date_visible(self) -> bool:
        """Check whether publication date is displayed."""
        return self._wait_visible(self.DATE).is_displayed()

