# DefaultSense AI — Project Context

> A living context document for anyone (developer or AI assistant) working on this repository.
> Read this first before writing code. It captures **what** we are building, **why**, **how** it is organized, and **how work is done** here.

---

## 1. One-line Summary

DefaultSense AI is a **Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform** that predicts a borrower's **Probability of Default (PD) up to 12 months in advance** and explains every prediction.

---

## 2. Why This Exists (The Problem)

**IDBI Bank Hackathon (Hack2Skill) — Problem Statement 4: Default Prediction Model.**

Current banking default-prediction systems are limited by:
- Low prediction accuracy (**16–22%**)
- Dependence on **structured data only**
- **Fragmented methodologies** across loan types and borrower segments
- Poor interpretability and late detection of stress

**Expected outcome:** a robust predictive solution that estimates PD to flag stressed loans **12 months in advance**, improves accuracy, uses **both structured and unstructured data**, applies **suitable methods per loan type / borrower profile**, and provides a **common interpretation framework** for consistent, comparable, actionable results.

---

## 3. Our Solution — Four Intelligence Layers

| Layer | Purpose | Key Tech |
| --- | --- | --- |
| **Structured Intelligence** | Credit history, repayment behaviour, transactions, financial ratios | PostgreSQL, feature engineering |
| **Unstructured Intelligence** | OCR of financial docs, loan-officer notes, industry news (NLP sentiment/keywords) | Tesseract OCR, NLP |
| **Relationship Intelligence** | Risk propagation through employer / industry / guarantor / region networks | Neo4j Knowledge Graph |
| **Decision Intelligence** | 12-month PD + risk category + confidence + explanation + recommendation | XGBoost + SHAP |

The four layers feed an **ensemble decision engine** that outputs a single, explainable PD score plus a recommended action.

---

## 4. Tech Stack (committed)

| Layer | Technology |
| --- | --- |
| Frontend | React + Vite, Tailwind CSS, Zustand, React Router, Axios, Recharts, React Flow, Lucide icons |
| Backend | FastAPI (Python 3.12+), SQLAlchemy, Pydantic, JWT/OAuth2 |
| Database | PostgreSQL |
| Graph DB | Neo4j |
| ML | XGBoost (primary); LightGBM / CatBoost / RandomForest / LogisticRegression (baselines) |
| Explainability | SHAP |
| OCR | Tesseract OCR |
| Deployment | Docker / docker-compose |

---

## 5. Repository Map

```
Default-Sense/
├── frontend/        # React + Vite app (src/: components, pages, layouts, hooks, services, store, routes, utils, types)
├── backend/         # FastAPI app (app/: api, auth, config, models, schemas, services, repositories, ai, graph, ocr, reports, middleware, utils, database)
├── database/        # migrations, schema, seeds, postgres/, neo4j/
├── datasets/        # raw, processed, synthetic, ocr_documents, sample_data
├── models/          # training, preprocessing, feature_engineering, prediction, evaluation, shap, saved_models, notebooks
├── docs/            # All design documentation (01–18) — the source of truth
├── docker/          # Dockerfiles
├── scripts/         # Utility scripts
├── tests/           # backend, frontend, ai, api, integration, performance
├── .env.example     # Environment template (copy to .env)
├── docker-compose.yml
├── README.md
└── CONTEXT.md       # This file
```

---

## 6. Documentation Index (docs/ — the source of truth)

| # | Document | Use it for |
| --- | --- | --- |
| 01 | Project PRD | Vision, features, scope, requirements |
| 02 | System Architecture | Layers, data flow, security |
| 03 | AI/ML Design | Models, feature engineering, ensemble, SHAP |
| 04 | Database Design | PostgreSQL tables + Neo4j schema |
| 05 | Backend Architecture | FastAPI service layout, request lifecycle |
| 06 | Frontend UI/UX | Screens, components, color/risk system |
| 07 | Implementation Guide | Phase-by-phase build sequence |
| 08 | Hackathon Guide | Demo script, judging alignment, pitch |
| 09 | AI Agent Instructions | Coding rules & conventions |
| 10 | API Specification | Every REST endpoint |
| 11 | Database ERD | Entity relationships & cardinality |
| 12 | Dataset & Data Sources | Public datasets + synthetic data plan |
| 13 | Development Roadmap | Day-by-day timeline |
| 14 | Project Structure | Folder layout, branch & naming conventions |
| 15 | Deployment Guide | Env vars, Docker, cloud, backup |
| 16 | UI Wireframes | ASCII wireframes per screen |
| 18 | AI Training Pipeline | ML train → evaluate → SHAP → serve |

> When a design question comes up, the answer is almost always already in `docs/`. Check there before inventing new behaviour.

---

## 7. Build Phases & Status

We build **one phase at a time**. Each phase is completed, verified end-to-end, and pushed to GitHub before the next begins.

