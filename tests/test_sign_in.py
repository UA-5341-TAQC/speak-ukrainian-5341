"""Tests around the API-based sign-in fixture."""

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.header.header_component import HeaderComponent
from pages.components.header.user_profile_menu import UserProfileMenu
from pages.modals.sign_in_modal import SignInModal
from data.config import Config


@pytest.mark.smoke
def test_user_is_signed_in_after_api_fixture(authenticated_driver: WebDriver) -> None:
    """Returning the authenticated_driver fixture leaves the session active.

    The fixture signs in via the /api/signin endpoint and injects the issued
    tokens, so the header must report the user as logged in.
    """
    header = HeaderComponent(authenticated_driver.find_element(By.TAG_NAME, "header"))
    assert header.click_user_profile().is_logged_in(), "Expected the header user menu to show a signed-in session."

@allure.title("TC-33: Login — empty fields(required-field enforcement)")
@allure.description(
    "Test verifies required-field validation for the Email and Password fields "
    "when submitting the login form with one field left empty."
)
@allure.tag("login", "validation", "required-fields")
def test_tc33_login_empty_fields(driver: WebDriver) -> None:
    with allure.step("Step 1: Click the user icon in the site header"):
        header = HeaderComponent(driver)
        user_menu = header.click_user_profile()

    with allure.step("Step 2: Click 'Увійти' in the dropdown"):
        login_modal = user_menu.click_login()

    with allure.step("Step 3: Leave both 'Емейл:' and 'Пароль:' empty and click the 'Увійти' button"):
        login_modal.click_submit()
        assert login_modal.get_validation_error_count() == 2, (
        "Both Email and Password fields should display validation errors."
    )

    with allure.step("Step 3: Fill only 'Емейл:' and leave 'Пароль:' empty, click the 'Увійти' button"):
        login_modal.enter_email(Config.USER_EMAIL)
        login_modal.click_submit()
        assert login_modal.get_validation_error_count() == 1, (
        "Password field should display validation errors."
    )

    with allure.step("Step 4: Fill only 'Пароль:' and leave 'Емейл:' empty, click the 'Увійти' button"):
        login_modal.enter_email("")

        login_modal.enter_password(Config.USER_PASSWORD)
        login_modal.click_submit()
        assert login_modal.get_validation_error_count() == 1, (
        "Email field should display validation errors."
    )
