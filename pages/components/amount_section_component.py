"""Amount and currency section component for WayForPay page."""

import allure
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent
from pages.types import Locator


class AmountSectionComponent(BaseComponent):
    """Component for WayForPay payment amount input and currency selection."""

    AMOUNT_INPUT: Locator = (By.CSS_SELECTOR, "#freepay-amount")
    CURRENCY_BUTTON: Locator = (By.CSS_SELECTOR, "#freepay-currency")
    CURRENCY_OPTIONS: Locator = (By.CSS_SELECTOR, "#freepay-currencies li a")

    @allure.step("Enter payment amount in WayForPay: {amount}")
    def enter_amount(self, amount: str) -> "AmountSectionComponent":
        """Enter payment amount using React-friendly clear helper."""
        amount_field = self._find_element(self.AMOUNT_INPUT)
        self.clear(amount_field)
        amount_field.send_keys(amount)
        return self

    @allure.step("Select payment currency in WayForPay: {currency_code}")
    def select_currency(self, currency_code: str) -> None:
        """Select currency from dropdown (e.g., UAH, USD, EUR)."""
        self._find_element(self.CURRENCY_BUTTON).click()
        for option in self._find_elements(self.CURRENCY_OPTIONS):
            if option.text.strip() == currency_code:
                option.click()
                break

    # Перевірки для TC-48, кроки 2-3
    @allure.step("Check if amount field is displayed")
    def is_amount_field_displayed(self) -> bool:
        """Check if amount field is displayed."""
        return self._find_element(self.AMOUNT_INPUT).is_displayed()

    @allure.step("Get currently selected currency in WayForPay")
    def get_selected_currency(self) -> str:
        """Get the currency currently shown (e.g. UAH)."""
        return self._find_element(self.CURRENCY_BUTTON).text.strip()
