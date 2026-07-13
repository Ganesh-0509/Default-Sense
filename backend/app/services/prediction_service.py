"""Prediction business logic — gathers multi-modal inputs, scores, and stores results."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai import predictor
from app.models import (
    AIPrediction,
    Customer,
    Loan,
    RepaymentHistory,
    ShapExplanation,
)
from app.services import graph_service
from app.utils.responses import APIException

_INDUSTRY_RISK_VALUE = {"Low": 20, "Moderate": 50, "High": 80}
_STRESS_KEYWORDS = ("down", "loss", "stress", "overdue", "decline", "default", "fell", "falling")


def _latest_loan(db: Session, customer_id: uuid.UUID, loan_id: uuid.UUID | None) -> Loan | None:
    if loan_id is not None:
        loan = db.get(Loan, loan_id)
        if loan is None or loan.customer_id != customer_id:
            raise APIException(404, "Loan not found for this customer.")
        return loan
    stmt = (
        select(Loan)
        .where(Loan.customer_id == customer_id)
        .order_by(Loan.created_at.desc())
        .limit(1)
    )
    return db.execute(stmt).scalars().first()


def _repayment_features(db: Session, customer_id: uuid.UUID) -> dict:
    stmt = (
        select(RepaymentHistory)
        .join(Loan, Loan.loan_id == RepaymentHistory.loan_id)
        .where(Loan.customer_id == customer_id)
        .order_by(RepaymentHistory.due_date)
    )
    reps = list(db.execute(stmt).scalars().all())
    missed = sum(1 for r in reps if r.payment_status == "Missed")
    late = sum(1 for r in reps if r.payment_status == "Late")
    delays = [int(r.delay_days or 0) for r in reps]
    avg_delay = sum(delays) / len(delays) if delays else 0.0
    trend = (delays[-1] - delays[0]) / len(delays) if len(delays) >= 2 else 0.0
    return {
        "missed_emi_count": missed,
        "late_payment_count": late,
        "avg_delay_days": round(avg_delay, 2),
        "delay_trend": round(trend, 3),
    }


def _graph_features(customer_id: uuid.UUID) -> dict:
    """Relationship features from Neo4j; degrade gracefully if unavailable."""
    try:
        risk = graph_service.get_customer_risk(customer_id)
        return {
            "employer_risk": risk.get("employer_risk") or 0,
            "industry_risk_value": _INDUSTRY_RISK_VALUE.get(risk.get("industry_risk"), 0),
            "connected_defaulters": len(risk.get("connected_defaulters") or []),
            "economic_event_flag": 1 if risk.get("economic_events") else 0,
        }
    except APIException:
        return {
            "employer_risk": 0,
            "industry_risk_value": 0,
            "connected_defaulters": 0,
            "economic_event_flag": 0,
        }


def _unstructured_features(db: Session, customer_id: uuid.UUID) -> dict:
    from sqlalchemy import text

    from app.models import Document, OCRResult

    # Average officer-note sentiment.
    sentiment = db.execute(
        text("SELECT AVG(sentiment_score) FROM loan_officer_notes WHERE customer_id = :cid"),
        {"cid": str(customer_id)},
    ).scalar()

    # OCR stress flag: any extracted text containing stress keywords.
    ocr_texts = (
        db.execute(
            select(OCRResult.extracted_text)
            .join(Document, Document.document_id == OCRResult.document_id)
            .where(Document.customer_id == customer_id)
        )
        .scalars()
        .all()
    )
    stress = any(t and any(k in t.lower() for k in _STRESS_KEYWORDS) for t in ocr_texts)
    return {
        "note_sentiment": float(sentiment) if sentiment is not None else 0.0,
        "ocr_stress_flag": 1 if stress else 0,
    }


def _gather_raw(db: Session, customer: Customer, loan: Loan | None) -> dict:
    raw: dict = {
        "credit_score": customer.credit_score,
        "annual_income": customer.annual_income,
    }
    if loan is not None:
        raw.update(
            {
                "loan_type": loan.loan_type,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "tenure_months": loan.tenure_months,
                "emi": loan.emi,
                "outstanding_amount": loan.outstanding_amount,
            }
        )

    # Credit history (utilization, active/overdue) + liabilities via raw SQL for brevity.
    from sqlalchemy import text

    ch = db.execute(
        text(
            "SELECT credit_utilization, active_loans, overdue_accounts "
            "FROM credit_history WHERE customer_id = :cid"
        ),
        {"cid": str(customer.customer_id)},
    ).mappings().first()
    if ch:
        raw.update(
            {
                "credit_utilization": ch["credit_utilization"],
                "active_loans": ch["active_loans"],
                "overdue_accounts": ch["overdue_accounts"],
            }
        )
    liabilities = db.execute(
        text(
            "SELECT COALESCE(SUM(monthly_payment), 0) FROM existing_liabilities "
            "WHERE customer_id = :cid"
        ),
        {"cid": str(customer.customer_id)},
    ).scalar()
    raw["monthly_liabilities"] = liabilities or 0

    raw.update(_repayment_features(db, customer.customer_id))
    raw.update(_unstructured_features(db, customer.customer_id))
    raw.update(_graph_features(customer.customer_id))
    return raw


def run_prediction(db: Session, customer_id: uuid.UUID, loan_id: uuid.UUID | None) -> AIPrediction:
    if not predictor.is_ready():
        raise APIException(503, "Prediction model is not trained. Run models/train.py.")
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise APIException(404, "Customer not found.")

    loan = _latest_loan(db, customer_id, loan_id)
    raw = _gather_raw(db, customer, loan)
    result = predictor.predict(raw)

    prediction = AIPrediction(
        customer_id=customer_id,
        loan_id=loan.loan_id if loan else None,
        probability_of_default=result["probability_of_default"],
        risk_level=result["risk_level"],
        confidence_score=result["confidence_score"],
        recommendation=result["recommendation"],
        model_version=result["model_version"],
    )
    db.add(prediction)
    db.flush()  # get prediction_id

    for driver in result["shap"]:
        db.add(
            ShapExplanation(
                prediction_id=prediction.prediction_id,
                feature_name=driver["feature_name"],
                contribution=driver["contribution"],
                impact_direction=driver["impact_direction"],
            )
        )
    db.commit()
    db.refresh(prediction)
    return prediction


def get_prediction(db: Session, prediction_id: uuid.UUID) -> AIPrediction:
    prediction = db.get(AIPrediction, prediction_id)
    if prediction is None:
        raise APIException(404, "Prediction not found.")
    return prediction


def list_for_customer(db: Session, customer_id: uuid.UUID) -> list[AIPrediction]:
    stmt = (
        select(AIPrediction)
        .where(AIPrediction.customer_id == customer_id)
        .order_by(AIPrediction.prediction_date.desc())
    )
    return list(db.execute(stmt).scalars().all())


def get_shap(db: Session, prediction_id: uuid.UUID) -> list[ShapExplanation]:
    get_prediction(db, prediction_id)
    stmt = select(ShapExplanation).where(ShapExplanation.prediction_id == prediction_id)
    return list(db.execute(stmt).scalars().all())


def portfolio_summary(db: Session) -> dict:
    """Distribution of the latest predictions across risk tiers."""
    rows = db.execute(
        select(AIPrediction.risk_level, func.count()).group_by(AIPrediction.risk_level)
    ).all()
    distribution = {level: count for level, count in rows}
    total = sum(distribution.values())
    avg_pd = db.execute(select(func.avg(AIPrediction.probability_of_default))).scalar()
    return {
        "total_predictions": total,
        "risk_distribution": distribution,
        "average_pd": round(float(avg_pd), 2) if avg_pd is not None else None,
        "high_or_critical": distribution.get("High", 0) + distribution.get("Critical", 0),
    }
