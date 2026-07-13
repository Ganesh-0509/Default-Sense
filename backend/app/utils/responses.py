"""Helpers for the consistent API response envelope (docs/10 §3)."""

from __future__ import annotations

from typing import Any

from fastapi.encoders import jsonable_encoder


def success(data: Any = None, message: str = "Request completed successfully.") -> dict[str, Any]:
    """Build a success envelope: {success, message, data}."""
    return {"success": True, "message": message, "data": jsonable_encoder(data)}


def error(message: str = "Request failed.", errors: Any = None) -> dict[str, Any]:
    """Build an error envelope: {success, message, errors}."""
    return {"success": False, "message": message, "errors": jsonable_encoder(errors)}


class APIException(Exception):
    """Domain-level exception carrying an HTTP status and message.

    Raised by services; converted to the error envelope by the global handler.
    """

    def __init__(self, status_code: int, message: str, errors: Any = None) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors
        super().__init__(message)
