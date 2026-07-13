# 03_AI_ML_Design.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** AI & Machine Learning Design

---

# 1. Objective

The AI Engine is the core intelligence of **DefaultSense AI**. Its objective is to accurately estimate the **Probability of Default (PD)** for the next **12 months** by combining structured banking data, unstructured intelligence, and relationship-based insights into a single explainable prediction.

Unlike conventional systems that rely only on structured financial data, DefaultSense AI integrates multiple information sources to improve prediction quality and provide transparent decision support.

---

# 2. AI Architecture

```text
                    DEFAULTSENSE AI

            ┌─────────────────────────┐
            │ Structured Data Engine  │
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Unstructured AI Engine  │
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Relationship Intelligence│
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Feature Engineering Hub │
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Loan Specific AI Models │
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Borrower Adaptation     │
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Ensemble Decision Engine│
            └────────────┬────────────┘
                         │
            ┌────────────▼────────────┐
            │ Explainable AI (SHAP)   │
            └────────────┬────────────┘
                         │
                  12-Month PD Prediction
```

---

# 3. AI Objectives

The AI engine must:

* Predict loan default **12 months in advance**.
* Support different loan products.
* Adapt to different borrower profiles.
* Combine structured and unstructured information.
* Explain every prediction.
* Generate actionable recommendations.

---

# 4. Multi-Modal Data Sources

## A. Structured Banking Data

Used for financial analysis.

Includes:

* Customer Profile
* Credit Score
* Loan Amount
* Loan Tenure
* Interest Rate
* Repayment History
* EMI History
* Transaction History
* Income
* Existing Liabilities
* Account Balance
* Branch Details

---

## B. Unstructured Data

Used to improve contextual understanding.

Sources:

* Loan Officer Remarks
* OCR Extracted Financial Statements
* Customer Declarations
* Employer News
* Industry News
* Business Registration Documents
* Income Tax Statements (OCR)

---

## C. Relationship Intelligence

Knowledge Graph Nodes

* Borrower
* Employer
* Industry
* Guarantor
* Region
* Branch
* Economic Event

Relationship Examples

* Works For
* Lives In
* Guaranteed By
* Owns Business
* Belongs To Industry
* Connected Borrowers

---

# 5. AI Pipeline

```text
Structured Data

+

Unstructured Data

+

Knowledge Graph

↓

Validation

↓

Cleaning

↓

Feature Engineering

↓

Feature Store

↓

Model Selection

↓

Loan-Type Model

↓

Borrower-Type Adaptation

↓

Ensemble Prediction

↓

Probability of Default

↓

SHAP Explanation

↓

Recommendation
```

---

# 6. Feature Engineering

## Financial Features

* Debt-to-Income Ratio
* Loan-to-Income Ratio
* Credit Utilization
* Total Outstanding Loans
* Savings Ratio
* EMI Burden

---

## Behaviour Features

* Missed EMI Count
* Late Payment Frequency
* Average Transaction Value
* Monthly Cash Flow
* Spending Behaviour

---

## Unstructured Features

Generated using NLP.

Examples

* Sentiment Score
* Risk Keywords
* Financial Stress Indicators
* Employer Stability Score
* Business Growth Indicators

---

## Graph Features

Calculated from Neo4j.

Examples

* Employer Risk Score
* Industry Risk Score
* Connected Borrower Defaults
* Shared Guarantor Risk
* Regional Economic Risk

---

# 7. Adaptive Prediction Models

Instead of one universal model, DefaultSense AI uses specialized models.

## Personal Loan Model

Optimized for

* Salary
* Credit History
* Spending Behaviour

---

## Home Loan Model

Optimized for

* Property Value
* Income Stability
* Long-Term Repayment

---

## MSME Loan Model

Optimized for

* Business Revenue
* GST Trends
* Cash Flow
* Industry Performance

---

## Agriculture Loan Model

Optimized for

* Crop Type
* Seasonal Income
* Weather Impact
* Regional Conditions

---

## Education Loan Model

Optimized for

* Course Type
* Employment Potential
* Co-Applicant Strength

---

# 8. Borrower Segmentation

Every borrower is categorized before prediction.

Segments

* Salaried Employee
* Self-Employed
* Business Owner
* MSME
* Corporate Borrower

Each segment uses customized feature weighting while producing a common PD score.

---

# 9. Model Selection Strategy

```text
Customer

↓

Identify Loan Type

↓

Identify Borrower Profile

↓

Load Best Prediction Model

↓

Extract Graph Features

↓

Generate Prediction
```

---

# 10. Ensemble Decision Engine

Predictions are generated by combining multiple intelligence sources.

```text
Structured Score

+

Unstructured Score

+

Relationship Score

↓

Weighted Ensemble

↓

Final Probability of Default
```

This improves robustness compared to relying on a single source of information.

---

# 11. Explainable AI

Every prediction includes:

* Risk Score
* Probability of Default
* Feature Importance
* Top Positive Factors
* Top Negative Factors
* Confidence Score
* Human-readable Explanation

Example

