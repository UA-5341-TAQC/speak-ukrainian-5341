"""Base smoke tests for the complaint API endpoints.

Covers every complaint endpoint listed in issue #284:

- ``GET    /api/complaints``
- ``GET    /api/complaints/club/{id}``
- ``GET    /api/complaints/recipient/{id}``
- ``GET    /api/complaints/sender/{id}``
- ``GET    /api/complaint/{id}``
- ``POST   /api/complaint``
- ``PUT    /api/complaint/{id}``
- ``PUT    /api/complaint/{id}/answer``
- ``PUT    /api/complaint/isActive/{id}``
- ``DELETE /api/complaint/{id}``

Observed auth/role matrix on this deployment (verified via live probe with
both ``USER`` and ``MANAGER`` tokens):

+------------------------------+------+------+--------+
| Endpoint                     | anon | USER | MGR    |
+==============================+======+======+========+
| GET  /complaints             | 200  | 200  | 200    |
| GET  /complaints/club/{id}   | 200  | 200  | 200    |
| GET  /complaints/recipient.. | 200  | 200  | 200    |
| GET  /complaints/sender/..   | 200  | 200  | 200    |
| GET  /complaint/{id}         | 200  | 200  | 200    |
| POST /complaint              | 401  | 200  | 200    |
| PUT  /complaint/{id}         | 401  | 200  | 200    |
| PUT  /complaint/{id}/answer  | 401  | 200  | 200    |
| PUT  /complaint/isActive/{id}| 401  | 200  | 200    |
| DELETE /complaint/{id}       | 401  | 200  | 200    |
+------------------------------+------+------+--------+

The read endpoints are public. The write/update/delete operations require
authentication with a valid access token.
"""

from __future__ import annotations

from typing import Any, cast

import allure

from api.complaint_client import ComplaintClient
from api.models.complaint_profile import ComplaintProfile
from api.models.complaint_response import ComplaintResponse
from api.models.success_created_complaint import SuccessCreatedComplaint
from api.schemas.validator import assert_response_matches

# A non-existing complaint id, used to verify 404 handling on the detail endpoint.
NONEXISTENT_COMPLAINT_ID = 999999


def _first_complaint(complaint_api: ComplaintClient) -> dict[str, Any]:
    """Return the first complaint dictionary from the public complaints list.

    Asserts that the list endpoint is reachable and non-empty so every smoke
    test that depends on an existing complaint has a stable starting point.
    """
    response = complaint_api.get_complaints(timeout=30)
    assert response.status_code == 200, (
        f"Complaints list request failed: {response.status_code}"
    )
    items = response.json()
    assert isinstance(items, list), "Complaints list payload must be a list"
    assert items, "Complaints list must not be empty"
    return cast(dict[str, Any], items[0])


def _first_complaint_id(complaint_api: ComplaintClient) -> int:
    """Return the id of the first complaint from the public complaints list."""
    complaint = _first_complaint(complaint_api)
    complaint_id = complaint["id"]
    assert isinstance(complaint_id, int), (
        f"Expected an integer complaint id, got {complaint_id!r}"
    )
    return complaint_id


def _first_complaint_context(complaint_api: ComplaintClient) -> tuple[int, int, int, int]:
    """Return (complaint_id, club_id, recipient_id, sender_id) dynamically from the list."""
    complaint = _first_complaint(complaint_api)
    complaint_id = complaint["id"]
    club_id = (complaint.get("club") or {}).get("id", 1)
    recipient_id = (complaint.get("recipient") or {}).get("id", 1)
    sender_id = (complaint.get("user") or {}).get("id", 1)
    return complaint_id, club_id, recipient_id, sender_id


@allure.title("Complaint-API-01: GET /complaints returns 200 with a complaint list")
@allure.tag("api", "smoke", "complaint")
def test_complaints_list_returns_items(complaint_api: ComplaintClient) -> None:
    """The public complaints list must return a 200 response with a JSON list."""
    with allure.step("Request the full complaints list"):
        response = complaint_api.get_complaints()
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    with allure.step("Validate the response against the stored ComplaintsList schema"):
        payload = response.json()
        assert_response_matches(payload, "complaints_list", name="GET /complaints")

    with allure.step("Deserialize each item via ComplaintResponse.model_validate"):
        [ComplaintResponse.model_validate(item) for item in payload]


