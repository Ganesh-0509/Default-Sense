# 18_AI_Training_Pipeline.md

# DefaultSense AI

### AI Training & Prediction Pipeline

**Version:** 2.0
**Document Type:** AI Training Pipeline

---

# 1. Objective

This document defines the end-to-end Machine Learning workflow for **DefaultSense AI**, enabling prediction of the **Probability of Default (PD)** up to **12 months in advance** using structured and unstructured data.

---

# 2. Pipeline Overview

```text
Raw Datasets

↓

Data Cleaning

↓

Feature Engineering

↓

Feature Selection

↓

Train / Validation / Test Split

↓

Model Training

↓

Model Evaluation

↓

Model Selection

↓

SHAP Explainability

↓

Save Model

↓

Prediction API
```

---

# 3. Data Sources

### Structured Data

* Customer Profile
* Loan Details
* Credit History
* Repayment History
* Transaction History

### Unstructured Data

* OCR Documents
* Loan Officer Notes
* Financial Statements

### Relationship Data

* Employer
* Industry
* Region
* Guarantor
* Connected Borrowers

---

# 4. Data Preprocessing

Perform:

* Remove duplicates
* Handle missing values
* Encode categorical variables
* Normalize numerical values
* Remove invalid records

**Class imbalance handling (required — key lever for the 90% target):**

* Compute the negative/positive class ratio and set XGBoost `scale_pos_weight` accordingly.
* Apply **SMOTE (or SMOTE-ENN) to the training fold ONLY, strictly after the train/test split**.
* ⚠️ **Never resample before splitting** — synthetic samples leaking into the test set produce fake ~99% scores that collapse in a real demo and destroy credibility.

---

# 5. Feature Engineering

Financial Features

* Debt-to-Income Ratio
* EMI Burden
* Credit Utilization
* Outstanding Balance

Behavioural Features

* EMI Delay Count
* Missed Payments
* Average Monthly Balance

Unstructured Features

* Sentiment Score
* Risk Keywords
* Financial Stress Indicators

Graph Features

* Employer Risk Score
* Industry Risk Score
* Connected Borrower Defaults

---

# 6. Train / Validation / Test Split

| Dataset    | Percentage |
| ---------- | ---------: |
| Training   |        70% |
| Validation |        15% |
| Testing    |        15% |

* Use a **stratified** split so the default rate is preserved across all three sets.
* Resampling (SMOTE) and scaler fitting happen **only on the training fold, after this split** (see Section 4).

---

# 7. Model Training

Recommended Model

* XGBoost Classifier (with `scale_pos_weight` set for imbalance)

Alternative / Ensemble Models

* LightGBM
* CatBoost
* Random Forest
* Logistic Regression (**Baseline** — structured-only, used for the before/after comparison)

**Training practices required to reach the 90% target:**

* **Ensemble/stack** XGBoost + LightGBM + CatBoost for the final model.
* **Hyperparameter tuning with Optuna.**
* **Stratified k-fold cross-validation** for honest, non-cherry-picked scores.
* **Threshold tuning** — select the operating threshold that meets the Recall ≥ 85% target (do not use the default 0.5 cutoff).
* **Probability calibration** (isotonic or Platt) so the output PD is a trustworthy probability, not just a ranking.

---

# 8. Model Evaluation

Evaluate using the **committed target bundle** (see `03_AI_ML_Design.md` §13):

| Metric | Target | Role |
| --- | --- | --- |
| **ROC-AUC** | **≥ 0.90** | Headline "90%" number |
| **Recall (defaulters)** | **≥ 85%** | Proves stress is actually caught |
| **Accuracy** | **≥ 90%** | Reported beside Recall, never alone |
| PR-AUC, F1, KS/Gini | Report | Imbalance-aware + banker-standard |
| Confusion Matrix | Report | At the tuned threshold |

Also report the **full bundle per loan type and per borrower segment**, and produce the **baseline (logistic, structured-only) vs full-pipeline** comparison as the demo narrative.

**Credibility guardrail:** target ROC-AUC in the **0.90–0.94** band. 0.98–0.99 signals leakage/overfitting — investigate the pipeline rather than reporting it.

Primary goal:

* High Recall for default cases
* Balanced Precision
* Strong, calibrated ROC-AUC

---

# 9. Explainable AI

Use **SHAP** to generate:

* Feature Importance
* Local Explanations
* Global Explanations
* Prediction Breakdown

Example Output

```text
Probability of Default : 81%

Top Contributors

Debt-to-Income Ratio

Late EMI Payments

Employer Risk

Credit Utilization
```

---

# 10. Model Saving

Save:

* Trained Model (`.pkl` or `.joblib`)
* Feature Encoder
* Scaler
* Feature List
* SHAP Explainer

---

# 11. Prediction Pipeline

```text
Customer Data

↓

Preprocessing

↓

Feature Engineering

↓

Graph Features

↓

Load Trained Model

↓

Predict PD

↓

Generate SHAP Explanation

↓

Recommendation Engine

↓

Return Prediction
```

---

# 12. Model Retraining

Retrain when:

* New repayment data is available
* Model accuracy decreases
* New loan products are introduced
* Economic conditions change significantly

---

# 13. AI Deliverables

* Data preprocessing pipeline
* Feature engineering pipeline
* Trained XGBoost model
* SHAP explainability module
* Prediction pipeline
* Model evaluation report
* Saved production model
* API-ready inference workflow

---

# 14. Success Criteria

The AI pipeline is considered complete when it can:

* Process structured and unstructured data.
* Generate a **12-month Probability of Default** prediction.
* Produce SHAP explanations for every prediction.
* Support different loan types and borrower profiles.
* Integrate seamlessly with the FastAPI backend for real-time inference.
* **Meet the target bundle: ROC-AUC ≥ 0.90, Recall (defaulters) ≥ 85%, Accuracy ≥ 90%**, reported per segment, with a baseline-vs-full comparison — and validated free of data leakage.
