"""API tests for POST /api/challenge-registration."""

import allure
from typing import Any
from api.challenge_registration_client import ChallengeRegistrationClient
from api.models.challenge_registration_create_dto import ChallengeRegistrationCreateDto
from api.models.challenge_registration_create_for_children_dto import ChallengeRegistrationCreateForChildrenDto
from api.schemas.validator import assert_response_matches

pytestmark = allure.feature("Challenge Registration")

EXPECTED_CHALLENGE_ID = 13
EXPECTED_CHILD_ID = 18


@allure.title("Create a challenge registration for a user")
def test_create_registration_for_user(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify POST /challenge-registration creates a new registration for the user."""
    user_client, raw_user_id = challenge_registration_api_user
    user_id = int(raw_user_id)

    payload = ChallengeRegistrationCreateDto(userId=str(user_id), challengeId=EXPECTED_CHALLENGE_ID)

    registration_id: int | None = None

    response = user_client.create_registration(payload.model_dump())

    try:
        with allure.step("Validate the response against the stored schema"):
            assert response.status_code == 201
            registration = response.json()
            assert_response_matches(
                registration,
                "challenge-registration/challenge_registration_response",
                name="POST /challenge-registration response",
            )

        with allure.step("Verify the registration was created correctly"):
            assert "id" in registration
            registration_id = registration["id"]

            assert registration["userId"] == user_id
            assert registration["challengeId"] == EXPECTED_CHALLENGE_ID
            assert registration["active"] is True
            assert registration["approved"] is False
    finally:
        if registration_id is not None:
            with allure.step("Clean up: cancel the created registration"):
                user_client.cancel_registration(registration_id)


@allure.title("Create a challenge registration for a child")
def test_create_registration_for_child(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify POST /challenge-registration/children creates a new registration for a child."""
    user_client, _ = challenge_registration_api_user

    payload = ChallengeRegistrationCreateForChildrenDto(childIds=[EXPECTED_CHILD_ID], challengeId=EXPECTED_CHALLENGE_ID)

    registration_id: int | None = None

    response = user_client.create_registration_for_children(payload.model_dump())

    try:
        with allure.step("Validate the response against the stored schema"):
            assert response.status_code == 201
            registrations = response.json()
            assert_response_matches(
                registrations,
                "challenge-registration/challenge_registration_for_children_response",
                name="POST /challenge-registration/children response",
            )

        with allure.step("Verify the registration was created correctly"):
            expected_registration: dict[str, Any] | None = next(
                (registration for registration in registrations if registration["childId"] == EXPECTED_CHILD_ID), None
            )
            assert expected_registration is not None, (
                f"Registration for childId={EXPECTED_CHILD_ID} not found: {registrations}"
            )

            registration_id = expected_registration["id"]

            assert expected_registration["challengeId"] == EXPECTED_CHALLENGE_ID
            assert expected_registration["active"] is True
            assert expected_registration["approved"] is False
    finally:
        if registration_id is not None:
            with allure.step("Clean up: cancel the created registration"):
                user_client.cancel_registration(registration_id)