| Phase | Description | Status |
| --- | --- | --- |
| 0 | Repo scaffold + GitHub setup | ✅ Done |
| 1 | Databases — PostgreSQL + Neo4j schema + seed data | ✅ Done |
| 2 | Backend APIs + JWT Authentication | ⬜ Pending |
| 3 | Frontend shell (routing, layout, auth screens) | ⬜ Pending |
| 4 | OCR module (Tesseract) | ⬜ Pending |
| 5 | Knowledge Graph (Neo4j integration + queries) | ⬜ Pending |
| 6 | AI / ML prediction engine (XGBoost + SHAP) | ⬜ Pending |
| 7 | Dashboard & Reports | ⬜ Pending |
| 8 | Deployment | ⬜ Pending |

---

## 8. Data Model (quick reference)

**PostgreSQL core tables:** Users, Customers, Loans, Repayment History, Transactions, Credit History, Loan Officer Notes, OCR Documents, AI Predictions, SHAP Explanations, Alerts, Audit Logs.

**Neo4j nodes:** Customer, Loan, Employer, Industry, Guarantor, Branch, Region, Economic Event.
**Neo4j relationships:** `HAS_LOAN`, `WORKS_FOR`, `BELONGS_TO`, `GUARANTEED_BY`, `LOCATED_IN`, `SERVES`, `AFFECTED_BY`, `RELATED_TO`.

Full field lists and constraints: `docs/04_Database_Design.md` and `docs/11_Database_ERD.md`.

---

## 9. Recommendation Tiers (business rule)

| PD Score | Risk | Recommendation |
| --- | --- | --- |
| 0–25 | Low | Approve |
| 26–50 | Moderate | Approve with Monitoring |
| 51–75 | High | Additional Verification |
| 76–100 | Critical | Reject / Escalate |

Risk colors: Green (Low), Yellow (Moderate), Orange (High), Red (Critical), Blue (Info).

---

## 10. Conventions

**Code**
- React components → `PascalCase`; Python files → `snake_case`; variables → `camelCase`; constants → `UPPER_CASE`; API routes → `kebab-case`.
- Backend: layered architecture (api → services → repositories → models). Keep frontend and backend logic separate.
- Every API returns a consistent envelope:
  ```json
  { "success": true, "message": "...", "data": {} }
  ```
  Errors: `{ "success": false, "message": "...", "errors": {} }`.
- Validate all inputs (Pydantic). Never hardcode secrets. Add error handling everywhere.

**Frontend pages** must handle: loading state, error state, empty state, responsive layout.

**Security:** JWT auth, bcrypt password hashing, RBAC, parameterized queries, CORS config, HTTPS in prod.

**Git branches:** `main` (stable), `develop` (active), `feature/*`, `fix/*`, `release/*`.

---

## 11. How We Work (Workflow Contract)

1. **Phase-driven & command-driven** — work proceeds one phase at a time, only on explicit instruction. No jumping ahead.
2. **Build completely** — finish the whole phase, not fragments.
3. **Double-verify** — actually run/test the result and show evidence it works, not just that code was written.
4. **Push per phase** — each completed, verified phase is committed with a clear message and pushed to GitHub.
5. **Report and wait** — summarize what was done + verification results, then wait for the next command.

**Commit messages:** clear and descriptive, prefixed with the phase (e.g. `Phase 1: PostgreSQL schema + Neo4j constraints + seed data`). No third-party tool attribution.

---

## 12. Environment Setup

```bash
git clone https://github.com/Ganesh-0509/Default-Sense.git
cd Default-Sense
cp .env.example .env        # then fill in values
docker-compose up -d        # brings up PostgreSQL + Neo4j (Phase 1+)
```

Key env vars: `DATABASE_URL`, `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`, `JWT_SECRET`, `MODEL_PATH`, `OCR_PATH`, `FRONTEND_URL`.

---

## 13. The 90% Accuracy Strategy (important for judging)

The problem statement targets **accuracy improving to 90%**. On imbalanced default data, **raw accuracy is misleading** (predicting "no default" for everyone can already score ~90%+ while catching zero defaulters). We therefore never report accuracy alone — we report a bundle and lead with ROC-AUC.

**Committed target bundle:** **ROC-AUC ≥ 0.90** (the headline "90%"), **Recall on defaulters ≥ 85%**, **Accuracy ≥ 90%** (never alone), plus PR-AUC, F1, and KS/Gini. Keep AUC in the credible **0.90–0.94** band — 0.98–0.99 reads as leakage/overfit.

**The four levers that get us from the 16–22% baseline to 90%:**
1. **Class imbalance handling** — `scale_pos_weight` + SMOTE **on the train fold only, after the split** (never before, or it leaks).
2. **Multi-modal feature engineering** — every layer emits numeric features (structured ratios/trends, OCR/NLP sentiment, Neo4j graph aggregates, 12-month temporal windows). This is what lifts the ceiling beyond structured-only.
3. **Model strength** — XGBoost+LightGBM+CatBoost stack, Optuna tuning, stratified k-fold CV, threshold tuning (not 0.5), probability calibration.
4. **Segment-aware evaluation** — report the bundle per loan type / borrower segment, plus a **baseline (logistic, structured-only) vs full-pipeline** before/after as the demo narrative.

Full detail lives in `docs/03` §13, `docs/18` §4/6/7/8, and `docs/12` §7.1. Frame all demo/report results this way.

---

*Keep this file updated as phases complete and decisions are made. It is the fastest way for anyone to get productive on DefaultSense AI.*
