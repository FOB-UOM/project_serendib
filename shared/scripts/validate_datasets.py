"""Validate layer1 instruction datasets for Project Serendib v2."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

EXPECTED_KEYS = [
    "record_id",
    "pillar",
    "sub_pillar",
    "title",
    "content",
    "language",
]

EXPECTED_SUBPILLARS = {
    "business-sme-bpm",
    "finance-financial-literacy",
    "political-economy",
    "teacher-empowerment",
    "philosophy-psychology-personality",
    "art-literature-culture",
    "sociology-social-dynamics",
    "sustainability-climate",
}

ENGLISH_CHAR_RE = re.compile(r"[A-Za-z]")
PLACEHOLDER_RE = re.compile(
    r"(placeholder|lorem ipsum|todo|sample text|replace me|write here)",
    re.IGNORECASE,
)
ZERO_WIDTH_RE = re.compile(r"[\u200B\u200E\u200F\u2060\uFEFF]")
CONTROL_RE = re.compile(r"[\u0000-\u0008\u000B\u000C\u000E-\u001F]")
SINHALA_RE = re.compile(r"[\u0D80-\u0DFF]")


@dataclass
class SubPillarReport:
    name: str
    file_path: Path | None = None
    count: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "PASS" if not self.issues else "FAIL"


def find_layer1_files(root: Path) -> list[Path]:
    return sorted(root.glob("pillar-*/**/layer1-instruction/records.v1.jsonl"))


def validate_payload(payload: dict, path: Path, line_no: int) -> list[str]:
    issues: list[str] = []
    keys = list(payload.keys())

    if keys != EXPECTED_KEYS:
        issues.append(
            f"line {line_no}: schema keys mismatch in {path.as_posix()} (expected {EXPECTED_KEYS}, got {keys})"
        )

    if payload.get("language") != "si":
        issues.append(f"line {line_no}: language must be 'si'")

    title = payload.get("title")
    content = payload.get("content")

    if not isinstance(title, str) or not title.strip():
        issues.append(f"line {line_no}: title must be a non-empty string")
    if not isinstance(content, str) or not content.strip():
        issues.append(f"line {line_no}: content must be a non-empty string")

    if isinstance(title, str) and ENGLISH_CHAR_RE.search(title):
        issues.append(f"line {line_no}: title contains English letters")
    if isinstance(content, str) and ENGLISH_CHAR_RE.search(content):
        issues.append(f"line {line_no}: content contains English letters")

    if isinstance(title, str) and PLACEHOLDER_RE.search(title):
        issues.append(f"line {line_no}: title contains placeholder text")
    if isinstance(content, str) and PLACEHOLDER_RE.search(content):
        issues.append(f"line {line_no}: content contains placeholder text")

    for field_name, value in (("title", title), ("content", content)):
        if isinstance(value, str):
            issues.extend(validate_unicode(field_name, value, line_no))

    if isinstance(title, str) and not SINHALA_RE.search(title):
        issues.append(f"line {line_no}: title must include Sinhala characters")
    if isinstance(content, str) and not SINHALA_RE.search(content):
        issues.append(f"line {line_no}: content must include Sinhala characters")

    return issues


def validate_unicode(field_name: str, text: str, line_no: int) -> list[str]:
    issues: list[str] = []
    normalized = unicodedata.normalize("NFC", text)
    if normalized != text:
        issues.append(f"line {line_no}: {field_name} should be NFC-normalized Unicode")

    if "\ufffd" in text:
        issues.append(f"line {line_no}: {field_name} contains Unicode replacement characters (�)")

    if ZERO_WIDTH_RE.search(text):
        issues.append(f"line {line_no}: {field_name} contains zero-width characters")

    if CONTROL_RE.search(text):
        issues.append(f"line {line_no}: {field_name} contains control characters")

    return issues


def validate_file(path: Path, reports: dict[str, SubPillarReport]) -> None:
    sub_pillar = path.parents[1].name
    expected_pillar = path.parents[2].name
    report = reports.setdefault(sub_pillar, SubPillarReport(name=sub_pillar, file_path=path))
    report.file_path = path

    seen_ids: set[str] = set()
    lines = path.read_text(encoding="utf-8-sig").splitlines()

    for line_no, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            report.issues.append(f"line {line_no}: invalid JSON ({exc})")
            continue

        if not isinstance(payload, dict):
            report.issues.append(f"line {line_no}: record must be a JSON object")
            continue

        report.issues.extend(validate_payload(payload, path, line_no))

        rid = payload.get("record_id")
        if rid in seen_ids:
            report.issues.append(f"line {line_no}: duplicate record_id '{rid}'")
        seen_ids.add(rid)

        if payload.get("pillar") != expected_pillar:
            report.issues.append(
                f"line {line_no}: pillar mismatch (expected '{expected_pillar}', got '{payload.get('pillar')}')"
            )
        if payload.get("sub_pillar") != sub_pillar:
            report.issues.append(
                f"line {line_no}: sub_pillar mismatch (expected '{sub_pillar}', got '{payload.get('sub_pillar')}')"
            )

        report.count += 1


def print_report(reports: dict[str, SubPillarReport], files_count: int) -> None:
    print("Project Serendib v2 - Layer1 Dataset Validation")
    print("=" * 54)
    print(f"Scanned files: {files_count}")
    print()

    for name in sorted(EXPECTED_SUBPILLARS):
        report = reports.get(name, SubPillarReport(name=name))
        if report.count < 8:
            report.issues.append(f"record count is {report.count}; minimum required is 8")

        path_display = report.file_path.as_posix() if report.file_path else "[missing file]"
        print(f"[{report.status}] {name} ({report.count} records)")
        print(f"  file: {path_display}")
        if report.issues:
            for issue in report.issues:
                print(f"  - {issue}")
        print()


def main() -> int:
    root = Path(".").resolve()
    files = find_layer1_files(root)
    reports: dict[str, SubPillarReport] = {}

    if not files:
        print("No layer1-instruction/records.v1.jsonl files were found.")
        return 1

    for path in files:
        validate_file(path, reports)

    print_report(reports, len(files))

    missing = EXPECTED_SUBPILLARS - set(reports.keys())
    has_issues = bool(missing)
    for name in EXPECTED_SUBPILLARS:
        report = reports.get(name)
        if report is None or report.count < 8 or report.issues:
            has_issues = True

    if has_issues:
        print("Validation result: FAILED")
        return 1

    print("Validation result: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
