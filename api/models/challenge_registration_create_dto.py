"""Payload model for POST /api/challenge-registration."""

from pydantic import BaseModel


class ChallengeRegistrationCreateDto(BaseModel):
    """Payload to register a user for a challenge."""

    userId: str
    challengeId: int
    comment: str = " "
