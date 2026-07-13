"""AI Prediction + Explainable AI endpoints (docs/10 §8-9)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai import predictor
from app.auth.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models import User
from app.schemas.prediction import PredictionOut, PredictionRunRequest, ShapOut
from app.services import prediction_service
from app.utils.responses import success

router = APIRouter(prefix="/predictions", tags=["AI Predictions"])


@router.get("/model")
def model_status(_: User = Depends(get_current_user)) -> dict:
    return success(predictor.model_info(), message="Model status.")


@router.get("/portfolio")
def portfolio(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    return success(prediction_service.portfolio_summary(db), message="Portfolio risk summary.")


@router.post("/run")
def run_prediction(
    payload: PredictionRunRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    prediction = prediction_service.run_prediction(db, payload.customer_id, payload.loan_id)
    return success(PredictionOut.model_validate(prediction), message="Prediction generated.")


@router.get("/customer/{customer_id}")
def customer_history(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    predictions = prediction_service.list_for_customer(db, customer_id)
    return success(
        [PredictionOut.model_validate(p) for p in predictions],
        message="Customer prediction history.",
    )


@router.get("/{prediction_id}")
def get_prediction(
    prediction_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    prediction = prediction_service.get_prediction(db, prediction_id)
    return success(PredictionOut.model_validate(prediction), message="Prediction details.")


@router.get("/{prediction_id}/shap")
def get_shap(
    prediction_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    shap_rows = prediction_service.get_shap(db, prediction_id)
    return success([ShapOut.model_validate(s) for s in shap_rows], message="SHAP explanation.")


# Alias required by docs/10 §9 (feature contributions == SHAP contributions).
@router.get("/{prediction_id}/features")
def get_features(
    prediction_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    shap_rows = prediction_service.get_shap(db, prediction_id)
    return success([ShapOut.model_validate(s) for s in shap_rows], message="Feature contributions.")
