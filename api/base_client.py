"""Shared HTTP client primitives for API clients."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import allure
import requests


class BaseClient:
    """Base class for API clients that share an HTTP session and authentication."""

    def __init__(self, base_url: str, access_token: str | None = None) -> None:
        """Initialize a client with its API root and optional access token.

        Args:
            base_url: Root URL used to resolve relative endpoint paths.
            access_token: Optional bearer token sent with each request.
        """
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send an HTTP request to an endpoint relative to ``base_url``.

        Request execution is kept in one method so derived clients can reuse it
        and so Allure logging remains consistent across the API surface.
        """
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        request_headers = dict(headers or {})
        if self.access_token is not None:
            request_headers.setdefault("Authorization", f"Bearer {self.access_token}")

        with allure.step(f"{method.upper()} {url}"):
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                **kwargs,
            )
            status_info = str(response.status_code)
            if response.status_code >= 400 and response.text:
                status_info += f" - {response.text}"
            allure.attach(
                status_info,
                name="Response status",
                attachment_type=allure.attachment_type.TEXT,
            )
            if response.status_code >= 400 and response.text:
                is_json = "json" in response.headers.get("Content-Type", "").lower()
                allure.attach(
                    response.text,
                    name="Response error",
                    attachment_type=allure.attachment_type.JSON
                    if is_json
                    else allure.attachment_type.TEXT,
                )
        return response
