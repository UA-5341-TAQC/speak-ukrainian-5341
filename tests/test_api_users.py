import allure
from typing import Any
from api.user_client import UserClient


@allure.feature("API")
@allure.story("User")
@allure.title("Successful retrieval of user information by ID")
def test_get_user(auth_data: dict[str, Any])-> None:
    """Verify successful retrieval of user information by ID."""
    client = UserClient(
        access_token=auth_data["accessToken"],
    )

    with allure.step("Get user information"):
        response = client.get_user(
            auth_data["id"],
        )

    with allure.step("Verify successful user information response"):
        assert response.status_code == 200

        data = response.json()

        assert data["id"] == auth_data["id"]


@allure.feature("API")
@allure.story("User")
@allure.title("Regular user cannot get all users")
def test_get_users_as_regular_user(auth_data: dict[str, Any])-> None:
    """Verify regular user cannot get all users."""
    client = UserClient(
        access_token=auth_data["accessToken"],
    )

    with allure.step("Attempt to get all users"):
        response = client.get_users()

    with allure.step("Verify forbidden response"):
        assert response.status_code == 403
