"""Generate a synthetic multi-modal loan dataset for training (Phase 6).

Follows docs/12 §7.1: real learnable signal across all four intelligence layers,
a realistic-but-learnable default rate (~30%), and enough noise that a strong model
lands in the credible 0.90-0.94 ROC-AUC band (not a leaky 0.99).

Usage:  python models/generate_synthetic.py [n_rows]
Output: datasets/synthetic/defaultsense_dataset.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

LOAN_TYPES = ["Personal", "Home", "MSME", "Agriculture", "Education"]
SEED = 42

# Per-loan-type priors (income scale, rate, tenure) → borrower/segment realism.
TYPE_PRIORS = {
    "Personal": dict(income=(700_000, 0.35), rate=(14, 2.5), tenure=(36, 12)),
    "Home": dict(income=(1_600_000, 0.30), rate=(8.7, 1.0), tenure=(220, 40)),
    "MSME": dict(income=(2_200_000, 0.45), rate=(12, 2.0), tenure=(72, 24)),
    "Agriculture": dict(income=(400_000, 0.40), rate=(9.5, 1.5), tenure=(36, 12)),
    "Education": dict(income=(600_000, 0.35), rate=(10.5, 1.5), tenure=(60, 18)),
}


def generate(n_rows: int = 8000) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []

    for _ in range(n_rows):
        loan_type = rng.choice(LOAN_TYPES, p=[0.30, 0.20, 0.20, 0.15, 0.15])
        prior = TYPE_PRIORS[loan_type]

        credit_score = float(np.clip(rng.normal(680, 90), 300, 900))
        annual_income = float(max(80_000, rng.lognormal(np.log(prior["income"][0]), prior["income"][1])))
        loan_amount = float(max(30_000, annual_income * rng.uniform(0.4, 3.0)))
        interest_rate = float(np.clip(rng.normal(*prior["rate"]), 5, 22))
        tenure_months = int(np.clip(rng.normal(*prior["tenure"]), 6, 300))
        emi = float(loan_amount * (interest_rate / 1200 + 1 / tenure_months))
        outstanding_amount = float(loan_amount * rng.uniform(0.2, 1.0))
        credit_utilization = float(np.clip(rng.normal(45, 22), 0, 100))
        active_loans = int(rng.poisson(1.4))
        overdue_accounts = int(rng.poisson(0.4))
        monthly_liabilities = float(annual_income / 12 * rng.uniform(0.0, 0.35))
        missed_emi_count = int(rng.poisson(0.6))
        late_payment_count = int(rng.poisson(1.0))
        avg_delay_days = float(max(0, rng.normal(6, 8)))
        delay_trend = float(rng.normal(0, 0.6))
        note_sentiment = float(np.clip(rng.normal(0.1, 0.5), -1, 1))
        ocr_stress_flag = int(rng.random() < 0.18)
        employer_risk = float(np.clip(rng.normal(45, 22), 0, 100))
        industry_risk_value = float(rng.choice([20, 50, 80], p=[0.4, 0.35, 0.25]))
        connected_defaulters = int(rng.poisson(0.3))
        economic_event_flag = int(rng.random() < 0.20)

        rows.append(
            dict(
                loan_type=loan_type,
                credit_score=round(credit_score),
                annual_income=round(annual_income, 2),
                loan_amount=round(loan_amount, 2),
                interest_rate=round(interest_rate, 2),
                tenure_months=tenure_months,
                emi=round(emi, 2),
                outstanding_amount=round(outstanding_amount, 2),
                credit_utilization=round(credit_utilization, 2),
                active_loans=active_loans,
                overdue_accounts=overdue_accounts,
                monthly_liabilities=round(monthly_liabilities, 2),
                missed_emi_count=missed_emi_count,
                late_payment_count=late_payment_count,
                avg_delay_days=round(avg_delay_days, 2),
                delay_trend=round(delay_trend, 3),
                note_sentiment=round(note_sentiment, 3),
                ocr_stress_flag=ocr_stress_flag,
                employer_risk=round(employer_risk, 1),
                industry_risk_value=industry_risk_value,
                connected_defaulters=connected_defaulters,
                economic_event_flag=economic_event_flag,
            )
        )

    df = pd.DataFrame(rows)

    # --- Latent default risk: a weighted blend of the real signals (all 4 layers) ---
    # Behavioural, unstructured and graph signals carry extra weight so that a
    # structured-only baseline genuinely underperforms the full multi-modal model.
    dti = ((df.monthly_liabilities + df.emi) * 12) / df.annual_income
    loan_to_income = df.loan_amount / df.annual_income
    structured = (
        -0.020 * (df.credit_score - 650)
        + 2.0 * loan_to_income
        + 2.5 * dti
        + 0.020 * df.credit_utilization
        + 0.50 * df.overdue_accounts
    )
    behavioural = (
        0.70 * df.missed_emi_count
        + 0.35 * df.late_payment_count
        + 0.030 * df.avg_delay_days
        + 1.8 * df.delay_trend
    )
    unstructured = -1.6 * df.note_sentiment + 1.3 * df.ocr_stress_flag
    graph = (
        0.030 * df.employer_risk
        + 0.020 * df.industry_risk_value
        + 1.1 * df.connected_defaulters
        + 1.1 * df.economic_event_flag
    )
    score = structured + behavioural + unstructured + graph

    # Standardize, add noise (controls separability → AUC band), calibrate base rate.
    rng = np.random.default_rng(SEED + 1)
    z = (score - score.mean()) / score.std()
    noise = rng.normal(0, 0.40, size=len(df))  # noise tuned for a credible ~0.90-0.94 AUC
    logit = 3.45 * z + noise - 1.95  # signal + intercept tuned for ~25% default rate
    prob = 1 / (1 + np.exp(-logit))
    df["default"] = (rng.random(len(df)) < prob).astype(int)

    return df


def main() -> None:
    n_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    df = generate(n_rows)

    out_dir = Path(__file__).resolve().parent.parent / "datasets" / "synthetic"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "defaultsense_dataset.csv"
    df.to_csv(out_path, index=False)

    rate = df["default"].mean()
    print(f"Wrote {len(df)} rows to {out_path}")
    print(f"Default rate: {rate:.1%}  (target ~25-35%)")


if __name__ == "__main__":
    main()
