"""Module containing Pydantic models for Club Registration API."""
 
from pydantic import BaseModel
 
 
class UserDto(BaseModel):
    """Short model for user in registration response."""
    id: int
    firstName: str
    lastName: str
    phone: str
    email: str