from pydantic import BaseModel


class ClubRegistrationCreatePayload(BaseModel):
    """Request payload for registering children to a club."""
    childIds: list[int]
    clubId: int
    comment: str


class ClubRegistrationResponseDto(BaseModel):
    """Response item after successful child club registration."""
    id: int
    childId: int
    clubId: int
    registrationDate: str
    comment: str
    active: bool
    approved: bool


class ClubUserRegistrationPayload(BaseModel):
    """Request payload for registering a user (adult) to a club."""
    userId: int
    clubId: int
    comment: str


class ClubUserRegistrationResponseDto(BaseModel):
    """Response item after successful user club registration."""
    id: int
    userId: int
    clubId: int
    registrationDate: str
    comment: str
    active: bool
    approved: bool