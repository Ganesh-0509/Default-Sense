"""Pytest fixtures for backend integration tests.

Requires the Phase 1 databases to be running. Uses the real app + DB.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Make the backend package importable.
BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402
from app.scripts.seed_admin import main as seed_admin  # noqa: E402

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@defaultsense.ai")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")


@pytest.fixture(scope="session", autouse=True)
def _ensure_admin() -> None:
    """Guarantee a working admin login before any test runs."""
    seed_admin()


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_headers(client: TestClient) -> dict[str, str]:
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
