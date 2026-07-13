-- ==========================================================
-- DefaultSense AI — PostgreSQL verification (Phase 1)
-- Row counts per table + a sample join proving referential integrity.
-- ==========================================================
\echo '--- Row counts per table ---'
SELECT 'branches'             AS table_name, count(*) FROM branches
UNION ALL SELECT 'users',              count(*) FROM users
UNION ALL SELECT 'customers',          count(*) FROM customers
UNION ALL SELECT 'loans',              count(*) FROM loans
UNION ALL SELECT 'repayment_history',  count(*) FROM repayment_history
UNION ALL SELECT 'transactions',       count(*) FROM transactions
UNION ALL SELECT 'credit_history',     count(*) FROM credit_history
UNION ALL SELECT 'existing_liabilities', count(*) FROM existing_liabilities
UNION ALL SELECT 'documents',          count(*) FROM documents
UNION ALL SELECT 'ocr_results',        count(*) FROM ocr_results
UNION ALL SELECT 'loan_officer_notes', count(*) FROM loan_officer_notes
UNION ALL SELECT 'ai_predictions',     count(*) FROM ai_predictions
UNION ALL SELECT 'shap_explanations',  count(*) FROM shap_explanations
UNION ALL SELECT 'alerts',             count(*) FROM alerts
UNION ALL SELECT 'audit_logs',         count(*) FROM audit_logs
ORDER BY table_name;

\echo '--- Customer risk view (join across customers, loans, predictions) ---'
SELECT c.customer_name, l.loan_type, l.loan_status,
       p.probability_of_default AS pd, p.risk_level, p.recommendation
FROM customers c
JOIN loans l          ON l.customer_id = c.customer_id
JOIN ai_predictions p ON p.customer_id = c.customer_id AND p.loan_id = l.loan_id
ORDER BY p.probability_of_default;
