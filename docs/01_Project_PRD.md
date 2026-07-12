# 01_Project_PRD.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Hackathon:** IDBI Bank Hackathon (Hack2Skill)
**Problem Statement:** PS-4 – Default Prediction Model

---

# 1. Project Overview

## Project Name

**DefaultSense AI**

## Project Vision

DefaultSense AI is a Hybrid Multi-Modal Loan Default Prediction Platform that predicts the **Probability of Default (PD)** up to **12 months in advance** by combining structured banking data, unstructured financial intelligence, relationship analysis, and Explainable AI.

The platform enables banks to identify financially stressed borrowers early, improve credit decisions, reduce Non-Performing Assets (NPAs), and provide transparent, actionable recommendations to loan officers.

---

# 2. Problem Statement

Current banking default prediction systems suffer from:

* Low prediction accuracy (16–22%)
* Heavy dependence on structured data only
* Separate approaches for different loan products
* Lack of borrower-specific intelligence
* Limited interpretability of predictions
* Delayed identification of financial stress

These limitations reduce the effectiveness of proactive credit risk management.

---

# 3. Proposed Solution

DefaultSense AI introduces a unified prediction framework that combines four intelligence layers:

### Structured Intelligence

Uses:

* Customer profile
* Credit history
* Repayment history
* Transaction patterns
* Loan characteristics
* Financial ratios

---

### Unstructured Intelligence

Processes:

* Loan officer remarks
* OCR-extracted financial statements
* Customer declarations
* Employer and industry news summaries

---

### Relationship Intelligence

Builds a Knowledge Graph connecting:

* Borrowers
* Employers
* Industries
* Guarantors
* Branches
* Geographic regions
* Economic events

The graph identifies hidden relationships that influence default risk.

---

### Decision Intelligence

Generates:

* 12-Month Probability of Default
* Risk Category
* Top Risk Factors
* Explainable AI insights
* Actionable recommendations

---

# 4. Objectives

* Predict borrower default risk up to **12 months in advance**.
* Combine structured and unstructured data sources.
* Adapt predictions for different loan products and borrower segments.
* Provide transparent AI explanations using Explainable AI.
* Support faster and more informed lending decisions.
* Create a scalable platform that can integrate with existing banking systems.

---

# 5. Target Users

### Primary Users

* Loan Officers
* Credit Analysts
* Branch Managers
* Risk Management Teams

### Secondary Users

* Senior Management
* Internal Auditors
* Compliance Teams

---

# 6. Problem Statement Mapping

| Official Requirement            | DefaultSense AI Solution                             |
| ------------------------------- | ---------------------------------------------------- |
| Predict Probability of Default  | AI-based 12-month PD prediction                      |
| Improve prediction accuracy     | Hybrid ML + Graph Intelligence + Feature Engineering |
| Structured Data                 | Customer, Loan, Transaction & Credit History         |
| Unstructured Data               | Officer Notes, OCR Documents, Industry News          |
| Different Loan Types            | Loan-type specific prediction pipeline               |
| Different Borrower Profiles     | Borrower segmentation and adaptive features          |
| Common Interpretation Framework | Explainable AI + Unified Risk Dashboard              |

---

# 7. Core Features

## Intelligent Borrower Profile

Creates a unified borrower profile using structured and unstructured information.

---

## 12-Month Default Prediction

Predicts the probability that a borrower may default within the next twelve months.

---

## Explainable AI

Displays:

* Prediction confidence
* Top contributing factors
* Feature importance
* Human-readable explanation

---

## Knowledge Graph

Visualizes borrower relationships with:

* Employers
* Guarantors
* Industries
* Branches
* Geographic regions

to identify indirect sources of financial risk.

---

## Smart Recommendations

Generates context-aware recommendations such as:

* Approve
* Approve with Monitoring
* Request Additional Verification
* Escalate to Credit Committee
* Reject

---

## Interactive Dashboard

Displays:

* Portfolio risk
* High-risk borrowers
* Upcoming stressed accounts
* Branch performance
* Loan category insights

---

# 8. Functional Requirements

### Authentication

* Secure Login
* JWT Authentication
* Role-Based Access Control

---

### Customer Management

* Create Customer
* Update Customer
* Search Customer
* Customer Profile

---

### Loan Management

* Create Loan
* Loan History
* Repayment Tracking
* Loan Status

---

### AI Engine

* Feature Engineering
* Default Prediction
* Explainability
* Recommendation Generation

---

### Knowledge Graph

* Relationship Discovery
* Connected Risk Analysis
* Graph Visualization

---

### Reporting

* Customer Risk Report
* Portfolio Risk Report
* PDF Export
* CSV Export

---

# 9. Non-Functional Requirements

### Performance

* Prediction response time < 3 seconds
* Dashboard load time < 2 seconds

### Security

* JWT Authentication
* Password Hashing
* Role-Based Access Control
* Encrypted API communication

### Scalability

* Modular architecture
* API-first design
* Containerized deployment

### Reliability

* Graceful error handling
* Audit logging
* Input validation

---

# 10. Success Metrics

The solution will be considered successful if it:

* Predicts borrower default probability for the next 12 months.
* Integrates both structured and unstructured data.
* Produces explainable predictions.
* Supports multiple loan categories.
* Supports multiple borrower profiles.
* Provides actionable recommendations for banking professionals.
* Demonstrates a unified and scalable prediction framework suitable for banking environments.

---

# 11. Project Scope

### Included (MVP)

* Authentication
* Customer Management
* Loan Management
* AI Prediction Engine
* Explainable AI
* Knowledge Graph
* Dashboard
* Reports
* Alerts

### Excluded (Future Scope)

* Core Banking System Integration
* Real-time RBI data integration
* Mobile Application
* Multi-bank deployment
* Live production deployment

---

# 12. Technology Stack

| Layer               | Technology    |
| ------------------- | ------------- |
| Frontend            | React + Vite  |
| UI                  | Tailwind CSS  |
| Backend             | FastAPI       |
| Database            | PostgreSQL    |
| Knowledge Graph     | Neo4j         |
| AI Model            | XGBoost       |
| Explainability      | SHAP          |
| Authentication      | JWT           |
| Charts              | Recharts      |
| Graph Visualization | React Flow    |
| OCR                 | Tesseract OCR |
| Deployment          | Docker        |

---

# 13. Risks & Mitigation

| Risk                        | Mitigation                                                                          |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Limited public banking data | Use validated public datasets with realistic synthetic banking records              |
| Missing unstructured data   | Simulate loan officer notes and OCR-extracted financial documents for the prototype |
| Model bias                  | Cross-validation, feature selection, and fairness checks                            |
| Complex graph relationships | Limit the MVP to high-value borrower, employer, guarantor, and industry connections |

---

# 14. Expected Outcome

DefaultSense AI enables financial institutions to move from reactive loan monitoring to proactive credit risk management by delivering:

* Early 12-month default prediction.
* Better lending decisions.
* Transparent AI explanations.
* Unified risk interpretation across loan products.
* Relationship-driven borrower intelligence.
* Reduced manual credit assessment effort.
* Improved portfolio monitoring through a single intelligent platform.

---

# 15. Future Roadmap

### Phase 2

* Graph Neural Networks (GNN)
* Real-time banking data integration
* LLM-powered credit summaries
* Fraud detection module
* Mobile application
* Portfolio stress simulation
* Regulatory reporting automation
* Multi-bank deployment support
