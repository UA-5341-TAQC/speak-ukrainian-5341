from api.models.base_dto import BaseDto
from api.models.child_dto import ChildDto
from api.models.club_dto import ClubDto
from api.models.club_user_dto import UserDto


class ClubApplicationDto(BaseDto):
    """Model representing a club registration application."""
    id: int
    user: UserDto | None = None
    child: ChildDto | None = None
    club: ClubDto
    registrationDate: str
    comment: str
    active: bool
    approved: bool
