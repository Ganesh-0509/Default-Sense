"""FastAPI dependencies for authentication and role-based access control."""

from __future__ import annotations

import uuid
from collections.abc import Callable

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.config import settings
from app.database import get_db
from app.models import User
from app.utils.responses import APIException

# tokenUrl is informational for Swagger's "Authorize" button.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Resolve the authenticated user from the bearer token."""
    unauthorized = APIException(401, "Invalid or expired authentication token.")
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise unauthorized
        user_id = uuid.UUID(subject)
    except (jwt.PyJWTError, ValueError):
        raise unauthorized

    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    if user.status != "active":
        raise APIException(403, "User account is not active.")
    return user


def require_roles(*allowed_roles: str) -> Callable[[User], User]:
    """Dependency factory enforcing that the current user has one of the roles."""

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if allowed_roles and current_user.role not in allowed_roles:
            raise APIException(
                403,
                "You do not have permission to perform this action.",
                {"required_roles": list(allowed_roles), "your_role": current_user.role},
            )
        return current_user

    return checker
