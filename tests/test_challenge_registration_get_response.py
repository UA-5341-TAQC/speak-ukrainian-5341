"""API tests for GET endpoints of /api/challenge-registration."""

import allure

from api.challenge_registration_client import ChallengeRegistrationClient
from api.schemas.validator import assert_response_matches

pytestmark = allure.feature("Challenge Registration")

REGISTERED_CHALLENGE_ID_FOR_USER = 1
REGISTERED_CHALLENGE_ID_FOR_CHILD = 2
EXPECTED_CHILD_ID = 18


@allure.title("Get unapproved registrations for a manager with none pending")
def test_get_unapproved_for_manager_with_no_registrations(challenge_registration_api_manager: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify GET /challenge-registration/unapproved/{managerId} returns an empty list."""
    manager_client, manager_id = challenge_registration_api_manager

    response = manager_client.get_unapproved_for_manager(int(manager_id))
    assert response.status_code == 200
    assert response.json() == []


@allure.title("Get applications submitted by a user with an existing application")
def test_get_user_applications_with_existing_application(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify GET /challenge-registration/user-applications/{userId} returns the submitted application."""
    user_client, user_id = challenge_registration_api_user
    user_id = int(user_id)

    response = user_client.get_user_applications(user_id)
    assert response.status_code == 200

    applications = response.json()
    with allure.step("Validate the response against the stored schema"):
        assert_response_matches(
            applications,
            "challenge-registration/get_user_registration_response",
            name="GET /challenge-registration/user-applications/{userId}",
        )

    application: dict | None = next(
        (app for app in applications if app["challenge"]["id"] == REGISTERED_CHALLENGE_ID_FOR_USER), None
    )
    assert application is not None, f"Application for challenge ID {REGISTERED_CHALLENGE_ID_FOR_USER} was not found"

    assert application["user"]["id"] == user_id
    assert application["active"] is True
    assert application["approved"] is False


@allure.title("Get children registered for a challenge")
def test_get_user_children(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify GET /challenge-registration/user-children/{challengeId} returns the registered child."""
    user_client, user_id = challenge_registration_api_user
    user_id = int(user_id)

    response = user_client.get_user_children(REGISTERED_CHALLENGE_ID_FOR_CHILD)
    assert response.status_code == 200

    children = response.json()
    with allure.step("Validate the response against the stored schema"):
        assert_response_matches(
            children,
            "challenge-registration/get_children_registration_response",
            name="GET /challenge-registration/user-children/{challengeId}",
        )

    expected_child: dict | None = next((child for child in children if child["id"] == EXPECTED_CHILD_ID), None)
    assert expected_child is not None, f"Child with ID {EXPECTED_CHILD_ID} was not found"

    assert expected_child["firstName"] == "Test"
    assert expected_child["lastName"] == "Test"
    assert expected_child["age"] == 3
    assert expected_child["gender"]["value"] == "FEMALE"
    assert expected_child["disabled"] is True
    assert expected_child["parent"]["id"] == user_id


@allure.title("Check registration status for a user registered on a challenge")
def test_is_user_registered_returns_true(challenge_registration_api_user: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify GET /challenge-registration/{challengeId}/{userId} returns true when registered."""
    user_client, user_id = challenge_registration_api_user
    user_id = int(user_id)

    response = user_client.get_registration(REGISTERED_CHALLENGE_ID_FOR_USER, user_id)
    assert response.status_code == 200
    assert response.json() is True


@allure.title("Get all registrations for a manager with none existing")
def test_get_registrations_for_manager_with_no_registrations(challenge_registration_api_manager: tuple[ChallengeRegistrationClient, str]) -> None:
    """Verify GET /challenge-registration/{managerId} returns an empty list."""
    manager_client, manager_id = challenge_registration_api_manager

    response = manager_client.get_registrations_for_manager(int(manager_id))
    assert response.status_code == 200
    assert response.json() == []