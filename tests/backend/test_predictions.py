"""AI prediction serving tests — uses the trained model + seeded customers.

Requires models/train.py to have produced default_model.joblib.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.ai import predictor

# Seeded customers spanning the risk spectrum.
PRIYA = "c0000000-0000-0000-0000-000000000001"  # strong profile
IMRAN = "c0000000-0000-0000-0000-000000000006"  # weak profile (defaulted loan)
MODEL_READY = predictor.is_ready()

pytestmark = pytest.mark.skipif(not MODEL_READY, reason="Model not trained")

_VALID_TIERS = {"Low", "Moderate", "High", "Critical"}


def test_model_status(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/predictions/model", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["ready"] is True
    assert data["metrics"]["roc_auc"] >= 0.90  # locked-in target


def test_run_prediction_and_shap(client: TestClient, auth_headers: dict[str, str]) -> None:
    run = client.post(
        "/api/v1/predictions/run", json={"customer_id": IMRAN}, headers=auth_headers
    )
    assert run.status_code == 200, run.text
    data = run.json()["data"]
    assert 0 <= float(data["probability_of_default"]) <= 100
    assert data["risk_level"] in _VALID_TIERS
    assert data["recommendation"]
    pid = data["prediction_id"]

    # SHAP explanation stored + retrievable
    shap = client.get(f"/api/v1/predictions/{pid}/shap", headers=auth_headers)
    assert shap.status_code == 200
    drivers = shap.json()["data"]
    assert len(drivers) >= 1
    assert all(d["impact_direction"] in ("positive", "negative") for d in drivers)

    # /features alias returns the same contributions
    feats = client.get(f"/api/v1/predictions/{pid}/features", headers=auth_headers)
    assert feats.status_code == 200


def test_risk_ordering_weak_vs_strong(client: TestClient, auth_headers: dict[str, str]) -> None:
    weak = client.post(
        "/api/v1/predictions/run", json={"customer_id": IMRAN}, headers=auth_headers
    ).json()["data"]
    strong = client.post(
        "/api/v1/predictions/run", json={"customer_id": PRIYA}, headers=auth_headers
    ).json()["data"]
    # A defaulted, high-utilization borrower should score riskier than a prime one.
    assert float(weak["probability_of_default"]) > float(strong["probability_of_default"])


def test_customer_history_and_portfolio(client: TestClient, auth_headers: dict[str, str]) -> None:
    client.post("/api/v1/predictions/run", json={"customer_id": PRIYA}, headers=auth_headers)

    history = client.get(f"/api/v1/predictions/customer/{PRIYA}", headers=auth_headers)
    assert history.status_code == 200
    assert len(history.json()["data"]) >= 1

    portfolio = client.get("/api/v1/predictions/portfolio", headers=auth_headers)
    assert portfolio.status_code == 200
    assert portfolio.json()["data"]["total_predictions"] >= 1


def test_run_unknown_customer(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.post(
        "/api/v1/predictions/run",
        json={"customer_id": "00000000-0000-0000-0000-000000000000"},
        headers=auth_headers,
    )
    assert resp.status_code == 404
