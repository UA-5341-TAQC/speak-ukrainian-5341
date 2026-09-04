"""API client for managing centers."""

from typing import Any

import allure
import requests

from api.base_client import BaseClient
from data.config import Config


class CenterClient(BaseClient):
    """Client for interacting with Center API endpoints."""

    def __init__(
        self,
        base_url: str = Config.BASE_API_URL,
        access_token: str | None = None,
    ) -> None:
        """Initialize CenterClient with base URL and optional access token."""
        super().__init__(base_url=base_url, access_token=access_token)

    @allure.step("Get all centers")
    def get_all_centers(self, **kwargs: Any) -> requests.Response:
        """Get information about all centers."""
        return self._request(
            "GET",
            "centers",
            **kwargs,
        )

    @allure.step("Get center by ID: {center_id}")
    def get_center_by_id(
        self,
        center_id: int,
        **kwargs: Any,
    ) -> requests.Response:
        """Get information about a center by center ID."""
        return self._request(
            "GET",
            f"center/{center_id}",
            **kwargs,
        )

    @allure.step("Get clubs by center ID: {center_id}")
    def get_clubs_by_center_id(
        self,
        center_id: int,
        size: int,
        page: int = 0,
        sort: list[str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Get clubs of a center with pagination."""
        params: dict[str, Any] = {
            "size": size,
            "page": page,
        }

        if sort is not None:
            params["sort"] = sort

        return self._request(
            "GET",
            f"centers/clubs/{center_id}",
            params=params,
            **kwargs,
        )

    @allure.step("Search centers with advanced search")
    def search_centers_advanced(
        self,
        center_name: str = "string",
        district_name: str = "string",
        city_name: str = "string",
        station_name: str = "string",
        page: int = 0,
        size: int = 1,
        sort: list[str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Search centers using advanced search with pagination."""
        params: dict[str, Any] = {
            "centerName": center_name,
            "districtName": district_name,
            "cityName": city_name,
            "stationName": station_name,
            "page": page,
            "size": size,
        }

        if sort is not None:
            params["sort"] = sort

        return self._request(
            "GET",
            "centers/search/advanced",
            params=params,
            **kwargs,
        )

    @allure.step("Get centers by user ID: {user_id}")
    def get_centers_by_user_id(
        self,
        user_id: int,
        page: int = 0,
        size: int = 1,
        sort: list[str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Get centers owned by a user with pagination."""
        params: dict[str, Any] = {
            "page": page,
            "size": size,
        }

        if sort is not None:
            params["sort"] = sort

        return self._request(
            "GET",
            f"centers/{user_id}",
            params=params,
            **kwargs,
        )

    @allure.step("Update centers rating")
    def update_center_rating(
        self,
        **kwargs: Any,
    ) -> requests.Response:
        """Update ratings for all centers."""
        return self._request(
            "PATCH",
            "centers/rating",
            **kwargs,
        )

    @allure.step("Create center")
    def create_center(
        self,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> requests.Response:
        """Create a new center."""
        return self._request(
            "POST",
            "center",
            json=payload,
            **kwargs,
        )

    @allure.step("Update center ID: {center_id}")
    def update_center(
        self,
        center_id: int,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> requests.Response:
        """Update an existing center."""
        return self._request(
            "PUT",
            f"center/{center_id}",
            json=payload,
            **kwargs,
        )

    @allure.step("Delete center ID: {center_id}")
    def delete_center(
        self,
        center_id: int,
        **kwargs: Any,
    ) -> requests.Response:
        """Delete a center by ID."""
        return self._request(
            "DELETE",
            f"center/{center_id}",
            **kwargs,
        )
