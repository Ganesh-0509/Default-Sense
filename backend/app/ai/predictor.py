"""Serving-side predictor: loads the trained artifact and scores a raw record.

Produces a 12-month PD, risk tier, recommendation, confidence, and SHAP-based
top risk drivers — using the same feature builder as training (app.ai.features).
"""

from __future__ import annotations

import threading
from pathlib import Path

import joblib
import numpy as np
import shap

from app.ai.features import FEATURE_NAMES, build_features, to_vector
from app.config import settings

_lock = threading.Lock()
_state: dict = {"artifact": None, "explainer": None}


def _model_path() -> Path:
    """Resolve the saved-model path (config override, else repo/models/saved_models)."""
    if settings.model_path:
        candidate = Path(settings.model_path)
        if candidate.is_absolute() and (candidate / "default_model.joblib").exists():
            return candidate / "default_model.joblib"
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "models" / "saved_models" / "default_model.joblib"


def is_ready() -> bool:
    return _model_path().exists()


def _load() -> dict:
    """Lazily load the artifact + SHAP explainer once."""
    if _state["artifact"] is None:
        with _lock:
            if _state["artifact"] is None:
                path = _model_path()
                if not path.exists():
                    raise FileNotFoundError(
                        f"Trained model not found at {path}. Run models/train.py."
                    )
                artifact = joblib.load(path)
                _state["artifact"] = artifact
                _state["explainer"] = shap.TreeExplainer(artifact["xgb_model"])
    return _state["artifact"]


def _risk_tier(pd_score: float) -> tuple[str, str]:
    """Map a 0-100 PD to (risk_level, recommendation) per docs/03 §12."""
    if pd_score <= 25:
        return "Low", "Approve"
    if pd_score <= 50:
        return "Moderate", "Approve with Monitoring"
    if pd_score <= 75:
        return "High", "Additional Verification"
    return "Critical", "Reject / Escalate"


def predict(raw: dict, top_k: int = 6) -> dict:
    """Score a raw multi-modal record. Returns PD, risk, recommendation, SHAP drivers."""
    artifact = _load()
    features = build_features(raw)
    vector = np.array([to_vector(features, artifact["feature_names"])], dtype=float)

    prob = float(artifact["calibrator"].predict_proba(vector)[0, 1])
    pd_score = round(prob * 100, 2)
    risk_level, recommendation = _risk_tier(pd_score)
    confidence = round(50 + abs(prob - 0.5) * 100, 2)  # 50 (uncertain) .. 100 (certain)

    # SHAP contributions on the underlying tree model.
    shap_values = _state["explainer"].shap_values(vector)
    contributions = np.array(shap_values)[0]
    order = np.argsort(np.abs(contributions))[::-1][:top_k]
    drivers = [
        {
            "feature_name": artifact["feature_names"][i],
            "contribution": round(float(contributions[i]), 5),
            "impact_direction": "positive" if contributions[i] >= 0 else "negative",
        }
        for i in order
    ]

    return {
        "probability_of_default": pd_score,
        "prediction_horizon": "12 Months",
        "risk_level": risk_level,
        "confidence_score": confidence,
        "recommendation": recommendation,
        "model_version": f"xgboost-{artifact.get('trained_at', 'v1')[:10]}",
        "shap": drivers,
    }


def model_info() -> dict:
    ready = is_ready()
    info = {"ready": ready, "feature_count": len(FEATURE_NAMES)}
    if ready:
        artifact = _load()
        info.update(
            {
                "trained_at": artifact.get("trained_at"),
                "metrics": artifact.get("metrics"),
                "default_rate": artifact.get("default_rate"),
            }
        )
    return info
