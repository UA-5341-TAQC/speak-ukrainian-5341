"""Validation of API payloads against stored JSON Schema contracts.

The Speak Ukrainian backend documents its entities (the ``components.schemas``
of its OpenAPI/swagger spec). Instead of validating response bodies with ad-hoc
field checks in every test, we keep those contracts as plain JSON Schema files
under ``api/schemas/<resource>/`` (one subdirectory per resource, for example
``api/schemas/news/`` or ``api/schemas/complaint/``) and check payloads against
them here.

How it works
------------
1. Schemas are plain ``.json`` files (draft-07). A schema declares the expected
   shape with keywords such as ``type``, ``properties`` and ``required``, and can
   reference other schemas via ``$ref`` (for example ``complaints_list.json``
   points at ``complaint_response.json``, which itself references
   ``user_preview.json``).

2. :func:`_load` reads a schema file from disk into a ``dict`` (caching it so the
   same file is parsed only once per process). The ``schema_ref`` argument may
   be either a bare file name (``"complaint_profile"``) or a subdirectory path
   (``"complaint/complaint_profile"``); both forms resolve correctly.

3. :func:`_build_registry` registers every schema file in every resource
   subdirectory under its local URI so the ``$ref`` links resolve when
   validating any of them. Without this registry the validator would not know
   what ``user_preview.json`` means inside another file.

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

# Root directory that holds per-resource JSON schema subdirectories (for example
# ``news/`` and ``complaint/``).
SCHEMAS_ROOT = Path(__file__).parent

# Cache of loaded schema documents, keyed by relative file path (for example
# ``complaint/complaint_profile.json``) so each file is parsed only once per
# process regardless of which subdirectory it lives in.
_CACHE: dict[str, dict[str, Any]] = {}


def _resolve_path(schema_ref: str) -> Path:
    """Resolve a ``schema_ref`` string to an absolute ``.json`` file on disk.

    The caller may pass either a bare file name (``"complaint_profile"`` or
    ``"complaint_profile.json"``) — in which case the file is looked up in any
    resource subdirectory — or a subdirectory-prefixed path
    (``"complaint/complaint_profile"``). When the same file name exists in more
    than one subdirectory, the first match in sorted order wins.

    Args:
        schema_ref: File name or subdirectory-prefixed file name of a stored
            schema, optionally without the ``.json`` extension.

    Returns:
        The absolute :class:`Path` to the schema document on disk.

    Raises:
        FileNotFoundError: If the schema cannot be located.
    """
    raw = schema_ref.strip()
    if not raw.endswith(".json"):
        raw = f"{raw}.json"

    candidate = (SCHEMAS_ROOT / raw).resolve()
    if candidate.is_file():
        return candidate

    bare = Path(raw).name
    for path in sorted(SCHEMAS_ROOT.glob(f"*/{bare}")):
        return path.resolve()

    raise FileNotFoundError(f"Schema file not found: {schema_ref}")


def _load(schema_ref: str) -> dict[str, Any]:
    """Load a single schema document from disk and cache it.

    Args:
        schema_ref: File name or subdirectory-prefixed file name of a stored
            schema, optionally without ``.json``.

    Returns:
        The parsed JSON Schema document as a ``dict``.
    """
    path = _resolve_path(schema_ref)
    cache_key = path.relative_to(SCHEMAS_ROOT).as_posix()
    if cache_key not in _CACHE:
        with path.open(encoding="utf-8") as handle:
            _CACHE[cache_key] = json.load(handle)
    return _CACHE[cache_key]


def _build_registry() -> Registry:
    """Register every schema file so ``$ref`` references resolve.

    Each schema under every per-resource subdirectory is registered under a
    URI derived from its file path (for example
    ``api/schemas/complaint/complaint_response.json``). With those URIs, a
    bare ``$ref`` such as ``user_preview.json`` written inside
    ``complaint_response.json`` resolves to its sibling in the same directory
    (``complaint/user_preview.json``) without colliding with another
    resource's file of the same name (for example
    ``news/user_preview.json``).

    Returns:
        A :class:`referencing.Registry` that maps all local schema URIs to their
        documents, passable to a validator so cross-file references work.
    """
    pairs: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(SCHEMAS_ROOT.glob("*/*.json")):
        rel_path = path.relative_to(SCHEMAS_ROOT).as_posix()
        doc = _load(rel_path)
        # Register under three keys so the validator can find the doc via any
        # of: (a) the path URI used by ``$ref`` resolution, (b) the schema's
        # declared ``$id``, or (c) a bare filename fallback (only safe when
        # the basename is unique across resources).
        uri = f"file:///{rel_path}"
        pairs.append((uri, doc))
        pairs.append((rel_path, doc))
        pairs.append((doc.get("$id", rel_path), doc))
        if not any(
            other.resolve() != path.resolve() for other in SCHEMAS_ROOT.glob(f"*/{path.name}")
        ):
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
            ``"complaint_profile"`` or ``"complaint/complaint_profile"``) or an
            inline schema ``dict``.
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
