import allure
import pytest

from api.categories_client import CategoriesClient
from api.models.category_profile import CategoryProfile
from api.models.category_response import CategoryResponse, PageCategoryResponse


@pytest.fixture(scope="session")
def existing_category(categories_api: CategoriesClient) -> CategoryResponse:
    """Fixture that fetches and returns a real category dictionary from the database."""
    categories = categories_api.get_categories().json()
    assert len(categories) > 0, "No categories available to test"
    return CategoryResponse.model_validate(categories[0])


DUMMY_CATEGORY_PROFILE = CategoryProfile(
    name="Hacker Edit",
    description="test",
    sortby=100,
    urlLogo="logo.png",
    backgroundColor="#000",
    tagBackgroundColor="#000",
    tagTextColor="#fff",
)


FORBIDDEN_ROLES = [
    pytest.param((CategoriesClient, "user"), "User", id="role_user"),
    pytest.param((CategoriesClient, "manager"), "Manager", id="role_manager"),
]


@allure.epic("Categories API")
@allure.feature("Read Categories")
class TestCategoriesRead:
    @allure.title("Category-API-01: GET /categories returns 200 OK and valid JSON list")
    @allure.tag("api", "smoke", "category")
    def test_get_categories_success(self, categories_api: CategoriesClient) -> None:
        """Verify that any user can fetch the list of categories successfully."""
        response = categories_api.get_categories()

        with allure.step("Verify response is 200 OK"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        with allure.step("Verify response is a valid list of categories"):
            categories = response.json()
            assert isinstance(categories, list), "Expected a JSON list"
            assert len(categories) > 0, "Expected at least one category to be returned"

        with allure.step("Validate response against Pydantic schema"):
            [CategoryResponse.model_validate(c) for c in categories]

    @allure.title("Category-API-02: GET /categories/search returns paginated list")
    @allure.tag("api", "smoke", "category")
    def test_search_categories(self, categories_api: CategoriesClient) -> None:
        """Verify that searching categories returns a paginated structure."""
        response = categories_api.search_categories()

        with allure.step("Verify response is 200 OK"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        with allure.step("Validate paginated response against Pydantic schema"):
            PageCategoryResponse.model_validate(response.json())

    @allure.title("Category-API-03: GET /category/{id} returns 200 OK for an existing category")
    @allure.tag("api", "smoke", "category")
    def test_get_category_by_id(
        self, categories_api: CategoriesClient, existing_category: CategoryResponse
    ) -> None:
        """Verify that a specific category can be fetched by its ID."""
        target_id = existing_category.id
        expected_name = existing_category.name

        response = categories_api.get_category_by_id(target_id)

        with allure.step("Verify response is 200 OK"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        with allure.step("Validate response against Pydantic schema"):
            category = CategoryResponse.model_validate(response.json())

        with allure.step("Verify response data matches requested parameters"):
            assert category.id == target_id, "Returned ID does not match requested ID"
            assert category.name == expected_name, "Category name mismatch"


@allure.epic("Categories API")
@allure.feature("Security & RBAC")
class TestCategoriesSecurity:
    @allure.title("Category-API-04: POST /category returns 401 for unauthenticated users")
    @allure.tag("api", "security", "category")
    def test_create_category_unauthorized(self, categories_api: CategoriesClient) -> None:
        """Verify Role-Based Access Control: Guests cannot create categories."""
        payload = DUMMY_CATEGORY_PROFILE.model_dump(exclude_none=True)
        response = categories_api.create_category(payload=payload)

        with allure.step("Verify response is 401 Unauthorized"):
            assert response.status_code == 401, (
                f"Expected 401 Unauthorized, got {response.status_code}"
            )
            assert response.json().get("status") == 401, "Expected status 401 in error body"

    @allure.title("Category-API-05: PUT /category/{id} returns 401 for unauthenticated users")
    @allure.tag("api", "security", "category")
    def test_update_category_unauthorized(
        self, categories_api: CategoriesClient, existing_category: CategoryResponse
    ) -> None:
        """Verify that guests cannot update categories."""
        payload = DUMMY_CATEGORY_PROFILE.model_dump(exclude_none=True)
        response = categories_api.update_category(existing_category.id, payload=payload)

        with allure.step("Verify PUT response is 401 Unauthorized"):
            assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    @allure.title("Category-API-06: DELETE /category/{id} returns 401 for unauthenticated users")
    @allure.tag("api", "security", "category")
    def test_delete_category_unauthorized(
        self, categories_api: CategoriesClient, existing_category: CategoryResponse
    ) -> None:
        """Verify that guests cannot delete categories."""
        with allure.step("Send DELETE request to /category/{id} without authentication"):
            response = categories_api.delete_category(existing_category.id)

        with allure.step("Verify DELETE response is 401 Unauthorized"):
            assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    @allure.title("Category-API-07: POST /category returns 403 Forbidden for {role_name}")
    @allure.tag("api", "security", "category")
    @pytest.mark.parametrize("rbac_client, role_name", FORBIDDEN_ROLES, indirect=["rbac_client"])
    def test_create_category_forbidden_roles(
        self, rbac_client: CategoriesClient, role_name: str
    ) -> None:
        """Verify Role-Based Access Control: Users and Managers get 403 Forbidden."""
        payload = DUMMY_CATEGORY_PROFILE.model_dump(exclude_none=True)
        response = rbac_client.create_category(payload=payload)

        with allure.step("Verify response is 403 Forbidden"):
            assert response.status_code == 403, f"Expected 403, got {response.status_code}"

    @allure.title("Category-API-08: PUT /category/{{id}} returns 403 Forbidden for {role_name}")
    @allure.tag("api", "security", "category")
    @pytest.mark.parametrize("rbac_client, role_name", FORBIDDEN_ROLES, indirect=["rbac_client"])
    def test_update_category_forbidden_roles(
        self,
        rbac_client: CategoriesClient,
        role_name: str,
        existing_category: CategoryResponse,
    ) -> None:
        """Verify Role-Based Access Control: Users and Managers cannot update categories."""
        payload = DUMMY_CATEGORY_PROFILE.model_dump(exclude_none=True)
        response = rbac_client.update_category(existing_category.id, payload=payload)

        with allure.step("Verify response is 403 Forbidden"):
            assert response.status_code == 403, f"Expected 403, got {response.status_code}"

    @allure.title("Category-API-09: DELETE /category/{{id}} returns 403 Forbidden for {role_name}")
    @allure.tag("api", "security", "category")
    @pytest.mark.parametrize("rbac_client, role_name", FORBIDDEN_ROLES, indirect=["rbac_client"])
    def test_delete_category_forbidden_roles(
        self,
        rbac_client: CategoriesClient,
        role_name: str,
        existing_category: CategoryResponse,
    ) -> None:
        """Verify Role-Based Access Control: Users and Managers cannot delete categories."""
        response = rbac_client.delete_category(existing_category.id)

        with allure.step("Verify response is 403 Forbidden"):
            assert response.status_code == 403, f"Expected 403, got {response.status_code}"
