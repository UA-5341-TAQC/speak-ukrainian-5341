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
from pages.home_page import HomePage


@pytest.mark.parametrize("email, password, expected_message",
    [("petro.visitor.qa@example.com", "WrongPass999!", "Введено невірний пароль або email")])
@allure.title("TC-31 Login — wrong password — Вхід modal (confirmed account).")
def test_login_wrong_password_tc31(driver: WebDriver, email:str, password:str, expected_message:list[str]) -> None:
    homepage = HomePage(driver)
    sign_in_mod = homepage.header.click_user_profile().click_login()

    with allure.step("1.Click the user icon in the site header."):
        sign_in_mod.fill_login_form(email, password)
        result = sign_in_mod.pop_up_error_trigger()
        assert result == expected_message
        assert sign_in_mod.is_displayed() == True
