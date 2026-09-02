"""API-related fixtures for tests."""

from collections.abc import Callable

import pytest
from pydantic.dataclasses import dataclass

from api.base_client import BaseClient
from api.club_registration_client import ClubRegistrationClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api


@dataclass
class ApiUserCredentials:
    """Container for API authentication data."""
    access_token: str
    user_id: int | None = None
    email: str | None = None

@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

@pytest.fixture
def authorized_client() -> Callable[..., BaseClient]:
    """Fixture factory to instantiate and authenticate any API client."""

    def _factory(client_class: type[BaseClient], role: str = "user") -> BaseClient:
        client = client_class(base_url=Config.BASE_API_URL)

        if role == "admin":
            email = Config.ADMIN_EMAIL
            password = Config.ADMIN_PASSWORD
        elif role == "manager":
            email = Config.MANAGER_EMAIL
            password = Config.MANAGER_PASSWORD
        else:
            email = Config.USER_EMAIL
            password = Config.USER_PASSWORD

        auth_data = sign_in_via_api(email, password)

        client.session.headers.update(
            {
                "Authorization": f"Bearer {auth_data.access_token}",
            }
        )

        return client

    return _factory


@pytest.fixture(scope="session")
def user_api_credentials() -> ApiUserCredentials:
    """Login as regular user via API and return token + user_id."""
    auth_data = sign_in_via_api(Config.USER_EMAIL, Config.USER_PASSWORD)
    user_id = getattr(auth_data, "id", None) or getattr(auth_data, "user_id", None)

    return ApiUserCredentials(
        access_token=auth_data.access_token,
        user_id=user_id,
        email=Config.USER_EMAIL,
    )


@pytest.fixture(scope="session")
def manager_api_credentials() -> ApiUserCredentials:
    """Login as manager via API and return token + user_id."""
    auth_data = sign_in_via_api(Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD)

    user_id = getattr(auth_data, "id", None) or getattr(auth_data, "user_id", None)

    return ApiUserCredentials(
        access_token=auth_data.access_token,
        user_id=user_id,
        email=Config.MANAGER_EMAIL,
    )


@pytest.fixture
def club_registration_client(user_api_credentials: ApiUserCredentials) -> ClubRegistrationClient:
    """Provides authorized ClubRegistrationClient (user role)."""
    return ClubRegistrationClient(access_token=user_api_credentials.access_token)


@pytest.fixture
def club_registration_client_manager(
    manager_api_credentials: ApiUserCredentials,
) -> ClubRegistrationClient:
    """Provides authorized ClubRegistrationClient (manager role)."""
    return ClubRegistrationClient(access_token=manager_api_credentials.access_token)
