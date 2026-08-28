"""API-related fixtures for tests."""

from collections.abc import Callable
from typing import Any

import pytest
from _pytest.fixtures import SubRequest

from api.base_client import BaseClient
from api.categories_client import CategoriesClient
from api.complaint_client import ComplaintClient
from api.news_client import NewsClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()


<<<<<<< HEAD
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
    session = sign_in_via_api(Config.USER_EMAIL, Config.USER_PASSWORD)
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
    session = sign_in_via_api(Config.USER_EMAIL, Config.USER_PASSWORD)
    client = ComplaintClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )
    return client, session.user_id


=======
>>>>>>> 6366b831 (feat(api): implement Categories API client, RBAC tests, and allure reporting)
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


@pytest.fixture
def categories_api() -> CategoriesClient:
    """Provides a client for the Category API endpoints."""
    return CategoriesClient(base_url=Config.BASE_API_URL)


@pytest.fixture
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
