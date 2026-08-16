"""Tests around the API-based sign-in fixture."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.config import Config
from pages.components.header_component import HeaderComponent
from pages.modals.sign_in_modal import SignInModal


@pytest.mark.smoke
def test_user_is_signed_in_after_api_fixture(authenticated_driver: WebDriver) -> None:
    """Returning the authenticated_driver fixture leaves the session active.

    The fixture signs in via the /api/signin endpoint and injects the issued
    tokens, so the header must report the user as logged in.
    """
    header = HeaderComponent(authenticated_driver.find_element(By.TAG_NAME, "header"))
    assert header.is_logged_in(), "Expected the header user menu to show a signed-in session."


@pytest.mark.smoke
def test_confirmed_user_can_log_in(driver: WebDriver) -> None:
    """TC-5: a confirmed user can log in via the 'Вхід' modal and stays signed in.

    Fills valid credentials for a confirmed account, submits the login form,
    and verifies the header reports a signed-in session, including after a
    page reload.

    NOTE: waits for `SignInModal.EMAIL_INPUT` to become visible rather than
    calling `SignInModal.is_displayed()`, because `MODAL_CONTENT`
    (`div.ant-modal-content`) is not specific to the Sign In modal — other
    modals mounted (but hidden) in the DOM share the same class, so
    `is_displayed()` can pick up the wrong element and report False even
    when the Sign In modal is genuinely open. Worth flagging to the team as
    a possible improvement to `SignInModal.is_displayed()`.
    """
    header = HeaderComponent(driver.find_element(By.TAG_NAME, "header"))
    header.click_login_menu_item()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(SignInModal.EMAIL_INPUT)
    )
    login_modal = SignInModal(driver)

    login_modal.fill_login_form(Config.USER_EMAIL, Config.USER_PASSWORD)
    login_modal.click_submit()

    header = HeaderComponent(driver.find_element(By.TAG_NAME, "header"))
    assert header.is_logged_in(), (
        "Expected the user to be authenticated after submitting valid "
        "credentials for a confirmed account."
    )

    driver.refresh()
    header = HeaderComponent(driver.find_element(By.TAG_NAME, "header"))
    assert header.is_logged_in(), "Expected the user to remain authenticated after a reload."
