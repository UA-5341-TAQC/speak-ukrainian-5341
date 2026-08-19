"""Pytest fixtures shared by all UI tests (home of the project-level fixtures)."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from data.config import Config
from fixtures.signin_api import SignInSession, sign_in_via_api


def _inject_session(driver: WebDriver, session: SignInSession) -> WebDriver:
    """Inject an API session into the SPA's localStorage and reload the page."""
    driver.execute_script(
        "var storage = arguments[0];"
        "for (var key in storage) { localStorage.setItem(key, storage[key]); }",
        session.to_storage(),
    )
    driver.refresh()
    return driver


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Provide a Selenium WebDriver instance and quit it after the test."""
    options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    if Config.MAXIMIZE:
        options.add_argument("--start-maximized")
    else:
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
    options.add_argument("--disable-gpu")
    web_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    web_driver.get(Config.BASE_UI_URL)
    yield web_driver
    web_driver.quit()


@pytest.fixture(scope="session")
def session_driver() -> SignInSession:
    """Provide API session data for the authenticated user."""
    return sign_in_via_api(Config.USER_EMAIL, Config.USER_PASSWORD)


@pytest.fixture(scope="session")
def manager_session_driver() -> SignInSession:
    """Provide API session data for the authenticated manager."""
    return sign_in_via_api(Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD)


@pytest.fixture
def authenticated_driver(driver: WebDriver, session_driver: SignInSession) -> WebDriver:
    """Provide a browser that is already signed in as the regular user via the API.

    The fixture authenticates through the sign-in API and injects the issued
    tokens into the SPA's localStorage, then reloads the page so the application
    boots with an active session. Future tests can reuse this fixture to start
    from an authenticated state without walking the UI form.
    """
    return _inject_session(driver, session_driver)


@pytest.fixture
def authenticated_manager_driver(
    driver: WebDriver, manager_session_driver: SignInSession
) -> WebDriver:
    """Provide a browser that is already signed in as the manager via the API.

    Mirrors the user-side ``authenticated_driver`` fixture but authenticates with
    the manager credentials, so tests that require a manager role can start from
    an authenticated state without walking the UI form.
    """
    return _inject_session(driver, manager_session_driver)
