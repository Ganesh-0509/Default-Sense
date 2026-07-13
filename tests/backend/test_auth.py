"""Auth flow + envelope tests."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_login_success(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@defaultsense.ai", "password": "ChangeMe123!"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["role"] == "admin"


def test_login_wrong_password(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@defaultsense.ai", "password": "wrong-password"},
    )
    assert resp.status_code == 401
    body = resp.json()
    assert body["success"] is False
    assert "errors" in body


def test_profile_requires_auth(client: TestClient) -> None:
    resp = client.get("/api/v1/auth/profile")
    assert resp.status_code == 401


def test_profile_with_token(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/auth/profile", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == "admin@defaultsense.ai"
