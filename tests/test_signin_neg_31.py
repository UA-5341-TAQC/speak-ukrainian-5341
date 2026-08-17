"""TC-31 Login — wrong password — Вхід modal (confirmed account)

Test Steps
Step 1  Enter the correct Email of a confirmed account
        and a wrong Password, then click "Увійти"                          -> Login is rejected: error message "Введено невірний пароль або email."; 
                                                                              the user stays unauthenticated; the modal stays open

"""


import allure
import pytest

from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.modals.sign_in_modal import SignInModal
from pages.components.header_component import HeaderComponent


@pytest.mark.parametrize("email, password, expected_message",
    [("petro.visitor.qa@example.com", "WrongPass999!", "Введено невірний пароль або email")])
@allure.title("TC-31 Registration — phone format — Реєстрація modal (invalid phone format).")
def test_login_wrong_password(driver: WebDriver, email:str, password:str, expected_message:list[str]) -> None:
    driver.get(Config.BASE_UI_URL)
    header = HeaderComponent(driver)
    header.click_user_profile()
    header.click_sign_in_button()
    
    sign_in_mod = header.get_sign_up_modal()

    with allure.step("1.Click the user icon in the site header."):
        assert sign_in_mod.is_displayed()

        sign_in_mod.enter_email(email)
        sign_in_mod.enter_password(password)
        result = sign_in_mod.pop_up_error_trigger()
        assert result == expected_message
              

    
