"""Document + OCR schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: uuid.UUID
    customer_id: uuid.UUID
    document_type: str
    file_name: str | None
    uploaded_by: uuid.UUID | None
    upload_date: datetime


class OCRResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ocr_result_id: uuid.UUID
    document_id: uuid.UUID
    extracted_text: str | None
    confidence_score: Decimal | None
    processed_at: datetime


class OCRProcessRequest(BaseModel):
    document_id: uuid.UUID
