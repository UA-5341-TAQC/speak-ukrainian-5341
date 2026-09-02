"""Module containing Task Pydantic model for Challenge API."""

from pydantic import BaseModel


class ChallengeTaskDto(BaseModel):
    """Model representing a task inside a challenge."""
    id: int
    name: str
    headerText: str | None = None
    description: str | None = None
    picture: str | None = None
    startDate: str | None = None
    challengeId: int | None = None
    isActive: bool | None = None
