"""Domain models for news API responses.

These mirror the fields returned by the news read endpoints (OpenAPI schemas
``NewsResponse`` and ``UserPreview``).  They are Pydantic models, so a response
body can be turned into a typed, validated object with ``model_validate()`` and
back into a dictionary with ``model_dump(exclude_none=True)``.
"""

from pydantic import BaseModel


class UserPreview(BaseModel):
    """A short profile of the user who authored a news article.

    Attributes:
        id: Unique identifier of the user.
        firstName: First name of the user.
        lastName: Last name of the user.
        urlLogo: URL or path of the user's avatar image.
    """

    id: int
    firstName: str | None = None
    lastName: str | None = None
    urlLogo: str | None = None


class NewsResponse(BaseModel):
    """A single news article returned by the news API.

    Attributes:
        id: Unique identifier of the news article.
        title: Headline of the news article.
        description: HTML body / description of the article.
        urlTitleLogo: URL or path of the article's title image.
        date: Publication date as a ``[year, month, day]`` integer array.
        isActive: Whether the news item is active.
        user: The :class:`UserPreview` of the article's author, if present.
    """

    id: int
    title: str | None = None
    description: str | None = None
    urlTitleLogo: str | None = None
    date: list[int] | None = None
    isActive: bool | None = None
    user: UserPreview | None = None
