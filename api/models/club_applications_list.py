"""Module containing main Club Application Response Pydantic model."""

from collections.abc import Iterator

from pydantic import RootModel

from api.models.club_application_dto import ClubApplicationDto


class UserApplicationsListResponse(RootModel[list[ClubApplicationDto]]):
    """Response model for list of user club applications."""

    root: list[ClubApplicationDto]

    def __iter__(self) -> Iterator[ClubApplicationDto]:  # type: ignore[override]
        """Allow iteration over applications."""
        return iter(self.root)

    def __len__(self) -> int:
        """Get length of applications list."""
        return len(self.root)
