"""Module containing Pydantic models for Club Registration API."""

from api.models.base_dto import BaseDto


class UserDto(BaseDto):
    """Short model for user in registration response."""
    id: int
    firstName: str
    lastName: str
    phone: str
    email: str
