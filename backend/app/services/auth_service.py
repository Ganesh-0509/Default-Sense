"""Authentication business logic."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.auth.security import create_access_token, hash_password, verify_password
from app.config import settings
from app.models import User
from app.repositories import user_repository
from app.utils.responses import APIException


def authenticate(db: Session, email: str, password: str) -> tuple[User, str, int]:
    """Validate credentials and return (user, access_token, expires_in_seconds)."""
    user = user_repository.get_by_email(db, email)
    # Verify even when user is missing? We short-circuit but return a generic message
    # to avoid leaking which emails exist.
    if user is None or not verify_password(password, user.password_hash):
        raise APIException(401, "Invalid email or password.")
    if user.status != "active":
        raise APIException(403, "User account is not active.")

    token = create_access_token(subject=user.user_id, role=user.role)
    return user, token, settings.access_token_expire_minutes * 60


def change_password(db: Session, user: User, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.password_hash):
        raise APIException(400, "Current password is incorrect.")
    if verify_password(new_password, user.password_hash):
        raise APIException(400, "New password must be different from the current password.")
    user.password_hash = hash_password(new_password)
    user_repository.save(db, user)
