# 11_Database_ERD.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Database Entity Relationship Diagram (ERD)

---

# 1. Objective

This document defines the logical database relationships for **DefaultSense AI**. It illustrates how structured banking data, unstructured information, AI outputs, and Knowledge Graph entities are connected to support **12-month Probability of Default (PD)** prediction.

---

# 2. Database Overview

DefaultSense AI uses a hybrid database architecture:

* **PostgreSQL** → Structured Banking Data
* **Neo4j** → Relationship Intelligence

---

# 3. PostgreSQL ER Diagram

```text
                                USERS
                                  │
                     Creates / Reviews Customers
                                  │
                                  ▼
                            CUSTOMERS
                                  │
      ┌──────────────┬────────────┼──────────────┬──────────────┐
      ▼              ▼            ▼              ▼              ▼
    LOANS      TRANSACTIONS   CREDIT_HISTORY   DOCUMENTS   OFFICER_NOTES
      │              │            │              │              │
      ▼              │            │              ▼              ▼
REPAYMENT_HISTORY    │            │        OCR_RESULTS    SENTIMENT_SCORE
      │              │            │
      └──────────────┴────────────┘
                     │
                     ▼
              AI_PREDICTIONS
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   SHAP_EXPLANATIONS         ALERTS
```

---

# 4. Primary Tables

## Users

Primary Key

* user_id

Relationships

* Reviews Customers
* Creates Officer Notes
* Generates Reports

---

## Customers

Primary Key

* customer_id

Relationships

* One Customer → Many Loans
* One Customer → Many Transactions
* One Customer → Many Documents
* One Customer → Many Predictions
* One Customer → Many Alerts

---

## Loans

Primary Key

* loan_id

Foreign Key

* customer_id

Relationships

* One Loan → Many EMI Records
* One Loan → Many Predictions

---

## Transactions

Primary Key

* transaction_id

Foreign Key

* customer_id

---

## Credit History

Primary Key

* credit_history_id

Foreign Key

* customer_id

---

## Documents

Primary Key

* document_id

Foreign Key

* customer_id

---

## OCR Results

Primary Key

* ocr_result_id

Foreign Key

* document_id

---

## Officer Notes

Primary Key

* note_id

Foreign Key

* customer_id
* user_id

---

## AI Predictions

Primary Key

* prediction_id

Foreign Key

* customer_id
* loan_id

---

## SHAP Explanations

Primary Key

* shap_id

Foreign Key

* prediction_id

---

## Alerts

Primary Key

* alert_id

Foreign Key

* prediction_id
* customer_id

---

## Repayment History

Primary Key

* repayment_id

Foreign Key

* loan_id

---

# 5. Relationship Cardinality

| Parent     | Child             | Relationship |
| ---------- | ----------------- | ------------ |
| Customer   | Loan              | One-to-Many  |
| Customer   | Transactions      | One-to-Many  |
| Customer   | Credit History    | One-to-One   |
| Customer   | Documents         | One-to-Many  |
| Customer   | Officer Notes     | One-to-Many  |
| Customer   | AI Predictions    | One-to-Many  |
| Customer   | Alerts            | One-to-Many  |
| Loan       | Repayment History | One-to-Many  |
| Loan       | AI Predictions    | One-to-Many  |
| Prediction | SHAP Explanation  | One-to-Many  |

---

# 6. Neo4j Knowledge Graph Model

## Nodes

```text
Customer

Loan

Employer

Industry

Guarantor

Branch

Region

Economic Event
```

---

## Relationships

```text
(Customer)-[:HAS_LOAN]->(Loan)

(Customer)-[:WORKS_FOR]->(Employer)

(Employer)-[:BELONGS_TO]->(Industry)

(Customer)-[:GUARANTEED_BY]->(Guarantor)

(Customer)-[:LOCATED_IN]->(Region)

(Branch)-[:SERVES]->(Customer)

(Industry)-[:AFFECTED_BY]->(Economic Event)
```

---

# 7. AI Data Flow

```text
Customer

+

Loan

+

Transactions

+

Credit History

+

OCR Results

+

Officer Notes

+

Knowledge Graph Features

↓

Feature Engineering

↓

AI Prediction

↓

SHAP Explanation

↓

Recommendation

↓

Alert
```

---

# 8. Data Integrity Rules

* Every Loan must belong to one Customer.
* Every Prediction must reference one Customer.
* Every SHAP Explanation must reference one Prediction.
* Every OCR Result must belong to one Document.
* Every Repayment record must belong to one Loan.
* All foreign keys must maintain referential integrity.

---

# 9. Index Strategy

### PostgreSQL

Index

* customer_id
* loan_id
* prediction_id
* credit_score
* loan_type
* created_at

### Neo4j

Index

* Customer
* Employer
* Industry
* Guarantor
* Region

---

# 10. Future Extensions

The ERD supports future additions without major redesign:

* Fraud Detection
* Core Banking Integration
* Credit Bureau Data
* Graph Neural Networks
* Real-time Streaming
* Multi-bank Support

---

# 11. ERD Deliverables

* Relational database model
* Entity relationships
* Primary and foreign key mapping
* Knowledge Graph schema
* AI prediction relationships
* Scalable database design for banking applications
