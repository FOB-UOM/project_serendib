"""Release snapshot generator for Serendib v2 data artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def count_jsonl_records(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def generate_release(root: Path, tag: str) -> Path:
    release_dir = root / "docs" / "releases" / tag
    release_dir.mkdir(parents=True, exist_ok=True)

    samples = sorted(root.glob("pillar-*/**/*.jsonl"))
    totals = {str(p.relative_to(root)): count_jsonl_records(p) for p in samples}

    payload = {
        "release_tag": tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(totals),
        "record_count": sum(totals.values()),
        "files": totals,
    }

    out = release_dir / "quality-report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release snapshot and quality report")
    parser.add_argument("--root", default=".")
    parser.add_argument("--tag", required=True, help="Release tag e.g. v0.1")
    args = parser.parse_args()

    out = generate_release(Path(args.root).resolve(), args.tag)
    print(f"Generated report: {out}")


if __name__ == "__main__":
    main()
