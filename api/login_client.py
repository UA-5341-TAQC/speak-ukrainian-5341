import requests

from api.base_client import BaseClient
from data.config import Config


class LoginClient(BaseClient):
    """Client for working with the Login API."""

    def __init__(self, base_url: str = Config.DEV_API_URL):
        """Initialize the client with the base URL."""
        super().__init__(base_url=base_url)

    def sign_in(self, email: str, password: str) -> requests.Response:
        """Perform a login request to the API.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            HTTP response from the login API.

        """
        payload = {"email": email, "password": password}
        return self._request(
            method="POST",
            endpoint="/signin",
            json=payload,
            timeout=30,
        )