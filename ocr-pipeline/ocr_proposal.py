from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def ocr_pdf(input_pdf: Path, output_txt: Path, dpi: int, lang: str, tesseract_cmd: str | None) -> None:
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    doc = fitz.open(str(input_pdf))
    parts: list[str] = []
    for i in range(doc.page_count):
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        txt = pytesseract.image_to_string(img, lang=lang) or ""
        header = f"\n\n===== PAGE {i+1}/{doc.page_count} =====\n\n"
        parts.append(header + txt.strip() + "\n")

    output_txt.write_text("".join(parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR an image-based PDF into a UTF-8 text file.")
    parser.add_argument("--input", type=Path, required=True, help="Path to PDF")
    parser.add_argument("--output", type=Path, required=True, help="Path to output .txt")
    parser.add_argument("--dpi", type=int, default=300, help="Render DPI (higher = slower, often better)")
    parser.add_argument("--lang", type=str, default="eng", help="Tesseract language code (e.g., eng)")
    parser.add_argument(
        "--tesseract-cmd",
        type=str,
        default=None,
        help="Optional path to tesseract.exe if it's not on PATH",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    ocr_pdf(args.input, args.output, dpi=args.dpi, lang=args.lang, tesseract_cmd=args.tesseract_cmd)
    print(f"Wrote OCR text to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

