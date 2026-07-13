"""Report endpoints (docs/10 §12)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import User
from app.services import report_service
from app.utils.responses import success

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/portfolio")
def portfolio(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(report_service.portfolio_report(db), message="Portfolio report.")


@router.get("/risk")
def risk(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return success(report_service.risk_report(db), message="Risk report.")


@router.get("/customer/{customer_id}")
def customer(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    return success(report_service.customer_report(db, customer_id), message="Customer report.")


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Response:
    data = report_service.portfolio_csv(db)
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=portfolio_report.csv"},
    )


@router.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Response:
    data = report_service.portfolio_pdf(db)
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=portfolio_report.pdf"},
    )
