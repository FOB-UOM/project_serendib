"""OCR batch + confidence loop for routing uncertain samples to Argilla."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from hybrid_router import route_ocr


def _estimate_confidence(document_name: str) -> float:
    lowered = document_name.lower()
    if any(token in lowered for token in ("handwritten", "scan", "blur", "lowres")):
        return 0.42
    return 0.88


def run_batch(
    incoming_dir: Path,
    output_path: Path,
    uncertain_queue_path: Path,
    threshold: float = 0.7,
) -> dict[str, int]:
    incoming_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    uncertain_queue_path.parent.mkdir(parents=True, exist_ok=True)

    uncertain = []
    processed = 0

    with output_path.open("w", encoding="utf-8") as out:
        for item in sorted(incoming_dir.iterdir()):
            if item.name.startswith("."):
                continue
            confidence = _estimate_confidence(item.name)
            engine = route_ocr(item.name, "auto")
            payload = {
                "document": item.name,
                "selected_engine": engine,
                "confidence": confidence,
                "processed_at": datetime.now(timezone.utc).isoformat(),
            }
            out.write(json.dumps(payload, ensure_ascii=False) + "\n")
            processed += 1
            if confidence < threshold:
                uncertain.append(payload)

    uncertain_queue_path.write_text(
        json.dumps(uncertain, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"processed": processed, "uncertain": len(uncertain)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OCR batch confidence routing")
    parser.add_argument("--incoming", default="shared/ocr-pipeline/incoming")
    parser.add_argument("--output", default="shared/ocr-pipeline/batch-results.jsonl")
    parser.add_argument(
        "--uncertain-queue", default="shared/argilla/infra/ocr_uncertain_queue.json"
    )
    parser.add_argument("--threshold", type=float, default=0.7)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    result = run_batch(
        root / args.incoming,
        root / args.output,
        root / args.uncertain_queue,
        args.threshold,
    )
    print(f"Processed: {result['processed']} | Uncertain: {result['uncertain']}")


if __name__ == "__main__":
    main()
