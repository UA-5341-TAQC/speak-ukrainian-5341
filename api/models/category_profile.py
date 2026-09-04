from pydantic import BaseModel, Field


class CategoryProfile(BaseModel):
    """Pydantic model representing the payload to create or update a category."""

    name: str = Field(min_length=1)
    description: str
    sortby: int
    urlLogo: str
    backgroundColor: str
    tagBackgroundColor: str
    tagTextColor: str
