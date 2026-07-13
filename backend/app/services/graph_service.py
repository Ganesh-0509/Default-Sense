"""Knowledge Graph business logic — relationship intelligence & risk propagation."""

from __future__ import annotations

import uuid

from app.graph import connection, queries
from app.utils.responses import APIException

_INDUSTRY_RISK_VALUE = {"Low": 20, "Moderate": 50, "High": 80}


def _ensure_available() -> None:
    if not connection.is_available():
        raise APIException(503, "Knowledge Graph (Neo4j) is not available.")


def _risk_level(score: float) -> str:
    if score <= 25:
        return "Low"
    if score <= 50:
        return "Moderate"
    if score <= 75:
        return "High"
    return "Critical"


def get_customer_graph(customer_id: uuid.UUID) -> dict:
    _ensure_available()
    exists = connection.run_read(queries.CUSTOMER_EXISTS, {"customer_id": str(customer_id)})
    if not exists:
        raise APIException(404, "Customer not found in the knowledge graph.")

    nodes, edges = connection.run_read_graph(
        queries.CUSTOMER_SUBGRAPH, {"customer_id": str(customer_id)}
    )
    return {
        "customer_id": str(customer_id),
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }


def get_customer_risk(customer_id: uuid.UUID) -> dict:
    _ensure_available()
    rows = connection.run_read(queries.CUSTOMER_RISK, {"customer_id": str(customer_id)})
    if not rows:
        raise APIException(404, "Customer not found in the knowledge graph.")
    row = rows[0]

    employer_risk = float(row.get("employer_risk") or 0)
    industry_risk_label = row.get("industry_risk")
    industry_value = _INDUSTRY_RISK_VALUE.get(industry_risk_label, 0)
    economic_events = [e for e in (row.get("economic_events") or []) if e]
    connected_borrowers = [c for c in (row.get("connected_borrowers") or []) if c]
    connected_defaulters = [c for c in (row.get("connected_defaulters") or []) if c]

    event_penalty = 15 if economic_events else 0
    defaulter_penalty = min(len(connected_defaulters) * 15, 30)

    score = (
        0.40 * employer_risk
        + 0.30 * industry_value
        + event_penalty
        + defaulter_penalty
    )
    score = round(min(max(score, 0), 100), 2)

    factors = []
    if employer_risk:
        factors.append(
            {"factor": "Employer risk", "detail": f"{row.get('employer')} ({employer_risk:.0f}/100)"}
        )
    if industry_value:
        factors.append(
            {"factor": "Industry risk", "detail": f"{row.get('industry')} ({industry_risk_label})"}
        )
    if economic_events:
        factors.append(
            {"factor": "Economic events", "detail": ", ".join(economic_events)}
        )
    if connected_defaulters:
        factors.append(
            {
                "factor": "Connected borrower defaults",
                "detail": f"{len(connected_defaulters)} via shared guarantor: "
                + ", ".join(connected_defaulters),
            }
        )

    return {
        "customer_id": str(customer_id),
        "customer": row.get("customer"),
        "employer": row.get("employer"),
        "employer_risk": employer_risk,
        "industry": row.get("industry"),
        "industry_risk": industry_risk_label,
        "region": row.get("region"),
        "economic_events": economic_events,
        "connected_borrowers": connected_borrowers,
        "connected_defaulters": connected_defaulters,
        "relationship_risk_score": score,
        "relationship_risk_level": _risk_level(score),
        "factors": factors,
    }


def search_nodes(q: str, limit: int = 25) -> list[dict]:
    _ensure_available()
    if not q or not q.strip():
        raise APIException(400, "Search query must not be empty.")
    return connection.run_read(queries.SEARCH_NODES, {"q": q.strip(), "limit": limit})


def status() -> dict:
    available = connection.is_available()
    return {"available": available, "engine": "neo4j"}
