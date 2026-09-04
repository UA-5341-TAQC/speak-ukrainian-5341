"""API client for the location endpoints of the Speak Ukrainian API.

The client covers the '/location' and 'locations' endpoints documented in
issue #282. Public list/detail read endpoints require no authentication, while
the write (``POST``/``PUT``) and maintenance (``DELETE``) operations are
restricted to an authenticated, admin-role account.
"""

from __future__ import annotations

from typing import Any

import requests

from api.base_client import BaseClient

LOCATION_END_POINT = "location"
LOCATIONS_END_POINT = "locations"


class LocationClient(BaseClient):
    """Client for the location endpoints of the Speak Ukrainian API.

    Reads from the public location are available without a token; create,
    update and delete operations need an ``access_token`` belonging to a role
    with the necessary permissions (admin).
    """

    def get_locations_list(self, **kwargs: Any) -> requests.Response:
        """Return the full list of locations."""
        return self._request("GET", LOCATIONS_END_POINT, **kwargs)

    def get_location(self, location_id: int, **kwargs: Any) -> requests.Response:
        """Return single location by its numeric ID."""
        return self._request("GET", f"{LOCATION_END_POINT}/{location_id}", **kwargs)

    def create_location(self, payload: dict[str, Any], **kwargs: Any) -> requests.Response:
        """Create a new news article (admin only)."""
        return self._request("POST", LOCATION_END_POINT, json=payload, **kwargs)

    def update_location(
        self, location_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Fully update an existing location (admin only)."""
        return self._request("PUT", f"{LOCATION_END_POINT}/{location_id}", json=payload, **kwargs)

    def delete_location(self, location_id: int, **kwargs: Any) -> requests.Response:
        """Delete a news article by its ID (admin only)."""
        return self._request("DELETE", f"{LOCATION_END_POINT}/{location_id}", **kwargs)
