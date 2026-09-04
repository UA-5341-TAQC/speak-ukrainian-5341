import requests

from api.base_client import BaseClient
from data.config import Config


class UserClient(BaseClient):
    """Client for working with the User API."""

    def __init__(self, base_url: str = Config.BASE_API_URL, access_token: str | None = None):
        """Initialize the client with the base URL."""
        super().__init__(base_url=base_url, access_token=access_token)

    def get_users(self) -> requests.Response:
        """Perform a request to get all users from the API.

        Returns:
            HTTP response from the API.
        """
        return self._request(
            method="GET",
            endpoint="/users",
            timeout=30,
        )

    def get_user(self, user_id: int) -> requests.Response:
        """Perform a request to get a specific user by ID from the API.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            HTTP response from the API.
        """
        return self._request(
            method="GET",
            endpoint=f"/user/{user_id}",
            timeout=30,
        )
