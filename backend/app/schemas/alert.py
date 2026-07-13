"""Alert schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: uuid.UUID
    customer_id: uuid.UUID
    prediction_id: uuid.UUID | None
    severity: str
    alert_type: str
    description: str | None
    status: str
    generated_at: datetime
