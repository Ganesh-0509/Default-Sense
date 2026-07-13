# ==========================================================
# DefaultSense AI - Verify databases (Phase 1)
# Prints PostgreSQL row counts + Neo4j node/relationship counts.
# Usage:  powershell -File scripts\verify_databases.ps1
# ==========================================================
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$PgUser  = if ($env:POSTGRES_USER)   { $env:POSTGRES_USER }   else { "defaultsense" }
$PgDb    = if ($env:POSTGRES_DB)     { $env:POSTGRES_DB }     else { "defaultsense" }
$NeoUser = if ($env:NEO4J_USERNAME)  { $env:NEO4J_USERNAME }  else { "neo4j" }
$NeoPass = if ($env:NEO4J_PASSWORD)  { $env:NEO4J_PASSWORD }  else { "changeme" }

Write-Host "############## PostgreSQL ##############"
Get-Content database\postgres\verify.sql -Raw | docker compose exec -T postgres psql -U $PgUser -d $PgDb

Write-Host ""
Write-Host "############## Neo4j ##############"
Get-Content database\neo4j\verify.cypher -Raw | docker compose exec -T neo4j cypher-shell -u $NeoUser -p $NeoPass
