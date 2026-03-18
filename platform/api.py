"""Production-baseline API for contributor accounts and gamification."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "state.json"
PUBLIC_TASKS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_tasks.json"
PUBLIC_SUBMISSIONS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_submissions.json"
_LOCK = Lock()


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
app = FastAPI(title="Project Serendib API", version="0.1.0")


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


def _load_json_list(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Invalid list payload at {path}")
    return payload


def _save_json_list(path: Path, payload: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stats")
def stats() -> dict[str, int]:
    state = gm.load_state(STATE_PATH)
    return {
        "users": len(state["users"]),
        "events": len(state["events"]),
    }


@app.get("/leaderboard")
def leaderboard(top: int = 20) -> list[dict[str, object]]:
    state = gm.load_state(STATE_PATH)
    top = max(1, min(top, 100))
    return gm.leaderboard(state, top)


@app.get("/public/tasks")
def public_tasks() -> list[dict[str, object]]:
    return _load_json_list(PUBLIC_TASKS_PATH)


@app.post("/public/submissions")
def public_submission(payload: PublicSubmissionCreate) -> dict[str, object]:
    with _LOCK:
        tasks = _load_json_list(PUBLIC_TASKS_PATH)
        if not any(task.get("task_id") == payload.task_id for task in tasks):
            raise HTTPException(status_code=404, detail=f"Unknown task_id '{payload.task_id}'")

        submissions = _load_json_list(PUBLIC_SUBMISSIONS_PATH)
        submission = {
            "task_id": payload.task_id,
            "response_text": payload.response_text.strip(),
            "contributor_name": (payload.contributor_name or "Anonymous").strip() or "Anonymous",
            "self_rating": payload.self_rating,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
        submissions.append(submission)
        _save_json_list(PUBLIC_SUBMISSIONS_PATH, submissions)

    return submission


@app.post("/users")
def create_user(payload: UserCreate) -> dict[str, object]:
    with _LOCK:
        state = gm.load_state(STATE_PATH)
        try:
            user = gm.register_user(state, payload.username.strip(), payload.display_name)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        gm.save_state(STATE_PATH, state)
    return user


@app.post("/events")
def create_event(payload: EventCreate) -> dict[str, object]:
    with _LOCK:
        state = gm.load_state(STATE_PATH)
        try:
            event = gm.record_event(
                state, payload.username.strip(), payload.event_type, payload.units
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        gm.save_state(STATE_PATH, state)
    return event
