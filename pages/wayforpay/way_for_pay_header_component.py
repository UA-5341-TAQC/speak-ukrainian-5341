"""Header component for WayForPay payment gateway."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class WayForPayHeaderComponent(BasePage):
    """Component for WayForPay portal header and initiative details."""

    TITLE: Locator = (By.CSS_SELECTOR, ".block-info .title")
    DESCRIPTION: Locator = (By.CSS_SELECTOR, ".block-info .description")

    @allure.step("Get merchant title text from WayForPay header")
    def get_title_text(self) -> str:
        """Get initiative or merchant title text."""
        return self._find_element(self.TITLE).text.strip()

    @allure.step("Get initiative description text from WayForPay header")
    def get_description_text(self) -> str:
        """Get initiative description text."""
        return self._find_element(self.DESCRIPTION).text.strip()
