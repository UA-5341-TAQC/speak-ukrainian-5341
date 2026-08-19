"""Verify what role/session each authenticated driver fixture represents.

Confirms that the ``authenticated_driver`` (user) and
``authenticated_manager_driver`` (manager) fixtures each boot the SPA with the
session issued by their respective credentials from ``.env``. The role and user
id are read back from the same localStorage keys the SPA uses on boot and are
cross-checked against the matching API session.
"""

from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.config import Config
from fixtures.signin_api import SignInSession
from pages.components.header.header_component import HeaderComponent


def _read_storage(driver: WebDriver, key: str) -> str:
    """Return the value of one auth key stored in the SPA's localStorage."""
    value = driver.execute_script(f"return localStorage.getItem('{key}')")
    return "" if value is None else str(value)


def _assert_signed_in(driver: WebDriver, session: SignInSession, who: str) -> None:
    """Assert the browser runs an authenticated session matching ``session``."""
    header = HeaderComponent(driver.find_element(By.TAG_NAME, "header"))
    assert header.click_user_profile().is_logged_in(), (
        f"Expected the header to show a signed-in {who} session."
    )
    assert _read_storage(driver, "role") == session.role, (
        f"Expected the {who} driver to be signed in with role {session.role!r}, "
        f"got {_read_storage(driver, 'role')!r}."
    )
    assert _read_storage(driver, "id") == session.user_id, (
        f"Expected the {who} driver to be signed in as user id {session.user_id!r}, "
        f"got {_read_storage(driver, 'id')!r}."
    )


@allure.feature("Fixtures")
@allure.story("Authenticated driver roles")
def test_authenticated_driver_returns_user_session(
    authenticated_driver: WebDriver, session_driver: SignInSession
) -> None:
    """The user driver boots the SPA with the regular-user API session.

    Args:
        authenticated_driver: Browser signed in with the user credentials.
        session_driver: The API session issued for the user credentials.
    """
    with allure.step("Check the user driver is signed in as the user session"):
        _assert_signed_in(authenticated_driver, session_driver, "user")
    print(
        f"[TC-drivers] authenticated_driver -> role={session_driver.role}, "
        f"id={session_driver.user_id}"
    )


@allure.feature("Fixtures")
@allure.story("Authenticated driver roles")
def test_authenticated_manager_driver_returns_manager_session(
    authenticated_manager_driver: WebDriver, manager_session_driver: SignInSession
) -> None:
    """The manager driver boots a session with the manager API credentials.

    Args:
        authenticated_manager_driver: Browser signed in as the manager credentials.
        manager_session_driver: The API session issued for the manager credentials.
    """
    with allure.step("Check the manager driver is signed in as the manager session"):
        _assert_signed_in(authenticated_manager_driver, manager_session_driver, "manager")
    print(
        f"[TC-drivers] authenticated_manager_driver -> role={manager_session_driver.role}, "
        f"id={manager_session_driver.user_id}"
    )


@allure.feature("Fixtures")
@allure.story("User vs manager credentials")
def test_user_and_manager_credentials_are_configured() -> None:
    """Ensure both user and manager credentials are present in the environment."""
    assert Config.USER_EMAIL, "USER_EMAIL is missing from the .env file."
    assert Config.USER_PASSWORD, "USER_PASSWORD is missing from the .env file."
    assert Config.MANAGER_EMAIL, "MANAGER_EMAIL is missing from the .env file."
    assert Config.MANAGER_PASSWORD, "MANAGER_PASSWORD is missing from the .env file."
