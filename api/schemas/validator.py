"""Validation of API payloads against stored JSON Schema contracts.

The Speak Ukrainian backend documents its entities (the ``components.schemas``
of its OpenAPI/swagger spec). Instead of validating response bodies with ad-hoc
field checks in every test, we keep those contracts as plain JSON Schema files
under ``api/schemas/news/`` and check payloads against them here.

How it works
------------
1. Schemas are plain ``.json`` files (draft-07). A schema declares the expected
   shape with keywords such as ``type``, ``properties`` and ``required``, and can
   reference other schemas via ``$ref`` (for example ``news_list.json`` points at
   ``news_response.json``, which itself references ``user_preview.json``).

2. :func:`_load` reads a schema file from disk into a ``dict`` (caching it so the
   same file is parsed only once per process).

3. :func:`_build_registry` registers every schema file under its local URI so the
   ``$ref`` links resolve when validating any of them. Without this registry the
   validator would not know what ``user_preview.json`` means inside another file.

4. :func:`assert_response_matches` ties it together: it loads the requested
   schema, builds a ``jsonschema.Draft7Validator`` wired to that registry, runs
   the payload against it and, when validation fails, raises :class:`AssertionError`
   with a readable list of the offending JSON paths.

This centralises contract checks: adding a field to a response only requires
updating its schema file, and any test that validates against it is kept honest
with no per-test duplication.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator
from referencing import Registry

# Directory that holds the JSON schema contracts for the news API.
SCHEMAS_DIR = Path(__file__).parent / "news"

# Cache of loaded schema documents, keyed by file name, to avoid re-parsing the
# same file on every call.
_CACHE: dict[str, dict[str, Any]] = {}


def _load(schema_ref: str) -> dict[str, Any]:
    """Load a single schema document from disk and cache it.

    The caller may pass the schema with or without the ``.json`` extension (for
    example ``"news_response"`` or ``"news_response.json"``). The resolved file
    is read once and cached under its file name in ``_CACHE`` so repeated
    validation calls do not hit the file system again.

    Args:
        schema_ref: File name of a stored schema, optionally without ``.json``.

    Returns:
        The parsed JSON Schema document as a ``dict``.
    """
    name = Path(schema_ref).name
    if not name.endswith(".json"):
        name = f"{name}.json"
    if name not in _CACHE:
        path = SCHEMAS_DIR / name
        with path.open(encoding="utf-8") as handle:
            _CACHE[name] = json.load(handle)
    return _CACHE[name]


def _build_registry() -> Registry:
    """Register every schema file so ``$ref`` references resolve.

    Each schema stored in ``SCHEMAS_DIR`` is registered under a URI; we key it by
    both its ``$id`` (if present) and its file name. Registering under the file
    name is what lets a ``$ref`` such as ``user_preview.json`` inside
    ``news_response.json`` point at the right document.

    Returns:
        A :class:`referencing.Registry` that maps all local schema URIs to their
        documents, passable to a validator so cross-file references work.
    """
    pairs: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        doc = _load(path.name)
        pairs.append((doc.get("$id", path.name), doc))
        pairs.append((path.name, doc))
    return Registry().with_contents(pairs)


def assert_response_matches(
    payload: Any,
    schema: str | dict[str, Any],
    name: str = "response",
) -> None:
    """Assert that ``payload`` conforms to the given JSON schema.

    This is the main entry point used by tests. It takes the response body
    returned by the API, validates it against a stored (or inline) schema, and
    fails the test if the body does not match.

    Args:
        payload: The JSON object returned by the API to validate.
        schema: Either the file name of a stored schema (for example
            ``"news_response"``) or an inline schema ``dict``.
        name: Human-readable label used in the failure message, so it is clear
            which endpoint/payload the error refers to.

    Raises:
        AssertionError: If ``payload`` does not conform to the schema. The error
            message lists each offending JSON path together with the reason
            (for example ``[0]['date']: [2022, 10, 21] is not of type 'string'``).
    """
    if isinstance(schema, str):
        schema_doc = _load(schema)
    else:
        schema_doc = schema

    validator = Draft7Validator(schema=schema_doc, registry=_build_registry())
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))

    if errors:
        details = "\n".join(f"  {list(e.path)}: {e.message}" for e in errors)
        raise AssertionError(
            f"{name} does not match the schema {schema_doc.get('title', '<inline>')}:\n{details}"
        )
