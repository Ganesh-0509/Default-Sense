"""Dashboard endpoints (docs/10 §11)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import User
from app.services import dashboard_service
from app.utils.responses import success

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(dashboard_service.summary(db), message="KPI summary.")


@router.get("/risk-distribution")
def risk_distribution(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(dashboard_service.risk_distribution(db), message="Risk distribution.")


@router.get("/high-risk")
def high_risk(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(dashboard_service.high_risk_borrowers(db), message="High-risk borrowers.")


@router.get("/trends")
def trends(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(dashboard_service.trends(db), message="Portfolio trends.")
