"""Domain model for the POST /complaint success response.

Mirrors the OpenAPI schema ``SuccessCreatedComplaint`` returned by
``POST /api/complaint`` on success. The fields listed below are the ones the
backend actually serialises on this deployment; the schema is permissive so
extra fields can ride along without breaking validation.
"""

from pydantic import BaseModel


class SuccessCreatedComplaint(BaseModel):
    """Response body returned by a successful ``POST /api/complaint``.

    Attributes:
        id: Identifier of the newly created complaint.
        text: Body of the complaint, as submitted.
        userId: Numeric id of the user filing the complaint.
        clubId: Numeric id of the club the complaint targets.
        recipientId: Numeric id of the user receiving the complaint.
        isActive: Whether the new complaint is active.
        hasAnswer: Always ``False`` immediately after creation — there is no
            answer yet. Exposed so the typed model matches the wire shape.
    """

    id: int
    text: str | None = None
    userId: int | None = None
    clubId: int | None = None
    recipientId: int | None = None
    isActive: bool | None = None
    hasAnswer: bool | None = None
