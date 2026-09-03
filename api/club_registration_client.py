"""Module containing the API client for club registration."""

from typing import Any

import allure
import requests

from api.base_client import BaseClient
from data.config import Config


class ClubRegistrationClient(BaseClient):
    """Client for interacting with Club Registration API endpoints."""

    def __init__(self, base_url: str = Config.BASE_API_URL,
                 access_token: str | None = None) -> None:
        """Initialize ClubRegistrationClient with base URL and session."""
        super().__init__(base_url=base_url, access_token=access_token)

    @allure.step("Get user applications by user ID: {user_id}")
    def get_user_applications(self, user_id: int) -> requests.Response:
        """Get list of club applications for a specific user."""
        return self._request(
            "GET",
            f"club-registration/user-applications/{user_id}"
        )

    @allure.step("Get children registered for club ID: {club_id}")
    def get_user_children(self, club_id: int) -> requests.Response:
        """Get list of children registered for a specific club."""
        return self._request(
            "GET",
            f"club-registration/user-children/{club_id}"
        )

    @allure.step("Check registration status for club ID: {club_id}, user ID: {user_id}")
    def get_registration_status(self, club_id: int, user_id: int) -> requests.Response:
        """Check whether a specific user is registered for a specific club."""
        return self._request(
            "GET",
            f"club-registration/{club_id}/{user_id}"
        )

    @allure.step("Register for club with payload: {payload}")
    def register_for_club(self, payload: dict[str, Any]) -> requests.Response:
        """Register one or more children for a club."""
        return self._request("POST", "club-registration", json=payload)

    @allure.step("Register user for club with payload: {payload}")
    def register_user_for_club(self, payload: dict[str, Any]) -> requests.Response:
        """Register a user (not a child) for a club."""
        return self._request("POST", "club-registration/user", json=payload)
