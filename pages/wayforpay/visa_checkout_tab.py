"""Visa Checkout payment tab component for WayForPay page."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class VisaCheckoutTab(BasePage):
    """Component for WayForPay Visa Checkout payment tab (#visa)."""

    CONTINUE_BUTTON: Locator = (By.CSS_SELECTOR, "#tab-visa button[type='submit']")

    @allure.step("Click 'Далі' button on WayForPay Visa Checkout tab")
    def click_next(self) -> None:
        """Click continue button to proceed with Visa Checkout."""
        self._find_element(self.CONTINUE_BUTTON).click()
