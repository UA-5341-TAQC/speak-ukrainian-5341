"""TC-4: Registration — required fields — Реєстрація modal (fields left empty)."""
import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import HomePage

FIELD_INPUTS: dict[str, str] = {
    "last_name": "Петров",
    "first_name": "Петро",
    "phone": "0991234567",
    "email": "petro.visitor.qa@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
}

FIELD_METHODS: dict[str, str] = {
    "last_name": "enter_last_name",
    "first_name": "enter_first_name",
    "phone": "enter_phone",
    "email": "enter_email",
    "password": "enter_password",
    "confirm_password": "enter_confirm_password",
}

FIELD_LOCATOR_NAMES: dict[str, str] = {
    "last_name": "LAST_NAME_INPUT",
    "first_name": "FIRST_NAME_INPUT",
    "phone": "PHONE_INPUT",
    "email": "EMAIL_INPUT",
    "password": "PASSWORD_INPUT",
    "confirm_password": "CONFIRM_PASSWORD_INPUT",
}

EXPECTED_ERRORS: dict[str, str] = {
    "last_name": "Введіть прізвище",
    "first_name": "Введіть ім`я",
    "phone": "Введіть номер телефону",
    "email": "Введіть email",
    "password": "Введіть пароль",
    "confirm_password": "Значення поля ‘Підтвердити пароль’ має бути еквівалентним значенню поля ‘Пароль’",
}


@allure.feature("Registration")
@pytest.mark.parametrize(
    "empty_field, field_label",
    [
        ("last_name", "Прізвище"),
        ("first_name", "Ім'я"),
        ("phone", "Телефон"),
        ("email", "Email"),
        ("password", "Пароль"),
        ("confirm_password", "Підтвердження паролю"),
    ],
)
@allure.title("TC-4: Registration — required field '{field_label}' left empty")
def test_registration_required_field(driver: WebDriver, empty_field: str, field_label: str) -> None:
    """Verify that leaving a required registration field empty shows a validation error below that field and keeps the 'Зареєструватися' button disabled."""
    home_page = HomePage(driver)

    with allure.step("Click the user icon and choose 'Зареєструватися' in the opened dropdown"):
        sign_up_modal = home_page.header.click_user_profile().click_register()
        assert sign_up_modal.is_displayed()

    assert sign_up_modal.is_visitor_role_selected()

    with allure.step(f"Fill all fields with data EXCEPT '{field_label}' (leave empty)"):
        for field, value in FIELD_INPUTS.items():
            if field != empty_field:
                setter = getattr(sign_up_modal, FIELD_METHODS[field])
                setter(value)

        empty_field_locator = getattr(sign_up_modal, FIELD_LOCATOR_NAMES[empty_field])
        sign_up_modal.type_and_clear(empty_field_locator)

    errors = sign_up_modal.wait_for_specific_error(EXPECTED_ERRORS[empty_field])
    assert EXPECTED_ERRORS[empty_field] in errors
    assert not sign_up_modal.is_submit_button_enabled()