# 15_Deployment_Guide.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Deployment Guide

---

# 1. Objective

This document describes how to deploy **DefaultSense AI** for development, testing, and hackathon demonstration. The deployment process is designed to be simple, reproducible, and scalable.

---

# 2. Deployment Architecture

```text id="k9v4xa"
                    User Browser
                         │
                         ▼
              React Frontend (Vite)
                         │
                    HTTPS / REST
                         │
                         ▼
                FastAPI Backend
             ┌───────────┴───────────┐
             ▼                       ▼
      PostgreSQL Database      Neo4j Database
             │                       │
             └───────────┬───────────┘
                         ▼
                  AI Prediction Engine
                         │
                         ▼
                  SHAP + OCR Services
```

---

# 3. Deployment Components

| Component                  | Technology    |
| -------------------------- | ------------- |
| Frontend                   | React + Vite  |
| Backend                    | FastAPI       |
| Database                   | PostgreSQL    |
| Graph Database             | Neo4j         |
| AI Engine                  | XGBoost       |
| OCR                        | Tesseract OCR |
| Containerization           | Docker        |
| Reverse Proxy *(Optional)* | Nginx         |

---

# 4. Environment Variables

Create a `.env` file with the following configuration:

```text id="6f7yab"
DATABASE_URL=

NEO4J_URI=

NEO4J_USERNAME=

NEO4J_PASSWORD=

JWT_SECRET=

MODEL_PATH=

OCR_PATH=

FRONTEND_URL=
```

---

# 5. Local Development

Start the services in the following order:

1. PostgreSQL
2. Neo4j
3. Backend (FastAPI)
4. Frontend (React)
5. AI Model
6. OCR Service

Verify:

* Frontend loads successfully.
* Backend APIs respond correctly.
* Database connections are established.
* AI prediction endpoint is operational.

---

# 6. Docker Deployment

Containerize the following services:

* Frontend
* Backend
* PostgreSQL
* Neo4j

Use a single `docker-compose.yml` file to orchestrate all services.

---

# 7. Cloud Deployment Options

Recommended platforms:

| Component  | Recommended Platform |
| ---------- | -------------------- |
| Frontend   | Vercel / Netlify     |
| Backend    | Render / Railway     |
| PostgreSQL | Supabase / Neon      |
| Neo4j      | Neo4j AuraDB         |
| Full Stack | Azure / AWS          |

---

# 8. Deployment Checklist

Before deployment, ensure:

* Environment variables are configured.
* Database migrations are complete.
* Sample data is loaded.
* AI model is trained and saved.
* OCR engine is installed.
* JWT authentication is enabled.
* CORS settings are configured.

---

# 9. Production Security

Enable:

* HTTPS
* JWT Authentication
* Password Hashing (bcrypt)
* Role-Based Access Control
* Input Validation
* Secure Environment Variables
* Audit Logging

Never expose:

* Database credentials
* API secrets
* Model files
* Internal configuration

---

# 10. Monitoring

Track:

* API response times
* Prediction latency
* Database performance
* Authentication failures
* Application errors
* Resource utilization

---

# 11. Backup Strategy

Back up:

* PostgreSQL database
* Neo4j database
* AI model files
* Uploaded documents
* Configuration files

Suggested frequency:

* Database: Daily
* Models: After retraining
* Documents: Daily

---

# 12. Demo Deployment (Hackathon)

For the hackathon demo:

* Deploy the frontend.
* Deploy the backend.
* Use a hosted PostgreSQL instance.
* Use Neo4j AuraDB (free tier if sufficient).
* Load a prepared demo dataset.
* Preload the trained AI model.
* Verify the end-to-end workflow before presentation.

---

# 13. Deployment Validation

Confirm the following after deployment:

* Login works.
* Customer and loan data loads.
* OCR processing completes successfully.
* AI prediction returns a Probability of Default.
* SHAP explanations are displayed.
* Knowledge Graph visualization loads.
* Reports can be exported.

---

# 14. Rollback Plan

If deployment fails:

1. Restore the previous application version.
2. Restore the latest database backup.
3. Verify environment variables.
4. Restart services.
5. Re-run health checks.

---

# 15. Final Deployment Deliverables

The deployed system should include:

* Live React frontend
* FastAPI backend
* PostgreSQL database
* Neo4j Knowledge Graph
* AI prediction engine
* OCR processing
* Explainable AI (SHAP)
* Reporting module
* Secure authentication
* End-to-end working demo for the IDBI Hackathon
