# DefaultSense AI — Backend (Phase 2)

FastAPI backend with JWT authentication, layered architecture
(`api → services → repositories → models`), and a consistent response envelope.
Design source: [`docs/05_Backend_Architecture.md`](../docs/05_Backend_Architecture.md),
[`docs/10_API_Specification.md`](../docs/10_API_Specification.md).

## Layout

```
backend/app/
├── main.py            # FastAPI app, CORS, exception handlers, health
├── config/            # Settings (env / .env)
├── database/          # SQLAlchemy engine + session + get_db
├── models/            # ORM models mapped onto the Phase 1 schema
├── schemas/           # Pydantic request/response models
├── auth/              # bcrypt hashing, JWT, RBAC dependencies
├── repositories/      # Data access (DB queries only)
├── services/          # Business logic
├── api/               # Routers (auth, customers, loans)
├── middleware/        # Global exception handlers → standard envelope
├── utils/             # Response helpers + APIException
└── scripts/           # seed_admin.py (sets a real admin password)
```

## Endpoints (all under `/api/v1`)

| Area | Endpoints |
| --- | --- |
| Auth | `POST /auth/login`, `POST /auth/logout`, `GET /auth/profile`, `POST /auth/change-password` |
| Customers | `GET /customers`, `GET /customers/search`, `GET /customers/{id}`, `POST /customers`, `PUT /customers/{id}`, `DELETE /customers/{id}` |
| Loans | `GET /loans`, `GET /loans/{id}`, `GET /loans/{id}/repayments`, `POST /loans`, `PUT /loans/{id}` |
| Documents & OCR | `POST /documents/upload`, `POST /ocr/process`, `GET /ocr/status`, `GET /documents/{id}`, `GET /documents/{id}/text` |
| Knowledge Graph | `GET /graph/status`, `GET /graph/search`, `GET /graph/customer/{id}`, `GET /graph/risk/{id}` |
| AI Predictions | `GET /predictions/model`, `POST /predictions/run`, `GET /predictions/{id}`, `GET /predictions/customer/{id}`, `GET /predictions/portfolio`, `GET /predictions/{id}/shap`, `GET /predictions/{id}/features` |
| Dashboard | `GET /dashboard/summary`, `/dashboard/risk-distribution`, `/dashboard/high-risk`, `/dashboard/trends` |
| Alerts | `GET /alerts`, `GET /alerts/{id}`, `PUT /alerts/{id}/read` |
| Reports | `GET /reports/portfolio`, `/reports/risk`, `/reports/customer/{id}`, `/reports/export/csv`, `/reports/export/pdf` |
| System | `GET /health`, `GET /` |

**Dashboard & Reports (Phase 7):** KPI/risk-distribution/high-risk/trends aggregations,
alert management, and portfolio/customer reports with CSV + PDF (reportlab) export.

**AI Predictions (Phase 6):** loads the XGBoost+SHAP artifact from `models/saved_models/`,
gathers multi-modal features for a customer (structured + behavioural + OCR/NLP + Neo4j graph),
returns a 12-month PD, risk tier, recommendation, confidence, and SHAP risk drivers — stored to
`ai_predictions` + `shap_explanations`. Train the model first: `python models/train.py`.

**Knowledge Graph (Phase 5):** Neo4j via the official driver. `/graph/customer/{id}` returns the
2-hop relationship subgraph (nodes + edges, ready for React Flow); `/graph/risk/{id}` computes a
relationship-risk score from employer risk, industry risk, economic events, and connected-borrower
defaults (shared guarantor) — the graph features the ML engine consumes in Phase 6.

**OCR (Phase 4):** Tesseract via `pytesseract`. Upload an image document (PNG/JPG/TIFF/BMP/WEBP),
then `POST /ocr/process` to extract text + confidence. The engine auto-detects the Tesseract
binary from `OCR_PATH`, PATH, or common install locations. Install Tesseract on the host
(`winget install UB-Mannheim.TesseractOCR`, or apt/brew). Uploaded files are stored under
`uploads/` (gitignored).

Every response uses the envelope `{ "success", "message", "data" }` (or `{ ..., "errors" }` on failure).
Protected endpoints require a `Bearer` JWT; writes are role-gated (RBAC).

## Run locally

Prerequisite: Phase 1 databases up (`bash scripts/init_databases.sh`).

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash;  .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

# from repo root or with DATABASE_URL set, seed a real admin password:
python -m app.scripts.seed_admin           # admin@defaultsense.ai / ChangeMe123!

uvicorn app.main:app --reload              # http://localhost:8000/docs
```

## Test

```bash
cd backend && python -m pytest ../tests/backend -v
```

## Default dev credentials

`admin@defaultsense.ai` / `ChangeMe123!` (override via `ADMIN_EMAIL` / `ADMIN_PASSWORD`).
Change these for any non-local deployment.
