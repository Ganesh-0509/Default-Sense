-- ==========================================================
-- DefaultSense AI — PostgreSQL Seed Data (Phase 1)
-- A small, referentially-consistent demo set covering all 5 loan
-- types and all 4 risk tiers. Fixed UUIDs → idempotent re-runs.
-- (The large synthetic 10k+ dataset is generated in the ML phase.)
-- ==========================================================

-- ---------- Branches ----------
INSERT INTO branches (branch_id, branch_name, region) VALUES
 ('b0000000-0000-0000-0000-000000000001', 'Mumbai Main',   'West'),
 ('b0000000-0000-0000-0000-000000000002', 'Chennai City',  'South'),
 ('b0000000-0000-0000-0000-000000000003', 'Delhi Central', 'North')
ON CONFLICT (branch_id) DO NOTHING;

-- ---------- Users (password_hash is a placeholder bcrypt stub; real auth in Phase 2) ----------
INSERT INTO users (user_id, full_name, email, password_hash, role, branch_id) VALUES
 ('a0000000-0000-0000-0000-000000000001', 'Asha Admin',    'admin@defaultsense.ai',   '$2b$12$seedplaceholderhashadmin000000000000000000000000000', 'admin',        'b0000000-0000-0000-0000-000000000003'),
 ('a0000000-0000-0000-0000-000000000002', 'Ravi Risk',     'risk@defaultsense.ai',    '$2b$12$seedplaceholderhashrisk0000000000000000000000000000', 'risk_manager', 'b0000000-0000-0000-0000-000000000001'),
 ('a0000000-0000-0000-0000-000000000003', 'Olivia Officer', 'officer@defaultsense.ai', '$2b$12$seedplaceholderhashoffcr000000000000000000000000000', 'loan_officer', 'b0000000-0000-0000-0000-000000000002')
ON CONFLICT (user_id) DO NOTHING;

-- ---------- Customers (6, spanning segments & risk tiers) ----------
INSERT INTO customers (customer_id, customer_name, gender, date_of_birth, occupation, employment_type, annual_income, credit_score, marital_status, phone, email, region, branch_id) VALUES
 ('c0000000-0000-0000-0000-000000000001', 'Priya Sharma',   'Female', '1990-04-12', 'Software Engineer', 'Salaried',       1800000,  810, 'Married', '+91-9000000001', 'priya@example.com',   'West',  'b0000000-0000-0000-0000-000000000001'),
 ('c0000000-0000-0000-0000-000000000002', 'Arjun Mehta',    'Male',   '1985-09-03', 'Shop Owner',        'Business Owner', 1200000,  690, 'Married', '+91-9000000002', 'arjun@example.com',   'South', 'b0000000-0000-0000-0000-000000000002'),
 ('c0000000-0000-0000-0000-000000000003', 'Kavya Nair',     'Female', '1993-12-21', 'Freelancer',        'Self-Employed',   700000,  640, 'Single',  '+91-9000000003', 'kavya@example.com',   'South', 'b0000000-0000-0000-0000-000000000002'),
 ('c0000000-0000-0000-0000-000000000004', 'Rohit Verma',    'Male',   '1978-06-30', 'Manufacturer',      'MSME',           2500000,  600, 'Married', '+91-9000000004', 'rohit@example.com',   'North', 'b0000000-0000-0000-0000-000000000003'),
 ('c0000000-0000-0000-0000-000000000005', 'Sunita Devi',    'Female', '1982-02-14', 'Farmer',            'Agriculture',     300000,  560, 'Married', '+91-9000000005', 'sunita@example.com',  'North', 'b0000000-0000-0000-0000-000000000003'),
 ('c0000000-0000-0000-0000-000000000006', 'Imran Khan',     'Male',   '1998-11-08', 'Student',           'Salaried',        450000,  520, 'Single',  '+91-9000000006', 'imran@example.com',   'West',  'b0000000-0000-0000-0000-000000000001')
ON CONFLICT (customer_id) DO NOTHING;

