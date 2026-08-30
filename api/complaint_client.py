"""API client for the complaint endpoints of the Speak Ukrainian API.

The client covers the ``/complaint`` and ``/complaints`` endpoints documented
in issue #284. The list/detail read endpoints are publicly accessible without
authentication. The write (``POST``/``PUT``) and maintenance (``DELETE``)
operations require an ``access_token`` (Spring Security rejects anonymous
callers with 401).
"""

from __future__ import annotations

from typing import Any

import requests

from api.base_client import BaseClient

COMPLAINTS_ENDPOINT = "complaints"
COMPLAINT_ENDPOINT = "complaint"


class ComplaintClient(BaseClient):
    """Client for the complaint endpoints of the Speak Ukrainian API.

    The public read endpoints (list, list-by-club, list-by-recipient,
    list-by-sender, get-by-id) require no token. The write/maintenance
    endpoints (create, update, update-answer, update-is-active, delete)
    require an ``access_token``.
    """

    def get_complaints(self, **kwargs: Any) -> requests.Response:
        """Return the full list of complaints.

        Args:
            **kwargs: Extra keyword arguments forwarded to the HTTP request
                (for example ``params`` or ``timeout``).

        Returns:
            The raw HTTP response containing a JSON list of complaints.
        """
        return self._request("GET", COMPLAINTS_ENDPOINT, **kwargs)

    def get_complaints_by_club(self, club_id: int, **kwargs: Any) -> requests.Response:
        """Return all complaints filed against a given club.

        Args:
            club_id: Numeric id of the club whose complaints should be listed.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing a JSON list of complaints.
        """
        return self._request("GET", f"{COMPLAINTS_ENDPOINT}/club/{club_id}", **kwargs)

    def get_complaints_by_recipient(self, recipient_id: int, **kwargs: Any) -> requests.Response:
        """Return all complaints addressed to a given recipient user.

        Args:
            recipient_id: Numeric id of the recipient user.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing a JSON list of complaints.
        """
        return self._request("GET", f"{COMPLAINTS_ENDPOINT}/recipient/{recipient_id}", **kwargs)

    def get_complaints_by_sender(self, sender_id: int, **kwargs: Any) -> requests.Response:
        """Return all complaints filed by a given sender user.

        Args:
            sender_id: Numeric id of the sender user.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing a JSON list of complaints.
        """
        return self._request("GET", f"{COMPLAINTS_ENDPOINT}/sender/{sender_id}", **kwargs)

    def get_complaint(self, complaint_id: int, **kwargs: Any) -> requests.Response:
        """Return a single complaint by its numeric ID.

        Args:
            complaint_id: The ID of the complaint to fetch.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response. A missing complaint yields 404.
        """
        return self._request("GET", f"{COMPLAINT_ENDPOINT}/{complaint_id}", **kwargs)

    def create_complaint(self, payload: dict[str, Any], **kwargs: Any) -> requests.Response:
        """Create a new complaint (authenticated).

        Args:
            payload: JSON body describing the complaint.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request("POST", COMPLAINT_ENDPOINT, json=payload, **kwargs)

    def update_complaint(
        self, complaint_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Fully update an existing complaint (authenticated).

        Args:
            complaint_id: The ID of the complaint to replace.
            payload: The JSON body with the new complaint data.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request("PUT", f"{COMPLAINT_ENDPOINT}/{complaint_id}", json=payload, **kwargs)

    def update_complaint_answer(
        self, complaint_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Attach an answer text to an existing complaint (authenticated).

        Args:
            complaint_id: The ID of the complaint to answer.
            payload: The JSON body with the new ``answerText``.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request(
            "PUT",
            f"{COMPLAINT_ENDPOINT}/{complaint_id}/answer",
            json=payload,
            **kwargs,
        )

    def update_complaint_is_active(
        self, complaint_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Flip the ``isActive`` flag of an existing complaint (authenticated).

        Args:
            complaint_id: The ID of the complaint to update.
            payload: The JSON body with the new ``isActive`` boolean.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request(
            "PUT",
            f"{COMPLAINT_ENDPOINT}/isActive/{complaint_id}",
            json=payload,
            **kwargs,
        )

    def delete_complaint(self, complaint_id: int, **kwargs: Any) -> requests.Response:
        """Delete a complaint by its ID (authenticated).

        Args:
            complaint_id: The ID of the complaint to delete.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response. Anonymous callers receive 401.
        """
        return self._request("DELETE", f"{COMPLAINT_ENDPOINT}/{complaint_id}", **kwargs)