@allure.title("Complaint-API-02: GET /complaints/club/{id} returns 200 with a list")
@allure.tag("api", "smoke", "complaint")
def test_complaints_by_club_returns_items(complaint_api: ComplaintClient) -> None:
    """Complaints filtered by club id must return a 200 response with a JSON list."""
    _, club_id, _, _ = _first_complaint_context(complaint_api)

    with allure.step(
        "Validate the by-club payload against the stored ComplaintsList schema"
    ):
        response = complaint_api.get_complaints_by_club(club_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )
        payload = response.json()
        assert_response_matches(payload, "complaints_list", name="GET /complaints/club/{id}")


@allure.title("Complaint-API-03: GET /complaints/recipient/{id} returns 200 with a list")
@allure.tag("api", "smoke", "complaint")
def test_complaints_by_recipient_returns_items(complaint_api: ComplaintClient) -> None:
    """Complaints filtered by recipient id must return 200 with a JSON list."""
    _, _, recipient_id, _ = _first_complaint_context(complaint_api)

    with allure.step(
        "Validate the by-recipient payload against the stored ComplaintsList schema"
    ):
        response = complaint_api.get_complaints_by_recipient(recipient_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )
        payload = response.json()
        assert_response_matches(
            payload, "complaints_list", name="GET /complaints/recipient/{id}"
        )


@allure.title("Complaint-API-04: GET /complaints/sender/{id} returns 200 with a list")
@allure.tag("api", "smoke", "complaint")
def test_complaints_by_sender_returns_items(complaint_api: ComplaintClient) -> None:
    """Complaints filtered by sender id must return 200 with a JSON list."""
    _, _, _, sender_id = _first_complaint_context(complaint_api)

    with allure.step(
        "Validate the by-sender payload against the stored ComplaintsList schema"
    ):
        response = complaint_api.get_complaints_by_sender(sender_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )
        payload = response.json()
        assert_response_matches(
            payload, "complaints_list", name="GET /complaints/sender/{id}"
        )


@allure.title("Complaint-API-05: GET /complaint/{id} returns 200 for an existing complaint")
@allure.tag("api", "smoke", "complaint")
def test_get_complaint_by_id_returns_complaint(complaint_api: ComplaintClient) -> None:
    """An existing complaint must be fetchable by id without auth."""
    complaint_id = _first_complaint_id(complaint_api)

    with allure.step(f"Request complaint with id {complaint_id}"):
        response = complaint_api.get_complaint(complaint_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    with allure.step("Verify the returned complaint matches the requested id"):
        payload = response.json()
        assert payload["id"] == complaint_id, (
            "Returned complaint id should match the request"
        )

    with allure.step("Validate the complaint against the stored ComplaintResponse schema"):
        assert_response_matches(
            payload, "complaint_response", name=f"GET /complaint/{complaint_id}"
        )

    with allure.step("Deserialize the complaint into a ComplaintResponse model"):
        complaint = ComplaintResponse.model_validate(payload)
        assert complaint.id == complaint_id, (
            "Model id must match the requested complaint id"
        )


@allure.title("Complaint-API-06: GET /complaint/{id} returns 404 for a missing complaint")
@allure.tag("api", "smoke", "complaint")
def test_get_complaint_by_id_returns_404_for_missing(complaint_api: ComplaintClient) -> None:
    """A non-existent complaint id must yield a 404 response."""
    with allure.step(
        f"GET complaint with a non-existent id {NONEXISTENT_COMPLAINT_ID}"
    ):
        response = complaint_api.get_complaint(NONEXISTENT_COMPLAINT_ID)
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )


@allure.title("Complaint-API-07: DELETE /complaint/{id} requires authentication (401)")
@allure.tag("api", "smoke", "complaint", "security")
def test_delete_complaint_requires_authentication(complaint_api: ComplaintClient) -> None:
    """An anonymous caller must not be able to delete a complaint (401)."""
    complaint_id = _first_complaint_id(complaint_api)

    with allure.step(f"Request DELETE /complaint/{complaint_id} without a token"):
        response = complaint_api.delete_complaint(complaint_id)
        assert response.status_code == 401, (
            f"Anonymous delete should be rejected with 401, got {response.status_code}"
        )


