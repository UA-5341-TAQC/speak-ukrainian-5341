"""Smoke tests for the public ``/version`` API endpoint."""

import allure

from api.version_client import VersionClient
from data.config import Config


@allure.title("API-01: /version returns 200 with backend commit metadata")
@allure.tag("api", "smoke", "version")
def test_version_endpoint_returns_metadata(version_api: VersionClient) -> None:
    """The public version endpoint must return a 200 response with backend commit metadata."""
    with allure.step("Request the public version information"):
        response = version_api._request("GET", "version")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        payload = response.json()

    with allure.step("Verify the version payload contains the expected fields"):
        for field in ("backendCommitNumber", "backendCommitDate", "buildDate"):
            assert field in payload, f"Missing expected field '{field}' in version payload"
        assert payload["backendCommitNumber"], "backendCommitNumber must not be empty"


@allure.title("API-02: /version responds to a plain GET without auth")
@allure.tag("api", "smoke", "version")
def test_version_endpoint_requires_no_auth() -> None:
    """The version endpoint is public and must not require authentication."""
    with allure.step("Send an unauthenticated GET to /version"):
        client = VersionClient(base_url=Config.BASE_API_URL)
        response = client._request("GET", "version")

    with allure.step("Confirm the request succeeds without credentials"):
        assert response.status_code == 200, (
            f"Unauthenticated request should succeed, got {response.status_code}"
        )


@allure.title("API-03: /version uses JSON content type")
@allure.tag("api", "smoke", "version")
def test_version_endpoint_returns_json(version_api: VersionClient) -> None:
    """The version endpoint must serve its payload as JSON."""
    with allure.step("Request the version information and inspect the content type"):
        response = version_api._request("GET", "version")

    with allure.step("Confirm the response is JSON"):
        assert "application/json" in response.headers.get("Content-Type", ""), (
            "Version endpoint must return JSON"
        )
        assert isinstance(
            response.json().get("backendCommitNumber"), str
        ), "backendCommitNumber should be a string"
