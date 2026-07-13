"""Dashboard, alerts, and reports endpoint tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.ai import predictor

PRIYA = "c0000000-0000-0000-0000-000000000001"
IMRAN = "c0000000-0000-0000-0000-000000000006"


@pytest.fixture(scope="module", autouse=True)
def _seed_predictions(client: TestClient, auth_headers: dict[str, str]) -> None:
    """Ensure some predictions exist so dashboards have data."""
    if predictor.is_ready():
        for cid in (PRIYA, IMRAN):
            client.post("/api/v1/predictions/run", json={"customer_id": cid}, headers=auth_headers)


def test_dashboard_summary(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_customers"] >= 6
    assert "high_risk_borrowers" in data
    assert "open_alerts" in data


def test_risk_distribution(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/dashboard/risk-distribution", headers=auth_headers)
    assert resp.status_code == 200
    dist = resp.json()["data"]["distribution"]
    assert set(dist.keys()) == {"Low", "Moderate", "High", "Critical"}


def test_high_risk_and_trends(client: TestClient, auth_headers: dict[str, str]) -> None:
    assert client.get("/api/v1/dashboard/high-risk", headers=auth_headers).status_code == 200
    assert client.get("/api/v1/dashboard/trends", headers=auth_headers).status_code == 200


def test_alerts_list_and_mark_read(client: TestClient, auth_headers: dict[str, str]) -> None:
    listing = client.get("/api/v1/alerts", headers=auth_headers)
    assert listing.status_code == 200
    alerts = listing.json()["data"]
    assert len(alerts) >= 1  # 3 seeded alerts

    alert_id = alerts[0]["alert_id"]
    read = client.put(f"/api/v1/alerts/{alert_id}/read", headers=auth_headers)
    assert read.status_code == 200
    assert read.json()["data"]["status"] == "acknowledged"


def test_alerts_status_filter(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/alerts?status=open", headers=auth_headers)
    assert resp.status_code == 200
    assert all(a["status"] == "open" for a in resp.json()["data"])


def test_reports_portfolio_and_customer(client: TestClient, auth_headers: dict[str, str]) -> None:
    portfolio = client.get("/api/v1/reports/portfolio", headers=auth_headers)
    assert portfolio.status_code == 200
    assert "summary" in portfolio.json()["data"]

    customer = client.get(f"/api/v1/reports/customer/{PRIYA}", headers=auth_headers)
    assert customer.status_code == 200
    assert customer.json()["data"]["customer"]["customer_id"] == PRIYA


def test_export_csv(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/reports/export/csv", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")
    assert b"Customer" in resp.content


def test_export_pdf(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/reports/export/pdf", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:4] == b"%PDF"  # valid PDF header
