import requests

from data.config import Config


class LoginClient:
    """Client for working with the Login API."""

    def __init__(self, base_url: str = Config.DEV_API_URL):
        """Initialize the client with the base URL."""
        self.base_url = base_url

    def sign_in(self, email: str, password: str) -> requests.Response:
        """Perform a login request to the API.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            the response data from the login API.

        """
        url = f"{self.base_url}/signin"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload, timeout=30)
        # Тесту потрібна можливість перевірити не тільки дані, а й HTTP status
        return response
