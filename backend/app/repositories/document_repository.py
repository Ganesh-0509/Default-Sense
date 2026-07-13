"""Data access for Document and OCRResult."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Document, OCRResult


def get_document(db: Session, document_id: uuid.UUID) -> Document | None:
    return db.get(Document, document_id)


def save_document(db: Session, document: Document) -> Document:
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_ocr_by_document(db: Session, document_id: uuid.UUID) -> OCRResult | None:
    stmt = (
        select(OCRResult)
        .where(OCRResult.document_id == document_id)
        .order_by(OCRResult.processed_at.desc())
    )
    return db.execute(stmt).scalars().first()


def save_ocr(db: Session, ocr: OCRResult) -> OCRResult:
    db.add(ocr)
    db.commit()
    db.refresh(ocr)
    return ocr
