"""Pydantic models for Club Registration API responses.

This module re-exports DTOs from their individual model files for backward compatibility.
"""

from api.models.child_dto import ChildDto
from api.models.child_gender_dto import GenderDto
from api.models.club_application_dto import ClubApplicationDto
from api.models.club_dto import ClubDto
from api.models.club_registration_payloads import (
    ClubRegistrationCreatePayload,
    ClubRegistrationResponseDto,
)
from api.models.club_user_dto import UserDto
from api.models.parent_dto import ParentDto

__all__ = [
    "ChildDto",
    "GenderDto",
    "ParentDto",
    "UserDto",
    "UserDto",
    "ClubDto",
    "ClubDto",
    "ClubApplicationDto",
    "ClubApplicationDto",
    "ClubRegistrationCreatePayload",
    "ClubRegistrationResponseDto",
]
