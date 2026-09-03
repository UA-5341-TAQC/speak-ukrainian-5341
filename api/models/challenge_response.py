"""Module containing main ChallengeResponse Pydantic model."""

from pydantic import BaseModel, Field

from api.models.challenge_task_dto import ChallengeTaskDto
from api.models.сhallenge_user_dto import ChallengeUserDto


class ChallengeResponse(BaseModel):
    """Main detailed model for a challenge."""

    id: int
    name: str
    title: str
    description: str
    picture: str
    sortNumber: int
    isActive: bool
    tasks: list[ChallengeTaskDto] = Field(default_factory=list)
    user: ChallengeUserDto | None = None
    registrationLink: str | None = None
