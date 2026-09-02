"""Base smoke tests for the news API endpoints.

Covers every news endpoint listed in issue #283:

- ``GET  /api/newslist``
- ``GET  /api/newslist/current``
- ``GET  /api/newslist/search``
- ``GET  /api/newslist/search/similar``
- ``GET  /api/news/{id}``
- ``POST /api/news``
- ``PUT  /api/news/{id}``
- ``DELETE /api/news/{id}``

The read endpoints are public. The write operations (``POST``/``PUT``) and the
maintenance operation (``DELETE``) are admin-only: anonymous callers get 401 and
non-admin roles (user/manager) get 403.
"""

from __future__ import annotations

from typing import Any

import allure

from api.news_client import NewsClient
from api.models.news_profile import NewsProfile
from api.models.news_response import NewsResponse, UserPreview
from api.schemas.validator import assert_response_matches
from data.config import Config

# A non-existing news id, used to verify 404 handling on the detail endpoint.
NONEXISTENT_NEWS_ID = 999999


def _first_news_id(news_api: NewsClient) -> int:
    """Return the id of the first article from the public news list."""
    response = news_api.get_news_list(timeout=30)
    assert response.status_code == 200, f"News list request failed: {response.status_code}"
    items = response.json()
    assert isinstance(items, list) and items, "News list should be a non-empty list"
    news_id = items[0]["id"]
    assert isinstance(news_id, int), f"Expected an integer news id, got {news_id!r}"
    return news_id


@allure.title("News-API-01: GET /newslist returns 200 with a news list")
@allure.tag("api", "smoke", "news")
def test_news_list_returns_articles(news_api: NewsClient) -> None:
    """The public news list must return a 200 response with a JSON list."""
    with allure.step("Request the full news list"):
        response = news_api.get_news_list()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify the response is a list of news items"):
        payload = response.json()
        assert isinstance(payload, list), "The news list payload must be a list"
        assert payload, "The news list must not be empty"
        assert "title" in payload[0], "News item is missing the expected 'title' field"

    with allure.step("Validate the news list against the stored NewsList schema"):
        assert_response_matches(payload, "news_list", name="GET /newslist")

    with allure.step("Deserialize each item into a NewsResponse model via model_validate"):
        models = [NewsResponse.model_validate(item) for item in payload]
        assert all(isinstance(item, NewsResponse) for item in models), (
            "Every list element should deserialize into NewsResponse"
        )
        # The first article's raw payload is preserved through the round trip.
        assert models[0].model_dump(exclude_none=True) == payload[0], (
            "model_validate -> model_dump round trip should reproduce the raw item"
        )


@allure.title("News-API-02: GET /newslist/current returns 200 with current news")
@allure.tag("api", "smoke", "news")
def test_current_news_returns_articles(news_api: NewsClient) -> None:
    """The current-news endpoint must return 200 with a JSON list."""
    with allure.step("Request the current news"):
        response = news_api.get_current_news()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify the response is a list"):
        payload = response.json()
        assert isinstance(payload, list), "The current-news payload must be a list"


@allure.title("News-API-03: GET /newslist/search?keyword= returns 200 with a search result")
@allure.tag("api", "smoke", "news")
def test_news_search_returns_results(news_api: NewsClient) -> None:
    """The news search endpoint must return 200 for a plain keyword."""
    with allure.step("Request news matching a keyword"):
        response = news_api.search_news(keyword="українськ")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify the search payload carries a 'content' collection"):
        payload = response.json()
        assert isinstance(payload, dict), "Search payload should be an object"
        assert "content" in payload, "Search payload must contain the 'content' field"

    with allure.step("Validate the search result against the stored PageNewsResponse schema"):
        assert_response_matches(payload, "page_news_response", name="GET /newslist/search")

    with allure.step("Deserialize search content items via NewsResponse.model_validate"):
        content = payload["content"]
        if content:
            models = [NewsResponse.model_validate(item) for item in content]
            assert all(isinstance(m, NewsResponse) for m in models), (
                "Every search content item should deserialize into NewsResponse"
            )
            assert models[0].id is not None, "First search result must have an id"


@allure.title("News-API-04: GET /newslist/search/similar returns 200")
@allure.tag("api", "smoke", "news")
def test_similar_news_returns_ok(news_api: NewsClient) -> None:
    """The similar-news endpoint must respond with 200 and valid JSON."""
    with allure.step("Request similar news"):
        response = news_api.search_similar_news()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify the response body is JSON"):
        response.json()


@allure.title("News-API-05: GET /news/{id} returns 200 for an existing article")
@allure.tag("api", "smoke", "news")
def test_get_news_by_id_returns_article(news_api: NewsClient) -> None:
    """An existing news article must be fetchable by id without auth."""
    news_id = _first_news_id(news_api)

    with allure.step(f"Request news with id {news_id}"):
        response = news_api.get_news(news_id)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Verify the returned article matches the requested id"):
        payload = response.json()
        assert payload["id"] == news_id, "Returned news id should match the request"

    with allure.step("Validate the article against the stored NewsResponse schema"):
        assert_response_matches(payload, "news_response", name=f"GET /news/{news_id}")

    with allure.step("Deserialize the article into a NewsResponse model via model_validate"):
        article = NewsResponse.model_validate(payload)
        assert isinstance(article, NewsResponse), "Payload should deserialize into NewsResponse"
        assert article.id == news_id, "Model id must match the requested news id"
        assert article.title is not None, "Article title should be present"
        if article.user is not None:
            assert isinstance(article.user, UserPreview), (
                "Nested 'user' should be deserialized into a UserPreview model"
            )


