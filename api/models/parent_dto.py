"""Module containing Parent Pydantic model."""

from api.models.base_dto import BaseDto


class ParentDto(BaseDto):
    """Model representing a parent."""
    id: int
    firstName: str
    lastName: str
    phone: str
    email: str
