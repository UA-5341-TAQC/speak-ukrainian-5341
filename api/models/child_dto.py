"""Module containing Child Pydantic model."""

from api.models.base_dto import BaseDto
from api.models.child_gender_dto import GenderDto
from api.models.parent_dto import ParentDto


class ChildDto(BaseDto):
    """Model representing a child registered for a club."""

    id: int
    firstName: str
    lastName: str
    parent: ParentDto | None = None
    age: int
    gender: GenderDto
    disabled: bool