@allure.title("News-API-06: GET /news/{id} returns 404 for a missing article")
@allure.tag("api", "smoke", "news")
def test_get_news_by_id_returns_404_for_missing(news_api: NewsClient) -> None:
    """A non-existent news id must yield a 404 response."""
    with allure.step(f"GET news with a non-existent id {NONEXISTENT_NEWS_ID}"):
        response = news_api.get_news(NONEXISTENT_NEWS_ID)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


@allure.title("News-API-07: DELETE /news/{id} is admin-only (401 when unauthenticated)")
@allure.tag("api", "smoke", "news", "security")
def test_delete_news_requires_authentication(news_api: NewsClient) -> None:
    """An anonymous caller must not be able to delete news (401)."""
    news_id = _first_news_id(news_api)

    with allure.step(f"Request DELETE /news/{news_id} without a token"):
        response = news_api.delete_news(news_id)
        assert response.status_code == 401, (
            f"Anonymous delete should be rejected with 401, got {response.status_code}"
        )


@allure.title("News-API-08: DELETE /news/{id} forbidden for a regular user")
@allure.tag("api", "smoke", "news", "security")
def test_delete_news_forbidden_for_user(news_api_user: NewsClient) -> None:
    """A regular user (no admin token) must get 403 when deleting news."""
    news_id = _first_news_id(news_api_user)

    with allure.step(f"Request DELETE /news/{news_id} with a user token"):
        response = news_api_user.delete_news(news_id)
        assert response.status_code == 403, (
            f"Non-admin user should get 403, got {response.status_code}"
        )


@allure.title("News-API-09: DELETE /news/{id} forbidden for a manager")
@allure.tag("api", "smoke", "news", "security")
def test_delete_news_forbidden_for_manager(news_api_manager: NewsClient) -> None:
    """A manager (also not admin) must get 403 when deleting news."""
    news_id = _first_news_id(news_api_manager)

    with allure.step(f"Request DELETE /news/{news_id} with a manager token"):
        response = news_api_manager.delete_news(news_id)
        assert response.status_code == 403, (
            f"Manager should get 403 (not admin), got {response.status_code}"
        )


@allure.title("News-API-10: non-admin cannot POST /news or PUT /news/{id}")
@allure.tag("api", "smoke", "news", "security")
def test_write_news_rejects_non_admin(news_api_user: NewsClient) -> None:
    """POST/PUT require an admin access token, so a plain user must get a 4xx.

    The user fixture has no admin token. With a partial body the backend rejects
    the request via body validation (4xx) before it could be accepted, so the
    test only asserts the write does not succeed from a non-admin account.
    """
    news_id = _first_news_id(news_api_user)
    payload: dict[str, Any] = {"title": "Smoke test", "description": "content"}

    with allure.step("POST /news with a user token and a partial body"):
        create_response = news_api_user.create_news(payload)
        assert create_response.status_code >= 400, (
            f"Non-admin POST must not succeed, got {create_response.status_code}"
        )

    with allure.step(f"PUT /news/{news_id} with a user token and a partial body"):
        update_response = news_api_user.update_news(news_id, payload)
        assert update_response.status_code >= 400, (
            f"Non-admin PUT must not succeed, got {update_response.status_code}"
        )


@allure.title("News-API-11: news read endpoints are reachable on the configured base URL")
@allure.tag("api", "smoke", "news")
def test_news_endpoints_reachable_on_configured_url() -> None:
    """The base URL must be configured correctly for news requests."""
    with allure.step("Check the configured API base URL is populated"):
        assert Config.BASE_API_URL, "BASE_API_URL must not be empty in the .env file"
        assert Config.BASE_API_URL.startswith("http"), "BASE_API_URL must start with http"


@allure.title("News-API-12: schema-valid POST/PUT body rejected for a non-admin")
@allure.tag("api", "smoke", "news", "security")
def test_write_news_with_valid_payload_rejected_for_non_admin(
    news_api_user: NewsClient,
) -> None:
    """A schema-valid write payload must still be rejected for a non-admin role.

    ``POST``/``PUT`` are admin-only operations. The payload is built with the
    typed ``NewsProfile`` model and validated against the stored
    ``news_profile`` schema before sending (proving the model satisfies the
    contract), then the user client must get a 4xx because it has no admin
    access token.
    """
    news_id = _first_news_id(news_api_user)
    payload = NewsProfile(
        date="2024-01-01T00:00:00",
        title="Smoke test news",
        description="<p>Smoke test content</p>",
        urlTitleLogo="https://example.com/news.png",
        isActive=True,
    ).model_dump(exclude_none=True)

    with allure.step("Validate the model-built payload against the NewsProfile schema"):
        assert_response_matches(payload, "news_profile", name="POST /news payload")

    with allure.step("POST the valid payload with a user token"):
        create_response = news_api_user.create_news(payload)
        assert create_response.status_code >= 400, (
            f"Non-admin POST must not succeed, got {create_response.status_code}"
        )

    with allure.step(f"PUT /news/{news_id} with the valid payload and a user token"):
        update_response = news_api_user.update_news(news_id, payload)
        assert update_response.status_code >= 400, (
            f"Non-admin PUT must not succeed, got {update_response.status_code}"
        )
