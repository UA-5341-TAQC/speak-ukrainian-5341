"""API-related fixtures for tests."""

import pytest

from api.login_client import LoginClient
from data.config import Config
from utils.email_api import TempMailAPIClient


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

@pytest.fixture(scope="session")
def auth_data() -> dict:
    """Return authentication data for API tests."""
    client = LoginClient()

    response = client.sign_in(
        Config.DEV_USER_EMAIL,
        Config.DEV_USER_PASSWORD,
    )

    assert response.status_code == 200

    return response.json()
