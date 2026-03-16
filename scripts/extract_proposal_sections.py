from __future__ import annotations

import argparse
import re
from pathlib import Path


def extract_sections(text: str) -> dict[str, str]:
    # Very lightweight heuristic extraction for the OCR'd proposal.
    sections: dict[str, str] = {}

    exec_match = re.search(
        r"EXECUTIVE SUMMARY:(?P<body>[\s\S]*?)===== PAGE 3/13 =====",
        text,
        flags=re.IGNORECASE,
    )
    if exec_match:
        sections["executive_summary"] = exec_match.group("body").strip()

    obj_match = re.search(
        r"PROJECT OBJECTIVES:(?P<body>[\s\S]*?)===== PAGE 6/13 =====",
        text,
        flags=re.IGNORECASE,
    )
    if obj_match:
        sections["objectives"] = obj_match.group("body").strip()

    meth_match = re.search(
        r"METHODOLOGY PHASE I:(?P<body>[\s\S]*?)===== PAGE 10/13 =====",
        text,
        flags=re.IGNORECASE,
    )
    if meth_match:
        sections["methodology"] = meth_match.group("body").strip()

    return sections


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract key sections from proposal_ocr.txt.")
    parser.add_argument("--input", type=Path, default=Path("proposal_ocr.txt"))
    parser.add_argument("--output", type=Path, default=Path("proposal_extracted.md"))
    args = parser.parse_args()

    raw = args.input.read_text(encoding="utf-8")
    sections = extract_sections(raw)

    md_parts = ["# Extracted proposal sections (OCR)\n"]
    if "executive_summary" in sections:
        md_parts.append("## Executive summary\n\n" + sections["executive_summary"] + "\n")
    if "objectives" in sections:
        md_parts.append("## Objectives\n\n" + sections["objectives"] + "\n")
    if "methodology" in sections:
        md_parts.append("## Methodology\n\n" + sections["methodology"] + "\n")

    args.output.write_text("\n".join(md_parts).strip() + "\n", encoding="utf-8")
    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

