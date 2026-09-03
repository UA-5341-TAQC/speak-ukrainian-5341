"""API client for the Challenge Registration resource."""

from __future__ import annotations

from requests import Response

from api.base_client import BaseClient


class ChallengeRegistrationClient(BaseClient):
    """Client for interacting with the /api/challenge-registration endpoints."""

    def get_unapproved_for_manager(self, manager_id: int) -> Response:
        """Get unapproved registrations for a manager."""
        return self._request("GET", f"challenge-registration/unapproved/{manager_id}")

    def get_user_applications(self, user_id: int) -> Response:
        """Get all applications submitted by a user."""
        return self._request("GET", f"challenge-registration/user-applications/{user_id}")

    def get_user_children(self, challenge_id: int) -> Response:
        """Get children registered by the user for a challenge."""
        return self._request("GET", f"challenge-registration/user-children/{challenge_id}")

    def get_registration(self, challenge_id: int, user_id: int) -> Response:
        """Get a specific registration for a challenge and user."""
        return self._request("GET", f"challenge-registration/{challenge_id}/{user_id}")

    def get_registrations_for_manager(self, manager_id: int) -> Response:
        """Get all registrations for a manager."""
        return self._request("GET", f"challenge-registration/{manager_id}")

    def approve_registration(self, registration_id: int) -> Response:
        """Approve a challenge registration."""
        return self._request("PATCH", f"challenge-registration/approve/{registration_id}")

    def cancel_registration(self, registration_id: int) -> Response:
        """Cancel a challenge registration."""
        return self._request("PATCH", f"challenge-registration/cancel/{registration_id}")

    def create_registration(self, payload: dict[str, str | int | float | bool]) -> Response:
        """Create a new challenge registration."""
        return self._request("POST", "challenge-registration", json=payload)

    def create_registration_for_children(
        self, payload: dict[str, str | int | float | bool]
    ) -> Response:
        """Create a challenge registration for children."""
        return self._request("POST", "challenge-registration/children", json=payload)
