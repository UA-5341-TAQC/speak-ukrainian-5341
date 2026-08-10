"""Header component for WayForPay payment gateway."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class WayForPayHeaderComponent(BaseComponent):
    """Component for WayForPay portal header and initiative details."""

    #TITLE: Locator = (By.CSS_SELECTOR, ".block-info .title")
    #DESCRIPTION: Locator = (By.CSS_SELECTOR, ".block-info .description")

    # Без префікса .block-info, бо root компонента вже = .block-info
    TITLE: Locator = (By.CSS_SELECTOR, ".title")
    DESCRIPTION: Locator = (By.CSS_SELECTOR, ".description")

    @allure.step("Get merchant title text from WayForPay header")
    def get_title_text(self) -> str:
        """Get initiative or merchant title text."""
        return self._find_element(self.TITLE).text.strip()

    @allure.step("Get initiative description text from WayForPay header")
    def get_description_text(self) -> str:
        """Get initiative description text."""
        return self._find_element(self.DESCRIPTION).text.strip()

    # Перевірка видимості для TC-48, крок 1
    @allure.step("Check if title is displayed on WayForPay header")
    def is_title_displayed(self) -> bool:
        """Check if title is displayed."""
        return self._find_element(self.TITLE).is_displayed()
