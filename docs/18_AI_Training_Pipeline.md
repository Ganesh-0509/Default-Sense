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
* Balance classes (if required)

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

---

# 7. Model Training

Recommended Model

* XGBoost Classifier

Alternative Models

* LightGBM
* CatBoost
* Random Forest
* Logistic Regression (Baseline)

---

# 8. Model Evaluation

Evaluate using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC
* Confusion Matrix

Primary goal:

* High Recall for default cases
* Balanced Precision
* Strong ROC-AUC

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
