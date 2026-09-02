"""Payload model for POST /api/challenge-registration/children."""

from pydantic import BaseModel


class ChallengeRegistrationCreateForChildrenDto(BaseModel):
    """Payload to register one or more children for a challenge."""

    childIds: list[int]
    challengeId: int
    comment: str = " "
