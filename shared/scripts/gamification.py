"""Contributor account and badge infrastructure for Project Serendib v2."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVENT_POINTS = {
    "verify": 1,
    "curate": 3,
    "evaluate": 3,
    "maintain": 8,
}

BADGE_THRESHOLDS = [
    ("Bronze", 10),
    ("Silver", 25),
    ("Gold", 50),
    ("Platinum", 100),
]


@dataclass
class Contributor:
    username: str
    display_name: str
    joined_at: str
    points: int = 0
    badges: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "display_name": self.display_name,
            "joined_at": self.joined_at,
            "points": self.points,
            "badges": self.badges or [],
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state() -> dict[str, Any]:
    return {"users": [], "events": []}


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _find_user(state: dict[str, Any], username: str) -> dict[str, Any] | None:
    for user in state["users"]:
        if user["username"] == username:
            return user
    return None


def _assign_badges(points: int) -> list[str]:
    badges: list[str] = []
    for badge, minimum in BADGE_THRESHOLDS:
        if points >= minimum:
            badges.append(badge)
    return badges


def register_user(
    state: dict[str, Any], username: str, display_name: str | None = None
) -> dict[str, Any]:
    if _find_user(state, username):
        raise ValueError(f"User '{username}' already exists")

    contributor = Contributor(
        username=username,
        display_name=display_name or username,
        joined_at=now_iso(),
        points=0,
        badges=[],
    )
    payload = contributor.to_dict()
    state["users"].append(payload)
    return payload


def record_event(
    state: dict[str, Any], username: str, event_type: str, units: int = 1
) -> dict[str, Any]:
    if event_type not in EVENT_POINTS:
        raise ValueError(f"Unsupported event_type '{event_type}'")
    if units < 1:
        raise ValueError("units must be >= 1")

    user = _find_user(state, username)
    if user is None:
        raise ValueError(f"Unknown user '{username}'")

    points_gained = EVENT_POINTS[event_type] * units
    user["points"] += points_gained
    user["badges"] = _assign_badges(user["points"])

    event = {
        "username": username,
        "event_type": event_type,
        "units": units,
        "points_gained": points_gained,
        "recorded_at": now_iso(),
    }
    state["events"].append(event)
    return event


def leaderboard(state: dict[str, Any], top_n: int = 20) -> list[dict[str, Any]]:
    ranked = sorted(state["users"], key=lambda item: (-item["points"], item["username"].lower()))
    return ranked[:top_n]
