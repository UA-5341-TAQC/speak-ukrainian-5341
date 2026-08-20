"""Tests for the Sign Up modal validation."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from fixtures.email_api import TempMailAPI
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
    request: pytest.FixtureRequest,
    driver: WebDriver,
    invalid_password: str,
    expected_error: str,
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

    assert (
        not sign_up_modal.is_submit_button_enabled()
    ), "Submit button should be disabled, but it remained enabled"


def test_verify_invalid_email_format(driver: WebDriver) -> None:
    """Verify that entering an invalid email format displays the correct validation error."""
    allure.dynamic.issue("TC-54")
    allure.dynamic.title("TC-54: Verify registration with invalid email format")
    allure.dynamic.description(
        "Verify that entering an invalid email format in the "
        "'Реєстрація' modal displays the validation error "
        "'Некоректний формат email' and keeps the "
        "'Зареєструватися' button enabled."
    )
    allure.dynamic.label("owner", "Svitlana Kovalova")

    home_page = HomePage(driver)

    with allure.step("Step 1 & 2: Open the Registration modal via user menu"):
        sign_up_modal = home_page.header.click_user_profile().click_register()

    with allure.step("Step 3: Verify that 'Відвідувач' role is selected by default"):
        assert (
            sign_up_modal.is_visitor_role_selected()
        ), "Visitor role should be selected by default"

    with allure.step("Step 4: Enter valid data into all fields except Email"):
        sign_up_modal.enter_last_name("Іванов")
        sign_up_modal.enter_first_name("Петро")
        sign_up_modal.enter_phone("0991234567")
        sign_up_modal.enter_password("TestPass123!")
        sign_up_modal.enter_confirm_password("TestPass123!")

    with allure.step("Step 5: Enter invalid email format"):
        sign_up_modal.enter_email("not-an-email")
        sign_up_modal.wait_for_error_message("Некоректний формат email")

    with allure.step("Step 6: Verify email validation error"):
        errors = sign_up_modal.get_error_messages()

        assert "Некоректний формат email" in errors, (
            f"Expected error message was not found. " f"Actual errors: {errors}"
        )

    with allure.step("Step 7: Verify registration button remains enabled"):
        assert (
            sign_up_modal.is_submit_button_enabled()
        ), "Registration button should remain enabled"


@pytest.mark.parametrize(
    ("tc_id", "role", "last_name", "first_name", "phone", "password"),
    [
        pytest.param(
            "TC-2",
            "user",
            "Ivanov",
            "Petro",
            "0991234567",
            "TestPass123!",
            id="Visitor",
        ),
        pytest.param(
            "TC-3",
            "manager",
            "Petrenko",
            "Olena",
            "0991234568",
            "ManagerPass123!",
            id="Manager",
        ),
    ],
)
def test_registration_flow(
    driver: WebDriver,
    tc_id: str,
    role: str,
    last_name: str,
    first_name: str,
    phone: str,
    password: str,
) -> None:
    """Verify successful registration with email confirmation (TC-2 and TC-3)."""
    allure.dynamic.title(
        f"{tc_id} Verify successful {role} registration with email confirmation"
    )

    home_page = HomePage(driver)
    home_page.open()

    with allure.step("Precondition: Open Registration modal via user menu"):
        sign_up_modal = home_page.header.click_user_profile().click_register()

    with allure.step(
        "Step 3: Observe the role radio buttons and select appropriate role"
    ):
        assert (
            sign_up_modal.is_visitor_role_selected()
        ), "The 'Відвідувач' role should be selected by default."
        if role == "manager":
            sign_up_modal.select_manager_role()
            assert (
                sign_up_modal.is_manager_role_selected()
            ), "The 'Керівник' role should be selected after click."

    mail_api = TempMailAPI()
    test_email = mail_api.generate_email()

    with allure.step(
        f"Steps 4-9: Fill valid registration data for email: {test_email}"
    ):
        sign_up_modal.fill_registration_form(
            last_name=last_name,
            first_name=first_name,
            phone=phone,
            email=test_email,
            password=password,
            confirm_password=password,
            role=role,
        )
        assert (
            sign_up_modal.is_submit_button_enabled()
        ), "Submit button should be enabled after filling all valid data."

    sign_up_modal.click_submit()

    with allure.step(
        "Step 11: Open the test Email inbox and find the confirmation message"
    ):
        message_id = mail_api.wait_for_email()
        email_html = mail_api.get_email_content(message_id)
        verification_link = mail_api.extract_verification_link(email_html)

    with allure.step("Step 12: Click the confirmation link from the email"):
        driver.get(verification_link)

    with allure.step("Verify successful registration toast message"):
        success_text = home_page.get_success_message_text()
        error_msg = f"Expected confirmation toast, got: {success_text}"
        assert "успішно зареєстрований" in success_text.lower(), error_msg

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
