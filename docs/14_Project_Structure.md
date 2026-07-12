# 14_Project_Structure.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Project Structure & Repository Organization

---

# 1. Objective

This document defines the complete folder structure, coding organization, and repository layout for **DefaultSense AI**. Following this structure ensures the project remains modular, scalable, and easy to maintain.

---

# 2. Root Folder Structure

```text
defaultsense-ai/

├── frontend/
├── backend/
├── database/
├── datasets/
├── models/
├── docs/
├── docker/
├── scripts/
├── tests/
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# 3. Frontend Structure

```text
frontend/

src/
├── assets/
├── components/
├── layouts/
├── pages/
├── hooks/
├── services/
├── store/
├── routes/
├── utils/
├── types/
├── App.jsx
└── main.jsx
```

---

# 4. Backend Structure

```text
backend/

app/
├── api/
├── auth/
├── config/
├── models/
├── schemas/
├── services/
├── repositories/
├── ai/
├── graph/
├── ocr/
├── reports/
├── middleware/
├── utils/
├── database/
└── main.py
```

---

# 5. AI Module

```text
models/

├── training/
├── preprocessing/
├── feature_engineering/
├── prediction/
├── evaluation/
├── shap/
├── saved_models/
└── notebooks/
```

---

# 6. Dataset Folder

```text
datasets/

├── raw/
├── processed/
├── synthetic/
├── ocr_documents/
└── sample_data/
```

---

# 7. Database Folder

```text
database/

├── migrations/
├── schema/
├── seeds/
├── postgres/
└── neo4j/
```

---

# 8. Documentation Folder

```text
docs/

01_PRD.md
02_System_Architecture.md
03_AI_ML_Design.md
04_Database_Design.md
05_Backend_Architecture.md
06_Frontend_UI_UX.md
07_Implementation_Guide.md
08_Hackathon_Guide.md
09_AI_Agent_Instructions.md
10_API_Specification.md
11_Database_ERD.md
12_Dataset_and_Data_Sources.md
13_Development_Roadmap.md
14_Project_Structure.md
15_Deployment_Guide.md
```

---

# 9. Docker Folder

```text
docker/

├── frontend.Dockerfile
├── backend.Dockerfile
├── postgres.Dockerfile
└── docker-compose.yml
```

---

# 10. Testing Folder

```text
tests/

├── backend/
├── frontend/
├── ai/
├── api/
├── integration/
└── performance/
```

---

# 11. Environment Variables

```text
.env

DATABASE_URL=

NEO4J_URI=

JWT_SECRET=

OPENAI_API_KEY=

OCR_PATH=

MODEL_PATH=
```

---

# 12. Branch Strategy

| Branch    | Purpose             |
| --------- | ------------------- |
| main      | Stable Production   |
| develop   | Active Development  |
| feature/* | New Features        |
| fix/*     | Bug Fixes           |
| release/* | Release Preparation |

---

# 13. Naming Convention

| Item             | Convention |
| ---------------- | ---------- |
| React Components | PascalCase |
| Python Files     | snake_case |
| Variables        | camelCase  |
| Constants        | UPPER_CASE |
| APIs             | kebab-case |

---

# 14. Deliverables

The repository will contain:

* Complete frontend
* Complete backend
* AI models
* Database schema
* Datasets
* Documentation
* Docker configuration
* Tests
* Deployment files

All components will be organized for easy development, testing, and deployment.
