"""Module containing main Club Application Response Pydantic model."""

from pydantic import RootModel

from api.models.club_application_dto import ClubApplicationDto


class UserApplicationsListResponse(RootModel):
    """Response model for list of user club applications."""
    root: list[ClubApplicationDto]

    def __iter__(self):
        """Allow iteration over applications."""
        return iter(self.root)

    def __len__(self):
        """Get length of applications list."""
        return len(self.root)
