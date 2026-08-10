"""TC-48: Verify payment page UI elements are displayed correctly."""

import allure
from selenium import webdriver

from pages.wayforpay.way_for_pay_page import WayForPayPage

PAYMENT_PAGE_URL = "https://secure.wayforpay.com/payment/s0f2891d77061"
EXPECTED_TITLE = 'Ініціатива "Навчай українською"'


@allure.epic("WayForPay")
@allure.feature("Payment page")
class TestPaymentPageUI:
    """TC-48: verify all mandatory payment page UI elements are displayed."""

    def setup_method(self) -> None:
        """Open the browser and navigate to the payment page before each test."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(PAYMENT_PAGE_URL)
        self.page = WayForPayPage(self.driver)
        self.card_tab = self.page.card_tab

    def teardown_method(self) -> None:
        """Close the browser after each test."""
        self.driver.quit()

    @allure.title("TC-48: Verify payment page UI elements are displayed correctly")
    def test_payment_page_ui_elements_displayed(self) -> None:
        """Verify title, amount, currency, express pay buttons, card form fields and submit button."""

        with allure.step("Verify title"):
            assert self.page.header.is_title_displayed()
            assert self.page.header.get_title_text() == EXPECTED_TITLE

        with allure.step("Verify amount input field"):
            assert self.page.amount_section.is_amount_field_displayed()

        with allure.step("Verify currency selector default"):
            assert self.page.amount_section.get_selected_currency() == "UAH"

        with allure.step("Verify Apple Pay button"):
            assert self.page.is_apple_pay_displayed()

        with allure.step("Verify Google Pay button"):
            assert self.page.is_google_pay_displayed()

        #"Інший спосіб оплати" dropdown
        with allure.step("Verify payment methods dropdown"):
            assert self.page.is_payment_methods_dropdown_displayed()

        with allure.step("Verify card number field"):
            assert self.card_tab.is_card_number_displayed()

        with allure.step("Verify expiration date field"):
            assert self.card_tab.is_validity_displayed()

        with allure.step("Verify CVV field"):
            assert self.card_tab.is_cvv_displayed()

        with allure.step("Verify cardholder name field"):
            assert self.card_tab.is_cardholder_displayed()

        with allure.step("Verify phone field"):
            assert self.card_tab.is_phone_displayed()

        with allure.step("Verify email field"):
            assert self.card_tab.is_email_displayed()

        with allure.step('Verify "Оплатити" button is visible and enabled after filling required data'):
            self.card_tab.fill_complete_form(
                number="4242424242424242",
                validity="12/30",
                cvv="123",
                holder="TEST TEST",
                phone="380501234567",
                email="test@example.com",
            )
            assert self.card_tab.is_submit_button_enabled()