@allure.title("Complaint-API-08: PUT /complaint/{id}/answer requires authentication (401)")
@allure.tag("api", "smoke", "complaint", "security")
def test_update_complaint_answer_requires_authentication(
    complaint_api: ComplaintClient,
) -> None:
    """PUT /complaint/{id}/answer must require an authenticated caller."""
    complaint_id = _first_complaint_id(complaint_api)
    payload: dict[str, Any] = {"answerText": "smoke answer"}

    with allure.step(
        f"PUT /complaint/{complaint_id}/answer with no token and an answer body"
    ):
        response = complaint_api.update_complaint_answer(complaint_id, payload)
        assert response.status_code == 401, (
            f"Anonymous answer-update should be rejected with 401, got "
            f"{response.status_code}"
        )


@allure.title("Complaint-API-09: PUT /complaint/isActive/{id} requires authentication (401)")
@allure.tag("api", "smoke", "complaint", "security")
def test_update_complaint_is_active_requires_authentication(
    complaint_api: ComplaintClient,
) -> None:
    """PUT /complaint/isActive/{id} must require an authenticated caller."""
    complaint_id = _first_complaint_id(complaint_api)
    payload: dict[str, Any] = {"isActive": True}

    with allure.step(
        f"PUT /complaint/isActive/{complaint_id} with no token and an isActive body"
    ):
        response = complaint_api.update_complaint_is_active(complaint_id, payload)
        assert response.status_code == 401, (
            f"Anonymous isActive-update should be rejected with 401, got "
            f"{response.status_code}"
        )


@allure.title("Complaint-API-10: POST /complaint requires authentication (401)")
@allure.tag("api", "smoke", "complaint", "security")
def test_create_complaint_requires_authentication(complaint_api: ComplaintClient) -> None:
    """An anonymous caller must not be able to create a complaint (401)."""
    _, club_id, recipient_id, _ = _first_complaint_context(complaint_api)
    payload = ComplaintProfile(
        text="Smoke test complaint text that has at least 40 characters for validation",
        userId=218,
        clubId=club_id,
        recipientId=recipient_id,
    ).model_dump(exclude_none=True)

    with allure.step("Validate the payload against the ComplaintProfile schema"):
        assert_response_matches(payload, "complaint_profile", name="POST /complaint payload")

    with allure.step("POST the schema-valid payload with no token"):
        response = complaint_api.create_complaint(payload)
        assert response.status_code == 401, (
            f"Anonymous POST must be rejected with 401, got {response.status_code}"
        )


@allure.title("Complaint-API-11: PUT /complaint/{id} requires authentication (401)")
@allure.tag("api", "smoke", "complaint", "security")
def test_update_complaint_requires_authentication(complaint_api: ComplaintClient) -> None:
    """An anonymous caller must not be able to update a complaint (401)."""
    complaint_id, club_id, recipient_id, _ = _first_complaint_context(complaint_api)
    payload = ComplaintProfile(
        text="Smoke test complaint text that has at least 40 characters for validation",
        userId=218,
        clubId=club_id,
        recipientId=recipient_id,
    ).model_dump(exclude_none=True)

    with allure.step("Validate the payload against the ComplaintProfile schema"):
        assert_response_matches(payload, "complaint_profile", name="PUT /complaint payload")

    with allure.step(f"PUT the schema-valid payload to /complaint/{complaint_id} with no token"):
        response = complaint_api.update_complaint(complaint_id, payload)
        assert response.status_code == 401, (
            f"Anonymous PUT must be rejected with 401, got {response.status_code}"
        )


@allure.title("Complaint-API-12: USER POST /complaint returns 200 with SuccessCreatedComplaint")
@allure.tag("api", "smoke", "complaint")
def test_create_complaint_authenticated_succeeds(
    complaint_api_user: tuple[ComplaintClient, str],
) -> None:
    """POST /complaint must succeed for an authenticated USER caller.

    The probe confirmed that both USER and MANAGER tokens can create a
    complaint. The response body matches the ``SuccessCreatedComplaint``
    schema (``id``/``userId``/``clubId``/``recipientId``/``hasAnswer``) and
    can be deserialized into the typed ``SuccessCreatedComplaint`` model.
    The body's ``userId`` must match the authenticated user's id — the
    backend rejects mismatched ids with 400.
    """
    api, user_id = complaint_api_user
    bootstrap = ComplaintClient(base_url=api.base_url)
    _, club_id, recipient_id, _ = _first_complaint_context(bootstrap)
    payload = ComplaintProfile(
        text="Smoke test complaint from authenticated USER - 40+ chars long text",
        userId=int(user_id),
        clubId=club_id,
        recipientId=recipient_id,
        isActive=True,
    ).model_dump(exclude_none=True)

    with allure.step("Validate the payload against the ComplaintProfile schema"):
        assert_response_matches(payload, "complaint_profile", name="POST /complaint payload")

    with allure.step("POST the payload with the USER token"):
        response = api.create_complaint(payload)
        assert response.status_code == 200, (
            f"Authenticated POST must succeed, got {response.status_code}"
        )

    with allure.step(
        "Validate the response against the stored SuccessCreatedComplaint schema"
    ):
        body = response.json()
        assert_response_matches(
            body, "success_created_complaint", name="POST /complaint response"
        )

    with allure.step(
        "Deserialize the response into SuccessCreatedComplaint.model_validate"
    ):
        created = SuccessCreatedComplaint.model_validate(body)
        assert created.id > 0, "Created complaint must have a positive id"
        assert created.hasAnswer is False, (
            "A freshly created complaint must have hasAnswer=False"
        )

    with allure.step(f"Delete the test complaint id={created.id} to keep state clean"):
        # Best-effort cleanup so probe runs do not pollute the public list.
        cleanup = api.delete_complaint(created.id)
        assert cleanup.status_code == 200, (
            f"Cleanup delete failed with {cleanup.status_code}; the test "
            f"complaint id={created.id} may still be visible in the list."
        )


