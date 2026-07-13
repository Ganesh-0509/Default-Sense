"""Train the DefaultSense 12-month PD model (Phase 6).

Implements the committed 90% strategy (docs/03 §13, docs/18):
  - stratified train/val/test split
  - class imbalance handling: scale_pos_weight + SMOTE on the TRAIN fold only
  - XGBoost, probability calibration (isotonic on val), threshold tuning
  - full metric bundle (ROC-AUC, Recall, Accuracy, PR-AUC, F1, KS, Gini)
  - per-segment (loan-type) metrics
  - baseline (logistic, structured-only) vs full pipeline

Usage:  python models/train.py
Artifacts: models/saved_models/default_model.joblib + metrics.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Import the canonical feature builder from the backend so train/serve never drift.
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "backend"))
from app.ai.features import FEATURE_NAMES, STRUCTURED_ONLY, build_features  # noqa: E402

RANDOM_STATE = 42
DATA = REPO / "datasets" / "synthetic" / "defaultsense_dataset.csv"
OUT_DIR = REPO / "models" / "saved_models"


def _ks_gini(y_true, y_prob) -> tuple[float, float]:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    ks = float(np.max(tpr - fpr))
    gini = float(2 * roc_auc_score(y_true, y_prob) - 1)
    return round(ks, 4), round(gini, 4)


def _metrics(y_true, y_prob, threshold: float) -> dict:
    y_pred = (y_prob >= threshold).astype(int)
    ks, gini = _ks_gini(y_true, y_prob)
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_prob), 4),
        "pr_auc": round(average_precision_score(y_true, y_prob), 4),
        "ks": ks,
        "gini": gini,
    }


def _tune_threshold(y_true, y_prob, min_recall: float = 0.85) -> float:
    """Pick the threshold maximizing F1 while keeping recall >= min_recall."""
    best_thr, best_f1 = 0.5, -1.0
    for thr in np.linspace(0.05, 0.95, 91):
        y_pred = (y_prob >= thr).astype(int)
        rec = recall_score(y_true, y_pred, zero_division=0)
        if rec < min_recall:
            continue
        f1 = f1_score(y_true, y_pred, zero_division=0)
        if f1 > best_f1:
            best_f1, best_thr = f1, float(thr)
    if best_f1 < 0:  # recall target unreachable → fall back to best-F1 overall
        for thr in np.linspace(0.05, 0.95, 91):
            f1 = f1_score(y_true, (y_prob >= thr).astype(int), zero_division=0)
            if f1 > best_f1:
                best_f1, best_thr = f1, float(thr)
    return round(best_thr, 3)


def _tune_accuracy_threshold(y_true, y_prob) -> float:
    """Pick the threshold that maximizes accuracy (the balanced operating point)."""
    best_thr, best_acc = 0.5, -1.0
    for thr in np.linspace(0.05, 0.95, 91):
        acc = accuracy_score(y_true, (y_prob >= thr).astype(int))
        if acc > best_acc:
            best_acc, best_thr = acc, float(thr)
    return round(best_thr, 3)


def main() -> None:
    if not DATA.exists():
        raise SystemExit(f"Dataset not found: {DATA}. Run generate_synthetic.py first.")

    df = pd.read_csv(DATA)
    y = df["default"].to_numpy()

    # Build the model matrix via the shared feature builder.
    feats = pd.DataFrame([build_features(row) for row in df.to_dict("records")])[FEATURE_NAMES]
    X = feats.to_numpy()
    loan_type = df["loan_type"].to_numpy()

    # --- Stratified 70/15/15 split ---
    X_tmp, X_test, y_tmp, y_test, lt_tmp, lt_test = train_test_split(
        X, y, loan_type, test_size=0.15, stratify=y, random_state=RANDOM_STATE
    )
    val_frac = 0.15 / 0.85
    X_train, X_val, y_train, y_val = train_test_split(
        X_tmp, y_tmp, test_size=val_frac, stratify=y_tmp, random_state=RANDOM_STATE
    )

    # --- Class imbalance: scale_pos_weight + SMOTE on the TRAIN fold only ---
    pos = int(y_train.sum())
    neg = int(len(y_train) - pos)
    scale_pos_weight = neg / pos if pos else 1.0
    X_train_res, y_train_res = SMOTE(random_state=RANDOM_STATE).fit_resample(X_train, y_train)

    # --- Full model: XGBoost ---
    xgb = XGBClassifier(
        n_estimators=400,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.5,
        min_child_weight=2,
        scale_pos_weight=scale_pos_weight,
        eval_metric="auc",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    xgb.fit(X_train_res, y_train_res)

    # --- Probability calibration (isotonic) on the real (non-resampled) val fold ---
    # sklearn >=1.6 removed cv="prefit" in favor of FrozenEstimator; support both.
    try:
        from sklearn.frozen import FrozenEstimator

        calibrator = CalibratedClassifierCV(FrozenEstimator(xgb), method="isotonic")
    except ImportError:  # older sklearn
        calibrator = CalibratedClassifierCV(xgb, method="isotonic", cv="prefit")
    calibrator.fit(X_val, y_val)

    # --- Threshold tuning on val ---
    val_prob = calibrator.predict_proba(X_val)[:, 1]
    # Recall-first operating point (bank priority: catch defaulters early)
    threshold = _tune_threshold(y_val, val_prob, min_recall=0.85)
    # Balanced operating point (max accuracy) — reported alongside for the 90% figure
    balanced_threshold = _tune_accuracy_threshold(y_val, val_prob)

    # --- Evaluate on the held-out test set ---
    test_prob = calibrator.predict_proba(X_test)[:, 1]
    full_metrics = _metrics(y_test, test_prob, threshold)
    balanced_metrics = _metrics(y_test, test_prob, balanced_threshold)

    # Per-segment (loan type) metrics on test
    per_segment = {}
    for t in np.unique(lt_test):
        mask = lt_test == t
        if mask.sum() >= 20 and len(np.unique(y_test[mask])) > 1:
            per_segment[t] = _metrics(y_test[mask], test_prob[mask], threshold)

    # --- Baseline: logistic regression, structured-only features (before/after) ---
    struct_idx = [FEATURE_NAMES.index(f) for f in STRUCTURED_ONLY]
    scaler = StandardScaler().fit(X_train[:, struct_idx])
    base = LogisticRegression(max_iter=1000, class_weight="balanced")
    base.fit(scaler.transform(X_train[:, struct_idx]), y_train)
    base_prob = base.predict_proba(scaler.transform(X_test[:, struct_idx]))[:, 1]
    baseline_metrics = _metrics(y_test, base_prob, 0.5)

    # --- Persist artifacts ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    trained_at = datetime.now(timezone.utc).isoformat()
    artifact = {
        "xgb_model": xgb,
        "calibrator": calibrator,
        "threshold": threshold,
        "balanced_threshold": balanced_threshold,
        "feature_names": FEATURE_NAMES,
        "scale_pos_weight": scale_pos_weight,
        "default_rate": round(float(y.mean()), 4),
        "trained_at": trained_at,
        "metrics": full_metrics,
    }
    joblib.dump(artifact, OUT_DIR / "default_model.joblib")

    report = {
        "trained_at": trained_at,
        "model": "XGBoost (calibrated) + SMOTE + threshold tuning",
        "rows": int(len(df)),
        "default_rate": round(float(y.mean()), 4),
        "recall_first_threshold": threshold,
        "balanced_threshold": balanced_threshold,
        "scale_pos_weight": round(scale_pos_weight, 3),
        "full_pipeline_recall_first": full_metrics,
        "full_pipeline_balanced": balanced_metrics,
        "baseline_structured_only_test": baseline_metrics,
        "per_segment_test": per_segment,
        "targets": {"roc_auc": ">=0.90", "recall": ">=0.85", "accuracy": ">=0.90"},
    }
    (OUT_DIR / "metrics.json").write_text(json.dumps(report, indent=2))

    # --- Console summary ---
    print("=" * 62)
    print("DefaultSense PD model — test-set results")
    print("=" * 62)
    print(f"Rows: {len(df)} | default rate: {y.mean():.1%}")
    print(f"\nFULL PIPELINE — recall-first point (threshold {threshold}):")
    for k, v in full_metrics.items():
        print(f"  {k:>10}: {v}")
    print(f"\nFULL PIPELINE — balanced point (threshold {balanced_threshold}):")
    for k in ("accuracy", "recall", "precision", "f1"):
        print(f"  {k:>10}: {balanced_metrics[k]}")
    print("\nBASELINE (logistic, structured-only):")
    for k in ("roc_auc", "recall", "accuracy"):
        print(f"  {k:>10}: {baseline_metrics[k]}")
    print("\nTARGET CHECK — headline metric is ROC-AUC (docs/03 §13):")
    print(f"  ROC-AUC  >= 0.90 : {'PASS' if full_metrics['roc_auc'] >= 0.90 else 'MISS'} ({full_metrics['roc_auc']})  <- the '90%'")
    print(f"  Recall   >= 0.85 : {'PASS' if full_metrics['recall'] >= 0.85 else 'MISS'} ({full_metrics['recall']})")
    print(f"  Accuracy (balanced): {balanced_metrics['accuracy']}  [reported alongside — honest ceiling at ~30% prevalence]")
    print(f"  Uplift vs structured-only baseline AUC: +{round(full_metrics['roc_auc'] - baseline_metrics['roc_auc'], 4)}")
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
