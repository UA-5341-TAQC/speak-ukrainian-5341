"""Main Page Object for WayForPay payment gateway page."""

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.components.amount_section_component import AmountSectionComponent
from pages.components.way_for_pay_header_component import WayForPayHeaderComponent
from pages.types import Locator
from pages.wayforpay.card_tab import CardTab
from pages.wayforpay.master_pass_tab import MasterPassTab
from pages.wayforpay.visa_checkout_tab import VisaCheckoutTab


class WayForPayPage(BasePage):
    """Main page object representing the WayForPay payment gateway page."""

    PAYMENT_METHOD_DROPDOWN: Locator = (By.CSS_SELECTOR, "#paymenu-selector")
    CARD_TAB_BUTTON: Locator = (By.CSS_SELECTOR, "#paymenu-dropdown-card-button")
    MASTER_PASS_TAB_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#paymenu-dropdown-master-button",
    )
    VISA_CHECKOUT_TAB_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#paymenu-dropdown-visa-button",
    )

    APPLE_PAY_BUTTON: Locator = (By.CSS_SELECTOR, "#apple-pay")
    GPAY_BUTTON: Locator = (By.CSS_SELECTOR, "#gpay-button-online-api-id")
    HEADER_ROOT: Locator = (By.CSS_SELECTOR, ".block-info")
    AMOUNT_ROOT: Locator = (By.CSS_SELECTOR, "div.price.form-group.validation-wrapper")

    @property
    def header(self) -> WayForPayHeaderComponent:
        """Get WayForPayHeaderComponent instance."""
        root = self._find_element(self.HEADER_ROOT)
        return WayForPayHeaderComponent(root)

    @property
    def amount_section(self) -> AmountSectionComponent:
        """Get AmountSectionComponent instance."""
        root = self._find_element(self.AMOUNT_ROOT)
        return AmountSectionComponent(root)

    @property
    def card_tab(self) -> CardTab:
        """Get CardTab instance (#card)."""
        return CardTab(self.driver)

    @property
    def masterpass_tab(self) -> MasterPassTab:
        """Get MasterPassTab instance (#master)."""
        return MasterPassTab(self.driver)

    @property
    def visa_checkout_tab(self) -> VisaCheckoutTab:
        """Get VisaCheckoutTab instance (#visa)."""
        return VisaCheckoutTab(self.driver)

    @allure.step("Click Apple Pay button on WayForPay")
    def click_apple_pay(self) -> None:
        """Click Apple Pay express payment button."""
        self._find_element(self.APPLE_PAY_BUTTON).click()

    @allure.step("Click Google Pay button on WayForPay")
    def click_google_pay(self) -> None:
        """Click Google Pay express payment button."""
        self._find_element(self.GPAY_BUTTON).click()

    @allure.step("Open payment method selection dropdown")
    def open_payment_methods_dropdown(self) -> "WayForPayPage":
        """Open dropdown to switch payment methods."""
        self._find_element(self.PAYMENT_METHOD_DROPDOWN).click()
        return self

    @allure.step("Switch to Credit Card payment tab")
    def select_card_tab(self) -> CardTab:
        """Switch active tab to Credit Card payment form and return tab instance."""
        self.open_payment_methods_dropdown()
        self._find_element(self.CARD_TAB_BUTTON).click()
        return self.card_tab

    @allure.step("Switch to MasterPass payment tab")
    def select_masterpass_tab(self) -> MasterPassTab:
        """Switch active tab to MasterPass payment form and return tab instance."""
        self.open_payment_methods_dropdown()
        self._find_element(self.MASTER_PASS_TAB_BUTTON).click()
        return self.masterpass_tab

    @allure.step("Switch to Visa Checkout payment tab")
    def select_visa_checkout_tab(self) -> VisaCheckoutTab:
        """Switch active tab to Visa Checkout payment form and return tab instance."""
        self.open_payment_methods_dropdown()
        self._find_element(self.VISA_CHECKOUT_TAB_BUTTON).click()
        return self.visa_checkout_tab

    @allure.step("Check if Apple Pay button is displayed")
    def is_apple_pay_displayed(self) -> bool:
        """Check if Apple Pay button is displayed."""
        return self._find_element(self.APPLE_PAY_BUTTON).is_displayed()

    @allure.step("Check if Google Pay button is displayed")
    def is_google_pay_displayed(self) -> bool:
        """Check if Google Pay button is displayed."""
        return self._find_element(self.GPAY_BUTTON).is_displayed()

    @allure.step("Check if payment methods dropdown is displayed")
    def is_payment_methods_dropdown_displayed(self) -> bool:
        """Check if payment methods dropdown is displayed."""
        return self._find_element(self.PAYMENT_METHOD_DROPDOWN).is_displayed()
