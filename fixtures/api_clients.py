"""API-related fixtures for tests."""

import collections.abc

import pytest

import utils.signin_api
from api.base_client import BaseClient
from data.config import Config
from utils.email_api import TempMailAPIClient


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

@pytest.fixture
def authorized_client() -> collections.abc.Callable[..., BaseClient]:
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

        auth_data = utils.signin_api.sign_in_via_api(email, password)

        client.session.headers.update(
            {
                "Authorization": f"Bearer {auth_data.access_token}",
            }
        )

        return client

    return _factory
