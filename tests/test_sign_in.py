"""Tests around the API-based sign-in fixture."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from pages.components.header.header_component import HeaderComponent
from pages.home_page import HomePage


@pytest.mark.smoke
def test_user_is_signed_in_after_api_fixture(authenticated_driver: WebDriver) -> None:
    """Returning the authenticated_driver fixture leaves the session active.

    The fixture signs in via the /api/signin endpoint and injects the issued
    tokens, so the header must report the user as logged in.
    """
    header = HeaderComponent(authenticated_driver.find_element(By.TAG_NAME, "header"))
    assert header.click_user_profile().is_logged_in(), (
        "Expected the header user menu to show a signed-in session."
    )


@pytest.mark.smoke
def test_confirmed_user_can_log_in(driver: WebDriver) -> None:
    """TC-5: a confirmed user can log in via the 'Вхід' modal and stays signed in.

    Fills valid credentials for a confirmed account, submits the login form,
    and verifies the user menu reports a signed-in session, including after
    a page reload.

    Uses the current `UserProfileMenu` API: `HeaderComponent.click_user_profile()`
    opens the dropdown and returns a `UserProfileMenu`; its `click_login()`
    opens the "Вхід" modal and returns the `SignInModal`; `is_logged_in()`
    lives on `UserProfileMenu`, so the dropdown must be reopened each time
    the auth state is checked.
    """
    home_page = HomePage(driver)
    user_menu = home_page.header.click_user_profile()
    login_modal = user_menu.click_login()

    login_modal.fill_login_form(Config.USER_EMAIL, Config.USER_PASSWORD)
    login_modal.click_submit()

    assert home_page.header.click_user_profile().is_logged_in(), (
        "Expected the user to be authenticated after submitting valid "
        "credentials for a confirmed account."
    )

    home_page.refresh()
    assert home_page.header.click_user_profile().is_logged_in(), (
        "Expected the user to remain authenticated after a reload."
    )