```text
Probability of Default

81%

Main Reasons

• High Debt Ratio

• Employer Under Financial Stress

• Multiple Late EMI Payments

Recommendation

Manual Credit Review
```

---

# 12. Recommendation Engine

| PD Score | Risk     | Recommendation          |
| -------- | -------- | ----------------------- |
| 0–25     | Low      | Approve                 |
| 26–50    | Moderate | Approve with Monitoring |
| 51–75    | High     | Additional Verification |
| 76–100   | Critical | Reject / Escalate       |

---

# 13. Model Evaluation & The 90% Accuracy Strategy

> **This section is the contract for hitting the Problem Statement 4 target (accuracy improving to 90%).** Every choice below exists to reach — and honestly defend — that number.

## 13.1 Why raw accuracy alone is a trap

Default data is **imbalanced** (defaulters are the minority). On a dataset with a 10% default rate, a model that blindly predicts "no default" for everyone already scores **~90% accuracy while catching zero defaulters**. Reporting that number would be meaningless and any technical judge will call it out. We therefore **never report accuracy alone** — we report a metric bundle and lead with ROC-AUC.

## 13.2 Committed target bundle

| Metric | Target | Role |
| --- | --- | --- |
| **ROC-AUC** | **≥ 0.90** | **Headline number** — this is our defensible "90%" |
| **Recall (defaulters)** | **≥ 85%** | Proves we actually catch stressed loans |
| **Accuracy** | **≥ 90%** | Reported, but always beside Recall — never alone |
| PR-AUC | Report | Honest view under class imbalance |
| F1 Score | Report | Precision/recall balance |
| KS Statistic / Gini | Report | Banker-standard scorecard metrics |
| Confusion Matrix | Report | At the tuned operating threshold |

**Credibility guardrail:** land ROC-AUC in the **0.90–0.94** band. Scores of 0.98–0.99 read as data leakage or overfitting to a technical judge and should trigger a review of the pipeline, not celebration.

**Benchmark grounding:** messy real-world data (Home Credit) tops out ~0.80 AUC; clean, well-structured data (Give Me Some Credit) reaches ~0.92–0.93; published SMOTE + XGBoost + feature-engineering studies report ~90–91% accuracy with ~92% recall. Our target sits within proven range for a well-designed dataset.

## 13.3 The four levers that get us from a 16–22% baseline to 90%

**Lever 1 — Class imbalance handling.** The single biggest recall lever.
* Set XGBoost `scale_pos_weight` to the negative/positive class ratio.
* Apply **SMOTE on the training fold only, strictly after the train/test split** — never before splitting, or synthetic samples leak into test and produce fake 99% scores.

**Lever 2 — Multi-modal feature engineering.** The baseline is low *because it is structured-data-only*. Each intelligence layer must emit real numeric features into the model (see Section 6): structured ratios/trends, OCR/NLP sentiment & extracted ratios, Neo4j graph aggregates (employer/industry/guarantor/region risk), and 12-month temporal windows. This breadth is what moves the ceiling.

**Lever 3 — Model strength.**
* Ensemble/stack XGBoost + LightGBM + CatBoost (Section 10).
* **Threshold tuning** — do not classify at the default 0.5 cutoff; select the operating threshold that meets the Recall ≥ 85% target while holding accuracy.
* **Probability calibration** (isotonic or Platt) — our output is a *PD probability*, so it must be calibrated, not just rank-ordered.
* Hyperparameter tuning with **Optuna**; validate with **stratified k-fold cross-validation** for honest, non-cherry-picked numbers.

**Lever 4 — Segment-aware evaluation.**
* Report the full metric bundle **per loan type and per borrower segment** (Sections 7–8) — this simultaneously satisfies the PS4 "different methods per segment" requirement and proves consistency across products.

## 13.4 Baseline-vs-full comparison (the demo narrative)

Train a plain **Logistic Regression on structured-only data** to reproduce the low baseline (~16–22% effective performance), then show the full 4-layer pipeline reaching the target bundle. This explicit **before → after** is the winning story: *"IDBI's current approach ≈ baseline; DefaultSense AI ≈ 0.90+ AUC / 85%+ recall."*

The overriding objective is to **maximize recall on defaulters (minimize missed high-risk borrowers)** while keeping precision and accuracy strong — not to inflate a single vanity metric.

---

# 14. Model Retraining

Retraining is triggered when:

* New loan performance data becomes available.
* Model performance degrades.
* Economic conditions change significantly.
* New borrower segments are introduced.

---

# 15. Future AI Enhancements

* Graph Neural Networks (GNN)
* Transformer-based document understanding
* Large Language Model (LLM) risk summaries
* Real-time streaming predictions
* Federated learning across banks
* AutoML model optimization
* Continuous learning pipeline

---

# 16. AI Deliverables

* Multi-modal feature engineering pipeline
* Loan-specific prediction models
* Borrower segmentation engine
* Knowledge Graph feature extraction
* Ensemble prediction engine
* 12-month Probability of Default prediction
* SHAP-based Explainable AI
* Intelligent recommendation engine
* Model evaluation and retraining workflow
