"""Pytest fixtures shared by all UI tests (home of the project-level fixtures)."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from api.signin import sign_in_via_api
from data.config import Config


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Provide a Selenium WebDriver instance and quit it after the test."""
    options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--disable-gpu")
    web_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    yield web_driver
    web_driver.quit()


@pytest.fixture
def authenticated_driver(driver: WebDriver) -> WebDriver:
    """Provide a browser that is already signed in via the API.

    The fixture authenticates through the sign-in API and injects the issued
    tokens into the SPA's localStorage, then reloads the page so the
    application boots with an active session. Future tests can reuse this
    fixture to start from an authenticated state without walking the UI form.
    """
    session = sign_in_via_api(Config.USER_EMAIL, Config.USER_PASSWORD)

    base_url = Config.BASE_UI_URL.rstrip("/") + "/"
    driver.get(base_url)
    driver.execute_script(
        "var storage = arguments[0];"
        "for (var key in storage) { localStorage.setItem(key, storage[key]); }",
        session.to_storage(),
    )
    driver.get(base_url)
    return driver
