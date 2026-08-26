from api.login_client import LoginClient
from data.config import Config

def test_successful_login():
    client = LoginClient()

    response = client.sign_in(
        Config.DEV_USER_EMAIL,
        Config.DEV_USER_PASSWORD,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == Config.DEV_USER_EMAIL
    assert data["roleName"] == "ROLE_USER"
    assert data["accessToken"]
    assert data["refreshToken"]

def test_login_with_wrong_password():
    client = LoginClient()

    response = client.sign_in(
        Config.DEV_USER_EMAIL,
        "wrong_password",
    )

    assert response.status_code == 401

    data = response.json()

    assert data["status"] == 401
    assert data["message"] == "Wrong password"