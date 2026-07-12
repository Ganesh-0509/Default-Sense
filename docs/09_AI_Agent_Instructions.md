# 09_AI_AGENT_INSTRUCTIONS.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** AI Agent Development Instructions

---

# 1. Objective

This document defines the development rules for AI coding agents and IDE-integrated assistants to ensure consistent, production-ready code generation throughout the project.

The AI agent should always prioritize clean architecture, modularity, and maintainability.

---

# 2. Project Goal

Build a full-stack web application that predicts the **Probability of Default (PD)** up to **12 months in advance** using:

* Structured Banking Data
* Unstructured Financial Data
* Knowledge Graph Intelligence
* Explainable AI (SHAP)

---

# 3. Technology Stack

| Layer          | Technology    |
| -------------- | ------------- |
| Frontend       | React + Vite  |
| Styling        | Tailwind CSS  |
| Backend        | FastAPI       |
| Database       | PostgreSQL    |
| Graph Database | Neo4j         |
| AI             | XGBoost       |
| Explainability | SHAP          |
| OCR            | Tesseract OCR |
| Authentication | JWT           |
| Charts         | Recharts      |
| Graph UI       | React Flow    |

---

# 4. Folder Structure

```text
defaultsense-ai/

frontend/
backend/
database/
datasets/
models/
docs/
docker/
scripts/
```

---

# 5. Development Rules

Always:

* Write modular code.
* Follow SOLID principles.
* Use reusable components.
* Keep functions small and focused.
* Use meaningful variable names.
* Add error handling.
* Validate all inputs.
* Return consistent API responses.

Never:

* Hardcode secrets.
* Duplicate business logic.
* Mix frontend and backend logic.
* Ignore validation or exceptions.

---

# 6. Backend Guidelines

Generate:

* FastAPI REST APIs
* SQLAlchemy models
* Pydantic schemas
* Service layer
* Repository layer
* Dependency Injection
* JWT Authentication
* OpenAPI documentation

Use asynchronous APIs where appropriate.

---

# 7. Frontend Guidelines

Generate:

* Functional React Components
* Tailwind CSS styling
* React Router
* Zustand state management
* Axios API integration

Every page should include:

* Loading state
* Error state
* Empty state
* Responsive layout

---

# 8. Database Guidelines

Generate:

### PostgreSQL

* Tables
* Relationships
* Foreign Keys
* Indexes
* Constraints

### Neo4j

Generate:

* Nodes
* Relationships
* Cypher Queries

---

# 9. AI Module Guidelines

Generate:

* Data preprocessing
* Feature engineering
* Model training
* Model evaluation
* SHAP explainability
* Recommendation engine

The AI model must predict:

**Probability of Default for the next 12 months.**

---

# 10. OCR Module

Generate APIs for:

* Document upload
* OCR processing
* Text extraction
* Database storage
* AI feature generation

Supported documents:

* Financial Statements
* Income Proof
* Business Documents
* KYC Documents

---

# 11. Knowledge Graph Module

Create relationships between:

* Customer
* Employer
* Industry
* Guarantor
* Branch
* Region
* Loan

Support:

* Graph queries
* Risk relationship analysis
* Interactive visualization

---

# 12. API Standards

Every API should return:

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

For errors:

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {}
}
```

---

# 13. Security Rules

Implement:

* JWT Authentication
* Password Hashing (bcrypt)
* Role-Based Access Control
* Input Validation
* SQL Injection Protection
* CORS Configuration

Never expose sensitive information in API responses.

---

# 14. Coding Standards

Naming

* Components → PascalCase
* Variables → camelCase
* Constants → UPPER_CASE
* Files → kebab-case

Documentation

* Comment only complex logic.
* Keep APIs self-documented.
* Use descriptive commit messages.

---

# 15. Development Order

```text
1. Project Setup

↓

2. Database

↓

3. Backend APIs

↓

4. Authentication

↓

5. Frontend

↓

6. OCR

↓

7. Knowledge Graph

↓

8. AI Model

↓

9. Dashboard

↓

10. Reports

↓

11. Testing

↓

12. Deployment
```

---

# 16. Quality Checklist

Before marking a task complete, ensure:

* Code compiles without errors.
* No linting issues.
* API tested successfully.
* Database migration completed.
* Responsive UI verified.
* Error handling implemented.
* Authentication secured.
* AI prediction tested.

---

# 17. AI Prompt Template

When generating new modules, follow this prompt structure:

```text
Build the [Module Name] for DefaultSense AI.

Requirements:
- Use FastAPI (Backend)
- Use React + Tailwind CSS (Frontend)
- PostgreSQL for structured data
- Neo4j for relationship data
- JWT Authentication
- Modular architecture
- Input validation
- Error handling
- Responsive UI
- Production-ready code
```

---

# 18. Expected Deliverables

The AI coding agent should generate:

* Production-ready source code
* Database models
* REST APIs
* React pages
* Reusable UI components
* AI prediction module
* OCR pipeline
* Knowledge Graph integration
* SHAP explainability
* Unit tests
* Deployment configuration

---

# 19. Definition of Done

A feature is considered complete when:

* Backend API is implemented.
* Frontend UI is connected.
* Database operations work correctly.
* Validation is complete.
* AI logic (if applicable) functions correctly.
* Tests pass.
* Documentation is updated.
* The feature integrates successfully with the overall system.

---

# 20. Final Goal

The AI agent should produce a scalable, secure, and maintainable implementation of **DefaultSense AI**, ensuring every generated module aligns with the official IDBI Hackathon Problem Statement by supporting **12-month default prediction**, **structured and unstructured data processing**, **adaptive loan-specific intelligence**, and **Explainable AI** for transparent banking decisions.
