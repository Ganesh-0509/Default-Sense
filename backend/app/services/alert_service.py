"""Alert business logic (docs/10 §13)."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert
from app.utils.responses import APIException


def list_alerts(db: Session, status: str | None = None) -> list[Alert]:
    stmt = select(Alert).order_by(Alert.generated_at.desc())
    if status:
        stmt = stmt.where(Alert.status == status)
    return list(db.execute(stmt).scalars().all())


def get_alert(db: Session, alert_id: uuid.UUID) -> Alert:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise APIException(404, "Alert not found.")
    return alert


def mark_read(db: Session, alert_id: uuid.UUID) -> Alert:
    alert = get_alert(db, alert_id)
    alert.status = "acknowledged"
    db.commit()
    db.refresh(alert)
    return alert
