"""TC-48: Verify payment page UI elements are displayed correctly."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.wayforpay.way_for_pay_page import WayForPayPage

PAYMENT_PAGE_URL = "https://secure.wayforpay.com/payment/s0f2891d77061"
EXPECTED_TITLE = 'Ініціатива "Навчай українською"'

@allure.feature("Payment page")
@allure.title("TC-48: Verify payment page UI elements are displayed correctly")
def test_payment_page_ui_elements_displayed(driver: WebDriver) -> None:
    """Verify title, amount, currency, express pay buttons, card form fields and submit button."""
    driver.get(PAYMENT_PAGE_URL)
    page = WayForPayPage(driver)
    header = page.wayforpay_header
    amount_section = page.amount_section
    card_tab = page.card_tab

    with allure.step("Verify title"):
        assert header.is_title_displayed()
        assert header.get_title_text() == EXPECTED_TITLE

    assert amount_section.is_amount_field_displayed()
    assert amount_section.get_selected_currency() == "UAH"

    assert page.is_apple_pay_displayed()
    assert page.is_google_pay_displayed()
    assert page.is_payment_methods_dropdown_displayed()

    assert card_tab.is_card_number_displayed()
    assert card_tab.is_validity_displayed()
    assert card_tab.is_cvv_displayed()
    assert card_tab.is_cardholder_displayed()
    assert card_tab.is_phone_displayed()
    assert card_tab.is_email_displayed()

    with allure.step('Verify "Оплатити" button is visible and enabled after filling required data'):
        card_tab.fill_complete_form(
            number="4242424242424242",
            validity="12/30",
            cvv="123",
            holder="TEST TEST",
            phone="380501234567",
            email="test@example.com",
        )
        assert card_tab.is_submit_button_displayed()
        assert card_tab.is_submit_button_enabled()