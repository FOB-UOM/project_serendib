from __future__ import annotations

import argparse
from pathlib import Path


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _ocr_with_tesseract(input_path: Path, output_txt: Path, dpi: int, lang: str, tesseract_cmd: str | None) -> None:
    try:
        import pytesseract  # type: ignore[import]
        from PIL import Image  # type: ignore[import]
    except ImportError:
        raise SystemExit("Missing OCR deps. Install: pip install pymupdf pillow pytesseract")

    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    text_parts: list[str] = []

    if input_path.suffix.lower() == ".pdf":
        try:
            import fitz  # type: ignore[import]
        except ImportError:
            raise SystemExit("Missing PyMuPDF. Install: pip install pymupdf")

        doc = fitz.open(str(input_path))
        for i in range(doc.page_count):
            page = doc[i]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            txt = pytesseract.image_to_string(img, lang=lang) or ""
            text_parts.append(f"\n\n===== PAGE {i+1}/{doc.page_count} =====\n\n{txt.strip()}\n")
    else:
        img = Image.open(input_path)
        txt = pytesseract.image_to_string(img, lang=lang) or ""
        text_parts.append(txt.strip() + "\n")

    _ensure_parent(output_txt)
    output_txt.write_text("".join(text_parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sinhala-centric OCR CLI (Tesseract first; TrOCR stub).")
    parser.add_argument("--input", type=Path, required=True, help="Path to PDF/image")
    parser.add_argument("--output", type=Path, required=True, help="Path to output .txt")
    parser.add_argument("--engine", type=str, default="tesseract", choices=["tesseract", "trocr"])
    parser.add_argument("--dpi", type=int, default=300, help="PDF render DPI (tesseract)")
    parser.add_argument("--lang", type=str, default="sin", help="Tesseract language code (e.g., sin, eng, sin+eng)")
    parser.add_argument("--tesseract-cmd", type=str, default=None, help="Optional path to tesseract executable")
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    if args.engine == "trocr":
        raise SystemExit(
            "TrOCR engine stub: implement model-backed OCR here (GPU optional). "
            "For now use --engine tesseract."
        )

    _ocr_with_tesseract(
        input_path=args.input,
        output_txt=args.output,
        dpi=args.dpi,
        lang=args.lang,
        tesseract_cmd=args.tesseract_cmd,
    )
    print(f"Wrote OCR text to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

