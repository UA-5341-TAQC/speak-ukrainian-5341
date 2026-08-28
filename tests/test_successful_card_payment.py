"""TC-41: Verify successful card payment form filling with valid input data."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.wayforpay.way_for_pay_page import WayForPayPage

PAYMENT_PAGE_URL = "https://secure.wayforpay.com/payment/s0f2891d77061"

AMOUNT = "100"
CURRENCY = "UAH"
CARD_NUMBER = "5555555555554444"
VALIDITY = "12 / 28"
CVV = "123"
CARDHOLDER = "Svitlana Kovalova"
PHONE = "+380971234567"
EMAIL = "user@example.com"


@allure.feature("Successful Payment")
@allure.title("TC-41: Verify successful card payment form filling with valid input data")
def test_successful_card_payment_form_filling(driver: WebDriver) -> None:
    """Verify that all card payment fields accept and correctly display valid data."""
    driver.get(PAYMENT_PAGE_URL)
    page = WayForPayPage(driver)
    card_tab = page.card_tab

    with allure.step("Enter a valid amount into the amount field"):
        page.amount_section.enter_amount(AMOUNT)
        assert page.amount_section.get_amount_value() == AMOUNT

    with allure.step("Choose currency from the dropdown"):
        page.amount_section.select_currency(CURRENCY)
        assert page.amount_section.get_selected_currency() == CURRENCY

    with allure.step("Fill in card and payer details"):
        card_tab.fill_complete_form(
            number=CARD_NUMBER,
            validity=VALIDITY,
            cvv=CVV,
            holder=CARDHOLDER,
            phone=PHONE,
            email=EMAIL,
        )

    with allure.step("Verify card number is formatted with spaces"):
        assert card_tab.get_card_number_value() == "5555 5555 5555 4444"

    with allure.step("Verify expiry date is accepted in MM/YY format"):
        assert card_tab.get_validity_value() == VALIDITY

    with allure.step("Verify cardholder name is accepted correctly"):
        assert card_tab.get_cardholder_value() == CARDHOLDER

    with allure.step("Verify phone number is fully entered"):
        assert card_tab.get_phone_value() == PHONE

    with allure.step("Verify email address is accepted in correct format"):
        assert card_tab.get_email_value() == EMAIL

    with allure.step("Verify the state of the 'Оплатити' submit button after all fields are filled"):
        assert card_tab.is_submit_button_displayed()
        assert card_tab.is_submit_button_enabled()

    with allure.step("Verify amount and currency remain correct after filling card details"):
        assert page.amount_section.get_amount_value() == AMOUNT
        assert page.amount_section.get_selected_currency() == CURRENCY