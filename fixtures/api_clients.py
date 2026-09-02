"""API-related fixtures for tests."""

from collections.abc import Callable

import pytest

from api.base_client import BaseClient
from api.address_controller import AddressControllerClient
from api.location_client import LocationClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api


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

@pytest.fixture
def location_api() -> LocationClient:
    """Provides a client for the Location API endpoints."""
    return LocationClient(base_url=Config.BASE_API_URL)

@pytest.fixture
def addres_control_api() -> AddressControllerClient:
    """Provides a client for the Address Controller  API endpoints."""
    return AddressControllerClient(base_url=Config.BASE_API_URL)
