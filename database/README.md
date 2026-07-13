# DefaultSense AI — Database (Phase 1)

Hybrid store: **PostgreSQL** for structured banking data, **Neo4j** for relationship intelligence (Knowledge Graph). Design source of truth: [`docs/04_Database_Design.md`](../docs/04_Database_Design.md) and [`docs/11_Database_ERD.md`](../docs/11_Database_ERD.md).

## Layout

```
database/
├── postgres/
│   ├── schema.sql     # All tables, constraints, indexes (idempotent)
│   ├── seed.sql       # Referentially-consistent demo data (fixed UUIDs)
│   └── verify.sql     # Row counts + sample join
└── neo4j/
    ├── constraints.cypher  # Uniqueness constraints + indexes
    ├── seed.cypher         # Graph nodes/relationships (mirrors PG UUIDs)
    └── verify.cypher       # Node/relationship counts + risk-propagation query
```

## What's modeled

**PostgreSQL (15 tables):** branches, users, customers, loans, repayment_history,
transactions, credit_history, existing_liabilities, documents, ocr_results,
loan_officer_notes, ai_predictions, shap_explanations, alerts, audit_logs.
Validation rules from `docs/04 §8` are enforced as `CHECK` constraints
(credit_score 300–900, PD 0–100, positive amounts, non-negative delays, etc.).

**Neo4j (8 node labels):** Customer, Loan, Employer, Industry, Guarantor, Branch,
Region, EconomicEvent — linked by HAS_LOAN, WORKS_FOR, BELONGS_TO, GUARANTEED_BY,
LOCATED_IN, SERVES, AFFECTED_BY, RELATED_TO. Customer/Loan use the **same UUIDs**
as PostgreSQL so the two stores join cleanly.

The seed spans all 5 loan types and all 4 risk tiers (Low → Critical), and includes
a shared-guarantor link (connected-borrower risk) and a High-risk industry affected
by an economic event — the signals the ML phase turns into graph features.

## Run it

Prerequisite: **Docker Desktop running**.

```bash
# Bash
bash scripts/init_databases.sh       # up + schema + constraints + seeds
bash scripts/verify_databases.sh     # print counts

# PowerShell
powershell -File scripts\init_databases.ps1
powershell -File scripts\verify_databases.ps1
```

All scripts are **idempotent** — re-running loads nothing twice (`CREATE ... IF NOT EXISTS`,
`ON CONFLICT DO NOTHING`, `MERGE`).

## Access

| Service | URL / DSN | Credentials |
| --- | --- | --- |
| PostgreSQL | `postgresql://defaultsense:changeme@localhost:5432/defaultsense` | defaultsense / changeme |
| Neo4j Browser | http://localhost:7474 | neo4j / changeme |
| Neo4j Bolt | `bolt://localhost:7687` | neo4j / changeme |

> Credentials are local dev defaults from `docker-compose.yml` / `.env.example`. Change them for any non-local deployment.
