-- ==========================================================
-- DefaultSense AI — PostgreSQL Schema (Phase 1)
-- Structured banking data for 12-month PD prediction.
-- Idempotent: safe to run multiple times (CREATE ... IF NOT EXISTS).
-- Ref: docs/04_Database_Design.md, docs/11_Database_ERD.md
-- ==========================================================

-- gen_random_uuid() is built into PostgreSQL 13+ core. pgcrypto kept for safety.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------- Reference / Auth ----------

CREATE TABLE IF NOT EXISTS branches (
    branch_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_name   TEXT NOT NULL,
    region        TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS users (
    user_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name     TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'loan_officer'
                    CHECK (role IN ('admin','risk_manager','loan_officer','auditor')),
    branch_id     UUID REFERENCES branches(branch_id) ON DELETE SET NULL,
    status        TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active','inactive','suspended')),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- Customer Management ----------

CREATE TABLE IF NOT EXISTS customers (
    customer_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name   TEXT NOT NULL,
    gender          TEXT CHECK (gender IN ('Male','Female','Other')),
    date_of_birth   DATE,
    occupation      TEXT,
    employment_type TEXT CHECK (employment_type IN
                        ('Salaried','Self-Employed','Business Owner','MSME','Corporate','Agriculture')),
    annual_income   NUMERIC(14,2) CHECK (annual_income >= 0),
    credit_score    INTEGER CHECK (credit_score BETWEEN 300 AND 900),
    marital_status  TEXT,
    address         TEXT,
    phone           TEXT UNIQUE,
    email           TEXT UNIQUE,
    region          TEXT,
    branch_id       UUID REFERENCES branches(branch_id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- Loan Management ----------

CREATE TABLE IF NOT EXISTS loans (
    loan_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id        UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    loan_type          TEXT NOT NULL CHECK (loan_type IN
                          ('Personal','Home','MSME','Agriculture','Education')),
    loan_amount        NUMERIC(14,2) NOT NULL CHECK (loan_amount > 0),
    interest_rate      NUMERIC(5,2) NOT NULL CHECK (interest_rate >= 0),
    tenure_months      INTEGER NOT NULL CHECK (tenure_months > 0),
    emi                NUMERIC(14,2) NOT NULL CHECK (emi > 0),
    outstanding_amount NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (outstanding_amount >= 0),
    loan_status        TEXT NOT NULL DEFAULT 'Active'
                          CHECK (loan_status IN ('Active','Closed','Overdue','Defaulted')),
    disbursement_date  DATE,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS repayment_history (
    repayment_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    loan_id        UUID NOT NULL REFERENCES loans(loan_id) ON DELETE CASCADE,
    due_date       DATE NOT NULL,
    payment_date   DATE,
    due_amount     NUMERIC(14,2) NOT NULL CHECK (due_amount > 0),
    payment_amount NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (payment_amount >= 0),
    delay_days     INTEGER NOT NULL DEFAULT 0 CHECK (delay_days >= 0),
    payment_status TEXT NOT NULL DEFAULT 'Paid'
                     CHECK (payment_status IN ('Paid','Late','Missed','Partial'))
);

-- ---------- Financial Data ----------

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id      UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    transaction_date DATE NOT NULL,
    debit_amount     NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (debit_amount >= 0),
    credit_amount    NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (credit_amount >= 0),
    balance          NUMERIC(14,2),
    transaction_type TEXT
);

CREATE TABLE IF NOT EXISTS credit_history (
    credit_history_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id        UUID NOT NULL UNIQUE REFERENCES customers(customer_id) ON DELETE CASCADE,
    credit_score       INTEGER CHECK (credit_score BETWEEN 300 AND 900),
    active_loans       INTEGER NOT NULL DEFAULT 0 CHECK (active_loans >= 0),
    closed_loans       INTEGER NOT NULL DEFAULT 0 CHECK (closed_loans >= 0),
    overdue_accounts   INTEGER NOT NULL DEFAULT 0 CHECK (overdue_accounts >= 0),
    credit_utilization NUMERIC(5,2) CHECK (credit_utilization BETWEEN 0 AND 100),
    credit_enquiries   INTEGER NOT NULL DEFAULT 0 CHECK (credit_enquiries >= 0),
    bureau_source      TEXT,
    recorded_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS existing_liabilities (
    liability_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    liability_type  TEXT NOT NULL,
    amount          NUMERIC(14,2) NOT NULL CHECK (amount >= 0),
    monthly_payment NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (monthly_payment >= 0)
);

-- ---------- Document Management (unstructured) ----------

CREATE TABLE IF NOT EXISTS documents (
    document_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id   UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    document_type TEXT NOT NULL,
    file_name     TEXT,
    uploaded_by   UUID REFERENCES users(user_id) ON DELETE SET NULL,
    upload_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ocr_results (
    ocr_result_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id      UUID NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    extracted_text   TEXT,
    confidence_score NUMERIC(5,2) CHECK (confidence_score BETWEEN 0 AND 100),
    processed_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS loan_officer_notes (
    note_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    officer_id      UUID REFERENCES users(user_id) ON DELETE SET NULL,
    note_text       TEXT NOT NULL,
    sentiment_score NUMERIC(4,3) CHECK (sentiment_score BETWEEN -1 AND 1),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- AI Intelligence ----------

CREATE TABLE IF NOT EXISTS ai_predictions (
    prediction_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id            UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    loan_id                UUID REFERENCES loans(loan_id) ON DELETE SET NULL,
    prediction_date        TIMESTAMPTZ NOT NULL DEFAULT now(),
    probability_of_default NUMERIC(5,2) NOT NULL CHECK (probability_of_default BETWEEN 0 AND 100),
    risk_level             TEXT NOT NULL CHECK (risk_level IN ('Low','Moderate','High','Critical')),
    confidence_score       NUMERIC(5,2) CHECK (confidence_score BETWEEN 0 AND 100),
    recommendation         TEXT,
    model_version          TEXT
);

CREATE TABLE IF NOT EXISTS shap_explanations (
    shap_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id    UUID NOT NULL REFERENCES ai_predictions(prediction_id) ON DELETE CASCADE,
    feature_name     TEXT NOT NULL,
    contribution     NUMERIC(8,5) NOT NULL,
    impact_direction TEXT NOT NULL CHECK (impact_direction IN ('positive','negative'))
);

-- ---------- Monitoring ----------

CREATE TABLE IF NOT EXISTS alerts (
    alert_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id   UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    prediction_id UUID REFERENCES ai_predictions(prediction_id) ON DELETE SET NULL,
    severity      TEXT NOT NULL CHECK (severity IN ('Low','Moderate','High','Critical')),
    alert_type    TEXT NOT NULL,
    description   TEXT,
    status        TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','acknowledged','resolved','dismissed')),
    generated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action     TEXT NOT NULL,
    module     TEXT,
    details    JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- Indexes (ref: docs/04 §9, docs/11 §9) ----------

CREATE INDEX IF NOT EXISTS idx_users_branch          ON users(branch_id);
CREATE INDEX IF NOT EXISTS idx_customers_branch       ON customers(branch_id);
CREATE INDEX IF NOT EXISTS idx_customers_credit_score ON customers(credit_score);
CREATE INDEX IF NOT EXISTS idx_loans_customer         ON loans(customer_id);
CREATE INDEX IF NOT EXISTS idx_loans_type             ON loans(loan_type);
CREATE INDEX IF NOT EXISTS idx_loans_status           ON loans(loan_status);
CREATE INDEX IF NOT EXISTS idx_repayment_loan         ON repayment_history(loan_id);
CREATE INDEX IF NOT EXISTS idx_repayment_due_date     ON repayment_history(due_date);
CREATE INDEX IF NOT EXISTS idx_transactions_customer  ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date      ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_credit_customer        ON credit_history(customer_id);
CREATE INDEX IF NOT EXISTS idx_liabilities_customer   ON existing_liabilities(customer_id);
CREATE INDEX IF NOT EXISTS idx_documents_customer     ON documents(customer_id);
CREATE INDEX IF NOT EXISTS idx_ocr_document           ON ocr_results(document_id);
CREATE INDEX IF NOT EXISTS idx_notes_customer         ON loan_officer_notes(customer_id);
CREATE INDEX IF NOT EXISTS idx_predictions_customer   ON ai_predictions(customer_id);
CREATE INDEX IF NOT EXISTS idx_predictions_loan       ON ai_predictions(loan_id);
CREATE INDEX IF NOT EXISTS idx_predictions_date       ON ai_predictions(prediction_date);
CREATE INDEX IF NOT EXISTS idx_shap_prediction        ON shap_explanations(prediction_id);
CREATE INDEX IF NOT EXISTS idx_alerts_customer        ON alerts(customer_id);
CREATE INDEX IF NOT EXISTS idx_alerts_status          ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_audit_user             ON audit_logs(user_id);

-- ==========================================================
-- End of schema
-- ==========================================================
