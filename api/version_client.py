"""API client for the public version endpoint."""

from __future__ import annotations

from typing import Any

from api.base_client import BaseClient

VERSION_ENDPOINT = "version"


class VersionClient(BaseClient):
    """Client for the ``/version`` endpoint of the Speak Ukrainian API."""

    def get_version(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve the backend build/commit metadata.

        Returns:
            Parsed JSON object with version details such as
            ``backendCommitNumber``, ``backendCommitDate`` and ``buildDate``.
        """
        response = self._request("GET", VERSION_ENDPOINT, **kwargs)
        return dict(response.json())
