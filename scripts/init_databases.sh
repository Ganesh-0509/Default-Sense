#!/usr/bin/env bash
# ==========================================================
# DefaultSense AI — Initialize databases (Phase 1)
# Brings up PostgreSQL + Neo4j, applies schema, constraints, and seeds.
# Idempotent: safe to re-run.
# Usage:  bash scripts/init_databases.sh
# ==========================================================
set -euo pipefail

cd "$(dirname "$0")/.."

PG_USER="${POSTGRES_USER:-defaultsense}"
PG_DB="${POSTGRES_DB:-defaultsense}"
NEO_USER="${NEO4J_USERNAME:-neo4j}"
NEO_PASS="${NEO4J_PASSWORD:-changeme}"

echo "==> Starting data services (docker compose up -d)..."
docker compose up -d postgres neo4j

echo "==> Waiting for PostgreSQL to be ready..."
until docker compose exec -T postgres pg_isready -U "$PG_USER" >/dev/null 2>&1; do
  sleep 2; printf '.'
done
echo " ready."

echo "==> Applying PostgreSQL schema..."
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U "$PG_USER" -d "$PG_DB" < database/postgres/schema.sql

echo "==> Loading PostgreSQL seed data..."
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U "$PG_USER" -d "$PG_DB" < database/postgres/seed.sql

echo "==> Waiting for Neo4j to be ready..."
until docker compose exec -T neo4j cypher-shell -u "$NEO_USER" -p "$NEO_PASS" "RETURN 1;" >/dev/null 2>&1; do
  sleep 3; printf '.'
done
echo " ready."

echo "==> Applying Neo4j constraints..."
docker compose exec -T neo4j cypher-shell -u "$NEO_USER" -p "$NEO_PASS" < database/neo4j/constraints.cypher

echo "==> Loading Neo4j seed data..."
docker compose exec -T neo4j cypher-shell -u "$NEO_USER" -p "$NEO_PASS" < database/neo4j/seed.cypher

echo "==> Done. Run 'bash scripts/verify_databases.sh' to check row/node counts."
