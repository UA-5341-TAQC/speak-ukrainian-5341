"""API client for the address controller endpoints of the Speak Ukrainian API.

The client covers the '/getAllBadAddress' and '/replaceIncorrectCity' endpoints documented in
issue #282. Covers 'GET' and 'POST' operations.
"""

from __future__ import annotations

from typing import Any

import requests

from api.base_client import BaseClient

GET_BAD_ADDRESS = "getAllBadAddress"
REPLACE_INCORRECT_CITY = "replaceIncorrectCity"


class AddressControllerClient(BaseClient):
    """Client for the address controller endpoints of the Speak Ukrainian API.

    Read and update operations need an ``access_token`` belonging to a role
    with the necessary permissions (admin).
    """

    def get_all_bad_address(self, **kwargs: Any) -> requests.Response:
        """Return the full list of bad addresses (admin only)."""
        return self._request("GET", GET_BAD_ADDRESS, **kwargs)

    def replace_incorrect_city(self, **kwargs: Any) -> requests.Response:
        """Replace the incorrect city (admin only)."""
        return self._request("POST", REPLACE_INCORRECT_CITY, **kwargs)
