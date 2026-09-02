"""Module containing Gender Pydantic model."""

from api.models.base_dto import BaseDto


class GenderDto(BaseDto):
    """Model representing gender."""
    id: int
    value: str
