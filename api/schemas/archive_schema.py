"""JSON schemas for Archive API responses."""

ARCHIVE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "id",
            "className",
            "data",
        ],
        "properties": {
            "id": {
                "type": "integer",
            },
            "className": {
                "type": "string",
            },
            "data": {
                "type": "string",
            },
        },
        "additionalProperties": True,
    },
}