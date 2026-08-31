"""API client for authentication."""

from __future__ import annotations

import requests

from api.base_client import BaseClient


class AuthClient(BaseClient):
    """Client for the /api/signin endpoint."""

    def sign_in(self, email: str, password: str) -> requests.Response:
        """Sign in and return the raw response (id, email, roleName, accessToken, refreshToken)."""
        return self._request("POST", "signin", json={"email": email, "password": password})
