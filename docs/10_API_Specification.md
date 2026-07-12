# 10_API_Specification.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** API Specification

---

# 1. Objective

This document defines the REST APIs required for **DefaultSense AI**. The APIs enable communication between the frontend, backend, AI engine, OCR module, Knowledge Graph, and reporting system.

All APIs follow REST principles and return JSON responses.

---

# 2. API Standards

**Base URL**

```text
/api/v1
```

**Content Type**

```text
application/json
```

**Authentication**

* JWT Bearer Token

---

# 3. Standard API Response

### Success

```json
{
  "success": true,
  "message": "Request completed successfully.",
  "data": {}
}
```

### Error

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {}
}
```

---

# 4. Authentication APIs

| Method | Endpoint              | Description     |
| ------ | --------------------- | --------------- |
| POST   | /auth/login           | User Login      |
| POST   | /auth/logout          | Logout          |
| GET    | /auth/profile         | Current User    |
| POST   | /auth/change-password | Change Password |

---

# 5. Customer APIs

| Method | Endpoint          | Description      |
| ------ | ----------------- | ---------------- |
| GET    | /customers        | List Customers   |
| GET    | /customers/{id}   | Customer Details |
| POST   | /customers        | Create Customer  |
| PUT    | /customers/{id}   | Update Customer  |
| DELETE | /customers/{id}   | Delete Customer  |
| GET    | /customers/search | Search Customers |

---

# 6. Loan APIs

| Method | Endpoint               | Description       |
| ------ | ---------------------- | ----------------- |
| GET    | /loans                 | List Loans        |
| GET    | /loans/{id}            | Loan Details      |
| POST   | /loans                 | Create Loan       |
| PUT    | /loans/{id}            | Update Loan       |
| GET    | /loans/{id}/repayments | Repayment History |

---

# 7. Document & OCR APIs

| Method | Endpoint             | Description     |
| ------ | -------------------- | --------------- |
| POST   | /documents/upload    | Upload Document |
| POST   | /ocr/process         | Extract Text    |
| GET    | /documents/{id}      | View Document   |
| GET    | /documents/{id}/text | OCR Result      |

Supported Documents

* Financial Statements
* Income Proof
* KYC Documents
* Business Documents

---

# 8. AI Prediction APIs

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| POST   | /predictions/run           | Generate Prediction         |
| GET    | /predictions/{id}          | Prediction Details          |
| GET    | /predictions/customer/{id} | Customer Prediction History |
| GET    | /predictions/portfolio     | Portfolio Risk Summary      |

**Response Example**

```json
{
  "probability_of_default": 81.4,
  "prediction_horizon": "12 Months",
  "risk_level": "High",
  "confidence": 92.1,
  "recommendation": "Additional Verification"
}
```

---

# 9. Explainable AI APIs

| Method | Endpoint                   | Description           |
| ------ | -------------------------- | --------------------- |
| GET    | /predictions/{id}/shap     | SHAP Explanation      |
| GET    | /predictions/{id}/features | Feature Contributions |

---

# 10. Knowledge Graph APIs

| Method | Endpoint             | Description                 |
| ------ | -------------------- | --------------------------- |
| GET    | /graph/customer/{id} | Customer Relationship Graph |
| GET    | /graph/risk/{id}     | Relationship Risk Analysis  |
| GET    | /graph/search        | Search Graph Nodes          |

---

# 11. Dashboard APIs

| Method | Endpoint                     | Description         |
| ------ | ---------------------------- | ------------------- |
| GET    | /dashboard/summary           | KPI Summary         |
| GET    | /dashboard/risk-distribution | Risk Distribution   |
| GET    | /dashboard/high-risk         | High-Risk Borrowers |
| GET    | /dashboard/trends            | Portfolio Trends    |

---

# 12. Reports APIs

| Method | Endpoint               | Description      |
| ------ | ---------------------- | ---------------- |
| GET    | /reports/customer/{id} | Customer Report  |
| GET    | /reports/portfolio     | Portfolio Report |
| GET    | /reports/risk          | Risk Report      |
| GET    | /reports/export/pdf    | Export PDF       |
| GET    | /reports/export/csv    | Export CSV       |

---

# 13. Alerts APIs

| Method | Endpoint          | Description   |
| ------ | ----------------- | ------------- |
| GET    | /alerts           | List Alerts   |
| GET    | /alerts/{id}      | Alert Details |
| PUT    | /alerts/{id}/read | Mark as Read  |

---

# 14. Request Flow

```text
Frontend

↓

JWT Authentication

↓

REST API

↓

Business Logic

↓

Database / AI Engine / Neo4j

↓

JSON Response
```

---

# 15. API Security

Every protected endpoint requires:

* JWT Authentication
* Role-Based Access Control
* Request Validation
* Input Sanitization

Security headers and HTTPS are mandatory for deployment.

---

# 16. HTTP Status Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Resource Created      |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Resource Not Found    |
| 409  | Conflict              |
| 422  | Validation Error      |
| 500  | Internal Server Error |

---

# 17. API Versioning

Current Version

```text
/api/v1
```

Future releases

```text
/api/v2
/api/v3
```

Backward compatibility should be maintained where possible.

---

# 18. Future APIs

Planned integrations:

* Credit Bureau API
* Core Banking System API
* RBI Economic Indicators API
* Email & SMS Notification API
* Real-time Transaction Streaming API
* LLM-powered Risk Summary API

---

# 19. API Testing

Recommended tools:

* Swagger UI
* Postman
* Pytest
* FastAPI TestClient

All endpoints should include unit and integration tests before deployment.

---

# 20. API Deliverables

* Authentication APIs
* Customer APIs
* Loan APIs
* OCR APIs
* AI Prediction APIs
* Explainable AI APIs
* Knowledge Graph APIs
* Dashboard APIs
* Report APIs
* Alert APIs
* Secure, documented REST API ready for frontend integration.
