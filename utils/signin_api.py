"""API helpers for signing in to the Speak Ukrainian application."""

from typing import Any

import allure
import requests

from data.config import Config


class SignInSession:
    """Session data returned by the sign-in API.

    Maps the backend response fields to the exact localStorage keys the SPA
    reads on boot to restore an authenticated state.
    """

    def __init__(self, access_token: str, refresh_token: str, user_id: str, role: str) -> None:
        """Initialize the session with auth tokens and user identity."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.role = role

    def to_storage(self) -> dict[str, str]:
        """Return the session as the SPA's localStorage key/value pairs."""
        return {
            "accessToken": self.access_token,
            "refreshToken": self.refresh_token,
            "id": self.user_id,
            "role": self.role,
        }


def sign_in_via_api(email: str, password: str) -> SignInSession:
    """Authenticate through the sign-in API and return the session payload.

    Args:
        email: The account email.
        password: The account password.

    Returns:
        A :class:`SignInSession` with the tokens and role issued by the API.

    Raises:
        requests.HTTPError: If the sign-in request fails.
    """
    url: str = f"{Config.BASE_API_URL}/signin"
    payload: dict[str, Any] = {"email": email, "password": password}
    with allure.step(f"POST {url}"):
        response = requests.post(url, json=payload, timeout=30)
        if not response.ok:
            allure.attach(
                f"status={response.status_code}\nbody={response.text}",
                name="Sign-in error response",
                attachment_type=allure.attachment_type.TEXT,
            )
            response.raise_for_status()
        data: dict[str, Any] = response.json()
    return SignInSession(
        access_token=data["accessToken"],
        refresh_token=data["refreshToken"],
        user_id=str(data["id"]),
        role=data["roleName"],
    )
