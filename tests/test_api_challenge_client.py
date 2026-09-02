"""Comprehensive integration test suite for Challenge API endpoints."""

import json
from collections.abc import Callable
from typing import Any

import allure
import pytest

from api.challenge_client import ChallengeClient
from api.models.challenge_response import ChallengeResponse
from data.config import Config

CREATE_PAYLOAD_PATH = "data/assets/challenge_create_payload.json"
CHALLENGE_ID = 15


@allure.feature("Challenge API - Lifecycle & CRUD")
class TestChallengeApi:
    """Test suite covering Challenge API endpoints."""

    @staticmethod
    def get_client(authorized_client: Callable[..., ChallengeClient], role: str,) -> ChallengeClient:
        """Return ChallengeClient for the required role."""
        if role == "unauthorized":
            return ChallengeClient(
                base_url=Config.BASE_API_URL,
            )

        return authorized_client(
            ChallengeClient,
            role=role,
        )

    @pytest.mark.parametrize(
        "role, active_status, expected_status, expected_message",
        [
            ("admin", None, 200, None),
            ("manager", None, 200, None),
            ("user", None, 200, None),
            ("unauthorized", None, 200, None),
        ],
    )
    @allure.story("1. Get All Challenges")
    @allure.title("Verify get_all_challenges method")
    @allure.label("owner", "Svitlana Kovalova")
    def test_get_all_challenges(self, authorized_client: Any, role: str, active_status: bool | None,
                                expected_status: int, expected_message: str | None, ) -> None:
        """Verify getting all challenges for all roles."""
        client = self.get_client(authorized_client, role)

        with allure.step(f"Step 1: Get all challenges as {role}"):
            response = client.get_all_challenges(active=active_status)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()

            if expected_status == 200:
                assert isinstance(body, list)
            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, challenge_id, expected_status, expected_message",
        [
            ("admin", 2, 200, None),
            ("admin", 99, 404, "Challenge not found by id: 99"),
            ("manager", 2, 200, None),
            ("manager", 99, 404, "Challenge not found by id: 99"),
            ("user", 2, 200, None),
            ("user", 99, 404, "Challenge not found by id: 99"),
            ("unauthorized", 2, 200, None),
            ("unauthorized", 99, 404, "Challenge not found by id: 99"),
        ],
    )
    @allure.story("2. Get Challenge by ID")
    @allure.title("Verify get_challenge_by_id method")
    @allure.label("owner", "Svitlana Kovalova")
    def test_get_challenge_by_id(self, authorized_client: Any, role: str, challenge_id: int,
                                 expected_status: int, expected_message: str | None,) -> None:
        """Verify getting a challenge by ID."""
        client = self.get_client(authorized_client, role)

        with allure.step(
            f"Step 1: Call get_challenge_by_id for ID {challenge_id}"
        ):
            response = client.get_challenge_by_id(challenge_id)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()

            if expected_status == 200:
                assert body.get("id") == challenge_id
            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 200, None),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("3. Create Challenge")
    @allure.title("Verify create_challenge for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_create_challenge(self, authorized_client: Any, role: str, expected_status: int,
                              expected_message: str | None,) -> None:
        """Verify creating a challenge for all roles."""
        client = self.get_client(authorized_client, role)

        with open(CREATE_PAYLOAD_PATH, "r", encoding="utf-8") as file:
            payload = json.load(file)

        if role == "admin":
                payload["sortNumber"] = client.get_free_sort_number()

        with allure.step(
            f"Step 1: Send create challenge request as {role}"
        ):
            response = client.create_challenge(payload)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()

            if expected_status == 200:
                challenge_model = ChallengeResponse(**body)
                assert challenge_model.name == payload["name"]
            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 200, None),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("4. Update Challenge (PUT)")
    @allure.title("Verify update_challenge (PUT) for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_update_challenge_put(self, authorized_client: Any, role: str, expected_status: int,
                                  expected_message: str | None,) -> None:
        """Verify updating a challenge using PUT."""
        client = self.get_client(authorized_client, role)

        with open(CREATE_PAYLOAD_PATH, "r", encoding="utf-8") as file:
            payload = json.load(file)

        payload["name"] = "Оновлений історичний челендж"
        payload["isActive"] = True

        with allure.step(f"Step 1: Send PUT request as {role}"):
            response = client.update_challenge(
                challenge_id=CHALLENGE_ID,
                payload=payload,
            )

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()

            if expected_status == 200:
                challenge_model = ChallengeResponse(**body)
                assert challenge_model.name == "Оновлений історичний челендж"
            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 200, None),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("5. Update Challenge Preview (PATCH)")
    @allure.title("Verify update_challenge_preview for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_update_challenge_patch(self, authorized_client: Any, role: str, expected_status: int,
                                    expected_message: str | None,) -> None:
        """Verify updating challenge preview using PATCH."""
        client = self.get_client(authorized_client, role)

        patch_payload = {
            "name": "Оновлений історичний челендж",
            "title": "Змінена назва олімпіади",
            "sortNumber": 101,
        }

        with allure.step(f"Step 1: Send PATCH request as {role}"):
            response = client.update_challenge_preview(
                challenge_id=CHALLENGE_ID,
                payload=patch_payload,
            )
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json()

            if expected_status == 200:
                assert body["name"] == "Оновлений історичний челендж"
                assert body["title"] == "Змінена назва олімпіади"
                assert body["sortNumber"] == 101
            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 200, None),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("6. Update Challenge Start Date")
    @allure.title("Verify update_challenge_start_date for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_update_challenge_start_date(self, authorized_client: Any, role: str, expected_status: int,
                                         expected_message: str | None,) -> None:
        """Verify updating challenge start date."""

        client = self.get_client(authorized_client, role)

        date_payload = {
            "startDate": "2026-09-10",
        }

        with allure.step(
                f"Step 1: Send start date update request as {role}"
        ):
            response = client.update_challenge_start_date(
                challenge_id=CHALLENGE_ID,
                payload=date_payload,
            )

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json() if response.content else {}

            if expected_status == 200:
                assert isinstance(body, list)
                assert body, "Expected at least one task in response"

                for task in body:
                    assert task["challengeId"] == CHALLENGE_ID
                    assert task["startDate"] == [2026, 9, 10]

            else:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 200, None),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("7. Clone Challenge")
    @allure.title("Verify clone_challenge for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_clone_challenge(self, authorized_client: Any, role: str, expected_status: int,
                             expected_message: str | None,) -> None:
        """Verify cloning a challenge."""
        client = self.get_client(authorized_client, role)

        with allure.step(f"Step 1: Send clone request as {role}"):
            response = client.clone_challenge(challenge_id=CHALLENGE_ID)

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json() if response.content else {}

            if expected_status != 200:
                assert body.get("message") == expected_message

    @pytest.mark.parametrize(
        "role, expected_status, expected_message",
        [
            ("admin", 404, "Challenge not found by id: 99"),
            ("manager", 403, "You have no necessary permissions (role)"),
            ("user", 403, "You have no necessary permissions (role)"),
            ("unauthorized", 401, "You are not authenticated"),
        ],
    )
    @allure.story("8. Delete / Archive Challenge")
    @allure.title("Verify delete_challenge for role: {role}")
    @allure.label("owner", "Svitlana Kovalova")
    def test_delete_challenge(
            self,
            authorized_client: Any,
            role: str,
            expected_status: int,
            expected_message: str | None,
    ) -> None:
        """Verify deleting/archiving a challenge."""

        client = self.get_client(authorized_client, role)

        with allure.step(
                f"Step 1: Send delete/archive request as {role} for ID 99"
        ):
            response = client.delete_challenge(
                challenge_id=99,
            )

        with allure.step(f"Step 2: Verify status code is {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("Step 3: Verify response data or error message"):
            body = response.json() if response.content else {}

            if expected_status != 200:
                assert body.get("message") == expected_message
