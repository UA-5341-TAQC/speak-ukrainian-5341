"""Module containing main Club Application Response Pydantic model."""

from pydantic import BaseModel, RootModel

from api.models.child_dto import ChildDto
from api.models.club_dto import ClubDto
from api.models.club_user_dto import UserDto


class ClubApplicationDto(BaseModel):
    """Model representing a club registration application."""
    id: int
    user: UserDto | None = None
    child: ChildDto | None = None
    club: ClubDto
    registrationDate: str
    comment: str
    active: bool
    approved: bool


class UserApplicationsListResponse(RootModel):
    """Response model for list of user club applications."""
    root: list[ClubApplicationDto]

    def __iter__(self):
        """Allow iteration over applications."""
        return iter(self.root)

    def __len__(self):
        """Get length of applications list."""
        return len(self.root)
