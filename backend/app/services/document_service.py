"""Document upload + OCR processing business logic."""

from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Document, OCRResult
from app.ocr import engine
from app.repositories import customer_repository, document_repository
from app.utils.responses import APIException


def _upload_dir() -> Path:
    path = Path(settings.upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _stored_path(document_id: uuid.UUID, file_name: str | None) -> Path:
    ext = Path(file_name or "").suffix.lower()
    return _upload_dir() / f"{document_id}{ext}"


def upload_document(
    db: Session,
    customer_id: uuid.UUID,
    document_type: str,
    original_name: str,
    content: bytes,
    uploaded_by: uuid.UUID | None,
) -> Document:
    if customer_repository.get_by_id(db, customer_id) is None:
        raise APIException(404, "Cannot upload document: customer not found.")

    ext = Path(original_name).suffix.lower()
    if ext not in engine.SUPPORTED_EXTENSIONS:
        raise APIException(
            400,
            "Unsupported file type.",
            {"supported": sorted(engine.SUPPORTED_EXTENSIONS)},
        )
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise APIException(413, f"File exceeds the {settings.max_upload_mb} MB limit.")
    if not content:
        raise APIException(400, "Uploaded file is empty.")

    document = Document(
        customer_id=customer_id,
        document_type=document_type,
        file_name=original_name,
        uploaded_by=uploaded_by,
    )
    document = document_repository.save_document(db, document)

    # Persist the bytes to disk keyed by the document id.
    _stored_path(document.document_id, original_name).write_bytes(content)
    return document


def get_document(db: Session, document_id: uuid.UUID) -> Document:
    document = document_repository.get_document(db, document_id)
    if document is None:
        raise APIException(404, "Document not found.")
    return document


def process_ocr(db: Session, document_id: uuid.UUID) -> OCRResult:
    document = get_document(db, document_id)
    path = _stored_path(document.document_id, document.file_name)
    if not path.exists():
        raise APIException(404, "Stored file for this document is missing.")

    if not engine.is_available():
        raise APIException(
            503, "OCR engine (Tesseract) is not available on the server."
        )

    try:
        text, confidence = engine.extract_text(path)
    except ValueError as exc:
        raise APIException(400, str(exc)) from exc
    except RuntimeError as exc:
        raise APIException(503, str(exc)) from exc

    ocr = OCRResult(
        document_id=document.document_id,
        extracted_text=text,
        confidence_score=confidence,
    )
    return document_repository.save_ocr(db, ocr)


def get_ocr_result(db: Session, document_id: uuid.UUID) -> OCRResult:
    get_document(db, document_id)  # 404 if the document itself is missing
    ocr = document_repository.get_ocr_by_document(db, document_id)
    if ocr is None:
        raise APIException(404, "No OCR result yet. Run /ocr/process first.")
    return ocr
