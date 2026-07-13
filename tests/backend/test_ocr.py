"""OCR module tests — generates an image with known text and verifies extraction.

Requires the Tesseract binary installed on the host (Phase 4 dependency).
"""

from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw, ImageFont

from app.ocr import engine

SEED_CUSTOMER = "c0000000-0000-0000-0000-000000000001"
OCR_AVAILABLE = engine.is_available()


def _font(size: int = 48) -> ImageFont.ImageFont:
    """A legible TrueType font for clean OCR; fall back to PIL's default."""
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _make_text_image(text: str) -> bytes:
    """Render text on a white image at a size Tesseract reads reliably."""
    img = Image.new("RGB", (900, 160), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((30, 50), text, fill="black", font=_font(48))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_ocr_status(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get("/api/v1/ocr/status", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["engine"] == "tesseract"


def test_upload_rejects_unsupported_type(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.post(
        "/api/v1/documents/upload",
        data={"customer_id": SEED_CUSTOMER, "document_type": "Salary Slip"},
        files={"file": ("notes.txt", b"hello", "text/plain")},
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_upload_unknown_customer(client: TestClient, auth_headers: dict[str, str]) -> None:
    png = _make_text_image("HELLO")
    resp = client.post(
        "/api/v1/documents/upload",
        data={
            "customer_id": "00000000-0000-0000-0000-000000000000",
            "document_type": "Salary Slip",
        },
        files={"file": ("doc.png", png, "image/png")},
        headers=auth_headers,
    )
    assert resp.status_code == 404


@pytest.mark.skipif(not OCR_AVAILABLE, reason="Tesseract binary not installed")
def test_upload_and_ocr_roundtrip(client: TestClient, auth_headers: dict[str, str]) -> None:
    png = _make_text_image("INVOICE 12345")

    # Upload
    up = client.post(
        "/api/v1/documents/upload",
        data={"customer_id": SEED_CUSTOMER, "document_type": "Financial Statement"},
        files={"file": ("invoice.png", png, "image/png")},
        headers=auth_headers,
    )
    assert up.status_code == 201, up.text
    document_id = up.json()["data"]["document_id"]

    # Process OCR
    proc = client.post(
        "/api/v1/ocr/process",
        json={"document_id": document_id},
        headers=auth_headers,
    )
    assert proc.status_code == 200, proc.text
    extracted = proc.json()["data"]["extracted_text"]
    assert "INVOICE" in extracted.upper()

    # Fetch stored OCR text
    got = client.get(f"/api/v1/documents/{document_id}/text", headers=auth_headers)
    assert got.status_code == 200
    assert "12345" in got.json()["data"]["extracted_text"]


def test_text_before_processing_returns_404(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    png = _make_text_image("PENDING")
    up = client.post(
        "/api/v1/documents/upload",
        data={"customer_id": SEED_CUSTOMER, "document_type": "KYC"},
        files={"file": ("pending.png", png, "image/png")},
        headers=auth_headers,
    )
    document_id = up.json()["data"]["document_id"]
    got = client.get(f"/api/v1/documents/{document_id}/text", headers=auth_headers)
    assert got.status_code == 404