-- ---------- Loans (one per customer, varied types/statuses) ----------
INSERT INTO loans (loan_id, customer_id, loan_type, loan_amount, interest_rate, tenure_months, emi, outstanding_amount, loan_status, disbursement_date) VALUES
 ('10000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'Home',        6000000, 8.50, 240, 52000, 5400000, 'Active',   '2023-01-15'),
 ('10000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', 'Personal',     800000, 13.00,  48, 21500,  600000, 'Active',   '2023-06-01'),
 ('10000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000003', 'Education',    500000, 10.50,  60,  9800,  420000, 'Active',   '2023-09-10'),
 ('10000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000004', 'MSME',        3000000, 12.00,  84, 52000, 2600000, 'Overdue',  '2022-11-20'),
 ('10000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000005', 'Agriculture', 400000, 9.00,   36, 12500,  360000, 'Overdue',  '2023-03-05'),
 ('10000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000006', 'Personal',     300000, 15.00,  24, 14500,  280000, 'Defaulted','2023-02-18')
ON CONFLICT (loan_id) DO NOTHING;

-- ---------- Repayment history (recent behaviour; low-risk pays on time, high-risk delays/misses) ----------
INSERT INTO repayment_history (repayment_id, loan_id, due_date, payment_date, due_amount, payment_amount, delay_days, payment_status) VALUES
 ('20000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '2024-04-05', '2024-04-04', 52000, 52000,  0, 'Paid'),
 ('20000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000001', '2024-05-05', '2024-05-05', 52000, 52000,  0, 'Paid'),
 ('20000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000002', '2024-04-01', '2024-04-09', 21500, 21500,  8, 'Late'),
 ('20000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000003', '2024-04-10', '2024-04-10',  9800,  9800,  0, 'Paid'),
 ('20000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000004', '2024-04-20', '2024-05-06', 52000, 52000, 16, 'Late'),
 ('20000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000004', '2024-05-20', NULL,        52000,     0,  0, 'Missed'),
 ('20000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000005', '2024-04-05', '2024-04-30', 12500, 12500, 25, 'Late'),
 ('20000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000006', '2024-03-18', NULL,        14500,     0,  0, 'Missed'),
 ('20000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000006', '2024-04-18', NULL,        14500,     0,  0, 'Missed')
ON CONFLICT (repayment_id) DO NOTHING;

-- ---------- Transactions (a couple per customer) ----------
INSERT INTO transactions (transaction_id, customer_id, transaction_date, debit_amount, credit_amount, balance, transaction_type) VALUES
 ('30000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', '2024-05-01',      0, 150000, 320000, 'Salary'),
 ('30000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', '2024-05-05',  52000,      0, 268000, 'EMI'),
 ('30000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000004', '2024-05-02',  85000,      0,  15000, 'Supplier'),
 ('30000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000006', '2024-05-03',  12000,      0,   2000, 'Withdrawal')
ON CONFLICT (transaction_id) DO NOTHING;

-- ---------- Credit history (one per customer, one-to-one) ----------
INSERT INTO credit_history (credit_history_id, customer_id, credit_score, active_loans, closed_loans, overdue_accounts, credit_utilization, credit_enquiries, bureau_source) VALUES
 ('40000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 810, 1, 2, 0, 18.00, 1, 'CIBIL'),
 ('40000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', 690, 2, 1, 0, 55.00, 3, 'CIBIL'),
 ('40000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000003', 640, 1, 0, 1, 62.00, 4, 'CIBIL'),
 ('40000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000004', 600, 3, 1, 1, 78.00, 5, 'CIBIL'),
 ('40000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000005', 560, 2, 0, 2, 84.00, 6, 'CIBIL'),
 ('40000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000006', 520, 1, 0, 1, 92.00, 7, 'CIBIL')
ON CONFLICT (credit_history_id) DO NOTHING;

-- ---------- Existing liabilities ----------
INSERT INTO existing_liabilities (liability_id, customer_id, liability_type, amount, monthly_payment) VALUES
 ('50000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000002', 'Credit Card', 150000,  9000),
 ('50000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000004', 'Vehicle Loan', 600000, 18000),
 ('50000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000006', 'Credit Card',  90000,  6000)
ON CONFLICT (liability_id) DO NOTHING;

-- ---------- Documents + OCR results ----------
INSERT INTO documents (document_id, customer_id, document_type, file_name, uploaded_by) VALUES
 ('60000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000004', 'GST Statement', 'gst_rohit_2024.pdf', 'a0000000-0000-0000-0000-000000000003'),
 ('60000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', 'Salary Slip',   'salary_priya_apr.pdf', 'a0000000-0000-0000-0000-000000000003')
ON CONFLICT (document_id) DO NOTHING;

INSERT INTO ocr_results (ocr_result_id, document_id, extracted_text, confidence_score) VALUES
 ('70000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000001', 'GSTIN 27ABCDE1234F1Z5 turnover Q4 down 22% vs prior quarter', 96.50),
 ('70000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000002', 'Net pay 150000 credited monthly, stable employer',            98.20)
ON CONFLICT (ocr_result_id) DO NOTHING;

-- ---------- Loan officer notes (sentiment: positive for low risk, negative for high) ----------
INSERT INTO loan_officer_notes (note_id, customer_id, officer_id, note_text, sentiment_score) VALUES
 ('80000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000003', 'Stable salaried profile, excellent repayment record.',  0.850),
 ('80000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000003', 'Business turnover falling, industry under stress.',    -0.720),
 ('80000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000003', 'Multiple missed EMIs, unresponsive to reminders.',     -0.880)
ON CONFLICT (note_id) DO NOTHING;

-- ---------- AI predictions (one per customer, all 4 risk tiers represented) ----------
INSERT INTO ai_predictions (prediction_id, customer_id, loan_id, probability_of_default, risk_level, confidence_score, recommendation, model_version) VALUES
 ('e0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 12.00, 'Low',      93.00, 'Approve',                 'v0-seed'),
 ('e0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 38.00, 'Moderate', 88.00, 'Approve with Monitoring', 'v0-seed'),
 ('e0000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000003', 44.00, 'Moderate', 85.00, 'Approve with Monitoring', 'v0-seed'),
 ('e0000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000004', 68.00, 'High',     90.00, 'Additional Verification', 'v0-seed'),
 ('e0000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000005', 72.00, 'High',     87.00, 'Additional Verification', 'v0-seed'),
 ('e0000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000006', 88.00, 'Critical', 94.00, 'Reject / Escalate',       'v0-seed')
ON CONFLICT (prediction_id) DO NOTHING;

-- ---------- SHAP explanations (top contributors for the critical & high cases) ----------
INSERT INTO shap_explanations (shap_id, prediction_id, feature_name, contribution, impact_direction) VALUES
 ('f0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000006', 'missed_emi_count',    0.31000, 'positive'),
 ('f0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000006', 'credit_utilization',  0.24000, 'positive'),
 ('f0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000006', 'credit_score',        0.19000, 'positive'),
 ('f0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'employer_risk_score', 0.22000, 'positive'),
 ('f0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000004', 'debt_to_income',      0.20000, 'positive'),
 ('f0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000001', 'income_stability',    0.28000, 'negative')
ON CONFLICT (shap_id) DO NOTHING;

-- ---------- Alerts (for High / Critical predictions) ----------
INSERT INTO alerts (alert_id, customer_id, prediction_id, severity, alert_type, description, status) VALUES
 ('a1000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'High',     'Repayment Stress', 'Missed EMI + industry stress detected 12 months out.', 'open'),
 ('a1000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000005', 'High',     'Seasonal Risk',    'Agricultural seasonal income risk elevated.',          'open'),
 ('a1000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000006', 'Critical', 'Default Imminent', 'Consecutive missed EMIs, critical PD.',                'open')
ON CONFLICT (alert_id) DO NOTHING;

-- ---------- Audit log sample ----------
INSERT INTO audit_logs (log_id, user_id, action, module, details) VALUES
 ('b1000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'SEED_LOAD', 'database', '{"phase":1,"note":"initial demo seed"}')
ON CONFLICT (log_id) DO NOTHING;

-- ==========================================================
-- End of seed
-- ==========================================================