@allure.title("Complaint-API-13: USER PUT /complaint/{id} returns 200")
@allure.tag("api", "smoke", "complaint")
def test_update_complaint_authenticated_succeeds(
    complaint_api_user: tuple[ComplaintClient, str],
) -> None:
    """PUT /complaint/{id} must succeed for an authenticated USER caller."""
    api, user_id = complaint_api_user
    bootstrap = ComplaintClient(base_url=api.base_url)
    complaint_id, club_id, recipient_id, _ = _first_complaint_context(bootstrap)
    payload = ComplaintProfile(
        text="Smoke test update text that has at least 40 characters for validation",
        userId=int(user_id),
        clubId=club_id,
        recipientId=recipient_id,
        isActive=True,
    ).model_dump(exclude_none=True)

    with allure.step("Validate the payload against the ComplaintProfile schema"):
        assert_response_matches(payload, "complaint_profile", name="PUT /complaint payload")

    with allure.step(
        f"PUT the schema-valid payload to /complaint/{complaint_id} with the USER token"
    ):
        response = api.update_complaint(complaint_id, payload)
        assert response.status_code == 200, (
            f"Authenticated PUT /complaint/{complaint_id} must succeed, got {response.status_code}"
        )

    with allure.step(
        "Validate the response against the stored ComplaintResponse schema"
    ):
        body = response.json()
        assert_response_matches(
            body, "complaint_response", name=f"PUT /complaint/{complaint_id} response"
        )


@allure.title("Complaint-API-14: USER PUT /complaint/{id}/answer returns 200")
@allure.tag("api", "smoke", "complaint")
def test_update_complaint_answer_authenticated_succeeds(
    complaint_api_user: tuple[ComplaintClient, str],
) -> None:
    """PUT /complaint/{id}/answer must succeed for an authenticated USER caller."""
    api, _ = complaint_api_user
    bootstrap = ComplaintClient(base_url=api.base_url)
    complaint_id = _first_complaint_id(bootstrap)
    payload: dict[str, Any] = {"answerText": "smoke answer from USER"}

    with allure.step(
        f"PUT /complaint/{complaint_id}/answer with the USER token"
    ):
        response = api.update_complaint_answer(complaint_id, payload)
        assert response.status_code == 200, (
            f"Authenticated answer-update must succeed, got {response.status_code}"
        )

    with allure.step(
        "Validate the response against the stored ComplaintResponse schema"
    ):
        body = response.json()
        assert_response_matches(
            body, "complaint_response", name="PUT /complaint/{id}/answer response"
        )

    with allure.step("The returned complaint must report hasAnswer=True"):
        updated = ComplaintResponse.model_validate(body)
        assert updated.id == complaint_id, "Updated complaint id should match"
        assert updated.hasAnswer is True, (
            "After answering, hasAnswer must be True"
        )


