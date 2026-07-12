# 04_Database_Design.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Database Design

---

# 1. Objective

The database is designed to support a **multi-modal AI prediction system** by storing structured banking data, unstructured intelligence, relationship metadata, AI predictions, and audit information.

DefaultSense AI uses a **hybrid database architecture**:

* **PostgreSQL** → Structured transactional data
* **Neo4j** → Relationship intelligence (Knowledge Graph)

---

# 2. Database Architecture

```text id="n5rt8g"
                    DefaultSense AI

                          │

        ┌─────────────────┴─────────────────┐

        ▼                                   ▼

 PostgreSQL                           Neo4j Graph

Structured Banking Data        Relationship Intelligence
```

---

# 3. PostgreSQL Modules

The relational database is divided into logical modules.

### Authentication

* Users
* Roles
* Permissions

---

### Customer Management

* Customers
* Customer Addresses
* Customer Contacts

---

### Loan Management

* Loans
* Loan Types
* EMI Schedule
* Repayment History

---

### Financial Data

* Transactions
* Credit History
* Income Details
* Existing Liabilities

---

### AI Intelligence

* Predictions
* SHAP Explanations
* Feature Scores

---

### Document Management

* Uploaded Documents
* OCR Results
* Loan Officer Notes

---

### Monitoring

* Alerts
* Notifications
* Audit Logs

---

# 4. PostgreSQL Tables

## Users

Purpose

Stores system users.

Fields

* user_id (UUID)
* full_name
* email
* password_hash
* role
* branch_id
* status
* created_at

---

## Customers

Purpose

Stores borrower information.

Fields

* customer_id
* customer_name
* gender
* date_of_birth
* occupation
* employment_type
* annual_income
* credit_score
* address
* phone
* email
* created_at

---

## Loans

Purpose

Stores all loan records.

Fields

* loan_id
* customer_id
* loan_type
* loan_amount
* interest_rate
* tenure
* emi
* outstanding_amount
* loan_status
* disbursement_date

---

## Repayment History

Purpose

Tracks repayment behaviour.

Fields

* repayment_id
* loan_id
* payment_date
* payment_amount
* due_amount
* delay_days
* payment_status

---

## Transactions

Purpose

Stores banking transaction history.

Fields

* transaction_id
* customer_id
* transaction_date
* debit_amount
* credit_amount
* balance
* transaction_type

---

## Credit History

Purpose

Stores credit behaviour.

Fields

* record_id
* customer_id
* credit_score
* overdue_accounts
* active_loans
* closed_loans
* bureau_source

---

## Loan Officer Notes

Purpose

Stores unstructured observations.

Fields

* note_id
* customer_id
* officer_id
* note_text
* sentiment_score
* created_at

---

## OCR Documents

Purpose

Stores extracted document information.

Fields

* document_id
* customer_id
* document_type
* extracted_text
* confidence_score
* upload_date

---

## AI Predictions

Purpose

Stores prediction history.

Fields

* prediction_id
* customer_id
* prediction_date
* probability_of_default
* risk_level
* confidence_score
* recommendation

---

## SHAP Explanations

Purpose

Stores explainability results.

Fields

* explanation_id
* prediction_id
* feature_name
* contribution
* impact_direction

---

## Alerts

Purpose

Stores generated alerts.

Fields

* alert_id
* customer_id
* severity
* alert_type
* description
* status
* generated_at

---

## Audit Logs

Purpose

Stores user activity.

Fields

* log_id
* user_id
* action
* module
* timestamp

---

# 5. Neo4j Knowledge Graph

## Node Types

* Customer
* Loan
* Employer
* Industry
* Branch
* Region
* Guarantor
* Economic Event

---

## Relationships

```text id="4yxv5l"
Customer

│

WORKS_FOR

↓

Employer

↓

BELONGS_TO

↓

Industry

↓

AFFECTED_BY

↓

Economic Event
```

Additional relationships

* HAS_LOAN
* GUARANTEED_BY
* LIVES_IN
* MANAGED_BY
* RELATED_TO
* LOCATED_IN

---

# 6. Database Relationships

```text id="vazrmu"
Customer

├── Loans

├── Transactions

├── Credit History

├── Loan Officer Notes

├── OCR Documents

├── AI Predictions

├── Alerts

└── Repayment History
```

---

# 7. Data Categories

## Structured Data

* Customer Profile
* Loan Details
* Credit Score
* Repayment History
* Transactions
* Income
* Liabilities

---

## Unstructured Data

* Loan Officer Notes
* OCR Text
* Customer Declarations
* Financial Statement Text
* Industry News Summary

---

## AI Generated Data

* Risk Score
* Probability of Default
* SHAP Values
* Recommendations
* Confidence Score

---

# 8. Data Validation Rules

Customer

* Email must be unique
* Phone must be unique
* Credit Score: 300–900

Loan

* Loan Amount > 0
* Interest Rate ≥ 0
* EMI > 0

Repayment

* Delay Days ≥ 0
* Payment Amount > 0

Prediction

* PD Score: 0–100
* Confidence: 0–100

---

# 9. Indexing Strategy

PostgreSQL

Index the following fields:

* customer_id
* loan_id
* prediction_date
* credit_score
* loan_type
* branch_id
* repayment_date

Neo4j

Index:

* Customer ID
* Employer Name
* Industry Name
* Region Name
* Loan ID

---

# 10. Database Security

* UUID primary keys
* Encrypted passwords (bcrypt)
* Role-Based Access Control
* Parameterized queries
* Audit logging
* Secure backups
* Foreign key constraints

---

# 11. Scalability

The schema is designed to support:

* Multiple bank branches
* Multiple loan products
* Millions of transactions
* Continuous AI predictions
* Future Core Banking System integration
* Additional AI models

---

# 12. Data Lifecycle

```text id="y1dc6q"
Customer Registration

↓

Loan Application

↓

Transaction Updates

↓

Document Upload

↓

OCR Processing

↓

Knowledge Graph Update

↓

AI Prediction

↓

SHAP Explanation

↓

Recommendation

↓

Alert Generation

↓

Dashboard
```

---

# 13. Estimated Prototype Dataset

| Dataset           | Approximate Records |
| ----------------- | ------------------: |
| Customers         |              10,000 |
| Loans             |               8,000 |
| Transactions      |             100,000 |
| Repayment Records |              75,000 |
| Credit History    |              10,000 |
| Officer Notes     |               5,000 |
| OCR Documents     |               5,000 |
| AI Predictions    |              20,000 |
| Alerts            |               4,000 |

---

# 14. Future Database Enhancements

* Real-time streaming transaction storage
* Document versioning
* Data lake integration
* Time-series analytics
* Feature Store integration
* Vector database for semantic document search
* Automated archival policy

---

# 15. Database Deliverables

* PostgreSQL relational schema
* Neo4j Knowledge Graph schema
* Structured & unstructured data storage
* AI prediction repository
* Explainability data storage
* Security and validation rules
* Scalable architecture for future banking integration
