"""Module containing Club Pydantic model."""

from pydantic import BaseModel


class ClubDto(BaseModel):
    """Model representing a club."""
    id: int
    name: str
