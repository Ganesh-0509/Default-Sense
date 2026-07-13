"""FastAPI application entrypoint for DefaultSense AI."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.router import api_router
from app.config import settings
from app.middleware.error_handlers import register_exception_handlers
from app.utils.responses import success

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform.",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["System"])
def health() -> dict:
    """Liveness probe."""
    return success({"status": "ok", "service": settings.app_name, "version": __version__})


@app.get("/", tags=["System"])
def root() -> dict:
    return success(
        {"service": settings.app_name, "docs": "/docs", "api": settings.api_v1_prefix},
        message="DefaultSense AI backend is running.",
    )
