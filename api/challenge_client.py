"""Module containing the API client for managing challenges."""

from pathlib import Path
from typing import Any

import allure
import requests

from data.config import Config


class ChallengeClient:
    """Client for interacting with Challenge API endpoints."""

    def __init__(self, session: requests.Session | None = None) -> None:
        """Initialize ChallengeClient with base URL and session."""
        self.base_url = Config.BASE_API_URL.rstrip("/")
        self.challenges_url = f"{self.base_url}/challenges"
        self.challenge_url = f"{self.base_url}/challenge"
        self.session = session or requests.Session()

    def _get_challenge_url(self, challenge_id: int) -> str:
        """Return specific challenge URL by ID."""
        return f"{self.challenge_url}/{challenge_id}"

    @staticmethod
    def _prepare_challenge_files(json_file_path: str, image_file_path: str | None = None,
                                 ) -> dict[str, tuple[str, Any, str]]:
        """Prepare JSON and image files for multipart request."""
        json_content = Path(json_file_path).read_text(encoding="utf-8")

        files: dict[str, tuple[str, Any, str]] = {
            "challenge": (
                "challenge.json",
                json_content,
                "application/json",
            ),
        }

        if image_file_path:
            image_path = Path(image_file_path)

            if image_path.exists():
                file_name = image_path.name
                file_extension = image_path.suffix.lower()

                mime_types = {
                    ".png": "image/png",
                    ".gif": "image/gif",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                }

                mime_type = mime_types.get(
                    file_extension,
                    "application/octet-stream",
                )

                files["images"] = (
                    file_name,
                    image_path.read_bytes(),
                    mime_type,
                )

        return files

    @allure.step("Get all challenges")
    def get_all_challenges(self, active: bool | None = None,) -> requests.Response:
        """Get list of all challenges."""
        params: dict[str, Any] = {"active": active} if active is not None else {}
        return self.session.get(self.challenges_url, params=params)

    @allure.step("Get challenge by ID: {challenge_id}")
    def get_challenge_by_id(self, challenge_id: int,) -> requests.Response:
        """Get challenge details by its ID."""
        return self.session.get(self._get_challenge_url(challenge_id))

    @allure.step("Create challenge with JSON and image")
    def create_challenge(self, json_file_path: str, image_file_path: str | None = None,
                         ) -> requests.Response:
        """Create a new challenge."""
        files = self._prepare_challenge_files(json_file_path, image_file_path,)
        return self.session.post(self.challenge_url, files=files)

    @allure.step("Update challenge (PUT) ID: {challenge_id}")
    def update_challenge(self, challenge_id: int, json_file_path: str,
                         image_file_path: str | None = None,) -> requests.Response:
        """Update an existing challenge completely (PUT)."""
        files = self._prepare_challenge_files(json_file_path, image_file_path)
        return self.session.put(self._get_challenge_url(challenge_id), files=files)

    @allure.step("Update challenge preview (PATCH) ID: {challenge_id}")
    def update_challenge_preview(self, challenge_id: int, payload: dict[str, Any],
                                 ) -> requests.Response:
        """Update challenge preview data."""
        return self.session.patch(self._get_challenge_url(challenge_id), json=payload)

    @allure.step("Update challenge start date ID: {challenge_id}")
    def update_challenge_start_date(self, challenge_id: int, payload: dict[str, Any],
                                    ) -> requests.Response:
        """Update challenge start date."""
        return self.session.put(self._get_challenge_url(challenge_id) + "/start/date", json=payload)

    @allure.step("Clone challenge ID: {challenge_id}")
    def clone_challenge(self, challenge_id: int,) -> requests.Response:
        """Clone an existing challenge."""
        return self.session.put(self._get_challenge_url(challenge_id) + "/clone")

    @allure.step("Archive challenge ID: {challenge_id}")
    def delete_challenge(self, challenge_id: int,) -> requests.Response:
        """Archive/delete a challenge by ID."""
        return self.session.delete(self._get_challenge_url(challenge_id))
