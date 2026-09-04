"""Module containing User Pydantic model."""

from pydantic import BaseModel


class ChallengeUserDto(BaseModel):
    """Model representing an organizer/creator of a challenge."""

    id: int
    firstName: str
    lastName: str
    urlLogo: str
