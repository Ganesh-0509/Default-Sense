"""Report business logic — JSON reports + CSV/PDF export (docs/10 §12)."""

from __future__ import annotations

import csv
import io
import uuid

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models import AIPrediction, Customer, Loan
from app.services import dashboard_service, prediction_service
from app.utils.responses import APIException


def customer_report(db: Session, customer_id: uuid.UUID) -> dict:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise APIException(404, "Customer not found.")

    loans = db.execute(select(Loan).where(Loan.customer_id == customer_id)).scalars().all()
    predictions = prediction_service.list_for_customer(db, customer_id)
    latest = predictions[0] if predictions else None
    shap = prediction_service.get_shap(db, latest.prediction_id) if latest else []

    return {
        "customer": {
            "customer_id": str(customer.customer_id),
            "customer_name": customer.customer_name,
            "employment_type": customer.employment_type,
            "credit_score": customer.credit_score,
            "annual_income": float(customer.annual_income) if customer.annual_income else None,
            "region": customer.region,
        },
        "loans": [
            {
                "loan_id": str(l.loan_id),
                "loan_type": l.loan_type,
                "loan_amount": float(l.loan_amount),
                "loan_status": l.loan_status,
                "outstanding_amount": float(l.outstanding_amount),
            }
            for l in loans
        ],
        "latest_prediction": (
            {
                "probability_of_default": float(latest.probability_of_default),
                "risk_level": latest.risk_level,
                "confidence_score": float(latest.confidence_score) if latest.confidence_score else None,
                "recommendation": latest.recommendation,
                "prediction_date": latest.prediction_date.isoformat(),
            }
            if latest
            else None
        ),
        "risk_drivers": [
            {
                "feature_name": s.feature_name,
                "contribution": float(s.contribution),
                "impact_direction": s.impact_direction,
            }
            for s in shap
        ],
    }


def portfolio_report(db: Session) -> dict:
    return {
        "summary": dashboard_service.summary(db),
        "risk_distribution": dashboard_service.risk_distribution(db)["distribution"],
        "high_risk": dashboard_service.high_risk_borrowers(db, limit=50),
    }


def risk_report(db: Session) -> dict:
    return {"high_risk": dashboard_service.high_risk_borrowers(db, limit=100)}


# ---------- Exports ----------

_PORTFOLIO_ROWS_SQL = """
SELECT c.customer_name, c.employment_type, c.credit_score, c.region,
       p.probability_of_default, p.risk_level, p.recommendation
FROM (
    SELECT DISTINCT ON (customer_id) customer_id, probability_of_default,
           risk_level, recommendation, prediction_date
    FROM ai_predictions
    ORDER BY customer_id, prediction_date DESC
) p
JOIN customers c ON c.customer_id = p.customer_id
ORDER BY p.probability_of_default DESC
"""


def portfolio_csv(db: Session) -> bytes:
    rows = db.execute(text(_PORTFOLIO_ROWS_SQL)).mappings().all()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Customer", "Employment", "Credit Score", "Region", "PD (%)", "Risk Level", "Recommendation"]
    )
    for r in rows:
        writer.writerow(
            [
                r["customer_name"],
                r["employment_type"],
                r["credit_score"],
                r["region"],
                float(r["probability_of_default"]),
                r["risk_level"],
                r["recommendation"],
            ]
        )
    return buffer.getvalue().encode("utf-8")


def portfolio_pdf(db: Session) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    summary = dashboard_service.summary(db)
    dist = dashboard_service.risk_distribution(db)["distribution"]
    high = dashboard_service.high_risk_borrowers(db, limit=25)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="DefaultSense Portfolio Report")
    styles = getSampleStyleSheet()
    story = [
        Paragraph("DefaultSense AI — Portfolio Risk Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(
            f"Customers: {summary['total_customers']} &nbsp;|&nbsp; "
            f"Loans: {summary['total_loans']} &nbsp;|&nbsp; "
            f"High-risk borrowers: {summary['high_risk_borrowers']} &nbsp;|&nbsp; "
            f"Average PD: {summary['average_pd']}",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph("Risk Distribution", styles["Heading2"]),
    ]

    dist_table = Table(
        [["Low", "Moderate", "High", "Critical"],
         [dist["Low"], dist["Moderate"], dist["High"], dist["Critical"]]]
    )
    dist_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    story += [dist_table, Spacer(1, 18), Paragraph("Top High-Risk Borrowers", styles["Heading2"])]

    data = [["Customer", "PD (%)", "Risk", "Recommendation"]]
    for r in high:
        data.append(
            [r["customer_name"], r["probability_of_default"], r["risk_level"], r["recommendation"]]
        )
    if len(data) == 1:
        data.append(["(none)", "-", "-", "-"])
    risk_table = Table(data, colWidths=[150, 60, 70, 180])
    risk_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(risk_table)

    doc.build(story)
    return buffer.getvalue()
