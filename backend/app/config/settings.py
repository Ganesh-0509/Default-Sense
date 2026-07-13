"""Application configuration, loaded from environment / .env."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object. Values come from environment variables or .env."""

    # ---- App ----
    app_name: str = "DefaultSense AI"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # ---- PostgreSQL ----
    database_url: str = "postgresql://defaultsense:changeme@localhost:5432/defaultsense"

    # ---- Neo4j (used from Phase 5; declared here so config is complete) ----
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "changeme"

    # ---- Authentication ----
    jwt_secret: str = "replace-with-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # ---- AI / ML (Phase 6) ----
    # Directory holding saved model artifacts. If empty/relative, the predictor
    # falls back to <repo>/models/saved_models. Env var: MODEL_PATH.
    model_path: str = ""

    # ---- OCR (Phase 4) ----
    # Explicit path to the Tesseract binary. If empty, the engine auto-detects it
    # from PATH or common install locations. Env var: OCR_PATH.
    ocr_path: str = ""
    # Directory where uploaded documents are stored (gitignored).
    upload_dir: str = "uploads"
    max_upload_mb: int = 10

    # ---- CORS ----
    frontend_url: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins(self) -> list[str]:
        return [self.frontend_url, "http://localhost:5173", "http://localhost:3000"]


settings = Settings()
