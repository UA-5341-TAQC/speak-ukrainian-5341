"""API client for Category endpoints."""

from typing import Any

import requests

from api.base_client import BaseClient


class CategoriesClient(BaseClient):
    """Client for managing Categories via API."""

    def search_categories(self, **kwargs: Any) -> requests.Response:
        """Search and paginate categories."""
        return self._request("GET", "categories/search", **kwargs)

    def get_categories(self, **kwargs: Any) -> requests.Response:
        """Fetch the list of all categories."""
        return self._request("GET", "categories", **kwargs)

    def get_category_by_id(self, category_id: int, **kwargs: Any) -> requests.Response:
        """Fetch a specific category by its ID."""
        return self._request("GET", f"category/{category_id}", **kwargs)

    def create_category(self, payload: dict[str, Any], **kwargs: Any) -> requests.Response:
        """Create a new category (requires Admin)."""
        return self._request("POST", "category", json=payload, **kwargs)

    def update_category(
        self, category_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Update an existing category (requires Admin)."""
        return self._request("PUT", f"category/{category_id}", json=payload, **kwargs)

    def delete_category(self, category_id: int, **kwargs: Any) -> requests.Response:
        """Delete a category by its ID (requires Admin)."""
        return self._request("DELETE", f"category/{category_id}", **kwargs)
