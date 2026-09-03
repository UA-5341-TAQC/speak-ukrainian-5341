"""API tests for PATCH endpoints of /api/challenge-registration."""

import allure

from api.challenge_registration_client import ChallengeRegistrationClient
from api.models.challenge_registration_create_dto import ChallengeRegistrationCreateDto
from api.schemas.validator import assert_response_matches

pytestmark = allure.feature("Challenge Registration")

EXPECTED_CHALLENGE_ID = 13


@allure.title("Approve a pending registration")
def test_approve_registration(
    challenge_registration_api_user: tuple[ChallengeRegistrationClient, str],
    challenge_registration_api_manager: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify PATCH /challenge-registration/approve/{id} marks the registration as approved."""
    user_client, user_id = challenge_registration_api_user
    manager_client, _ = challenge_registration_api_manager

    payload = ChallengeRegistrationCreateDto(userId=str(int(user_id)), challengeId=EXPECTED_CHALLENGE_ID)

    with allure.step("Create the registration to be approved"):
        create_response = user_client.create_registration(payload.model_dump())
        assert create_response.status_code == 201
        registration_id: int = create_response.json()["id"]

    try:
        with allure.step("Approve the registration as manager"):
            response = manager_client.approve_registration(registration_id)
            assert response.status_code == 200

        with allure.step("Validate the response against the stored schema"):
            body = response.json()
            assert_response_matches(
                body,
                "challenge-registration/challenge_registration_approve_response",
                name="PATCH /challenge-registration/approve/{id} response",
            )

        with allure.step("Verify the registration is now approved"):
            assert body["id"] == registration_id
            assert body["approved"] is True
    finally:
        with allure.step("Clean up: cancel the created registration"):
            user_client.cancel_registration(registration_id)


@allure.title("Cancel an active registration")
def test_cancel_registration(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify PATCH /challenge-registration/cancel/{id} marks the registration as inactive."""
    user_client, user_id = challenge_registration_api_user

    payload = ChallengeRegistrationCreateDto(userId=str(int(user_id)), challengeId=EXPECTED_CHALLENGE_ID)

    with allure.step("Create the registration to be cancelled"):
        create_response = user_client.create_registration(payload.model_dump())
        assert create_response.status_code == 201
        registration_id = create_response.json()["id"]

    with allure.step("Cancel the registration"):
        response = user_client.cancel_registration(registration_id)
        assert response.status_code == 200

    with allure.step("Validate the response against the stored schema"):
        body = response.json()
        assert_response_matches(
            body,
            "challenge-registration/challenge_registration_cancel_response",
            name="PATCH /challenge-registration/cancel/{id} response",
        )

    with allure.step("Verify the registration is now inactive"):
        assert body["id"] == registration_id
        assert body["active"] is False