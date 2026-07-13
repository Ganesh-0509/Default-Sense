"""Aggregate router mounting all v1 endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.api import (
    alerts,
    auth,
    customers,
    dashboard,
    documents,
    graph,
    loans,
    predictions,
    reports,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(customers.router)
api_router.include_router(loans.router)
api_router.include_router(documents.router)
api_router.include_router(graph.router)
api_router.include_router(predictions.router)
api_router.include_router(dashboard.router)
api_router.include_router(alerts.router)
api_router.include_router(reports.router)
