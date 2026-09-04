"""Base DTO model with common configuration for all API models."""

from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    """Base class for all DTO models with shared configuration."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True,
        use_enum_values=True,
    )
