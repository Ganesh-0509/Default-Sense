"""Prediction + SHAP schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PredictionRunRequest(BaseModel):
    customer_id: uuid.UUID
    loan_id: uuid.UUID | None = None


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prediction_id: uuid.UUID
    customer_id: uuid.UUID
    loan_id: uuid.UUID | None
    prediction_date: datetime
    probability_of_default: Decimal
    risk_level: str
    confidence_score: Decimal | None
    recommendation: str | None
    model_version: str | None


class ShapOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shap_id: uuid.UUID
    prediction_id: uuid.UUID
    feature_name: str
    contribution: Decimal
    impact_direction: str
