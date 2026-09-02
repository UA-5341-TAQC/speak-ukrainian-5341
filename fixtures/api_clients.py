"""API-related fixtures for tests."""

from collections.abc import Callable

import pytest
from pydantic.dataclasses import dataclass

from api.base_client import BaseClient
from api.complaint_client import ComplaintClient
from api.news_client import NewsClient
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
            email = Config.API_USER_EMAIL
            password = Config.API_USER_PASSWORD

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
    auth_data = sign_in_via_api(Config.API_USER_EMAIL, Config.API_USER_PASSWORD)
    user_id = getattr(auth_data, "id", None) or getattr(auth_data, "user_id", None)

    return ApiUserCredentials(
        access_token=auth_data.access_token,
        user_id=user_id,
        email=Config.API_USER_EMAIL,
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
