"""Module containing the API client for managing challenges."""

from typing import Any

import allure
import requests

from api.base_client import BaseClient
from data.config import Config


class ChallengeClient(BaseClient):
    """Client for interacting with Challenge API endpoints."""

    def __init__(self, base_url: str = Config.BASE_API_URL,
                 access_token: str | None = None) -> None:
        """Initialize ChallengeClient with base URL and session."""
        super().__init__(base_url=base_url, access_token=access_token)

    @allure.step("Get all challenges")
    def get_all_challenges(self, active: bool | None = None,) -> requests.Response:
        """Get list of all challenges."""
        params: dict[str, Any] = {"active": active} if active is not None else {}
        return self._request("GET","challenges",params=params)

    @allure.step("Get challenge by ID: {challenge_id}")
    def get_challenge_by_id(self, challenge_id: int,) -> requests.Response:
        """Get challenge details by its ID."""
        return self._request("GET", f"challenge/{challenge_id}")

    @allure.step("Create challenge")
    def create_challenge(self, payload: dict[str, Any]) -> requests.Response:
        """Create a new challenge."""
        return self._request("POST", "challenge", json=payload)

    @allure.step("Update challenge (PUT) ID: {challenge_id}")
    def update_challenge(self, challenge_id: int, payload: dict[str, Any]) -> requests.Response:
        """Update an existing challenge completely (PUT)."""
        return self._request("PUT",  f"challenge/{challenge_id}", json=payload)

    @allure.step("Update challenge preview (PATCH) ID: {challenge_id}")
    def update_challenge_preview(self, challenge_id: int,
                                 payload: dict[str, Any],) -> requests.Response:
        """Update challenge preview data."""
        return self._request("PATCH", f"challenge/{challenge_id}", json=payload)

    @allure.step("Update challenge start date ID: {challenge_id}")
    def update_challenge_start_date(self, challenge_id: int,
                                    payload: dict[str, Any],) -> requests.Response:
        """Update challenge start date."""
        return self._request("PUT", f"challenge/{challenge_id}/start/date",
                             json=payload)

    @allure.step("Clone challenge ID: {challenge_id}")
    def clone_challenge(self, challenge_id: int,) -> requests.Response:
        """Clone an existing challenge."""
        return self._request("PUT", f"challenge/{challenge_id}/clone")

    @allure.step("Archive challenge ID: {challenge_id}")
    def delete_challenge(self, challenge_id: int,) -> requests.Response:
        """Archive/delete a challenge by ID."""
        return self._request("DELETE", f"challenge/{challenge_id}")

    def get_free_sort_number(self) -> int:
        """Return the first available sort number."""
        response = self.get_all_challenges()
        response.raise_for_status()

        challenges = response.json()

        used_sort_numbers = {
            challenge["sortNumber"]
            for challenge in challenges
        }

        sort_number = 1

        while sort_number in used_sort_numbers:
            sort_number += 1

        return sort_number
