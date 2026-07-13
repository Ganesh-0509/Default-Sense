"""Shared response schemas — the consistent API envelope (docs/10 §3)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Request completed successfully."
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = "Request failed."
    errors: Any | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
