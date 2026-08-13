"""TC-55 Registration — phone format — Реєстрація modal (invalid phone format).

Test Steps
Step 1  Click the user icon in the site header.                           -> A dropdown menu opens with registration and login options.
Step 2  Click "Зареєструватися" in the dropdown.                          -> The "Реєстрація" modal opens.
Step 3  Observe the role selection.                                       -> The "Відвідувач" role is selected by default.
Step 4  Fill all fields with valid data except "Телефон".                 -> Valid fields show a green check mark.
Step 5 	Enter an invalid phone suffix into the "Телефон" 
        field and observe the error.                                      -> A red error appears below the field with the corresponding <ErrorMessage>; 
                                                                             other fields keep their green check; the button remains disabled.
"""


import allure
import pytest

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from data.config import Config
from pages.modals.sign_up_modal import SignUpModal
from pages.components.header_component import HeaderComponent
from pages.types import Locator


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
def test_registration_inv_num(driver: WebDriver, phone: str, expected_message: list[str]) -> None:
    driver.get(Config.BASE_UI_URL)
    header = HeaderComponent(driver)
    sign_up_mod = SignUpModal(driver)

    with allure.step("1.Click the user icon in the site header."):
        header.click_user_profile()
        assert header.is_user_profile_dropdown_visible() == True

    with allure.step("2.Click 'Зареєструватися' in the dropdown."):
        header.click_registration_in_button()
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
            