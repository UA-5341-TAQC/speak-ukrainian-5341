"""Comprehensive integration test suite for Challenge API endpoints."""
from typing import Any

import allure
import pytest

from api.challenge_client import ChallengeClient


@allure.feature("Challenge API - Lifecycle & CRUD")
class TestChallengeApi:
    """Test suite covering the complete CRUD lifecycle of Challenge API."""
    create_payload_path = "data/assets/challenge_create_payload.json"

    @pytest.fixture(autouse=True)
    def setup(self, authorized_client: Any) -> None:
        """Initialize authorized Challenge API client."""
        self.challenge_client = authorized_client(ChallengeClient, role="manager")

    @pytest.mark.parametrize(
        "active_status, expected_status",
        [
            (None, 200),
            (True, 200),
            (False, 200),
        ],
    )
    @allure.story("1. Get All Challenges")
    @allure.title("Verify get_all_challenges method")
    @allure.label("owner", "Svitlana Kovalova")
    def test_get_all_challenges(self, active_status: bool | None, expected_status: int) -> None:
        with allure.step("Step 1: Call get_all_challenges method"):
            response = self.challenge_client.get_all_challenges(active=active_status)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response is a list"):
            assert isinstance(response.json(), list)

    @pytest.mark.parametrize(
        "challenge_id, expected_status, expected_message",
        [
            (2, 200, None),
            (99, 404, "Challenge not found by id: 99"),
        ],
    )
    @allure.story("2. Get Challenge by ID")
    @allure.title("Verify get_challenge_by_id method")
    @allure.label("owner", "Svitlana Kovalova")
    def test_get_challenge_by_id(
            self, challenge_id: int, expected_status: int, expected_message: str | None
    ) -> None:
        with allure.step(f"Step 1: Call get_challenge_by_id for ID {challenge_id}"):
            response = self.challenge_client.get_challenge_by_id(challenge_id)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()
            if expected_status == 200:
                assert body.get("id") == challenge_id
            else:
                assert body.get("message") == expected_message
