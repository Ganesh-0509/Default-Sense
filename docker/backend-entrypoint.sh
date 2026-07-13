#!/usr/bin/env bash
# DefaultSense AI — backend container entrypoint.
# Bootstraps the environment (idempotent), then starts the API server.
set -e

cd /app

echo "==> Bootstrapping DefaultSense (DB init + seed + model)..."
python -m app.scripts.init_all

echo "==> Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir /app/backend
