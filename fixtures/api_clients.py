"""API-related fixtures for tests."""

import pytest

from utils.email_api import TempMailAPIClient


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()
