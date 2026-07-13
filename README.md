# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

> Predicts the **Probability of Default (PD)** up to **12 months in advance** by combining structured banking data, unstructured financial intelligence, relationship analysis (Knowledge Graph), and Explainable AI (SHAP).

**Hackathon:** IDBI Bank Hackathon (Hack2Skill) — **Problem Statement 4: Default Prediction Model**

---

## Problem We Solve

Current banking default-prediction systems are limited by **low accuracy (16–22%)**, dependence on **structured data only**, and **fragmented methodologies** across loan types and borrower segments. DefaultSense AI targets a robust, explainable solution that:

- Estimates probability of default to flag stressed loans **12 months in advance**
- Uses **both structured and unstructured data**
- Applies **loan-type and borrower-profile specific** analytical methods
- Provides a **common interpretation framework** (SHAP + unified dashboard) for consistent, comparable, actionable output

---

## Four Intelligence Layers

| Layer | What it does |
| --- | --- |
| **Structured Intelligence** | Credit history, repayment behaviour, transactions, financial ratios |
| **Unstructured Intelligence** | OCR financial docs, loan-officer notes, industry news (NLP) |
| **Relationship Intelligence** | Neo4j Knowledge Graph — employer/industry/guarantor risk propagation |
| **Decision Intelligence** | 12-month PD + risk category + SHAP explanation + recommendation |

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React + Vite, Tailwind CSS, Zustand, React Router, Axios, Recharts, React Flow |
| Backend | FastAPI (Python 3.12+), SQLAlchemy, Pydantic, JWT/OAuth2 |
| Database | PostgreSQL |
| Graph Database | Neo4j |
| AI / ML | XGBoost, SHAP |
| OCR | Tesseract OCR |
| Deployment | Docker / docker-compose |

---

## Repository Structure

```
defaultsense-ai/
├── frontend/     # React + Vite application
├── backend/      # FastAPI application (app/ with layered architecture)
├── database/     # Migrations, schema, seeds (PostgreSQL + Neo4j)
├── datasets/     # Raw, processed, synthetic & sample data
├── models/       # ML training, preprocessing, prediction, SHAP, saved models
├── docs/         # Full project documentation (01–18)
├── docker/       # Dockerfiles
├── scripts/      # Utility scripts
├── tests/        # Backend, frontend, AI, API, integration, performance tests
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## Documentation

All design docs live in [`docs/`](./docs):

| # | Document |
| --- | --- |
| 01 | Project PRD |
| 02 | System Architecture |
| 03 | AI/ML Design |
| 04 | Database Design |
| 05 | Backend Architecture |
| 06 | Frontend UI/UX |
| 07 | Implementation Guide |
| 08 | Hackathon Guide |
| 09 | AI Agent Instructions |
| 10 | API Specification |
| 11 | Database ERD |
| 12 | Dataset & Data Sources |
| 13 | Development Roadmap |
| 14 | Project Structure |
| 15 | Deployment Guide |
| 16 | UI Wireframes |
| 18 | AI Training Pipeline |

---

## Build Status (Phase-wise)

| Phase | Description | Status |
| --- | --- | --- |
| 0 | Repo scaffold + GitHub setup | ✅ Done |
| 1 | Databases (PostgreSQL + Neo4j schema) | ✅ Done |
| 2 | Backend APIs + Authentication | ✅ Done |
| 3 | Frontend shell | ⬜ Pending |
| 4 | OCR module | ⬜ Pending |
| 5 | Knowledge Graph | ⬜ Pending |
| 6 | AI / ML prediction engine | ⬜ Pending |
| 7 | Dashboard & Reports | ⬜ Pending |
| 8 | Deployment | ⬜ Pending |

---

## Getting Started

> Detailed setup arrives with each phase. For now:

```bash
# 1. Clone
git clone https://github.com/Ganesh-0509/Default-Sense.git
cd Default-Sense

# 2. Configure environment
cp .env.example .env   # then edit values

# 3. (Phases 1+) bring up services
# docker-compose up -d
```

---

## License

See [LICENSE](./LICENSE).
