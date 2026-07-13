"""Customer + loan endpoint tests (against seeded Phase 1 data)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_customers_has_seed(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/customers", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] >= 6  # 6 seeded customers
    assert len(data["items"]) >= 6


def test_customer_crud_roundtrip(client: TestClient, auth_headers: dict[str, str]) -> None:
    # Create
    payload = {
        "customer_name": "Test Roundtrip",
        "employment_type": "Salaried",
        "annual_income": 500000,
        "credit_score": 700,
        "email": "roundtrip@example.com",
        "phone": "+91-9999900001",
    }
    created = client.post("/api/v1/customers", json=payload, headers=auth_headers)
    assert created.status_code == 201, created.text
    cid = created.json()["data"]["customer_id"]

    # Duplicate email → 409
    dup = client.post("/api/v1/customers", json=payload, headers=auth_headers)
    assert dup.status_code == 409

    # Read
    got = client.get(f"/api/v1/customers/{cid}", headers=auth_headers)
    assert got.status_code == 200
    assert got.json()["data"]["customer_name"] == "Test Roundtrip"

    # Update
    upd = client.put(
        f"/api/v1/customers/{cid}", json={"credit_score": 750}, headers=auth_headers
    )
    assert upd.status_code == 200
    assert upd.json()["data"]["credit_score"] == 750

    # Search
    found = client.get("/api/v1/customers/search?q=Roundtrip", headers=auth_headers)
    assert found.status_code == 200
    assert any(c["customer_id"] == cid for c in found.json()["data"])

    # Delete
    deleted = client.delete(f"/api/v1/customers/{cid}", headers=auth_headers)
    assert deleted.status_code == 200

    # Confirm gone
    missing = client.get(f"/api/v1/customers/{cid}", headers=auth_headers)
    assert missing.status_code == 404


def test_invalid_credit_score_rejected(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.post(
        "/api/v1/customers",
        json={"customer_name": "Bad Score", "credit_score": 9999},
        headers=auth_headers,
    )
    assert resp.status_code == 422  # Pydantic validation (300-900)


def test_list_loans_and_repayments(client: TestClient, auth_headers: dict[str, str]) -> None:
    loans = client.get("/api/v1/loans", headers=auth_headers)
    assert loans.status_code == 200
    items = loans.json()["data"]["items"]
    assert len(items) >= 6

    loan_id = items[0]["loan_id"]
    reps = client.get(f"/api/v1/loans/{loan_id}/repayments", headers=auth_headers)
    assert reps.status_code == 200
    assert isinstance(reps.json()["data"], list)


def test_create_loan_unknown_customer(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.post(
        "/api/v1/loans",
        json={
            "customer_id": "00000000-0000-0000-0000-000000000000",
            "loan_type": "Personal",
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure_months": 24,
            "emi": 5000,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 404
