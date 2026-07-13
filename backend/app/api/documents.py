"""Document & OCR endpoints (docs/10 §7)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models import User
from app.ocr import engine
from app.schemas.document import DocumentOut, OCRProcessRequest, OCRResultOut
from app.services import document_service
from app.utils.responses import success

router = APIRouter(tags=["Documents & OCR"])


@router.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    customer_id: uuid.UUID = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    content = await file.read()
    document = document_service.upload_document(
        db,
        customer_id=customer_id,
        document_type=document_type,
        original_name=file.filename or "upload",
        content=content,
        uploaded_by=current_user.user_id,
    )
    return success(DocumentOut.model_validate(document), message="Document uploaded.")


@router.post("/ocr/process")
def process_ocr(
    payload: OCRProcessRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    ocr = document_service.process_ocr(db, payload.document_id)
    return success(OCRResultOut.model_validate(ocr), message="OCR completed.")


@router.get("/ocr/status")
def ocr_status(_: User = Depends(get_current_user)) -> dict:
    available = engine.is_available()
    return success(
        {"available": available, "engine": "tesseract", "version": engine.tesseract_version()},
        message="OCR engine status.",
    )


@router.get("/documents/{document_id}")
def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    document = document_service.get_document(db, document_id)
    return success(DocumentOut.model_validate(document), message="Document details.")


@router.get("/documents/{document_id}/text")
def get_document_text(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    ocr = document_service.get_ocr_result(db, document_id)
    return success(OCRResultOut.model_validate(ocr), message="OCR result.")
