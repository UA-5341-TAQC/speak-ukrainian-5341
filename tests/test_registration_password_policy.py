"""Automated test for TC-53: Registration password policy validation."""

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.components.header_component import HeaderComponent
from pages.home_page import HomePage
from pages.modals.sign_up_modal import SignUpModal


@allure.title(
    "TC-53 Verify registration password policy validation (length, class, Cyrillic)"
)
@pytest.mark.parametrize(
    "invalid_password, expected_error",
    [
        pytest.param(
            "Ab1!",
            "Пароль не може бути коротшим, ніж 8 та довшим, ніж 20 символів",
            id="Length < 8",
        ),
        pytest.param(
            "Ab1!Ab1!Ab1!Ab1!Ab1!X",
            "Пароль не може бути коротшим, ніж 8 та довшим, ніж 20 символів",
            id="Length > 20",
        ),
        pytest.param(
            "abcdefgh",
            "Пароль повинен містити хоча б одну велику літеру",
            id="Missing uppercase",
        ),
        pytest.param(
            "ABCDEFGH",
            "Пароль повинен містити хоча б одну маленьку літеру",
            id="Missing lowercase",
        ),
        pytest.param(
            "!!!!!!!!",
            "Пароль повинен містити хоча б одну велику літеру",
            id="Missing letters/digits",
        ),
        pytest.param(
            "12345678",
            "Пароль повинен містити хоча б одну велику літеру",
            id="Missing letters/special",
        ),
        pytest.param(
            "Пароль123!",
            "Пароль не може містити українські та російські літери",
            id="Contains Cyrillic",
        ),
    ],
)
def test_registration_password_policy(
    driver: WebDriver, invalid_password: str, expected_error: str
) -> None:
    """Verify that entering an invalid password displays the correct validation error."""
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("Precondition: Open Registration modal via user menu"):
        home_page.header.click_register_menu_item()
        
        sign_up_modal = SignUpModal(driver)
        sign_up_modal.is_displayed()

    with allure.step("1. Enter valid baseline data into all fields except Password"):
        sign_up_modal.enter_last_name("Іванов")
        sign_up_modal.enter_first_name("Петро")
        sign_up_modal.enter_phone("0991234567")
        sign_up_modal.enter_email("petro.visitor.qa@example.com")

    with allure.step(
        f"2. Enter invalid password '{invalid_password}' and observe error"
    ):
        sign_up_modal.enter_password(invalid_password)
        sign_up_modal.enter_confirm_password(invalid_password)

        # Wait for the error message to appear
        sign_up_modal.wait_for_error_message(expected_error)

        errors = sign_up_modal.get_error_messages()
        assert expected_error in errors, (
            f"Expected error '{expected_error}' not found. Actual errors: {errors}"
        )
        
        try:
            sign_up_modal.wait_for_submit_button_disabled()
        except Exception:
            assert False, "Submit button should be disabled, but it remained enabled"
