"""Module containing Club Pydantic model."""

from api.models.base_dto import BaseDto


class ClubDto(BaseDto):
    """Model representing a club."""
    id: int
    name: str
