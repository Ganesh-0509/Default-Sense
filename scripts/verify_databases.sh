#!/usr/bin/env bash
# ==========================================================
# DefaultSense AI — Verify databases (Phase 1)
# Prints PostgreSQL row counts + Neo4j node/relationship counts.
# Usage:  bash scripts/verify_databases.sh
# ==========================================================
set -euo pipefail
cd "$(dirname "$0")/.."

PG_USER="${POSTGRES_USER:-defaultsense}"
PG_DB="${POSTGRES_DB:-defaultsense}"
NEO_USER="${NEO4J_USERNAME:-neo4j}"
NEO_PASS="${NEO4J_PASSWORD:-changeme}"

echo "############## PostgreSQL ##############"
docker compose exec -T postgres psql -U "$PG_USER" -d "$PG_DB" < database/postgres/verify.sql

echo ""
echo "############## Neo4j ##############"
docker compose exec -T neo4j cypher-shell -u "$NEO_USER" -p "$NEO_PASS" < database/neo4j/verify.cypher
