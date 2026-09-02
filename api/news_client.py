"""API client for the news endpoints of the Speak Ukrainian API.

The client covers the ``/newslist`` and ``/news`` endpoints documented in
issue #283. Public list/detail read endpoints require no authentication, while
the write (``POST``/``PUT``) and maintenance (``DELETE``) operations are
restricted to an authenticated, admin-role account.
"""

from __future__ import annotations

from typing import Any

import requests

from api.base_client import BaseClient

NEWS_LIST_ENDPOINT = "newslist"
NEWS_ENDPOINT = "news"


class NewsClient(BaseClient):
    """Client for the news endpoints of the Speak Ukrainian API.

    Reads from the public news feed are available without a token; create,
    update and delete operations need an ``access_token`` belonging to a role
    with the necessary permissions (admin).
    """

    def get_news_list(self, **kwargs: Any) -> requests.Response:
        """Return the full list of news articles.

        Args:
            **kwargs: Extra keyword arguments forwarded to the HTTP request
                (for example ``params`` or ``timeout``).

        Returns:
            The raw HTTP response containing a JSON list of news items.
        """
        return self._request("GET", NEWS_LIST_ENDPOINT, **kwargs)

    def get_current_news(self, **kwargs: Any) -> requests.Response:
        """Return the currently published/active news items.

        Args:
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing a JSON list of current news items.
        """
        return self._request("GET", f"{NEWS_LIST_ENDPOINT}/current", **kwargs)

    def search_news(self, keyword: str, **kwargs: Any) -> requests.Response:
        """Search news by keyword (full-text search).

        Args:
            keyword: Search term to filter news articles by.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing paginated news search results.
        """
        params = dict(kwargs.pop("params", {}))
        params["keyword"] = keyword
        return self._request("GET", f"{NEWS_LIST_ENDPOINT}/search", params=params, **kwargs)

    def search_similar_news(self, **kwargs: Any) -> requests.Response:
        """Return news that is similar in content.

        Args:
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response containing a JSON list of similar news items.
        """
        return self._request("GET", f"{NEWS_LIST_ENDPOINT}/search/similar", **kwargs)

    def get_news(self, news_id: int, **kwargs: Any) -> requests.Response:
        """Return a single news article by its numeric ID.

        Args:
            news_id: The ID of the news article to fetch.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response. A missing article yields 404.
        """
        return self._request("GET", f"{NEWS_ENDPOINT}/{news_id}", **kwargs)

    def create_news(self, payload: dict[str, Any], **kwargs: Any) -> requests.Response:
        """Create a new news article (admin only).

        Args:
            payload: JSON body describing the news article.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request("POST", NEWS_ENDPOINT, json=payload, **kwargs)

    def update_news(
        self, news_id: int, payload: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Fully update an existing news article (admin only).

        Args:
            news_id: The ID of the news article to replace.
            payload: The JSON body with the new news article data.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response from the backend.
        """
        return self._request("PUT", f"{NEWS_ENDPOINT}/{news_id}", json=payload, **kwargs)

    def delete_news(self, news_id: int, **kwargs: Any) -> requests.Response:
        """Delete a news article by its ID (admin only).

        Args:
            news_id: The ID of the news article to delete.
            **kwargs: Extra keyword arguments forwarded to the HTTP request.

        Returns:
            The raw HTTP response. Anonymous callers receive 401 and
            non-admin roles receive 403.
        """
        return self._request("DELETE", f"{NEWS_ENDPOINT}/{news_id}", **kwargs)
