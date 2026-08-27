"""API-related fixtures for tests."""

import pytest

from api.version_client import VersionClient
from data.config import Config
from utils.email_api import TempMailAPIClient


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()


@pytest.fixture
def version_api() -> VersionClient:
    """Provides a client for the public ``/version`` endpoint."""
    return VersionClient(base_url=Config.BASE_API_URL)
