import allure
from jsonschema import validate

from api.login_client import LoginClient
from data.config import Config

LOGIN_SUCCESS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string"},
        "roleName": {"type": "string"},
        "accessToken": {"type": "string"},
        "refreshToken": {"type": "string"},
    },
    "required": [
        "id",
        "email",
        "roleName",
        "accessToken",
        "refreshToken",
    ],
}

LOGIN_ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "integer"},
        "message": {"type": "string"},
    },
    "required": [
        "status",
        "message",
    ],
}

@allure.feature("API")
@allure.story("Login")
@allure.title("Successful user login")
def test_successful_login():
    """Verify successful login with valid user credentials."""
    client = LoginClient()

    with allure.step("Sign in with valid credentials"):
        response = client.sign_in(
            Config.DEV_USER_EMAIL,
            Config.DEV_USER_PASSWORD,
        )

    with allure.step("Verify successful login response"):
        assert response.status_code == 200

        data = response.json()
        validate(instance=data, schema=LOGIN_SUCCESS_RESPONSE_SCHEMA)

        assert data["email"] == Config.DEV_USER_EMAIL
        assert data["roleName"] 
        assert data["accessToken"]
        assert data["refreshToken"]


@allure.feature("API")
@allure.story("Login")
@allure.title("Login with wrong password")
def test_login_with_wrong_password():
    """Verify login fails when the user provides a wrong password."""
    client = LoginClient()

    with allure.step("Sign in with wrong password"):
        response = client.sign_in(
            Config.DEV_USER_EMAIL,
            "wrong_password",
        )

    with allure.step("Verify unauthorized response"):
        assert response.status_code == 401

        data = response.json()
        validate(instance=data, schema=LOGIN_ERROR_RESPONSE_SCHEMA)

        assert data["status"] == 401
        assert data["message"] == "Wrong password"
