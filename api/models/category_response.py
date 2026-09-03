from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    """Pydantic model representing a category object returned by the API."""

    id: int
    name: str = Field(min_length=1)
    description: str
    sortby: int
    urlLogo: str
    backgroundColor: str
    tagBackgroundColor: str
    tagTextColor: str


class PageCategoryResponse(BaseModel):
    """Pydantic model representing a paginated list of categories."""

    content: list[CategoryResponse]
    totalElements: int
    totalPages: int
    # Optional fields from Spring Data Page
    size: int | None = None
    number: int | None = None
