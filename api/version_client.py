"""API client for the public version endpoint."""

from __future__ import annotations

from typing import Any

import requests

from api.base_client import BaseClient

VERSION_ENDPOINT = "version"


class VersionClient(BaseClient):
    """Client for the ``/version`` endpoint of the Speak Ukrainian API."""

    def get_version(self, **kwargs: Any) -> requests.Response:
        """Retrieve the backend build/commit metadata.

        Args:
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing version details such as
            ``backendCommitNumber``, ``backendCommitDate`` and ``buildDate``.
        """
        return self._request("GET", VERSION_ENDPOINT, **kwargs)
