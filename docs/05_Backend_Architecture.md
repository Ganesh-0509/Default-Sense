# 05_Backend_Architecture.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Backend Architecture

---

# 1. Objective

The backend is responsible for managing business logic, AI orchestration, authentication, data processing, Knowledge Graph interactions, OCR processing, and report generation. It exposes secure REST APIs for the frontend while coordinating all intelligence modules.

---

# 2. Technology Stack

| Component       | Technology                          |
| --------------- | ----------------------------------- |
| Framework       | FastAPI                             |
| Language        | Python 3.12+                        |
| Authentication  | JWT + OAuth2                        |
| ORM             | SQLAlchemy                          |
| Validation      | Pydantic                            |
| Database        | PostgreSQL                          |
| Graph Database  | Neo4j                               |
| AI              | XGBoost + SHAP                      |
| OCR             | Tesseract OCR                       |
| Background Jobs | Celery + Redis *(optional for MVP)* |
| API Docs        | Swagger (OpenAPI)                   |

---

# 3. Backend Architecture

```text
                 React Frontend
                        │
                 HTTPS REST APIs
                        │
                 FastAPI Application
                        │
 ┌───────────┬──────────┬───────────┬───────────┐
 │           │          │           │           │
 ▼           ▼          ▼           ▼           ▼
Auth     Customer    Loan      AI Engine   Reports
Service   Service   Service      Service    Service
 │           │          │           │           │
 └───────────┴──────────┴───────────┴───────────┘
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
 PostgreSQL                         Neo4j Graph
```

---

# 4. Project Structure

```text
backend/

app/
 ├── api/
 ├── auth/
 ├── models/
 ├── schemas/
 ├── services/
 ├── repositories/
 ├── ai/
 ├── graph/
 ├── ocr/
 ├── reports/
 ├── utils/
 ├── middleware/
 ├── config/
 └── main.py
```

---

# 5. Core Services

## Authentication Service

Responsibilities

* User Login
* JWT Token Generation
* Role-Based Access Control
* Password Hashing

---

## Customer Service

Responsibilities

* Customer CRUD
* Customer Search
* Customer Profile
* Validation

---

## Loan Service

Responsibilities

* Loan Management
* Repayment History
* Loan Status
* Loan Search

---

## AI Service

Responsibilities

* Feature Engineering
* Model Selection
* 12-Month PD Prediction
* SHAP Explainability
* Recommendation Generation

---

## OCR Service

Responsibilities

* Document Upload
* OCR Processing
* Text Extraction
* Store Parsed Results

---

## Knowledge Graph Service

Responsibilities

* Create Nodes
* Create Relationships
* Graph Queries
* Relationship Risk Analysis

---

## Report Service

Responsibilities

* PDF Reports
* CSV Export
* Dashboard Metrics
* Portfolio Summary

---

# 6. Request Lifecycle

```text
Client Request

↓

Authentication

↓

Input Validation

↓

Business Logic

↓

Database Access

↓

AI Processing (if required)

↓

Knowledge Graph Query (if required)

↓

Generate Response

↓

Return JSON
```

---

# 7. AI Prediction Flow

```text
Customer Data

+

Loan Data

+

OCR Data

+

Officer Notes

+

Graph Features

↓

Feature Engineering

↓

Select Loan-Type Model

↓

Borrower Adaptation

↓

PD Prediction

↓

SHAP Explanation

↓

Recommendation

↓

Store Prediction
```

---

# 8. Authentication Flow

```text
User Login

↓

Validate Credentials

↓

Generate JWT

↓

Return Access Token

↓

Protected API Access
```

---

# 9. Error Handling

Standard HTTP Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 422  | Validation Error      |
| 500  | Internal Server Error |

All errors return a consistent JSON response.

---

# 10. Logging

The backend records:

* User Activity
* API Requests
* Prediction Events
* Authentication Events
* System Errors

Logs include timestamps for auditability.

---

# 11. Security

Authentication

* JWT Access Tokens
* Refresh Token Support *(Future)*

Authorization

* Role-Based Access Control

Data Protection

* Password Hashing (bcrypt)
* HTTPS
* Input Validation
* SQL Injection Protection
* CORS Configuration

---

# 12. Performance

Target Performance

* Authentication < 500 ms
* CRUD APIs < 300 ms
* AI Prediction < 3 seconds
* Dashboard Load < 2 seconds

---

# 13. Deployment

The backend supports:

* Docker
* Docker Compose
* Railway
* Render
* Azure App Service
* AWS EC2

---

# 14. Future Enhancements

* Async task processing
* Event-driven architecture
* Kafka integration
* Real-time notifications
* Model version management
* API rate limiting
* Multi-tenant banking support

---

# 15. Backend Deliverables

* FastAPI REST API
* Secure Authentication Module
* Customer & Loan Management APIs
* AI Prediction Service
* OCR Processing Service
* Neo4j Integration
* Reporting Module
* Centralized Error Handling
* Audit Logging
* Production-ready Backend Architecture