@allure.title("Complaint-API-15: USER PUT /complaint/isActive/{id} returns 200")
@allure.tag("api", "smoke", "complaint")
def test_update_complaint_is_active_authenticated_succeeds(
    complaint_api_user: tuple[ComplaintClient, str],
) -> None:
    """PUT /complaint/isActive/{id} must succeed for an authenticated USER caller."""
    api, _ = complaint_api_user
    bootstrap = ComplaintClient(base_url=api.base_url)
    complaint_id = _first_complaint_id(bootstrap)
    payload: dict[str, Any] = {"isActive": False}

    with allure.step(
        f"PUT /complaint/isActive/{complaint_id} with the USER token"
    ):
        response = api.update_complaint_is_active(complaint_id, payload)
        assert response.status_code == 200, (
            f"Authenticated isActive-update must succeed, got {response.status_code}"
        )

    with allure.step(
        "Validate the response against the stored ComplaintResponse schema"
    ):
        body = response.json()
        assert_response_matches(
            body, "complaint_response", name="PUT /complaint/isActive/{id} response"
        )

    with allure.step("The returned complaint must report isActive=False"):
        updated = ComplaintResponse.model_validate(body)
        assert updated.id == complaint_id, "Updated complaint id should match"
        assert updated.isActive is False, (
            "After flipping isActive to False, the returned complaint must "
            "report isActive=False"
        )


@allure.title("Complaint-API-16: USER DELETE /complaint/{id} returns 200 and removes the row")
@allure.tag("api", "smoke", "complaint")
def test_delete_complaint_authenticated_succeeds(
    complaint_api_user: tuple[ComplaintClient, str],
) -> None:
    """DELETE /complaint/{id} must succeed for an authenticated USER caller.

    The probe confirmed both USER and MANAGER can delete. The test creates
    a complaint, deletes it, then re-reads via the public list to confirm
    the row is gone.
    """
    api, user_id = complaint_api_user
    bootstrap = ComplaintClient(base_url=api.base_url)
    _, club_id, recipient_id, _ = _first_complaint_context(bootstrap)
    payload = ComplaintProfile(
        text="Smoke test delete me - this text must be at least forty characters long!",
        userId=int(user_id),
        clubId=club_id,
        recipientId=recipient_id,
        isActive=True,
    ).model_dump(exclude_none=True)

    with allure.step("Create the complaint that will be deleted"):
        create_response = api.create_complaint(payload)
        assert create_response.status_code == 200, (
            f"Setup POST failed with {create_response.status_code}; "
            f"the delete test cannot run"
        )
        created = SuccessCreatedComplaint.model_validate(create_response.json())
        assert created.id > 0, "Created complaint must have a positive id"

    with allure.step(f"DELETE /complaint/{created.id} with the USER token"):
        delete_response = api.delete_complaint(created.id)
        assert delete_response.status_code == 200, (
            f"Authenticated delete must succeed, got {delete_response.status_code}"
        )

    with allure.step(
        f"GET /complaint/{created.id} must now return 404 (the row is gone)"
    ):
        # The public read endpoint will return 404 for a deleted id.
        get_response = api.get_complaint(created.id)
        assert get_response.status_code == 404, (
            f"After delete, GET must return 404, got {get_response.status_code}"
        )


@allure.title("Complaint-API-17: ComplaintProfile preserves required fields and drops None")
@allure.tag("api", "smoke", "complaint")
def test_complaint_profile_preserves_fields() -> None:
    """ComplaintProfile.model_dump must keep every required field verbatim.

    The expected payload is a hand-written literal derived from the JSON
    Schema, not from re-reading the model, so the assertion can disagree
    with the model if a field is silently dropped or renamed.
    """
    profile = ComplaintProfile(
        text="Smoke test complaint text that is at least 40 characters in length",
        userId=218,
        clubId=368,
        recipientId=233,
    )

    with allure.step(
        "Dump the model with exclude_none=True and compare to the independent literal"
    ):
        actual = profile.model_dump(exclude_none=True)

    # Hand-written independent expected, derived from the JSON Schema.
    expected: dict[str, Any] = {
        "text": "Smoke test complaint text that is at least 40 characters in length",
        "userId": 218,
        "clubId": 368,
        "recipientId": 233,
    }
    assert actual == expected, (
        f"ComplaintProfile.model_dump must equal the schema-required literal, "
        f"got {actual!r}"
    )

    with allure.step("Validate the dumped payload against the ComplaintProfile schema"):
        assert_response_matches(
            actual, "complaint_profile", name="ComplaintProfile dump"
        )

    with allure.step(
        "Setting isActive=True must include the field, not silently drop it"
    ):
        active_payload = ComplaintProfile(
            text="x",
            userId=1,
            clubId=1,
            recipientId=1,
            isActive=True,
        ).model_dump(exclude_none=True)
        assert active_payload.get("isActive") is True, (
            "isActive=True must survive serialization"
        )
