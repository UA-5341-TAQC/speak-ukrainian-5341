"""API client for Archive endpoints."""

import requests

from api.base_client import BaseClient
from data.config import Config


class ArchiveClient(BaseClient):
    """Client for working with the Archive API."""

    def __init__(
        self,
        base_url: str = Config.BASE_API_URL,
        access_token: str | None = None,
    ) -> None:
        """Initialize the Archive API client."""
        super().__init__(
            base_url=base_url,
            access_token=access_token,
        )

    def get_archives(self) -> requests.Response:
        """Get all archives."""
        return self._request(
            method="GET",
            endpoint="/archives",
            timeout=30,
        )

    def get_archives_by_class_name(
        self,
        class_name: str,
    ) -> requests.Response:
        """Get archives by class name."""
        return self._request(
            method="GET",
            endpoint=f"/archives/{class_name}",
            timeout=30,
        )
