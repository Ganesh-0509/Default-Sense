"""Knowledge Graph endpoints (docs/10 §10)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.models import User
from app.services import graph_service
from app.utils.responses import success

router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])


@router.get("/status")
def graph_status(_: User = Depends(get_current_user)) -> dict:
    return success(graph_service.status(), message="Knowledge graph status.")


@router.get("/search")
def search_graph(
    q: str = Query(..., min_length=1, description="Name or id fragment"),
    limit: int = Query(25, ge=1, le=100),
    _: User = Depends(get_current_user),
) -> dict:
    results = graph_service.search_nodes(q, limit)
    return success(results, message="Graph search results.")


@router.get("/customer/{customer_id}")
def customer_graph(
    customer_id: uuid.UUID,
    _: User = Depends(get_current_user),
) -> dict:
    graph = graph_service.get_customer_graph(customer_id)
    return success(graph, message="Customer relationship graph.")


@router.get("/risk/{customer_id}")
def customer_risk(
    customer_id: uuid.UUID,
    _: User = Depends(get_current_user),
) -> dict:
    risk = graph_service.get_customer_risk(customer_id)
    return success(risk, message="Relationship risk analysis.")
