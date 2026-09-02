"""Module containing Parent Pydantic model."""

from pydantic import BaseModel


class ParentDto(BaseModel):
    """Model representing a parent."""
    id: int
    firstName: str
    lastName: str
    phone: str
    email: str
