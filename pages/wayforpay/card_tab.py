"""Credit card payment tab component for WayForPay page."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.types import Locator


class CardTab(BasePage):
    """Component for WayForPay credit card payment form (#card)."""

    CARD_NUMBER_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-cardnumber")
    VALIDITY_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-validity")
    CVV_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-cardsecure")
    CARDHOLDER_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-cardholder")
    PHONE_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-clientphone")
    EMAIL_INPUT: Locator = (By.CSS_SELECTOR, "#cardpay-clientemail")
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "#cardpay-submit")

    @allure.step("Fill complete payment form in WayForPay")
    def fill_complete_form(
        self, number: str, validity: str, cvv: str, holder: str, phone: str, email: str
    ) -> "CardTab":
        """Fill all card and payer contact details in the form."""
        fields = [
            (self.CARD_NUMBER_INPUT, number),
            (self.VALIDITY_INPUT, validity),
            (self.CVV_INPUT, cvv),
            (self.CARDHOLDER_INPUT, holder),
            (self.PHONE_INPUT, phone),
            (self.EMAIL_INPUT, email),
        ]
        for locator, value in fields:
            el = self._find_element(locator)
            self.clear(el)
            el.send_keys(value)

        return self

    @allure.step("Click 'Pay' button on WayForPay card form")
    def click_pay(self) -> None:
        """Submit payment form."""
        self._find_element(self.SUBMIT_BUTTON).click()

    @allure.step("Get entered card number value")
    def get_card_number_value(self) -> str:
        """Get value from card number input field."""
        return self._find_element(self.CARD_NUMBER_INPUT).get_attribute("value") or ""

    @allure.step("Get entered validity date value")
    def get_validity_value(self) -> str:
        """Get value from validity date input field."""
        return self._find_element(self.VALIDITY_INPUT).get_attribute("value") or ""

    @allure.step("Get entered CVV value")
    def get_cvv_value(self) -> str:
        """Get value from CVV input field."""
        return self._find_element(self.CVV_INPUT).get_attribute("value") or ""

    @allure.step("Get entered cardholder name value")
    def get_cardholder_value(self) -> str:
        """Get value from cardholder input field."""
        return self._find_element(self.CARDHOLDER_INPUT).get_attribute("value") or ""

    @allure.step("Get entered phone number value")
    def get_phone_value(self) -> str:
        """Get value from phone input field."""
        return self._find_element(self.PHONE_INPUT).get_attribute("value") or ""

    @allure.step("Get entered email value")
    def get_email_value(self) -> str:
        """Get value from email input field."""
        return self._find_element(self.EMAIL_INPUT).get_attribute("value") or ""

    @allure.step("Check if submit button is enabled")
    def is_submit_button_enabled(self) -> bool:
        """Check whether 'Pay' button is clickable/enabled."""
        return self._find_element(self.SUBMIT_BUTTON).is_enabled()

    @allure.step("Check if card payment form is displayed")
    def is_form_displayed(self) -> bool:
        """Verify that card payment tab content is visible."""
        return self._find_element(self.CARD_NUMBER_INPUT).is_displayed()

    #Перевірки видимості для TC-48, кроки 7-12
    @allure.step("Check if card number field is displayed")
    def is_card_number_displayed(self) -> bool:
        """Check if card number field is displayed."""
        return self._find_element(self.CARD_NUMBER_INPUT).is_displayed()

    @allure.step("Check if validity date field is displayed")
    def is_validity_displayed(self) -> bool:
        """Check if validity date field is displayed."""
        return self._find_element(self.VALIDITY_INPUT).is_displayed()

    @allure.step("Check if CVV field is displayed")
    def is_cvv_displayed(self) -> bool:
        """Check if CVV field is displayed."""
        return self._find_element(self.CVV_INPUT).is_displayed()

    @allure.step("Check if cardholder name field is displayed")
    def is_cardholder_displayed(self) -> bool:
        """Check if cardholder name field is displayed."""
        return self._find_element(self.CARDHOLDER_INPUT).is_displayed()

    @allure.step("Check if phone field is displayed")
    def is_phone_displayed(self) -> bool:
        """Check if phone field is displayed."""
        return self._find_element(self.PHONE_INPUT).is_displayed()

    @allure.step("Check if email field is displayed")
    def is_email_displayed(self) -> bool:
        """Check if email field is displayed."""
        return self._find_element(self.EMAIL_INPUT).is_displayed()

    @allure.step("Check if submit button is displayed")
    def is_submit_button_displayed(self) -> bool:
        """Check if submit button is displayed."""
        return self._find_element(self.SUBMIT_BUTTON).is_displayed()
