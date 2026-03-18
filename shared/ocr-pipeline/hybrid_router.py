"""Simple hybrid OCR router for Project Serendib v2."""

from __future__ import annotations


def route_ocr(document_name: str, mode: str = "auto") -> str:
    """Return OCR engine selection for a given document and mode."""
    if mode in {"tesseract", "qwen2_vl"}:
        return mode

    lowered = document_name.lower()
    difficult_tokens = ("handwritten", "scan", "lowres", "blur")
    if any(token in lowered for token in difficult_tokens):
        return "qwen2_vl"
    return "tesseract"
