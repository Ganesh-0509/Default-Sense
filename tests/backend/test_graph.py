"""Knowledge Graph tests — run against the Phase 1 Neo4j seed.

Requires Neo4j running (docker compose) with the seed loaded.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.graph import connection

# Seeded customers (mirror the PostgreSQL UUIDs).
PRIYA = "c0000000-0000-0000-0000-000000000001"  # low risk (IT employer)
ROHIT = "c0000000-0000-0000-0000-000000000004"  # high risk (manufacturing, shared guarantor)
GRAPH_UP = connection.is_available()

pytestmark = pytest.mark.skipif(not GRAPH_UP, reason="Neo4j not available")


def test_graph_status(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/graph/status", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["engine"] == "neo4j"


def test_customer_graph(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(f"/api/v1/graph/customer/{ROHIT}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["node_count"] > 0
    assert data["edge_count"] > 0
    labels = {n["label"] for n in data["nodes"]}
    # Rohit works for a manufacturer → Employer + Industry should appear.
    assert "Customer" in labels
    assert "Employer" in labels


def test_customer_graph_unknown(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(
        "/api/v1/graph/customer/00000000-0000-0000-0000-000000000000", headers=auth_headers
    )
    assert resp.status_code == 404


def test_risk_high_for_rohit(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(f"/api/v1/graph/risk/{ROHIT}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["industry"] == "Manufacturing"
    assert data["employer_risk"] >= 70
    # Rohit shares a guarantor with a defaulted borrower (Imran).
    assert len(data["connected_defaulters"]) >= 1
    assert data["relationship_risk_level"] in ("High", "Critical")


def test_risk_low_for_priya(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(f"/api/v1/graph/risk/{PRIYA}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["relationship_risk_score"] < data.get("employer_risk", 0) + 50
    assert data["relationship_risk_level"] in ("Low", "Moderate")


def test_graph_search(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/graph/search?q=Manufacturing", headers=auth_headers)
    assert resp.status_code == 200
    results = resp.json()["data"]
    assert any(r["name"] == "Manufacturing" for r in results)
