"""Authentication endpoints (docs/10 §4)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.auth import ChangePasswordRequest, LoginRequest, UserOut
from app.services import auth_service
from app.utils.responses import success

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user, token, expires_in = auth_service.authenticate(db, payload.email, payload.password)
    return success(
        {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": expires_in,
            "user": UserOut.model_validate(user),
        },
        message="Login successful.",
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)) -> dict:
    # Stateless JWT: logout is client-side (discard token). Endpoint provided for symmetry.
    return success(message="Logged out. Please discard your access token.")


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)) -> dict:
    return success(UserOut.model_validate(current_user), message="Current user profile.")


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    auth_service.change_password(db, current_user, payload.current_password, payload.new_password)
    return success(message="Password changed successfully.")
