"""CLI entry point for the shared OCR pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid_router import route_ocr


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Serendib OCR router")
    parser.add_argument("document", help="Document file name or identifier")
    parser.add_argument(
        "--mode",
        default="auto",
        choices=["auto", "tesseract", "qwen2_vl"],
        help="Routing mode",
    )
    args = parser.parse_args()

    engine = route_ocr(args.document, args.mode)
    print(f"Selected OCR engine: {engine}")


if __name__ == "__main__":
    main()
