import pytest

from api.archive_client import ArchiveClient
from data.config import Config
from utils.email_api import TempMailAPIClient
from utils.signin_api import sign_in_via_api


@pytest.fixture
def temp_mail() -> TempMailAPIClient:
    """Provides an authenticated temporary email client."""
    return TempMailAPIClient()

@pytest.fixture
def archive_client() -> ArchiveClient:
    """Provides an authenticated Archive API client."""
    session = sign_in_via_api(
        Config.MANAGER_EMAIL,
        Config.MANAGER_PASSWORD,
    )

    return ArchiveClient(
        base_url=Config.BASE_API_URL,
        access_token=session.access_token,
    )
