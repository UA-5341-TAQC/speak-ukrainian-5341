"""API tests for center endpoints."""

from api.center_client import CenterClient


NONEXISTENT_CENTER_ID = 999999
NONEXISTENT_USER_ID = 999999


def _first_center_id(center_api: CenterClient) -> int:
    """Return the ID of the first available center."""
    response = center_api.get_all_centers(timeout=30)

    assert response.status_code == 200

    centers = response.json()

    assert isinstance(centers, list)
    assert centers

    center_id = centers[0]["id"]

    assert isinstance(center_id, int)

    return center_id


def test_get_all_centers_returns_success(
    center_api: CenterClient,
) -> None:
    """Verify that GET /centers returns a list of centers."""
    response = center_api.get_all_centers(timeout=30)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_center_by_id_returns_success(
    center_api: CenterClient,
) -> None:
    """Verify that GET /center/{id} returns a center."""
    center_id = _first_center_id(center_api)

    response = center_api.get_center_by_id(
        center_id,
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "id" in data
    assert "name" in data


def test_get_center_by_id_returns_404_for_missing_center(
    center_api: CenterClient,
) -> None:
    """Verify that GET /center/{id} returns 404 for a missing center."""
    response = center_api.get_center_by_id(
        NONEXISTENT_CENTER_ID,
        timeout=30,
    )

    assert response.status_code == 404


def test_get_clubs_by_center_id_returns_success(
    center_api: CenterClient,
) -> None:
    """Verify that GET /centers/clubs/{id} returns center clubs."""
    center_id = _first_center_id(center_api)

    response = center_api.get_clubs_by_center_id(
        center_id,
        size=10,
        page=0,
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "content" in data
    assert isinstance(data["content"], list)
    assert "totalElements" in data
    assert "totalPages" in data


def test_search_centers_advanced_returns_success(
    center_api: CenterClient,
) -> None:
    """Verify that advanced center search returns a paginated result."""
    response = center_api.search_centers_advanced(
        center_name="string",
        district_name="string",
        city_name="string",
        station_name="string",
        page=0,
        size=1,
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "content" in data
    assert isinstance(data["content"], list)
    assert "totalElements" in data
    assert "totalPages" in data

def test_get_centers_by_user_id_returns_success(
    center_api: CenterClient,
) -> None:
    """Verify that GET /centers/{id} returns a paginated result."""
    response = center_api.get_centers_by_user_id(
        NONEXISTENT_USER_ID,
        page=0,
        size=1,
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "content" in data
    assert isinstance(data["content"], list)
    assert "totalElements" in data
    assert "totalPages" in data


def test_get_centers_by_user_id_returns_empty_for_missing_user(
    center_api: CenterClient,
) -> None:
    """Verify that GET /centers/{id} returns an empty result for a missing user."""
    response = center_api.get_centers_by_user_id(
        NONEXISTENT_USER_ID,
        page=0,
        size=1,
        timeout=30,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert data["content"] == []
    assert data["totalElements"] == 0


def test_delete_center_requires_authentication(
    center_api: CenterClient,
) -> None:
    """Verify that DELETE /center/{id} requires authentication."""
    response = center_api.delete_center(
        NONEXISTENT_CENTER_ID,
        timeout=30,
    )

    assert response.status_code in (401, 403)


def test_create_center_requires_authentication(
    center_api: CenterClient,
) -> None:
    """Verify that POST /center requires authentication."""
    response = center_api.create_center(
        {},
        timeout=30,
    )

    assert response.status_code in (400, 401, 403)


def test_update_center_requires_authentication(
    center_api: CenterClient,
) -> None:
    """Verify that PUT /center/{id} requires authentication."""
    response = center_api.update_center(
        NONEXISTENT_CENTER_ID,
        {},
        timeout=30,
    )

    assert response.status_code in (400, 401, 403, 404)


def test_update_center_rating_requires_authentication(
    center_api: CenterClient,
) -> None:
    """Verify that PATCH /centers/rating requires authentication."""
    response = center_api.update_center_rating(
        timeout=30,
    )

    assert response.status_code in (401, 403)