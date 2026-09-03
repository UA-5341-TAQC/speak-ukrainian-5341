"""Integration test suite for Club Registration API endpoints."""

import allure
import pytest

from api.models.club_registration_dto import ChildDto, ClubApplicationDto
from api.models.club_registration_payloads import ClubRegistrationResponseDto
from fixtures.api_clients import ApiUserCredentials, ClubRegistrationClient


@allure.feature("Club Registration API")
class TestClubRegistrationApi:
    """Test suite for club registration user-applications endpoint."""

    @pytest.fixture(autouse=True)
    def setup(self, club_registration_client: ClubRegistrationClient,
              user_api_credentials: ApiUserCredentials) -> None:
        """Inject authorized client and user_id from login response."""
        self.client = club_registration_client
        self.user_id = user_api_credentials.user_id

    @allure.story("Get User Applications")
    @allure.title("Verify get_user_applications returns 200 and valid list")
    @allure.label("owner")
    def test_get_user_applications_success(self) -> None:
        with allure.step(f"Step 1: Call GET /user-applications/{self.user_id}"):
            response = self.client.get_user_applications(self.user_id)

        with allure.step("Step 2: Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Step 3: Parse and validate response body"):
            data = response.json()
            applications = [ClubApplicationDto(**item) for item in data]
            assert len(applications) > 0

        with allure.step("Step 4: Validate common fields"):
            for app in applications:
                assert app.id > 0
                assert app.club.id > 0
                assert app.club.name
                assert app.registrationDate
                assert isinstance(app.active, bool)
                assert isinstance(app.approved, bool)

        with allure.step("Step 5: Validate application with child (user=null)"):
            child_apps = [a for a in applications if a.child is not None]
            assert len(child_apps) > 0
            app = child_apps[0]
            assert app.user is None
            assert app.child is not None
            assert app.child.id > 0
            assert app.child.firstName
            assert app.child.parent is not None
            assert app.child.parent.id == self.user_id
            assert app.child.gender.value in ("MALE", "FEMALE")

        with allure.step("Step 6: Validate application with user (child=null)"):
            user_apps = [a for a in applications if a.user is not None]
            assert len(user_apps) > 0
            app = user_apps[0]
            assert app.child is None
            assert app.user is not None
            assert app.user.id == self.user_id
            assert app.user.email

    @allure.story("Get User Applications — Schema Validation")
    @allure.title("Verify response schema matches ClubApplicationDto")
    @allure.label("owner")
    def test_get_user_applications_schema_validation(self) -> None:
        with allure.step(f"Step 1: Fetch applications for user {self.user_id}"):
            response = self.client.get_user_applications(self.user_id)
            assert response.status_code == 200

        with allure.step("Step 2: Validate each item against ClubApplicationDto"):
            for item in response.json():
                model = ClubApplicationDto(**item)
                assert model.id is not None
                assert model.club is not None

    @allure.story("Get User Children by Club")
    @allure.title("Verify get_user_children returns 200 and valid child list")
    @allure.label("owner")
    def test_get_user_children_success(self) -> None:
        """Test retrieving children registered for an existing club."""
        club_id = 26

        with allure.step(f"Step 1: Call GET /user-children/{club_id}"):
            response = self.client.get_user_children(club_id)

        with allure.step("Step 2: Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Step 3: Parse and validate response body"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

        with allure.step("Step 4: Validate child schema and fields"):
            children = [ChildDto(**item) for item in data]
            child = children[0]
            assert child.id > 0
            assert child.firstName
            assert child.lastName
            assert child.age >= 0
            assert child.gender.id > 0
            assert child.gender.value in ("MALE", "FEMALE")
            assert isinstance(child.disabled, bool)

        with allure.step("Step 5: Validate parent nested object"):
            assert child.parent is not None
            assert child.parent.id > 0
            assert child.parent.firstName
            assert child.parent.email

    @allure.story("Get User Children by Club — Schema Validation")
    @allure.title("Verify every child matches ChildDto schema")
    @allure.label("owner")
    def test_get_user_children_schema_validation(self) -> None:
        """Test strict Pydantic validation for all children in response."""
        club_id = 26

        with allure.step(f"Step 1: Fetch children for club {club_id}"):
            response = self.client.get_user_children(club_id)
            assert response.status_code == 200

        with allure.step("Step 2: Validate each item against ChildDto"):
            for item in response.json():
                model = ChildDto(**item)
                assert model.id is not None
                assert model.parent is not None

    @allure.story("Check Registration Status")
    @allure.title("Verify existing registration returns true")
    @allure.label("owner")
    def test_get_registration_status_true(self) -> None:
        """Test that registered user+club pair returns true."""
        club_id = 26

        with allure.step(f"Step 1: Call GET /club-registration/{club_id}/{self.user_id}"):
            response = self.client.get_registration_status(club_id, self.user_id)

        with allure.step("Step 2: Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Step 3: Verify response body is true"):
            data = response.json()
            assert isinstance(data, bool)
            assert data is True

    @allure.story("Check Registration Status — Edge Cases")
    @allure.title("Verify non-registered pair returns false")
    @allure.label("owner")
    def test_get_registration_status_false(self) -> None:
        """Test that non-existing registration returns false."""
        club_id = 999
        user_id = 99999

        with allure.step(f"Step 1: Call GET /club-registration/{club_id}/{user_id}"):
            response = self.client.get_registration_status(club_id, user_id)

        with allure.step("Step 2: Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Step 3: Verify response body is false"):
            data = response.json()
            assert isinstance(data, bool)
            assert data is False

    @allure.story("Register for Club")
    @allure.title("Verify register_for_club returns 201 and valid response")
    @allure.label("owner")
    def test_register_for_club_success(self) -> None:
        """Test successful registration of a single child for a club."""
        payload = {
            "childIds": [13],
            "clubId": 26,
            "comment": "Test registration via API",
        }

        with allure.step("Step 1: Send POST /club-registration"):
            response = self.client.register_for_club(payload)

        with allure.step("Step 2: Verify status code is 201"):
            assert response.status_code == 201

        with allure.step("Step 3: Parse and validate response body"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1

        with allure.step("Step 4: Validate registration fields"):
            reg = ClubRegistrationResponseDto(**data[0])
            assert reg.id > 0
            assert reg.childId == 13
            assert reg.clubId == 26
            assert reg.comment == "Test registration via API"
            assert reg.active is True
            assert reg.approved is False
            assert reg.registrationDate

    @allure.story("Register for Club — Negative")
    @allure.title("Verify non-existent child returns 404")
    @allure.label("owner")
    def test_register_for_club_child_not_found(self) -> None:
        """Test that registration with non-existent childId returns 404."""
        payload = {
            "childIds": [99999],
            "clubId": 26,
            "comment": "Should fail",
        }

        with allure.step("Step 1: Send POST with invalid childId"):
            response = self.client.register_for_club(payload)

        with allure.step("Step 2: Verify status code is 404"):
            assert response.status_code == 404

        with allure.step("Step 3: Verify error message"):
            body = response.json()
            assert "Child has not found" in body.get("message", "")

    @allure.story("Register for Club — Schema Validation")
    @allure.title("Verify response schema matches ClubRegistrationResponseDto")
    @allure.label("owner")
    def test_register_for_club_schema_validation(self) -> None:
        """Test strict Pydantic validation for registration response."""
        payload = {
            "childIds": [13],
            "clubId": 26,
            "comment": "Schema validation test",
        }

        with allure.step("Step 1: Create registration"):
            response = self.client.register_for_club(payload)
            assert response.status_code == 201

        with allure.step("Step 2: Validate against ClubRegistrationResponseDto"):
            for item in response.json():
                model = ClubRegistrationResponseDto(**item)
                assert model.id is not None
                assert model.childId > 0
                assert model.clubId > 0
                assert isinstance(model.active, bool)
                assert isinstance(model.approved, bool)

    @allure.story("Register User for Club")
    @allure.title("Verify register_user_for_club returns 201 and valid response")
    @allure.label("owner")
    def test_register_user_for_club_success(self) -> None:
        """Test successful registration of a user (adult) for a club."""
        from api.models.club_registration_payloads import (
            ClubUserRegistrationPayload,
            ClubUserRegistrationResponseDto,
        )

        payload = ClubUserRegistrationPayload(
            userId=self.user_id,
            clubId=26,
            comment="Test user registration via API",
        ).model_dump()

        with allure.step("Step 1: Send POST /club-registration/user"):
            response = self.client.register_user_for_club(payload)

        with allure.step("Step 2: Verify status code is 201"):
            assert response.status_code == 201

        with allure.step("Step 3: Parse and validate response body"):
            data = response.json()
            assert isinstance(data, dict)

        with allure.step("Step 4: Validate registration fields"):
            reg = ClubUserRegistrationResponseDto(**data)
            assert reg.id > 0
            assert reg.userId == self.user_id
            assert reg.clubId == 26
            assert reg.comment == "Test user registration via API"
            assert reg.active is True
            assert reg.approved is False
            assert reg.registrationDate

    @allure.story("Register User for Club — Schema Validation")
    @allure.title("Verify response schema matches ClubUserRegistrationResponseDto")
    @allure.label("owner")
    def test_register_user_for_club_schema_validation(self) -> None:
        """Test strict Pydantic validation for user registration response."""
        from api.models.club_registration_payloads import ClubUserRegistrationResponseDto

        payload = {
            "userId": self.user_id,
            "clubId": 26,
            "comment": "Schema validation test",
        }

        with allure.step("Step 1: Create user registration"):
            response = self.client.register_user_for_club(payload)

        with allure.step("Step 2: Validate against ClubUserRegistrationResponseDto"):
            data = response.json()
            model = ClubUserRegistrationResponseDto(**data)
            assert model.id is not None
            assert model.userId == self.user_id
            assert model.clubId > 0
            assert isinstance(model.active, bool)
            assert isinstance(model.approved, bool)