"""TC-56 Registration — password mismatch — Реєстрація modal (confirm ≠ password)"""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.home_page import HomePage
from pages.modals.sign_up_modal import SignUpModal


@allure.title("TC-56 Registration — password mismatch — Реєстрація modal (confirm ≠ password).")
def test_registration_password_missmatch_59(driver: WebDriver) -> None:
    homepage = HomePage(driver)
    
    with allure.step("1.Click the user icon in the site header."):
        user_profile = homepage.header.click_user_profile()
        assert  user_profile.is_visible() == True

    with allure.step("2.Click 'Зареєструватися' in the dropdown."):
        sign_up_mod = user_profile.click_register()
        assert sign_up_mod.is_displayed() ==True

    with allure.step("3.Observe the role selection."):
        assert sign_up_mod.is_visitor_role_selected() == True

    with allure.step("4.Fill all fields with valid data."):
        sign_up_mod.enter_last_name("Іванов")
        sign_up_mod.enter_first_name("Петро")
        sign_up_mod.enter_phone("+38011114567")
        sign_up_mod.enter_email("petro.visitor.qa@example.com")
        sign_up_mod.enter_password("TestPass123!")

    with allure.step("4.Fill all fields with valid data."):
        sign_up_mod.enter_confirm_password("OtherPass123!")


