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
| System | `GET /health`, `GET /` |

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
