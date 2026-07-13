"""One-shot environment bootstrap (used by the backend container entrypoint).

Idempotent. Waits for the databases, applies the PostgreSQL schema + seed and the
Neo4j constraints + seed, ensures an admin login, and trains the ML model if no
artifact exists yet.

Usage:  python -m app.scripts.init_all
"""

from __future__ import annotations

import time
from pathlib import Path

from sqlalchemy import create_engine, text

from app.config import settings

# Repo root: .../backend/app/scripts/init_all.py -> parents[3]
REPO = Path(__file__).resolve().parents[3]


def _wait_for_postgres(retries: int = 30, delay: int = 2) -> None:
    engine = create_engine(settings.database_url)
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("PostgreSQL is ready.")
            return
        except Exception as exc:  # noqa: BLE001 - retry loop
            print(f"Waiting for PostgreSQL ({attempt}/{retries})... {exc.__class__.__name__}")
            time.sleep(delay)
    raise SystemExit("PostgreSQL did not become ready in time.")


def _apply_postgres() -> None:
    schema = (REPO / "database" / "postgres" / "schema.sql").read_text(encoding="utf-8")
    seed = (REPO / "database" / "postgres" / "seed.sql").read_text(encoding="utf-8")
    engine = create_engine(settings.database_url)
    # Use the raw DBAPI cursor: a single-arg execute() does NO %-parameter
    # interpolation, so literal '%' in seed text (e.g. "down 22%") is safe.
    raw = engine.raw_connection()
    try:
        cursor = raw.cursor()
        cursor.execute(schema)
        cursor.execute(seed)
        raw.commit()
    finally:
        raw.close()
    print("PostgreSQL schema + seed applied.")


def _run_cypher_file(session, path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    # Strip // comment lines, then split into statements on ';'.
    lines = [ln for ln in raw.splitlines() if not ln.strip().startswith("//")]
    for statement in " ".join(lines).split(";"):
        stmt = statement.strip()
        if stmt:
            session.run(stmt)


def _apply_neo4j(retries: int = 30, delay: int = 2) -> None:
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password)
    )
    for attempt in range(1, retries + 1):
        try:
            driver.verify_connectivity()
            break
        except Exception as exc:  # noqa: BLE001
            print(f"Waiting for Neo4j ({attempt}/{retries})... {exc.__class__.__name__}")
            time.sleep(delay)
    else:
        print("WARNING: Neo4j not reachable; skipping graph seed.")
        return

    with driver.session() as session:
        _run_cypher_file(session, REPO / "database" / "neo4j" / "constraints.cypher")
        _run_cypher_file(session, REPO / "database" / "neo4j" / "seed.cypher")
    driver.close()
    print("Neo4j constraints + seed applied.")


def _train_model_if_missing() -> None:
    from app.ai import predictor

    if predictor.is_ready():
        print("ML model already present; skipping training.")
        return
    print("No trained model found — generating data and training (first boot)...")
    import sys

    sys.path.insert(0, str(REPO / "models"))
    import generate_synthetic  # type: ignore
    import train  # type: ignore

    generate_synthetic.main()
    train.main()


def main() -> None:
    _wait_for_postgres()
    _apply_postgres()
    _apply_neo4j()

    from app.scripts.seed_admin import main as seed_admin

    seed_admin()
    _train_model_if_missing()
    print("Bootstrap complete.")


if __name__ == "__main__":
    main()
