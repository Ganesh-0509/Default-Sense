"""Alert endpoints (docs/10 §13)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models import User
from app.schemas.alert import AlertOut
from app.services import alert_service
from app.utils.responses import success

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
def list_alerts(
    status: str | None = Query(None, description="Filter by status (open/acknowledged/…)"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    alerts = alert_service.list_alerts(db, status)
    return success([AlertOut.model_validate(a) for a in alerts], message="Alerts.")


@router.get("/{alert_id}")
def get_alert(
    alert_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    alert = alert_service.get_alert(db, alert_id)
    return success(AlertOut.model_validate(alert), message="Alert details.")


@router.put("/{alert_id}/read")
def mark_read(
    alert_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    alert = alert_service.mark_read(db, alert_id)
    return success(AlertOut.model_validate(alert), message="Alert marked as read.")
