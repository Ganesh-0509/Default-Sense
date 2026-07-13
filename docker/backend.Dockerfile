# DefaultSense AI — Backend image (Phase 8)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

WORKDIR /app

# System deps: Tesseract OCR (Phase 4) + libgomp for xgboost.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Python deps first (better layer caching)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Application + ML + DB init assets
COPY backend ./backend
COPY models ./models
COPY database ./database

# Entrypoint: bootstrap (DB init + seed + train), then serve.
COPY docker/backend-entrypoint.sh /usr/local/bin/backend-entrypoint.sh
RUN chmod +x /usr/local/bin/backend-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/backend-entrypoint.sh"]
