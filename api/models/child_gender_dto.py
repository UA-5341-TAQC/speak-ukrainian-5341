"""Module containing Gender Pydantic model."""

from pydantic import BaseModel


class GenderDto(BaseModel):
    """Model representing gender."""
    id: int
    value: str  # e.g., "MALE", "FEMALE"
