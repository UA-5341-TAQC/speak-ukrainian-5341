"""Root pytest configuration.

The shared fixtures live in the project-level ``fixtures`` package and are
re-exported here so they are visible to every test in the ``tests`` directory.
pytest auto-loads conftest.py files it finds, so the fixtures module must not
be registered twice via ``pytest_plugins`` - re-exporting the fixture
functions is enough.
"""

from typing import Generator, cast

import allure
from allure_commons.types import AttachmentType
from pluggy import Result
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from fixtures.drivers import *

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Generator[None, Result[pytest.TestReport], None]:
    """Attach screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if isinstance(item, pytest.Function) and "driver" in item.funcargs:
            web_driver = cast(WebDriver, item.funcargs["driver"])
            try:
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name=f"screenshot_on_failure_{item.name}",
                    attachment_type=AttachmentType.PNG,
                )
            except Exception as e:
                print(f"Failed to take screenshot: {e}")

