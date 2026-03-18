"""Validate sub-pillar JSONL records against local data contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def validate_file(schema_path: Path, jsonl_path: Path) -> tuple[int, int]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    valid = 0
    invalid = 0
    for idx, raw in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        payload = json.loads(raw)
        errors = sorted(validator.iter_errors(payload), key=lambda err: err.path)
        if errors:
            invalid += 1
            print(f"[INVALID] {jsonl_path}:{idx}")
            for err in errors:
                print(f"  - {err.message}")
        else:
            valid += 1

    return valid, invalid


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate pillar records with JSON Schema")
    parser.add_argument("--root", default=".", help="Repository root path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    schema_paths = sorted(root.glob("pillar-*/**/record.schema.json"))
    total_valid = 0
    total_invalid = 0

    for schema_path in schema_paths:
        jsonl_path = schema_path.with_name("seed.sample.jsonl")
        if not jsonl_path.exists():
            continue
        valid, invalid = validate_file(schema_path, jsonl_path)
        total_valid += valid
        total_invalid += invalid

    print(f"Validated records: valid={total_valid}, invalid={total_invalid}")
    if total_invalid > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
