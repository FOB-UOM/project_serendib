from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from tqdm import tqdm


def _load_schema(schema_path: Path) -> dict:
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            yield idx, line


def validate_jsonl(input_path: Path, schema_path: Path) -> int:
    schema = _load_schema(schema_path)
    validator = Draft202012Validator(schema)

    errors = 0
    for line_no, raw in tqdm(list(_iter_jsonl(input_path)), desc="Validating", unit="lines"):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            errors += 1
            print(f"[line {line_no}] JSON decode error: {e}")
            continue

        for e in validator.iter_errors(obj):
            errors += 1
            loc = "/".join([str(p) for p in e.absolute_path]) or "<root>"
            print(f"[line {line_no}] schema error at {loc}: {e.message}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Lanka-Instruct-v1 JSONL against schema.")
    parser.add_argument("--input", type=Path, required=True, help="Path to a .jsonl file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("instruction/hf_dataset_template/schema.json"),
        help="Path to schema.json",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    if not args.schema.exists():
        raise SystemExit(f"Schema not found: {args.schema}")

    error_count = validate_jsonl(args.input, args.schema)
    if error_count:
        print(f"Validation failed with {error_count} error(s).")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

