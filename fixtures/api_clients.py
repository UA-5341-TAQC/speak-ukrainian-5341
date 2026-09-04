"""API-related fixtures for tests."""

from collections.abc import Callable
from typing import Any, TypeVar, cast

import pytest
from _pytest.fixtures import SubRequest
from pydantic.dataclasses import dataclass

from api.address_controller import AddressControllerClient
from api.base_client import BaseClient
from api.categories_client import CategoriesClient
from api.challenge_registration_client import ChallengeRegistrationClient
from api.club_registration_client import ClubRegistrationClient
from api.complaint_client import ComplaintClient
from api.location_client import LocationClient
from api.login_client import LoginClient
from api.news_client import NewsClient
from api.version_client import VersionClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api

T = TypeVar("T", bound=BaseClient)


@dataclass
class ApiUserCredentials:
    """Container for API authentication data."""

    access_token: str
    user_id: int | None = None
    email: str | None = None


@pytest.fixture(scope="session")
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()


@pytest.fixture(scope="session")
def auth_data() -> dict[str, Any]:
    """Return authentication data for API tests."""
    client = LoginClient()

    response = client.sign_in(
        Config.API_USER_EMAIL,
        Config.API_USER_PASSWORD,
    )
    return response.json()


@pytest.fixture
def version_api() -> VersionClient:
    """Provides a client for the public ``/version`` endpoint."""
    return VersionClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def user_api_credentials() -> ApiUserCredentials:
    """Authenticate the API test user and return its session credentials."""
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    return ApiUserCredentials(
        access_token=session.access_token,
        user_id=int(session.user_id),
        email=Config.API_USER_EMAIL,
    )


@pytest.fixture
def club_registration_client(
    user_api_credentials: ApiUserCredentials,
) -> ClubRegistrationClient:
    """Provide a club registration client authenticated as the API user."""
    return ClubRegistrationClient(
        base_url=Config.BASE_API_URL,
        access_token=user_api_credentials.access_token,
    )


@pytest.fixture(scope="session")
def news_api() -> NewsClient:
    """Provide an unauthenticated client for the public news endpoints."""
    return NewsClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def news_api_user() -> NewsClient:
    """Provide a news client authenticated with the regular-user token."""
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    return NewsClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )


@pytest.fixture(scope="session")
def news_api_manager() -> NewsClient:
    """Provide a news client authenticated with the manager token."""
    session = sign_in_via_api(Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD)
    return NewsClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )


@pytest.fixture(scope="session")
def complaint_api() -> ComplaintClient:
    """Provide an unauthenticated client for the public complaint endpoints."""
    return ComplaintClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def complaint_api_user() -> tuple[ComplaintClient, str]:
    """Provide a user-authenticated client together with the sender's user id."""
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    client = ComplaintClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )
    return client, session.user_id


@pytest.fixture(scope="session")
def authorized_client() -> Callable[[type[T], str], T]:
    """Fixture factory to instantiate and authenticate any API client."""

    def _factory(client_class: type[T], role: str = "user") -> T:
        client = client_class(base_url=Config.BASE_API_URL)

        credentials = {
            "admin": (Config.API_ADMIN_EMAIL, Config.API_ADMIN_PASSWORD),
            "manager": (Config.API_MANAGER_EMAIL, Config.API_MANAGER_PASSWORD),
            "user": (Config.API_USER_EMAIL, Config.API_USER_PASSWORD),
        }

        if role not in credentials:
            raise ValueError(f"Unsupported role: {role}")
        email, password = credentials[role]

        auth_data = sign_in_via_api(email, password)

        client.session.headers.update(
            {
                "Authorization": f"Bearer {auth_data.access_token}",
            }
        )

        return client

    return _factory


@pytest.fixture
def location_api() -> LocationClient:
    """Provides a client for the Location API endpoints."""
    return LocationClient(base_url=Config.BASE_API_URL)


@pytest.fixture
def address_control_api() -> AddressControllerClient:
    """Provides a client for the Address Controller API endpoints."""
    return AddressControllerClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def categories_api() -> CategoriesClient:
    """Provides a client for the Category API endpoints."""
    return CategoriesClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def rbac_client(request: SubRequest) -> BaseClient:
    """Universal factory fixture for initializing any API client with authentication.

    Designed for Role-Based Access Control (RBAC) testing using indirect parametrization.

    Requires `request.param` to provide a tuple of two elements:
    1. client_class (Type[BaseClient]): The specific API client class to instantiate.
    2. role (str): The role name ('user' or 'manager') to authenticate as.

    Returns:
        An instance of the provided `client_class` authenticated with the corresponding token.
    """
    client_class, role = request.param
    if role == "user":
        email, password = Config.USER_EMAIL, Config.USER_PASSWORD
    elif role == "manager":
        email, password = Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD
    else:
        raise ValueError(f"Unknown role: {role}")

    session = sign_in_via_api(email, password)
    return cast(
        BaseClient, client_class(base_url=Config.BASE_API_URL, access_token=session.access_token)
    )


@pytest.fixture(scope="session")
def challenge_registration_api_user() -> tuple[ChallengeRegistrationClient, str]:
    """Provide a user-authenticated ChallengeRegistrationClient together with the user's id."""
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    client = ChallengeRegistrationClient(
        base_url=Config.BASE_API_URL, access_token=session.access_token
    )
    return client, session.user_id


@pytest.fixture(scope="session")
def challenge_registration_api_manager() -> tuple[ChallengeRegistrationClient, str]:
    """Provide a manager-authenticated ChallengeRegistrationClient together with the manager id."""
    session = sign_in_via_api(Config.API_MANAGER_EMAIL, Config.API_MANAGER_PASSWORD)
    client = ChallengeRegistrationClient(
        base_url=Config.BASE_API_URL, access_token=session.access_token
    )
    return client, session.user_id
