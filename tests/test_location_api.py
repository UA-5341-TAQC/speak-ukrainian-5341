"""Base smoke tests for the location API endpoints.

Covers every location endpoint listed in issue #282:

- DELETE /api/location/{id}
- GET /api/location/{id}
- GET /api/locations
- POST /api/location
- PUT /api/location/{id}
"""
from __future__ import annotations

from typing import Any, cast
import pytest

import allure

from api.location_client import LocationClient

@pytest.fixture
def existing_location(location_api:LocationClient) -> dict[str, Any]:
    """Fixture that fetches and returns a real location dictionary from the database."""
    locations = location_api.get_locations_list().json()
    assert len(locations) > 0, "No locations available to test"
    return cast(dict[str, Any], locations[0])

DUMMY_LOCATION_PAYLOAD = {
    "id": 0,
    "name": "string",
    "address": "string",
    "cityName": "string",
    "districtName": "string",
    "stationName": "string",
    "cityId": 0,
    "districtId": 0,
    "stationId": 0,
    "centerId": 0,
    "clubId": 0,
    "coordinates": "string",
    "longitude": 0,
    "latitude": 0,
    "phone": "0057751478"
}

class TestLocationRead:
    
    @allure.title("Location-API-01: GET /locations returns 200 OK and valid JSON list")
    def test_return_locations_list(self, location_api:LocationClient) -> None:
        """The public location list must return a 200 response with a JSON list."""

        response = location_api.get_locations_list()

        with allure.step("Verify response is 200 OK"):
            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}"

        with allure.step("Verify response is a valid list of locations"):
            locations = response.json()
            assert isinstance(locations, list), "Expected a JSON list"
            assert len(locations) > 0, "Expected at least one location to be returned"
            assert "id" in locations[0], "Location object missing 'id'"
            assert "name" in locations[0], "Location object missing 'name'"


    @allure.title(
        "Location-API-02: GET /location/{id} returns 200 OK for an existing location"
    )
    def test_get_location_by_id(
        self, location_api:LocationClient, existing_location: dict[str, Any]
    ) -> None:
        """Verify that a specific location can be fetched by its ID."""
        target_id = existing_location["id"]
        expected_name = existing_location["name"]

        response = location_api.get_location(target_id)

        with allure.step("Verify response is 200 OK and data matches"):
            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}"
            location = response.json()
            assert (
                location["id"] == target_id
            ), "Returned ID does not match requested ID"
            assert location["name"] == expected_name, "Location name mismatch"


class TestLocationSeс:

    @allure.title(
        "Location-API-03: POST /location returns 401 for unauthenticated users")
    def test_create_location_unauthorized(
        self, location_api:LocationClient
    ) -> None:
        """Verify Role-Based Access Control: Guests cannot create locations."""
        response = location_api.create_location(payload=DUMMY_LOCATION_PAYLOAD)

        with allure.step("Verify response is 401 Unauthorized"):
            assert (
                response.status_code == 401
            ), f"Expected 401 Unauthorized, got {response.status_code}"
            assert (
                response.json().get("status") == 401
            ), "Expected status 401 in error body"

    @allure.title(
        "Location-API-04: PUT /location/{id} returns 401 for unauthenticated users"
    )
    def test_update_location_unauthorized(
        self, location_api: LocationClient, existing_location: dict[str, Any]
    ) -> None:
        """Verify that guests cannot update locations."""
        response = location_api.update_location(
            existing_location["id"], payload=DUMMY_LOCATION_PAYLOAD
        )

        with allure.step("Verify PUT response is 401 Unauthorized"):
            assert (
                response.status_code == 401
            ), f"Expected 401, got {response.status_code}"

    @allure.title(
        "Location-API-06: DELETE /location/{id} returns 401 for unauthenticated users"
    )
    def test_delete_category_unauthorized(
        self, location_api: LocationClient, existing_location: dict[str, Any]
    ) -> None:
        """Verify that guests cannot delete location."""
        with allure.step(
            "Send DELETE request to /location/{id} without authentication"
        ):
            response = location_api.delete_location(existing_location["id"])

        with allure.step("Verify DELETE response is 401 Unauthorized"):
            assert (
                response.status_code == 401
            ), f"Expected 401, got {response.status_code}"
