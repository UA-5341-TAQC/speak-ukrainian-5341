"""API helpers for temporary email verification using the mail.tm service."""

import re
import time
import uuid
from typing import Any

import allure
import requests


class TempMailAPIClient:
    """Helper class to interact with the mail.tm API.

    Usage:
        mail_api = TempMailAPIClient()
        email = mail_api.email_address
        msg_id = mail_api.wait_for_email()
        content = mail_api.get_email_content(msg_id)
    """

    BASE_URL = "https://api.mail.tm"
    DEFAULT_PASSWORD = "Password123!"
    DEFAULT_TIMEOUT = 10

    def __init__(self) -> None:
        """Initialize the API client, create a temp email, and authenticate."""
        self.domain: str = self._get_domain()
        self.email_address: str = self._generate_email_address()
        self.password: str = self.DEFAULT_PASSWORD

        self._create_account()
        self.token: str = self._authenticate()

    def _request_with_retry(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Execute a request with exponential backoff on 429 Too Many Requests."""
        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)

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
        response = self._request_with_retry("GET", f"{self.BASE_URL}/domains")
        data = response.json()

        domains = data.get("hydra:member", [])
        if not domains:
            raise RuntimeError("No domains available from mail.tm API")

        return str(domains[0].get("domain"))

    def _generate_email_address(self) -> str:
        """Generate a unique email address string."""
        username = f"qavisitor{uuid.uuid4().hex[:8]}"
        return f"{username}@{self.domain}"

    @allure.step("Create temporary email account")
    def _create_account(self) -> None:
        """Create a new temporary email account."""
        self._request_with_retry(
            "POST",
            f"{self.BASE_URL}/accounts",
            json={"address": self.email_address, "password": self.password},
        )

    @allure.step("Authenticate to get token")
    def _authenticate(self) -> str:
        """Authenticate and retrieve the token."""
        token_resp = self._request_with_retry(
            "POST",
            f"{self.BASE_URL}/token",
            json={"address": self.email_address, "password": self.password},
        )
        return str(token_resp.json().get("token", ""))

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
            response = requests.get(
                f"{self.BASE_URL}/messages", headers=headers, timeout=self.DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            messages: list[dict[str, Any]] = response.json().get("hydra:member", [])

            if messages:
                return str(messages[0]["id"])

            time.sleep(poll_frequency)

        raise TimeoutError(f"No email received within {timeout} seconds.")

    @allure.step("Fetch received email content")
    def get_email_content(self, message_id: str) -> str:
        """Fetch the HTML content of a specific email message."""
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(
            f"{self.BASE_URL}/messages/{message_id}", headers=headers, timeout=self.DEFAULT_TIMEOUT
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        html_content = data.get("html", "")

        if isinstance(html_content, list):
            if not html_content:
                raise ValueError("Email HTML content is empty.")
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
