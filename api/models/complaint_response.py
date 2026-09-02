"""Domain models for complaint API responses.

These mirror the fields returned by the complaint read endpoints (OpenAPI
schemas ``ComplaintResponse`` and ``UserPreview``). They are Pydantic models,
so a response body can be turned into a typed, validated object with
``model_validate()`` and back into a dictionary with
``model_dump(exclude_none=True)``.

The nested ``user`` and ``recipient`` previews reuse the same ``UserPreview``
shape as the news API. ``club`` is intentionally typed loosely (a ``dict``)
because the live backend embeds the full ``ClubResponse`` object (many fields
we do not want to declare here).
"""

from typing import Any

from pydantic import BaseModel


class UserPreview(BaseModel):
    """A short profile of a user referenced by a complaint.

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


class ComplaintResponse(BaseModel):
    """A single complaint returned by the complaint API.

    Attributes:
        id: Unique identifier of the complaint.
        text: Body of the complaint.
        date: Publication date. The OpenAPI docs describe it as a ``date``
            string but the live backend emits a ``[year, month, day]`` integer
            array, so both shapes are accepted.
        user: The :class:`UserPreview` of the complaint's author (sender).
        club: The full club object the complaint targets. Typed as a ``dict``
            to mirror the live payload without hard-coding every
            ``ClubResponse`` field.
        recipient: The :class:`UserPreview` of the user receiving the
            complaint.
        isActive: Whether the complaint is active.
        hasAnswer: Whether the complaint already has an answer from the
            recipient.
        answerText: Body of the recipient's answer, if any.
    """

    id: int
    text: str | None = None
    date: list[int] | str | None = None
    user: UserPreview | None = None
    club: dict[str, Any] | None = None
    recipient: UserPreview | None = None
    isActive: bool | None = None
    hasAnswer: bool | None = None
    answerText: str | None = None
