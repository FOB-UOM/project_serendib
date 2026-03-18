"""Simple Argilla-oriented moderation/export pipeline for Serendib v2."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODERATION_QUEUE_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "moderation_queue.json"
sys.path.insert(0, str(REPO_ROOT / "platform"))
from persistence import connect, list_public_submissions, mark_exported  # noqa: E402

DB_CONN = connect()


def _load_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_list(path: Path, payload: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_moderation_queue() -> list[dict]:
    queue = _load_list(MODERATION_QUEUE_PATH)
    submissions = list_public_submissions(DB_CONN)
    existing = {item.get("submission_id") for item in queue}

    for idx, submission in enumerate(submissions, start=1):
        submission_id = f"submission-{submission.get('id', idx):05d}"
        if submission_id in existing:
            continue
        queue.append(
            {
                "submission_id": submission_id,
                "task_id": submission.get("task_id", "unknown"),
                "contributor_name": submission.get("contributor_name", "Anonymous"),
                "response_text": submission.get("response_text", ""),
                "status": "pending",
                "reviewer": None,
                "reviewed_at": None,
                "decision_note": None,
                "created_at": submission.get("submitted_at")
                or datetime.now(timezone.utc).isoformat(),
            }
        )
        existing.add(submission_id)

    _save_list(MODERATION_QUEUE_PATH, queue)
    return queue


def moderate_item(
    submission_id: str, decision: str, reviewer: str, note: str | None = None
) -> dict:
    if decision not in {"approved", "rejected"}:
        raise ValueError("decision must be approved or rejected")

    queue = _load_list(MODERATION_QUEUE_PATH)
    for item in queue:
        if item.get("submission_id") == submission_id:
            item["status"] = decision
            item["reviewer"] = reviewer
            item["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            item["decision_note"] = note
            _save_list(MODERATION_QUEUE_PATH, queue)
            return item

    raise ValueError(f"Unknown submission_id '{submission_id}'")


def export_approved_to_pillar(root: Path | None = None) -> int:
    root = root or REPO_ROOT
    queue = _load_list(MODERATION_QUEUE_PATH)

    task_map = {
        "ocr-001": ("pillar-education-human-development", "teacher-empowerment"),
        "edu-001": ("pillar-education-human-development", "teacher-empowerment"),
        "env-001": ("pillar-society-environment", "sustainability-climate"),
    }

    exported = 0
    for item in queue:
        if item.get("status") != "approved" or item.get("exported"):
            continue
        pillar, sub = task_map.get(
            item.get("task_id"), ("pillar-society-environment", "sociology-social-dynamics")
        )
        target = root / pillar / sub / "community.approved.jsonl"

        record = {
            "record_id": item["submission_id"],
            "pillar": pillar,
            "sub_pillar": sub,
            "title": f"Community submission {item['submission_id']}",
            "content": item.get("response_text", ""),
            "language": "en",
            "provenance": {
                "source_name": "Public Task Studio",
                "source_type": "classroom_input",
                "collected_at": datetime.now(timezone.utc).date().isoformat(),
                "collector": item.get("contributor_name", "Anonymous"),
            },
            "license": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
            "review_status": "approved",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "quality_score": 0.7,
        }

        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

        item["exported"] = True
        numeric_id = int(str(item["submission_id"]).split("-")[-1])
        mark_exported(DB_CONN, numeric_id)
        exported += 1

    _save_list(MODERATION_QUEUE_PATH, queue)
    return exported
