"""Tests for the Sign Up modal validation."""
from __future__ import annotations


import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage
from pages.modals.sign_up_modal import SignUpModal


@pytest.mark.parametrize(
    ("invalid_password", "expected_error"),
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
def test_sign_up_password_policy(
    request: pytest.FixtureRequest, driver: WebDriver, invalid_password: str, expected_error: str
) -> None:
    """Verify that entering an invalid password displays the correct validation error."""
    allure.dynamic.title(
        f"TC-53 Verify registration password policy validation [{request.node.callspec.id}]"
    )
    driver.get(Config.BASE_UI_URL)
    home_page = HomePage(driver)

    with allure.step("Precondition: Open Registration modal via user menu"):
        sign_up_modal = home_page.header.click_user_profile().click_register()
        sign_up_modal.is_displayed()

    with allure.step("1. Enter valid baseline data into all fields except Password"):
        sign_up_modal.enter_last_name("Іванов")
        sign_up_modal.enter_first_name("Петро")
        sign_up_modal.enter_phone("0991234567")
        sign_up_modal.enter_email("petro.visitor.qa@example.com")

    with allure.step("2. Enter invalid password and observe validation error"):
        sign_up_modal.enter_password(invalid_password)
        sign_up_modal.enter_confirm_password(invalid_password)
        sign_up_modal.wait_for_error_message(expected_error)

        errors = sign_up_modal.get_error_messages()
        assert (
            expected_error in errors
        ), f"Expected error '{expected_error}' not found. Actual errors: {errors}"

    with allure.step("3. Verify submit button is disabled"):
        assert (
            not sign_up_modal.is_submit_button_enabled()
        ), "Submit button should be disabled, but it remained enabled"


def test_verify_invalid_email_format(driver: WebDriver) -> None:
    """Verify that entering an invalid email format displays the correct validation error."""
    allure.dynamic.issue("TC-54")
    allure.dynamic.title(
        "TC-54: Verify registration with invalid email format"
    )
    allure.dynamic.description(
        "Verify that entering an invalid email format in the "
        "'Реєстрація' modal displays the validation error "
        "'Некоректний формат email' and keeps the "
        "'Зареєструватися' button enabled."
    )
    allure.dynamic.label("owner", "Svitlana Kovalova")

    
    home_page = HomePage(driver)

    with allure.step(
        "Step 1 & 2: Open the Registration modal via user menu"
    ):
        sign_up_modal = home_page.header.click_user_profile().click_register()

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

@pytest.mark.parametrize("phone, expected_message",[
     ("991234567",["Телефон не відповідає вказаному формату", "Телефон не відповідає українському формату (+380)"]),
     ("380991234567",["Телефон не відповідає вказаному формату", "Телефон не відповідає українському формату (+380)"]),
     ("099123456",["Телефон не відповідає вказаному формату"]),
     ("099123456789",["Телефон не відповідає вказаному формату"]),
     ("+380****4567",["Телефон не відповідає вказаному формату", "Телефон не відповідає українському формату (+380)","Телефон не може містити спеціальні символи"]),
     ("099-123-45-67",["Телефон не відповідає вказаному формату","Телефон не може містити спеціальні символи"]),
     ("099 123 4567",["Телефон не може містити пробіли","Телефон не відповідає вказаному формату"])
     ])
@allure.title("TC-55 Registration — phone format — Реєстрація modal (invalid phone format).")
def test_registration_inv_num_55(driver: WebDriver, phone: str, expected_message: list[str]) -> None:
    homepage = HomePage(driver)
    
    with allure.step("1.Click the user icon in the site header."):
        user_profile = homepage.header.click_user_profile()
        assert  user_profile.is_visible() == True

    with allure.step("2.Click 'Зареєструватися' in the dropdown."):
        sign_up_mod = user_profile.click_register()
        assert sign_up_mod.is_displayed() ==True

    with allure.step("3.Observe the role selection."):
        assert sign_up_mod.is_visitor_role_selected() == True

    with allure.step("4. Fill all fields with valid data except 'Телефон'"):
        sign_up_mod.enter_first_name("Петро")
        sign_up_mod.enter_last_name("Іванов")
        sign_up_mod.enter_email("petro.visitor.qa@example.com")
        sign_up_mod.enter_password("TestPass123!")
        sign_up_mod.enter_confirm_password("TestPass123!")

        assert sign_up_mod.is_successfull_icon_visible_first_name() == True
        assert sign_up_mod.is_successfull_icon_visible_last_name() == True
        assert sign_up_mod.is_successfull_icon_visible_email() == True
        assert sign_up_mod.is_successfull_icon_visible_password() == True
        assert sign_up_mod.is_successfull_icon_visible_password_confirm() == True

    
    with allure.step("5.Enter an invalid phone suffix into the 'Телефон' field and observe the error"):
            sign_up_mod.enter_phone(phone)
            actual_result = sign_up_mod.get_error_messages_phone()

            assert actual_result == expected_message
            assert sign_up_mod.is_error_icon_visible_phone() == True
            assert sign_up_mod.is_successfull_icon_visible_first_name() == True
            assert sign_up_mod.is_successfull_icon_visible_last_name() == True
            assert sign_up_mod.is_successfull_icon_visible_email() == True
            assert sign_up_mod.is_successfull_icon_visible_password() == True
            assert sign_up_mod.is_successfull_icon_visible_password_confirm() == True
