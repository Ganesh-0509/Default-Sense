"""Ensure a working admin login exists.

Phase 1's SQL seed inserts user rows with placeholder password hashes (no real
password). This script sets a real bcrypt password on the demo admin so the auth
flow is usable. Idempotent: creates the admin if missing, otherwise updates the hash.

Usage:
    python -m app.scripts.seed_admin
Environment overrides:
    ADMIN_EMAIL     (default: admin@defaultsense.ai)
    ADMIN_PASSWORD  (default: ChangeMe123!)
"""

from __future__ import annotations

import os

from app.auth.security import hash_password
from app.database import SessionLocal
from app.models import User
from app.repositories import user_repository


def main() -> None:
    email = os.getenv("ADMIN_EMAIL", "admin@defaultsense.ai")
    password = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")

    db = SessionLocal()
    try:
        user = user_repository.get_by_email(db, email)
        if user is None:
            user = User(
                full_name="Asha Admin",
                email=email,
                password_hash=hash_password(password),
                role="admin",
                status="active",
            )
            action = "created"
        else:
            user.password_hash = hash_password(password)
            user.status = "active"
            action = "updated"
        user_repository.save(db, user)
        print(f"Admin {action}: {email} (password set from ADMIN_PASSWORD env or default).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
