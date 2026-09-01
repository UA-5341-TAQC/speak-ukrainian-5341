"""API tests for GET endpoints of /api/challenge-registration."""

import allure

from api.challenge_registration_client import ChallengeRegistrationClient

pytestmark = allure.feature("Challenge Registration")

REGISTERED_CHALLENGE_ID_FOR_USER = 5
REGISTERED_CHALLENGE_ID_FOR_CHILD = 4
EXPECTED_CHILD_ID = 4


@allure.title("Get unapproved registrations for a manager with none pending")
def test_get_unapproved_for_manager_with_no_registrations(manager_client: ChallengeRegistrationClient, manager_id: int) -> None:
    """Verify GET /challenge-registration/unapproved/{managerId} returns an empty list."""
    response = manager_client.get_unapproved_for_manager(manager_id)
    assert response.status_code == 200
    assert response.json() == []


@allure.title("Get applications submitted by a user with an existing application")
def test_get_user_applications_with_existing_application(user_client: ChallengeRegistrationClient, user_id: int) -> None:
    """Verify GET /challenge-registration/user-applications/{userId} returns the submitted application."""
    response = user_client.get_user_applications(user_id)
    assert response.status_code == 200

    applications = response.json()
    assert isinstance(applications, list)
    assert applications

    application: dict | None = next((app for app in applications if app["challenge"]["id"] == REGISTERED_CHALLENGE_ID_FOR_USER), None)
    assert application is not None, f"Application for challenge ID {REGISTERED_CHALLENGE_ID_FOR_USER} was not found"

    assert application["user"]["id"] == user_id
    assert application["active"] is True
    assert application["approved"] is False


@allure.title("Get children registered for a challenge")
def test_get_user_children(user_client: ChallengeRegistrationClient, user_id: int) -> None:
    """Verify GET /challenge-registration/user-children/{challengeId} returns the registered child."""
    response = user_client.get_user_children(REGISTERED_CHALLENGE_ID_FOR_CHILD)
    assert response.status_code == 200

    children = response.json()
    assert isinstance(children, list)
    assert children

    expected_child: dict | None = next((child for child in children if child["id"] == EXPECTED_CHILD_ID), None)
    assert expected_child is not None, f"Child with ID {EXPECTED_CHILD_ID} was not found"

    assert expected_child["firstName"] == "AAA"
    assert expected_child["lastName"] == "SSS"
    assert expected_child["age"] == 12
    assert expected_child["gender"]["value"] == "FEMALE"
    assert expected_child["disabled"] is True
    assert expected_child["parent"]["id"] == user_id


@allure.title("Check registration status for a user registered on a challenge")
def test_is_user_registered_returns_true(user_client: ChallengeRegistrationClient, user_id: int) -> None:
    """Verify GET /challenge-registration/{challengeId}/{userId} returns true when registered."""
    response = user_client.get_registration(REGISTERED_CHALLENGE_ID_FOR_USER, user_id)
    assert response.status_code == 200
    assert response.json() is True


@allure.title("Get all registrations for a manager with none existing")
def test_get_registrations_for_manager_with_no_registrations(manager_client: ChallengeRegistrationClient, manager_id: int) -> None:
    """Verify GET /challenge-registration/{managerId} returns an empty list."""
    response = manager_client.get_registrations_for_manager(manager_id)
    assert response.status_code == 200
    assert response.json() == []