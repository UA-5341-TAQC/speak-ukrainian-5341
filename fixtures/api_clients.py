"""API-related fixtures for tests."""

import pytest

from api.auth_client import AuthClient
from api.challenge_registration_client import ChallengeRegistrationClient
from data.config import Config
from utils.email_api import TempMailAPIClient


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

def _sign_in(email: str, password: str) -> dict:
    """Signs in with the given credentials and returns the full response body."""
    auth_client = AuthClient(base_url=Config.BASE_API_URL)
    response = auth_client.sign_in(email, password)
    assert response.status_code == 200, f"Sign-in failed: {response.status_code} {response.text}"
    return response.json()


@pytest.fixture
def user_auth_data() -> dict:
    """Signs in as the configured test user once per test."""
    return _sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)


@pytest.fixture
def manager_auth_data() -> dict:
    """Signs in as the configured test manager once per test."""
    return _sign_in(Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD)


@pytest.fixture
def user_id(user_auth_data: dict) -> int:
    """ID of the currently signed-in test user."""
    return user_auth_data["id"]


@pytest.fixture
def user_client(user_auth_data: dict) -> ChallengeRegistrationClient:
    """Provides a ChallengeRegistrationClient authenticated as a regular user."""
    return ChallengeRegistrationClient(base_url=Config.BASE_API_URL, access_token=user_auth_data["accessToken"])  # noqa: E501


@pytest.fixture
def manager_id(manager_auth_data: dict) -> int:
    """ID of the currently signed-in test manager."""
    return manager_auth_data["id"]


@pytest.fixture
def manager_client(manager_auth_data: dict) -> ChallengeRegistrationClient:
    """Provides a ChallengeRegistrationClient authenticated as a manager."""
    return ChallengeRegistrationClient(base_url=Config.BASE_API_URL, access_token=manager_auth_data["accessToken"])  # noqa: E501


