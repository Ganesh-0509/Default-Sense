// ==========================================================
// DefaultSense AI — Neo4j Constraints & Indexes (Phase 1)
// Relationship Intelligence (Knowledge Graph).
// Idempotent: IF NOT EXISTS on every statement.
// Ref: docs/04 §5, docs/11 §6
// ==========================================================

// ---------- Uniqueness constraints (each auto-creates a backing index) ----------
CREATE CONSTRAINT customer_id_unique  IF NOT EXISTS FOR (c:Customer)      REQUIRE c.customer_id IS UNIQUE;
CREATE CONSTRAINT loan_id_unique      IF NOT EXISTS FOR (l:Loan)          REQUIRE l.loan_id     IS UNIQUE;
CREATE CONSTRAINT employer_name_unique IF NOT EXISTS FOR (e:Employer)     REQUIRE e.name        IS UNIQUE;
CREATE CONSTRAINT industry_name_unique IF NOT EXISTS FOR (i:Industry)     REQUIRE i.name        IS UNIQUE;
CREATE CONSTRAINT guarantor_id_unique IF NOT EXISTS FOR (g:Guarantor)     REQUIRE g.guarantor_id IS UNIQUE;
CREATE CONSTRAINT branch_id_unique    IF NOT EXISTS FOR (b:Branch)        REQUIRE b.branch_id   IS UNIQUE;
CREATE CONSTRAINT region_name_unique  IF NOT EXISTS FOR (r:Region)        REQUIRE r.name        IS UNIQUE;
CREATE CONSTRAINT event_id_unique     IF NOT EXISTS FOR (ev:EconomicEvent) REQUIRE ev.event_id  IS UNIQUE;

// ---------- Secondary lookup indexes (non-unique properties) ----------
CREATE INDEX customer_name_idx IF NOT EXISTS FOR (c:Customer) ON (c.name);
CREATE INDEX employer_risk_idx IF NOT EXISTS FOR (e:Employer) ON (e.risk_score);
CREATE INDEX industry_risk_idx IF NOT EXISTS FOR (i:Industry) ON (i.risk_level);
