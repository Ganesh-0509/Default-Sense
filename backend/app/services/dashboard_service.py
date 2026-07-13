"""Dashboard aggregation logic (docs/10 §11)."""

from __future__ import annotations

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.models import AIPrediction, Alert, Customer, Loan

# Latest prediction per customer (Postgres DISTINCT ON).
_LATEST_PER_CUSTOMER = """
SELECT DISTINCT ON (customer_id)
       customer_id, probability_of_default, risk_level, recommendation, prediction_date
FROM ai_predictions
ORDER BY customer_id, prediction_date DESC
"""


def summary(db: Session) -> dict:
    total_customers = db.execute(select(func.count()).select_from(Customer)).scalar_one()
    total_loans = db.execute(select(func.count()).select_from(Loan)).scalar_one()
    active_loans = db.execute(
        select(func.count()).select_from(Loan).where(Loan.loan_status == "Active")
    ).scalar_one()
    at_risk_loans = db.execute(
        select(func.count()).select_from(Loan).where(Loan.loan_status.in_(["Overdue", "Defaulted"]))
    ).scalar_one()

    latest = db.execute(text(_LATEST_PER_CUSTOMER)).mappings().all()
    high_risk = sum(1 for r in latest if r["risk_level"] in ("High", "Critical"))
    avg_pd = (
        round(sum(float(r["probability_of_default"]) for r in latest) / len(latest), 2)
        if latest
        else None
    )
    open_alerts = db.execute(
        select(func.count()).select_from(Alert).where(Alert.status == "open")
    ).scalar_one()

    return {
        "total_customers": total_customers,
        "total_loans": total_loans,
        "active_loans": active_loans,
        "at_risk_loans": at_risk_loans,
        "high_risk_borrowers": high_risk,
        "average_pd": avg_pd,
        "open_alerts": open_alerts,
        "customers_scored": len(latest),
    }


def risk_distribution(db: Session) -> dict:
    latest = db.execute(text(_LATEST_PER_CUSTOMER)).mappings().all()
    dist = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
    for r in latest:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    return {"distribution": dist, "total": len(latest)}


def high_risk_borrowers(db: Session, limit: int = 20) -> list[dict]:
    rows = db.execute(text(_LATEST_PER_CUSTOMER)).mappings().all()
    high = [r for r in rows if r["risk_level"] in ("High", "Critical")]
    high.sort(key=lambda r: float(r["probability_of_default"]), reverse=True)
    out = []
    for r in high[:limit]:
        customer = db.get(Customer, r["customer_id"])
        out.append(
            {
                "customer_id": str(r["customer_id"]),
                "customer_name": customer.customer_name if customer else "—",
                "probability_of_default": float(r["probability_of_default"]),
                "risk_level": r["risk_level"],
                "recommendation": r["recommendation"],
            }
        )
    return out


def trends(db: Session) -> list[dict]:
    """Prediction volume + average PD by month."""
    rows = db.execute(
        text(
            "SELECT to_char(date_trunc('month', prediction_date), 'YYYY-MM') AS month, "
            "COUNT(*) AS predictions, ROUND(AVG(probability_of_default), 2) AS avg_pd "
            "FROM ai_predictions GROUP BY 1 ORDER BY 1"
        )
    ).mappings().all()
    return [
        {"month": r["month"], "predictions": r["predictions"], "avg_pd": float(r["avg_pd"])}
        for r in rows
    ]
