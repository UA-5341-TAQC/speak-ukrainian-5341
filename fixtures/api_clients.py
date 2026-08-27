"""API-related fixtures for tests."""

import pytest

from api.news_client import NewsClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()


@pytest.fixture
def news_api() -> NewsClient:
    """Provide an unauthenticated client for the public news endpoints."""
    return NewsClient(base_url=Config.BASE_API_URL)


@pytest.fixture
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


@pytest.fixture
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
