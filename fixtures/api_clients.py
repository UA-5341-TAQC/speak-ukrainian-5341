"""API-related fixtures for tests."""

import collections.abc
from collections.abc import Callable
from typing import Any

import pytest
from pydantic.dataclasses import dataclass
from _pytest.fixtures import SubRequest

import utils.signin_api
from api.base_client import BaseClient
from api.club_registration_client import ClubRegistrationClient
from api.address_controller import AddressControllerClient
from api.base_client import BaseClient
from api.categories_client import CategoriesClient
from api.challenge_registration_client import ChallengeRegistrationClient
from api.complaint_client import ComplaintClient
from api.login_client import LoginClient
from api.location_client import LocationClient
from api.news_client import NewsClient
from api.version_client import VersionClient
from data.config import Config
from utils.email_api import TempMailAPIClient


@dataclass
class ApiUserCredentials:
    """Container for API authentication data."""

    access_token: str
    user_id: int | None = None
    email: str | None = None


@pytest.fixture
@pytest.fixture(scope="session")
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

@pytest.fixture(scope="session")
def auth_data() -> dict:
    """Return authentication data for API tests."""
    client = LoginClient()

    response = client.sign_in(
        Config.API_USER_EMAIL,
        Config.API_USER_PASSWORD,
    )

    assert response.status_code == 200

    return response.json()
@pytest.fixture
def authorized_client() -> collections.abc.Callable[..., BaseClient]:

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
    """Provide a news client authenticated with the regular-user token.

    Authenticates through the sign-in API using the ``USER_*`` credentials and
    attaches the issued access token so the client can hit user-permissioned
    news endpoints.
    """
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    return NewsClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )


@pytest.fixture(scope="session")
def news_api_manager() -> NewsClient:
    """Provide a news client authenticated with the manager token.

    Authenticates through the sign-in API using the ``MANAGER_*`` credentials.
    The manager role still lacks admin rights, so admin-only news operations
    (for example ``DELETE /news/{id}``) remain forbidden.
    """
    session = sign_in_via_api(Config.MANAGER_EMAIL, Config.MANAGER_PASSWORD)
    return NewsClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )


@pytest.fixture(scope="session")
def complaint_api() -> ComplaintClient:
    """Provide an unauthenticated client for the public complaint endpoints.

    The complaint list, list-by-club, list-by-recipient, list-by-sender and
    get-by-id endpoints are publicly accessible without a token, so this
    fixture is enough to exercise every read path. The write/maintenance
    operations (``POST``, ``PUT /{id}``, ``PUT /{id}/answer``,
    ``PUT /isActive/{id}``, ``DELETE /{id}``) are exercised in dedicated
    tests through this unauthenticated client to confirm the backend rejects
    anonymous callers, and through ``complaint_api_user`` to confirm the
    authenticated behaviour.
    """
    return ComplaintClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def complaint_api_user() -> tuple[ComplaintClient, str]:
    """Provide a user-authenticated client together with the sender's user id.

    Authenticates through the sign-in API using the ``USER_*`` credentials
    and returns ``(client, user_id)``. The backend's ``POST /complaint``
    requires the body's ``userId`` to match the authenticated user; this
    fixture exposes both pieces so tests building a POST body can use the
    right id without re-running the sign-in dance.

    The probe shows that USER and MANAGER have the same write permissions
    on this deployment, so a single user-role fixture covers the full
    authenticated-write matrix. ``POST /complaint``, ``PUT /{id}/answer``,
    ``PUT /isActive/{id}`` and ``DELETE /{id}`` succeed with this token;
    ``PUT /{id}`` currently returns 400 from the backend regardless of role
    (a known bug pinned by the test suite).
    """
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    client = ComplaintClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )
    return client, session.user_id


@pytest.fixture(scope="session")
def authorized_client() -> Callable[..., BaseClient]:
    """Fixture factory to instantiate and authenticate any API client."""

    def _factory(client_class: type[BaseClient], role: str = "user") -> BaseClient:
        client = client_class(base_url=Config.BASE_API_URL)

        credentials = {
        "admin": (Config.API_ADMIN_EMAIL, Config.API_ADMIN_PASSWORD),
        "manager": (Config.API_MANAGER_EMAIL, Config.API_MANAGER_PASSWORD),
        "user": (Config.API_USER_EMAIL, Config.API_USER_PASSWORD),
        }

        if role not in credentials:
            raise ValueError(f"Unsupported role: {role}")
        email, password = credentials[role]

        auth_data = utils.signin_api.sign_in_via_api(email, password)

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
def addres_control_api() -> AddressControllerClient:
    """Provides a client for the Address Controller  API endpoints."""
    return AddressControllerClient(base_url=Config.BASE_API_URL)

@pytest.fixture(scope="session")
def categories_api() -> CategoriesClient:
    """Provides a client for the Category API endpoints."""
    return CategoriesClient(base_url=Config.BASE_API_URL)


@pytest.fixture(scope="session")
def rbac_client(request: SubRequest) -> Any:
    """Universal factory fixture for initializing any API client with authentication.

    Designed for Role-Based Access Control (RBAC) testing using indirect parametrization.

    Requires `request.param` to provide a tuple of exactly three elements:
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
    return client_class(base_url=Config.BASE_API_URL, access_token=session.access_token)

@pytest.fixture(scope="session")
def challenge_registration_api_user() -> tuple[ChallengeRegistrationClient, str]:
    """Provide a user-authenticated ChallengeRegistrationClient together with the user's id."""
    session = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)  # noqa: E501
    client = ChallengeRegistrationClient(base_url=Config.BASE_API_URL, access_token=session.access_token)  # noqa: E501
    return client, session.user_id


@pytest.fixture(scope="session")
def challenge_registration_api_manager() -> tuple[ChallengeRegistrationClient, str]:
    """Provide a manager-authenticated ChallengeRegistrationClient together with the manager's id."""  # noqa: E501
    session = sign_in_via_api(Config.API_MANAGER_EMAIL, Config.API_MANAGER_PASSWORD)
    client = ChallengeRegistrationClient(base_url=Config.BASE_API_URL, access_token=session.access_token)  # noqa: E501
    return client, session.user_id
