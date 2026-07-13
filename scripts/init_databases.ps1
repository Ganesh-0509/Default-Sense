# ==========================================================
# DefaultSense AI - Initialize databases (Phase 1)
# Brings up PostgreSQL + Neo4j, applies schema, constraints, and seeds.
# Idempotent: safe to re-run.
# Usage:  powershell -File scripts\init_databases.ps1
# ==========================================================
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$PgUser  = if ($env:POSTGRES_USER)   { $env:POSTGRES_USER }   else { "defaultsense" }
$PgDb    = if ($env:POSTGRES_DB)     { $env:POSTGRES_DB }     else { "defaultsense" }
$NeoUser = if ($env:NEO4J_USERNAME)  { $env:NEO4J_USERNAME }  else { "neo4j" }
$NeoPass = if ($env:NEO4J_PASSWORD)  { $env:NEO4J_PASSWORD }  else { "changeme" }

Write-Host "==> Starting data services (docker compose up -d)..."
docker compose up -d postgres neo4j

Write-Host "==> Waiting for PostgreSQL to be ready..."
do {
  Start-Sleep -Seconds 2
  docker compose exec -T postgres pg_isready -U $PgUser *> $null
} while ($LASTEXITCODE -ne 0)
Write-Host "    ready."

Write-Host "==> Applying PostgreSQL schema..."
Get-Content database\postgres\schema.sql -Raw | docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $PgUser -d $PgDb

Write-Host "==> Loading PostgreSQL seed data..."
Get-Content database\postgres\seed.sql -Raw | docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $PgUser -d $PgDb

Write-Host "==> Waiting for Neo4j to be ready..."
do {
  Start-Sleep -Seconds 3
  docker compose exec -T neo4j cypher-shell -u $NeoUser -p $NeoPass "RETURN 1;" *> $null
} while ($LASTEXITCODE -ne 0)
Write-Host "    ready."

Write-Host "==> Applying Neo4j constraints..."
Get-Content database\neo4j\constraints.cypher -Raw | docker compose exec -T neo4j cypher-shell -u $NeoUser -p $NeoPass

Write-Host "==> Loading Neo4j seed data..."
Get-Content database\neo4j\seed.cypher -Raw | docker compose exec -T neo4j cypher-shell -u $NeoUser -p $NeoPass

Write-Host "==> Done. Run scripts\verify_databases.ps1 to check row/node counts."
