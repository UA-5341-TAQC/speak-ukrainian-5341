"""API tests for POST /api/challenge-registration."""

import allure

from api.challenge_registration_client import ChallengeRegistrationClient

pytestmark = allure.feature("Challenge Registration")

REGISTERED_CHALLENGE_ID_FOR_USER = 2
REGISTERED_CHALLENGE_ID_FOR_CHILD = 1
EXPECTED_CHILD_ID = 4


@allure.title("Create a challenge registration for a user")
def test_create_registration_for_user(user_client: ChallengeRegistrationClient, user_id: int) -> None:
    """Verify POST /challenge-registration creates a new registration for the user."""
    payload = {"userId": str(user_id), "challengeId": REGISTERED_CHALLENGE_ID_FOR_USER, "comment": " "}
    registration_id: int | None = None
    response = user_client.create_registration(payload)

    try:
        with allure.step("Verify the user's registration was created correctly"):
            assert response.status_code == 201

            registration = response.json()

            assert "id" in registration
            registration_id = registration["id"]

            assert registration["userId"] == user_id
            assert registration["challengeId"] == REGISTERED_CHALLENGE_ID_FOR_USER
            assert registration["active"] is True
            assert registration["approved"] is False
    finally:
        if registration_id is not None:
            with allure.step("Clean up: cancel the created user's registration"):
                user_client.cancel_registration(registration_id)


@allure.title("Create a challenge registration for a child")
def test_create_registration_for_child(user_client: ChallengeRegistrationClient) -> None:
    """Verify POST /challenge-registration/children creates a new registration for a child."""
    payload = {"childIds": [EXPECTED_CHILD_ID], "challengeId": REGISTERED_CHALLENGE_ID_FOR_CHILD, "comment": " "}
    registration_id: int | None = None
    response = user_client.create_registration_for_children(payload)

    try:
        with allure.step("Verify the child's registration was created correctly"):
            assert response.status_code == 201
            registrations = response.json()

            assert isinstance(registrations, list)
            assert registrations

            expected_registration: dict | None = next((registration for registration in registrations if registration["childId"] == EXPECTED_CHILD_ID), None)
            assert expected_registration is not None, f"Registration for childId={EXPECTED_CHILD_ID} not found: {registrations}"

            registration_id = expected_registration["id"]

            assert expected_registration["challengeId"] == REGISTERED_CHALLENGE_ID_FOR_CHILD
            assert expected_registration["active"] is True
            assert expected_registration["approved"] is False
    finally:
        if registration_id is not None:
            with allure.step("Clean up: cancel the created child's registration"):
                user_client.cancel_registration(registration_id)