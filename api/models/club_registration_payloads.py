from api.models.base_dto import BaseDto


class ClubRegistrationCreatePayload(BaseDto):
    """Request payload for registering children to a club."""
    childIds: list[int]
    clubId: int
    comment: str


class ClubRegistrationResponseDto(BaseDto):
    """Response item after successful child club registration."""
    id: int
    childId: int
    clubId: int
    registrationDate: str
    comment: str
    active: bool
    approved: bool


class ClubUserRegistrationPayload(BaseDto):
    """Request payload for registering a user (adult) to a club."""
    userId: int
    clubId: int
    comment: str


class ClubUserRegistrationResponseDto(BaseDto):
    """Response item after successful user club registration."""
    id: int
    userId: int
    clubId: int
    registrationDate: str
    comment: str
    active: bool
    approved: bool
