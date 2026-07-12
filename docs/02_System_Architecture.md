# 02_System_Architecture.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** System Architecture

---

# 1. Architecture Overview

DefaultSense AI follows a modular, AI-first architecture designed to predict the **Probability of Default (PD)** up to **12 months in advance** by integrating structured banking data, unstructured intelligence, relationship analysis, and explainable AI.

The architecture is divided into six independent layers to ensure scalability, maintainability, and easy integration with existing banking systems.

---

# 2. High-Level Architecture

```text
                         DEFAULTSENSE AI

                        ┌─────────────────────┐
                        │   React Dashboard   │
                        └──────────┬──────────┘
                                   │
                            REST API (HTTPS)
                                   │
                     ┌─────────────▼─────────────┐
                     │      FastAPI Backend      │
                     └─────────────┬─────────────┘
                                   │
      ┌──────────────┬─────────────┼──────────────┬──────────────┐
      │              │             │              │              │
      ▼              ▼             ▼              ▼              ▼
Authentication   AI Engine    OCR Engine    Knowledge Graph   Reporting
      │              │             │              │              │
      └──────────────┴─────────────┴──────────────┴──────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │     PostgreSQL + Neo4j    │
                     └───────────────────────────┘
```

---

# 3. System Layers

## Layer 1 – Presentation Layer

Technology

* React
* Vite
* Tailwind CSS

Responsibilities

* User Interface
* Dashboard
* Reports
* Graph Visualization
* AI Explanation
* User Authentication

---

## Layer 2 – API Layer

Technology

* FastAPI

Responsibilities

* REST APIs
* Authentication
* Request Validation
* Business Logic Routing
* API Documentation

---

## Layer 3 – Business Logic Layer

Modules

* Customer Service
* Loan Service
* AI Service
* OCR Service
* Knowledge Graph Service
* Report Service
* Alert Service

Responsibilities

* Data validation
* Business rules
* Service orchestration
* AI invocation
* Recommendation generation

---

## Layer 4 – AI Intelligence Layer

Components

### Structured Data Engine

Processes

* Credit Score
* Loan History
* Repayment Behaviour
* Transactions
* Financial Ratios

---

### Unstructured Intelligence Engine

Processes

* Loan Officer Notes
* OCR Financial Statements
* KYC Document Text
* Employer & Industry News Summaries

---

### Relationship Intelligence Engine

Processes

* Borrower Relationships
* Employer Networks
* Guarantors
* Industry Connections
* Regional Risk
* Economic Events

---

### Decision Intelligence Engine

Produces

* Probability of Default (12 Months)
* Risk Level
* Confidence Score
* SHAP Explanation
* Recommendation

---

# 4. Data Layer

## PostgreSQL

Stores

* Users
* Customers
* Loans
* Transactions
* Repayment History
* Documents
* AI Predictions
* Alerts

---

## Neo4j

Stores

* Borrowers
* Employers
* Industries
* Guarantors
* Branches
* Economic Events
* Relationship Links

---

# 5. Complete Data Flow

```text
Customer Application

↓

Structured Banking Data

+

Loan Officer Notes

+

Financial Documents

+

Industry News

↓

Data Validation

↓

OCR & Text Extraction

↓

Feature Engineering

↓

Knowledge Graph Feature Extraction

↓

Loan-Type Prediction Model

↓

Borrower Profile Adaptation

↓

12-Month PD Prediction

↓

Explainable AI (SHAP)

↓

Recommendation Engine

↓

Dashboard & Reports
```

---

# 6. AI Decision Flow

```text
Input Data

↓

Data Cleaning

↓

Feature Engineering

↓

Model Selection

↓

Loan-Type Model

↓

Borrower-Type Optimization

↓

Knowledge Graph Enrichment

↓

Probability of Default

↓

SHAP Explanation

↓

Recommendation
```

---

# 7. Adaptive Prediction Strategy

Instead of using a single prediction model, DefaultSense AI selects the most suitable prediction pipeline based on borrower and loan characteristics.

### Loan Categories

* Home Loan
* Personal Loan
* Vehicle Loan
* Education Loan
* MSME Loan
* Agriculture Loan

---

### Borrower Segments

* Salaried
* Self-Employed
* Business Owner
* MSME
* Corporate

Each segment uses tailored feature engineering while producing a common Probability of Default output.

---

# 8. Explainable AI Flow

```text
Prediction

↓

SHAP Analysis

↓

Feature Importance

↓

Natural Language Explanation

↓

Recommended Action
```

Example Output

* High Debt-to-Income Ratio
* Frequent EMI Delays
* Employer Industry Under Stress
* Negative Financial Trend

---

# 9. Knowledge Graph Flow

```text
Borrower

↓

Employer

↓

Industry

↓

Economic Events

↓

Related Borrowers

↓

Risk Propagation Analysis

↓

Graph Risk Score
```

The graph provides contextual intelligence that complements the machine learning model.

---

# 10. Security Architecture

Authentication

* JWT Access Tokens
* Secure Password Hashing (bcrypt)

Authorization

* Role-Based Access Control (RBAC)

Data Protection

* HTTPS Communication
* Encrypted Sensitive Data
* Audit Logging

---

# 11. Scalability

The architecture is designed as loosely coupled modules.

Future enhancements can include:

* Additional AI models
* New loan products
* External banking APIs
* Real-time data ingestion
* Multi-bank deployment

No major architectural changes are required.

---

# 12. Deployment Architecture

```text
Browser

↓

React Application

↓

FastAPI Backend

↓

PostgreSQL

+

Neo4j

+

AI Model

+

OCR Service
```

Each service can be containerized using Docker and deployed independently.

---

# 13. External Integrations (Future Scope)

Potential integrations include:

* Core Banking System (CBS)
* Credit Bureau APIs
* RBI Data Sources
* OCR Document Services
* News APIs
* SMS & Email Notification Services

These integrations are optional for the hackathon MVP but supported by the architecture.

---

# 14. Technology Stack

| Layer               | Technology    |
| ------------------- | ------------- |
| Frontend            | React + Vite  |
| Styling             | Tailwind CSS  |
| Backend             | FastAPI       |
| Database            | PostgreSQL    |
| Graph Database      | Neo4j         |
| AI Framework        | XGBoost       |
| Explainable AI      | SHAP          |
| OCR                 | Tesseract OCR |
| Authentication      | JWT           |
| Graph Visualization | React Flow    |
| Charts              | Recharts      |
| Deployment          | Docker        |

---

# 15. Architecture Benefits

* Predicts loan default up to **12 months in advance**.
* Combines **structured and unstructured data** in a unified workflow.
* Adapts prediction strategies to different loan types and borrower profiles.
* Uses **Knowledge Graphs** to capture hidden relationships affecting borrower risk.
* Provides transparent, explainable AI recommendations for banking professionals.
* Modular and scalable architecture suitable for prototype demonstration and future enterprise deployment.
