"""API helpers for temporary email verification using the mail.tm service."""

import re
import time
import uuid
from typing import Any

import allure
import requests


class TempMailAPI:
    """Helper class to interact with the mail.tm API.

    Usage:
        mail_api = TempMailAPI()
        email = mail_api.generate_email("test_user")
        msg_id = mail_api.wait_for_email()
        content = mail_api.get_email_content(msg_id)
    """

    def __init__(self) -> None:
        """Initialize the API client and fetch an active domain."""
        self.base_url = "https://api.mail.tm"
        self.token: str | None = None
        self.domain: str = self._get_domain()

    def _request_with_retry(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Execute a request with exponential backoff on 429 Too Many Requests."""
        for attempt in range(5):
            response = requests.request(method, url, **kwargs)
            if response.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            response.raise_for_status()
            return response
        raise RuntimeError(f"Max retries exceeded with 429 errors for {method} {url}")

    def _get_domain(self) -> str:
        """Fetch an active domain from mail.tm."""
        response = self._request_with_retry("GET", f"{self.base_url}/domains", timeout=10)
        return str(response.json()["hydra:member"][0]["domain"])

    @allure.step("Generate temporary email")
    def generate_email(self) -> str:
        """Create a new temporary email account and save the auth token.

        Generates a unique local part (username) automatically using UUID to
        ensure isolation for parallel test execution.

        Returns:
            A string containing the full email address.
        """
        username = f"qavisitor{uuid.uuid4().hex[:8]}"
        address = f"{username}@{self.domain}"
        password = "Password123!"

        self._request_with_retry(
            "POST",
            f"{self.base_url}/accounts",
            json={"address": address, "password": password},
            timeout=10,
        )

        token_resp = self._request_with_retry(
            "POST",
            f"{self.base_url}/token",
            json={"address": address, "password": password},
            timeout=10,
        )

        self.token = token_resp.json()["token"]
        return address

    @allure.step("Wait for an email to arrive")
    def wait_for_email(self, timeout: int = 30, poll_frequency: int = 3) -> str:
        """Wait for an email to arrive in the inbox within the specified timeout.

        Args:
            timeout: Maximum time in seconds to wait for the email. Defaults to 30.
            poll_frequency: Delay in seconds between API requests. Defaults to 3.

        Returns:
            The string ID of the latest received message if found.

        Raises:
            TimeoutError: If the email is not received within the timeout.
        """
        end_time = time.time() + timeout
        headers = {"Authorization": f"Bearer {self.token}"}

        while time.time() < end_time:
            response = requests.get(f"{self.base_url}/messages", headers=headers, timeout=10)
            response.raise_for_status()
            messages: list[dict[str, Any]] = response.json().get("hydra:member", [])

            if messages:
                return str(messages[0]["id"])

            time.sleep(poll_frequency)

        raise TimeoutError(f"No email received within {timeout} seconds.")

    @allure.step("Fetch email content for message ID: {message_id}")
    def get_email_content(self, message_id: str) -> str:
        """Fetch the HTML content of a specific email message."""
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(
            f"{self.base_url}/messages/{message_id}", headers=headers, timeout=10
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()

        html_content = data.get("html", "")
        if isinstance(html_content, list) and len(html_content) > 0:
            return str(html_content[0])
        return str(html_content)

    @allure.step("Extract verification link from email HTML")
    def extract_verification_link(self, email_html: str) -> str:
        """Parse the confirmation link from the email HTML.

        Args:
            email_html: The raw HTML content of the email.

        Returns:
            The extracted URL string.

        Raises:
            ValueError: If the verification link cannot be found in the HTML.
        """
        match = re.search(r'href="(https?://[^"]*speak-ukrainian[^"]+)"', email_html)
        if not match:
            raise ValueError("Verification link not found in the email content.")
        return match.group(1)
