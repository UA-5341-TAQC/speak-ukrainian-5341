"""Base smoke tests for the location API endpoints.

Covers every address controller endpoint listed in issue #282:

- GET /api/getAllBadAddress
- POST /api/replaceIncorrectCity
"""

from __future__ import annotations

from typing import Any, cast
import pytest

import allure

from api.address_controller import AddressControllerClient


class TestAddressControllerSeс:

    @allure.title(
        "ADDRESS-CONTROL-API-01: GET /getAllBadAddress returns 401 for unauthenticated users")
    def test_get_all_bad_addresses(
        self, addres_control_api:AddressControllerClient
    ) -> None:
        """Verify Role-Based Access Control: Guests cannot create categories."""
        response = addres_control_api.get_all_bad_address()

        with allure.step("Verify response is 401 Unauthorized"):
            assert (
                response.status_code == 401
            ), f"Expected 401 Unauthorized, got {response.status_code}"
            assert (
                response.json().get("status") == 401
            ), "Expected status 401 in error body"

    @allure.title(
        "ADDRESS-CONTROL-API-02: POST /replaceIncorrectCity returns 401 for unauthenticated users"
    )
    def test_update_location_unauthorized(
        self, addres_control_api:AddressControllerClient
    ) -> None:
        """Verify that guests cannot update locations."""
        response = addres_control_api.replace_incorrect_city()

        with allure.step("Verify POST response is 401 Unauthorized"):
            assert (
                response.status_code == 401
            ), f"Expected 401, got {response.status_code}"

