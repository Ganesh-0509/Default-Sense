"""Tesseract OCR engine wrapper.

Resolves the Tesseract binary (from config, PATH, or common install locations),
and extracts text + a confidence score from image documents.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytesseract
from PIL import Image, UnidentifiedImageError

from app.config import settings

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}

# Common Windows install locations for the UB-Mannheim Tesseract build.
_COMMON_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/opt/homebrew/bin/tesseract",
]


def _resolve_tesseract_cmd() -> str | None:
    """Find the Tesseract executable. Returns the path or None if unavailable."""
    # 1) Explicit config / OCR_PATH env
    if settings.ocr_path and Path(settings.ocr_path).exists():
        return settings.ocr_path
    # 2) On PATH
    found = shutil.which("tesseract")
    if found:
        return found
    # 3) Known install locations
    for candidate in _COMMON_PATHS:
        if Path(candidate).exists():
            return candidate
    return None


# Configure pytesseract at import time (best effort).
_cmd = _resolve_tesseract_cmd()
if _cmd:
    pytesseract.pytesseract.tesseract_cmd = _cmd


def is_available() -> bool:
    """True if the Tesseract binary is reachable."""
    cmd = _resolve_tesseract_cmd()
    if not cmd:
        return False
    pytesseract.pytesseract.tesseract_cmd = cmd
    try:
        pytesseract.get_tesseract_version()
        return True
    except (pytesseract.TesseractNotFoundError, OSError):
        return False


def tesseract_version() -> str | None:
    try:
        return str(pytesseract.get_tesseract_version())
    except Exception:  # noqa: BLE001 - version probe is best-effort
        return None


def extract_text(file_path: str | Path) -> tuple[str, float]:
    """Run OCR on an image file.

    Returns (extracted_text, mean_confidence 0-100).
    Raises ValueError for unreadable images and RuntimeError if Tesseract is missing.
    """
    path = Path(file_path)
    if not is_available():
        raise RuntimeError(
            "Tesseract OCR engine is not installed or not found. "
            "Install it and set OCR_PATH if it is not on PATH."
        )
    try:
        image = Image.open(path)
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Could not read image file: {exc}") from exc

    text = pytesseract.image_to_string(image).strip()

    # Mean confidence across recognized words (Tesseract reports -1 for non-words).
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    confidences = [float(c) for c in data.get("conf", []) if str(c) not in ("-1", "")]
    mean_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0.0

    return text, mean_conf
