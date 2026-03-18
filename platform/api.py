"""Production-baseline API for contributor, moderation, and operations flows."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from persistence import (
    connect,
    db_stats,
    init_db,
    insert_event,
    insert_public_submission,
    list_public_submissions,
    mark_exported,
    moderate_submission,
    upsert_user,
)
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TASKS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_tasks.json"
PILLAR_ROOTS = [
    REPO_ROOT / "pillar-education-human-development",
    REPO_ROOT / "pillar-economy-enterprise",
    REPO_ROOT / "pillar-society-environment",
]
_LOCK = Lock()
_CONN = connect()
init_db(_CONN)


def load_gamification_module():
    module_path = REPO_ROOT / "shared" / "scripts" / "gamification.py"
    spec = importlib.util.spec_from_file_location("gamification", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load gamification module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gm = load_gamification_module()
app = FastAPI(title="Project Serendib API", version="0.2.0")


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    display_name: str | None = Field(default=None, max_length=120)


class EventCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    event_type: str = Field(pattern="^(verify|curate|evaluate|maintain)$")
    units: int = Field(default=1, ge=1, le=10000)


class PublicSubmissionCreate(BaseModel):
    task_id: str = Field(min_length=1, max_length=64)
    response_text: str = Field(min_length=1, max_length=5000)
    contributor_name: str | None = Field(default=None, max_length=120)
    self_rating: int = Field(default=3, ge=1, le=5)


class ModerationDecision(BaseModel):
    submission_id: int = Field(ge=1)
    decision: str = Field(pattern="^(approved|rejected)$")
    note: str | None = Field(default=None, max_length=400)


class OCRBatchRequest(BaseModel):
    incoming_dir: str = Field(default="shared/ocr-pipeline/incoming")
    output_path: str = Field(default="shared/ocr-pipeline/batch-results.jsonl")
    uncertain_queue_path: str = Field(default="shared/argilla/infra/ocr_uncertain_queue.json")
    threshold: float = Field(default=0.7, ge=0, le=1)


def _load_json_list(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Invalid list payload at {path}")
    return payload


def _role_from_key(api_key: str) -> str | None:
    staff_key = os.getenv("SERENDIB_STAFF_API_KEY", "serendib-staff-local")
    maintainer_key = os.getenv("SERENDIB_MAINTAINER_API_KEY", "serendib-maintainer-local")
    if api_key == maintainer_key:
        return "maintainer"
    if api_key == staff_key:
        return "staff"
    return None


def require_staff_or_maintainer(
    x_api_key: Annotated[str | None, Header()] = None,
) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing x-api-key")
    role = _role_from_key(x_api_key)
    if role not in {"staff", "maintainer"}:
        raise HTTPException(status_code=403, detail="Invalid API key for staff endpoint")
    return role


def require_maintainer(
    x_api_key: Annotated[str | None, Header()] = None,
) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing x-api-key")
    role = _role_from_key(x_api_key)
    if role != "maintainer":
        raise HTTPException(status_code=403, detail="Maintainer key required")
    return role


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stats")
def stats() -> dict[str, int]:
    with _LOCK:
        return db_stats(_CONN)


@app.get("/leaderboard")
def leaderboard(top: int = 20) -> list[dict[str, object]]:
    with _LOCK:
        rows = _CONN.execute(
            """
            SELECT username, display_name, joined_at, points, badges_json
            FROM users
            ORDER BY points DESC, username ASC
            LIMIT ?
            """,
            (max(1, min(top, 100)),),
        ).fetchall()
    payload = []
    for row in rows:
        payload.append(
            {
                "username": row["username"],
                "display_name": row["display_name"],
                "joined_at": row["joined_at"],
                "points": row["points"],
                "badges": json.loads(row["badges_json"]),
            }
        )
    return payload


@app.get("/public/tasks")
def public_tasks() -> list[dict[str, object]]:
    return _load_json_list(PUBLIC_TASKS_PATH)


@app.post("/public/submissions")
def public_submission(payload: PublicSubmissionCreate) -> dict[str, object]:
    tasks = _load_json_list(PUBLIC_TASKS_PATH)
    if not any(task.get("task_id") == payload.task_id for task in tasks):
        raise HTTPException(status_code=404, detail=f"Unknown task_id '{payload.task_id}'")

    submission = {
        "task_id": payload.task_id,
        "response_text": payload.response_text.strip(),
        "contributor_name": (payload.contributor_name or "Anonymous").strip() or "Anonymous",
        "self_rating": payload.self_rating,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    with _LOCK:
        submission_id = insert_public_submission(_CONN, submission)
    submission["submission_id"] = submission_id
    submission["status"] = "pending"
    return submission


@app.get("/moderation/queue")
def moderation_queue(
    status: str = "pending",
    _: str = Depends(require_staff_or_maintainer),
) -> list[dict[str, object]]:
    with _LOCK:
        items = list_public_submissions(_CONN, status=status if status != "all" else None)
    return items


@app.post("/moderation/review")
def moderation_review(
    payload: ModerationDecision,
    role: str = Depends(require_staff_or_maintainer),
) -> dict[str, object]:
    reviewer = f"api-{role}"
    with _LOCK:
        item = moderate_submission(
            _CONN,
            payload.submission_id,
            payload.decision,
            reviewer,
            datetime.now(timezone.utc).isoformat(),
            payload.note,
        )
    if item is None:
        raise HTTPException(status_code=404, detail="submission not found")
    return item


@app.post("/moderation/export-approved")
def export_approved(_: str = Depends(require_maintainer)) -> dict[str, int]:
    exported = 0
    with _LOCK:
        approved = _CONN.execute(
            """
            SELECT * FROM public_submissions
            WHERE status='approved' AND exported=0
            ORDER BY id ASC
            """
        ).fetchall()
        for row in approved:
            task_id = row["task_id"]
            if task_id in {"ocr-001", "edu-001"}:
                pillar, sub = "pillar-education-human-development", "teacher-empowerment"
            elif task_id == "env-001":
                pillar, sub = "pillar-society-environment", "sustainability-climate"
            else:
                pillar, sub = "pillar-society-environment", "sociology-social-dynamics"

            out = REPO_ROOT / pillar / sub / "community.approved.jsonl"
            out.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "record_id": f"moderated_{row['id']}",
                "pillar": pillar,
                "sub_pillar": sub,
                "title": f"Moderated public contribution {row['id']}",
                "content": row["response_text"],
                "language": "en",
                "provenance": {
                    "source_name": "Public Task Studio",
                    "source_type": "classroom_input",
                    "collected_at": datetime.now(timezone.utc).date().isoformat(),
                    "collector": row["contributor_name"],
                },
                "license": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
                "review_status": "approved",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "quality_score": 0.75,
            }
            with out.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            mark_exported(_CONN, int(row["id"]))
            exported += 1

    return {"exported": exported}


@app.post("/users")
def create_user(
    payload: UserCreate,
    _: str = Depends(require_staff_or_maintainer),
) -> dict[str, object]:
    with _LOCK:
        existing = _CONN.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (payload.username.strip(),),
        ).fetchone()
        if existing:
            raise HTTPException(
                status_code=409, detail=f"User '{payload.username.strip()}' already exists"
            )

        state = gm.default_state()
        user = gm.register_user(state, payload.username.strip(), payload.display_name)
        upsert_user(
            _CONN,
            user["username"],
            user["display_name"],
            user["joined_at"],
            user["points"],
            json.dumps(user["badges"], ensure_ascii=False),
        )
    return user


@app.post("/events")
def create_event(
    payload: EventCreate,
    _: str = Depends(require_staff_or_maintainer),
) -> dict[str, object]:
    with _LOCK:
        row = _CONN.execute(
            """
            SELECT username, display_name, joined_at, points, badges_json
            FROM users
            WHERE username = ?
            """,
            (payload.username.strip(),),
        ).fetchone()
        if row is None:
            raise HTTPException(
                status_code=400, detail=f"Unknown user '{payload.username.strip()}'"
            )

        state = {
            "users": [
                {
                    "username": row["username"],
                    "display_name": row["display_name"],
                    "joined_at": row["joined_at"],
                    "points": int(row["points"]),
                    "badges": json.loads(row["badges_json"]),
                }
            ],
            "events": [],
        }
        try:
            event = gm.record_event(
                state, payload.username.strip(), payload.event_type, payload.units
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        user = state["users"][0]
        upsert_user(
            _CONN,
            user["username"],
            user["display_name"],
            user["joined_at"],
            int(user["points"]),
            json.dumps(user["badges"], ensure_ascii=False),
        )
        insert_event(_CONN, event)
    return event


@app.post("/ocr/batch-run")
def ocr_batch_run(
    payload: OCRBatchRequest,
    _: str = Depends(require_staff_or_maintainer),
) -> dict[str, int]:
    batch_path = REPO_ROOT / "shared" / "ocr-pipeline" / "batch.py"
    spec = importlib.util.spec_from_file_location("ocr_batch", batch_path)
    if spec is None or spec.loader is None:
        raise HTTPException(status_code=500, detail="Unable to load OCR batch module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module.run_batch(
        REPO_ROOT / payload.incoming_dir,
        REPO_ROOT / payload.output_path,
        REPO_ROOT / payload.uncertain_queue_path,
        payload.threshold,
    )


@app.get("/operations/metrics")
def operations_metrics(_: str = Depends(require_staff_or_maintainer)) -> dict[str, object]:
    with _LOCK:
        stats_payload = db_stats(_CONN)

    subpillars = sorted(REPO_ROOT.glob("pillar-*/**/seed.sample.jsonl"))
    growth = {
        str(path.parent.relative_to(REPO_ROOT)): sum(
            1 for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()
        )
        for path in subpillars
    }

    quality_denom = stats_payload["approved_submissions"] + stats_payload["rejected_submissions"]
    quality_score = (
        stats_payload["approved_submissions"] / quality_denom if quality_denom else 0.0
    )

    return {
        "throughput": stats_payload,
        "quality_score": round(quality_score, 4),
        "pillar_growth": growth,
    }
