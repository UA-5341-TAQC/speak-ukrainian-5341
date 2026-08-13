"""Test suite for verifying email format validation in the Registration modal (TC-54)."""

from __future__ import annotations

import allure
import pytest

from data.config import Config
from pages.home_page import HomePage
from pages.modals.sign_up_modal import SignUpModal


@allure.feature("Registration Modal Validation")
class TestSignUpEmailValidation:
    """Test suite for verifying email format validation (TC-54)."""

    @pytest.fixture(autouse=True)
    def setup(self, driver) -> None:
        """Open home page before each test."""
        driver.get(Config.BASE_UI_URL)

    @allure.issue("TC-54")
    @allure.title(
        "TC-54: Verify registration with invalid email format"
    )
    @allure.description(
        "Verify that entering an invalid email format in the "
        "'Реєстрація' modal displays the validation error "
        "'Некоректний формат email' and keeps the "
        "'Зареєструватися' button enabled."
    )
    @allure.label("owner", "Svitlana Kovalova")
    def test_verify_invalid_email_format(self, driver) -> None:
        home_page = HomePage(driver)
        sign_up_modal = SignUpModal(driver)

        with allure.step(
            "Step 1 & 2: Open the Registration modal via user menu"
        ):
            home_page.get_header().click_register_menu_item()
            sign_up_modal.is_displayed()

        with allure.step(
            "Step 3: Verify that 'Відвідувач' role is selected by default"
        ):
            assert sign_up_modal.is_visitor_role_selected(), (
                "Visitor role should be selected by default"
            )

        with allure.step(
            "Step 4: Enter valid data into all fields except Email"
        ):
            sign_up_modal.enter_last_name("Іванов")
            sign_up_modal.enter_first_name("Петро")
            sign_up_modal.enter_phone("0991234567")
            sign_up_modal.enter_password("TestPass123!")
            sign_up_modal.enter_confirm_password("TestPass123!")

        with allure.step(
            "Step 5: Enter invalid email format"
        ):
            sign_up_modal.enter_email("not-an-email")
            sign_up_modal.wait_for_error_message(
                "Некоректний формат email"
            )

        with allure.step(
            "Step 6: Verify email validation error"
        ):
            errors = sign_up_modal.get_error_messages()

            assert "Некоректний формат email" in errors, (
                f"Expected error message was not found. "
                f"Actual errors: {errors}"
            )

        with allure.step(
            "Step 7: Verify registration button remains enabled"
        ):
            assert sign_up_modal.is_submit_button_enabled(), (
                "Registration button should remain enabled"
            )
