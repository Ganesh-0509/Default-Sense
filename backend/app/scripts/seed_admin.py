"""Ensure working demo logins exist.

Phase 1's SQL seed inserts user rows with placeholder password hashes (no real
password). This script sets real bcrypt passwords on the seeded accounts so the
auth flow is usable out of the box. Idempotent: creates each account if missing,
otherwise updates the hash + status.

Seeds two accounts:
  * Admin        — full access incl. user/admin surface.
  * Demo Reviewer — role `risk_manager`: every business flow (view, create
    customers/loans, predictions, SHAP, documents, alerts, reports). Intended
    for hackathon judges to click in and explore without signing up.

Usage:
    python -m app.scripts.seed_admin
Environment overrides (admin only):
    ADMIN_EMAIL     (default: admin@defaultsense.ai)
    ADMIN_PASSWORD  (default: ChangeMe123!)
    DEMO_EMAIL      (default: demo@defaultsense.ai)
    DEMO_PASSWORD   (default: Demo@1234)
"""

from __future__ import annotations

import os

from app.auth.security import hash_password
from app.database import SessionLocal
from app.models import User
from app.repositories import user_repository


def _upsert_user(db, *, full_name: str, email: str, password: str, role: str) -> str:
    """Create the user if absent, else reset password/status. Returns the action taken."""
    user = user_repository.get_by_email(db, email)
    if user is None:
        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            status="active",
        )
        action = "created"
    else:
        user.password_hash = hash_password(password)
        user.role = role
        user.status = "active"
        action = "updated"
    user_repository.save(db, user)
    return action


def main() -> None:
    accounts = [
        {
            "full_name": "Asha Admin",
            "email": os.getenv("ADMIN_EMAIL", "admin@defaultsense.ai"),
            "password": os.getenv("ADMIN_PASSWORD", "ChangeMe123!"),
            "role": "admin",
        },
        {
            "full_name": "Demo Reviewer",
            "email": os.getenv("DEMO_EMAIL", "demo@defaultsense.ai"),
            "password": os.getenv("DEMO_PASSWORD", "Demo@1234"),
            "role": "risk_manager",
        },
    ]

    db = SessionLocal()
    try:
        for acct in accounts:
            action = _upsert_user(db, **acct)
            print(f"User {action}: {acct['email']} (role={acct['role']}).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
