"""Domain model for the complaint write operations.

The :class:`ComplaintProfile` models the request body used by
``POST /api/complaint`` and ``PUT /api/complaint/{id}`` (OpenAPI schema
``ComplaintProfile``). It provides a typed, reusable way to build a valid
payload instead of constructing bare dictionaries in every test. Serialization
to a JSON request body is inherited from Pydantic's ``BaseModel``.
"""

from pydantic import BaseModel


class ComplaintProfile(BaseModel):
    """Complaint data used to create or update a complaint.

    Attributes:
        id: Existing complaint id. Populated by the backend on create; left as
            ``None`` when creating a new complaint (it is optional in the
            ``ComplaintProfile`` schema and is omitted from the serialized
            payload when ``None``).
        text: Body of the complaint.
        userId: Numeric id of the user filing the complaint (sender).
        clubId: Numeric id of the club the complaint targets.
        recipientId: Numeric id of the user receiving the complaint.
        isActive: Whether the complaint is active. When left as ``None`` the
            field is omitted from the serialized payload (it is optional in the
            ``ComplaintProfile`` schema); setting ``True``/``False`` includes
            it.
    """

    id: int | None = None
    text: str
    userId: int
    clubId: int
    recipientId: int
    isActive: bool | None = None
