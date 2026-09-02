"""Domain model for the News write operations.

The :class:`NewsProfile` models the request body used by ``POST /api/news`` and
``PUT /api/news/{id}`` (OpenAPI schema ``NewsProfile``).  It provides a typed,
reusable way to build a valid payload instead of constructing bare dictionaries
in every test.  Serialization to a JSON request body is inherited from
Pydantic's ``BaseModel``.
"""

from pydantic import BaseModel


class NewsProfile(BaseModel):
    """News article data used to create or update a news item.

    Attributes:
        date: Publication date serialized as an ISO-8601 string.
        title: Headline of the news article.
        description: HTML body / description of the article.
        urlTitleLogo: URL or path of the article's title image.
        isActive: Whether the news item is active. When left as ``None`` the
            field is omitted from the serialized payload (it is optional in the
            ``NewsProfile`` schema); setting ``True``/``False`` includes it.
    """

    date: str
    title: str
    description: str
    urlTitleLogo: str
    isActive: bool | None = None
