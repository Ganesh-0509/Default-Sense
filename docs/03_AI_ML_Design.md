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

# 13. Model Evaluation

Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC
* Confusion Matrix

The objective is to maximize predictive performance while minimizing false approvals of high-risk borrowers.

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
