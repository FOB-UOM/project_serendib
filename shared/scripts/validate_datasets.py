"""Validate layer1 instruction datasets for Sinhala data quality rules."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXPECTED_KEYS = [
    "record_id",
    "pillar",
    "sub_pillar",
    "title",
    "content",
    "language",
]

EXPECTED_SUBPILLARS = [
    "business-sme-bpm",
    "finance-financial-literacy",
    "political-economy",
    "teacher-empowerment",
    "philosophy-psychology-personality",
    "art-literature-culture",
    "sociology-social-dynamics",
    "sustainability-climate",
]

ENGLISH_RE = re.compile(r"[A-Za-z]")
PLACEHOLDER_RE = re.compile(
    r"(instruction record|layer \d+ example|placeholder|lorem ipsum)",
    re.IGNORECASE,
)


def validate_line(path: Path, line_no: int, payload: dict) -> list[str]:
    errors: list[str] = []

    if list(payload.keys()) != EXPECTED_KEYS:
        errors.append(
            f"{path}:{line_no} invalid schema keys; expected {EXPECTED_KEYS}, got {list(payload.keys())}"
        )

    if payload.get("language") != "si":
        errors.append(f"{path}:{line_no} language must be 'si'")

    title = payload.get("title", "")
    content = payload.get("content", "")

    if not isinstance(title, str) or not title.strip():
        errors.append(f"{path}:{line_no} title must be non-empty text")
    if not isinstance(content, str) or not content.strip():
        errors.append(f"{path}:{line_no} content must be non-empty text")

    if ENGLISH_RE.search(title) or ENGLISH_RE.search(content):
        errors.append(f"{path}:{line_no} contains English letters in title/content")

    if PLACEHOLDER_RE.search(title) or PLACEHOLDER_RE.search(content):
        errors.append(f"{path}:{line_no} contains placeholder-like text")

    sentence_count = sum(1 for part in re.split(r"[.!?।]", content) if part.strip())
    if sentence_count < 2 or sentence_count > 4:
        errors.append(f"{path}:{line_no} content must contain 2-4 sentences")

    return errors


def main() -> int:
    root = Path(".").resolve()
    files = sorted(root.glob("pillar-*/**/layer1-instruction/records.v1.jsonl"))
    errors: list[str] = []

    if not files:
        print("No layer1-instruction dataset files found.")
        return 1

    counts_by_subpillar: dict[str, int] = {}

    for path in files:
        seen_ids: set[str] = set()
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for idx, raw in enumerate(lines, start=1):
            if not raw.strip():
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{idx} invalid JSON: {exc}")
                continue

            errors.extend(validate_line(path, idx, payload))

            record_id = payload.get("record_id")
            if record_id in seen_ids:
                errors.append(f"{path}:{idx} duplicate record_id '{record_id}'")
            seen_ids.add(record_id)

            sub_pillar = payload.get("sub_pillar", "")
            counts_by_subpillar[sub_pillar] = counts_by_subpillar.get(sub_pillar, 0) + 1

    for sub_pillar in EXPECTED_SUBPILLARS:
        count = counts_by_subpillar.get(sub_pillar, 0)
        if count < 8:
            errors.append(
                f"Sub-pillar '{sub_pillar}' has only {count} records in layer1-instruction; minimum is 8"
            )

    if errors:
        print("Dataset validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Dataset validation passed for all layer1-instruction sub-pillars.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
