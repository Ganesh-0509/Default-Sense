"""Canonical feature engineering — shared by training and serving.

Both the training pipeline (models/) and the live predictor (backend) build the
model input vector through `build_features`, so the two can never drift. Raw inputs
span all four intelligence layers (structured, behavioural, unstructured, graph).
"""

from __future__ import annotations

LOAN_TYPES = ["Personal", "Home", "MSME", "Agriculture", "Education"]

# Model input vector, in a fixed order. Serving and training MUST agree on this.
FEATURE_NAMES = [
    # --- Structured / financial ---
    "credit_score",
    "loan_to_income",
    "emi_to_income",
    "interest_rate",
    "tenure_months",
    "outstanding_ratio",
    "credit_utilization",
    "active_loans",
    "overdue_accounts",
    "dti",
    # --- Behavioural / temporal ---
    "missed_emi_count",
    "late_payment_count",
    "avg_delay_days",
    "delay_trend",
    # --- Unstructured (OCR / NLP) ---
    "note_sentiment",
    "ocr_stress_flag",
    # --- Relationship (graph) ---
    "employer_risk",
    "industry_risk_value",
    "connected_defaulters",
    "economic_event_flag",
    # --- Loan type (one-hot) ---
    *[f"loan_type_{t}" for t in LOAN_TYPES],
]

# Structured-only subset — used for the baseline (before/after) comparison.
STRUCTURED_ONLY = [
    "credit_score",
    "loan_to_income",
    "emi_to_income",
    "interest_rate",
    "tenure_months",
    "outstanding_ratio",
    "credit_utilization",
    "active_loans",
    "overdue_accounts",
    "dti",
]


def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def build_features(raw: dict) -> dict[str, float]:
    """Turn a raw record (all four modalities) into the named feature vector.

    Missing keys default to safe zeros so serving is robust to sparse data.
    """
    income = float(raw.get("annual_income") or 0)
    loan_amount = float(raw.get("loan_amount") or 0)
    emi = float(raw.get("emi") or 0)
    monthly_liabilities = float(raw.get("monthly_liabilities") or 0)

    features: dict[str, float] = {
        "credit_score": float(raw.get("credit_score") or 0),
        "loan_to_income": _safe_div(loan_amount, income),
        "emi_to_income": _safe_div(emi * 12, income),
        "interest_rate": float(raw.get("interest_rate") or 0),
        "tenure_months": float(raw.get("tenure_months") or 0),
        "outstanding_ratio": _safe_div(raw.get("outstanding_amount") or 0, loan_amount),
        "credit_utilization": float(raw.get("credit_utilization") or 0),
        "active_loans": float(raw.get("active_loans") or 0),
        "overdue_accounts": float(raw.get("overdue_accounts") or 0),
        "dti": _safe_div((monthly_liabilities + emi) * 12, income),
        "missed_emi_count": float(raw.get("missed_emi_count") or 0),
        "late_payment_count": float(raw.get("late_payment_count") or 0),
        "avg_delay_days": float(raw.get("avg_delay_days") or 0),
        "delay_trend": float(raw.get("delay_trend") or 0),
        "note_sentiment": float(raw.get("note_sentiment") or 0),
        "ocr_stress_flag": float(raw.get("ocr_stress_flag") or 0),
        "employer_risk": float(raw.get("employer_risk") or 0),
        "industry_risk_value": float(raw.get("industry_risk_value") or 0),
        "connected_defaulters": float(raw.get("connected_defaulters") or 0),
        "economic_event_flag": float(raw.get("economic_event_flag") or 0),
    }

    loan_type = raw.get("loan_type")
    for t in LOAN_TYPES:
        features[f"loan_type_{t}"] = 1.0 if loan_type == t else 0.0

    return features


def to_vector(features: dict[str, float], names: list[str] | None = None) -> list[float]:
    """Order a feature dict into a plain list following FEATURE_NAMES (or a subset)."""
    order = names or FEATURE_NAMES
    return [float(features.get(name, 0.0)) for name in order]
