"""SQLite persistence helpers for Project Serendib platform."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "serendib.db"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            joined_at TEXT NOT NULL,
            points INTEGER NOT NULL DEFAULT 0,
            badges_json TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            event_type TEXT NOT NULL,
            units INTEGER NOT NULL,
            points_gained INTEGER NOT NULL,
            recorded_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS public_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            response_text TEXT NOT NULL,
            contributor_name TEXT NOT NULL,
            self_rating INTEGER NOT NULL,
            submitted_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            reviewer TEXT,
            reviewed_at TEXT,
            decision_note TEXT,
            exported INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    conn.commit()


def upsert_user(
    conn: sqlite3.Connection,
    username: str,
    display_name: str,
    joined_at: str,
    points: int,
    badges_json: str,
) -> None:
    conn.execute(
        """
        INSERT INTO users (username, display_name, joined_at, points, badges_json)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
          display_name=excluded.display_name,
          joined_at=excluded.joined_at,
          points=excluded.points,
          badges_json=excluded.badges_json
        """,
        (username, display_name, joined_at, points, badges_json),
    )
    conn.commit()


def insert_event(conn: sqlite3.Connection, payload: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO events (username, event_type, units, points_gained, recorded_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload["username"],
            payload["event_type"],
            int(payload["units"]),
            int(payload["points_gained"]),
            payload["recorded_at"],
        ),
    )
    conn.commit()


def insert_public_submission(conn: sqlite3.Connection, payload: dict[str, Any]) -> int:
    cur = conn.execute(
        """
        INSERT INTO public_submissions (
            task_id, response_text, contributor_name, self_rating, submitted_at, status
        )
        VALUES (?, ?, ?, ?, ?, 'pending')
        """,
        (
            payload["task_id"],
            payload["response_text"],
            payload["contributor_name"],
            int(payload["self_rating"]),
            payload["submitted_at"],
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def list_public_submissions(
    conn: sqlite3.Connection, status: str | None = None
) -> list[dict[str, Any]]:
    if status:
        rows = conn.execute(
            """
            SELECT id, task_id, response_text, contributor_name, self_rating, submitted_at,
                   status, reviewer, reviewed_at, decision_note, exported
            FROM public_submissions
            WHERE status = ?
            ORDER BY id ASC
            """,
            (status,),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT id, task_id, response_text, contributor_name, self_rating, submitted_at,
                   status, reviewer, reviewed_at, decision_note, exported
            FROM public_submissions
            ORDER BY id ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def moderate_submission(
    conn: sqlite3.Connection,
    submission_id: int,
    status: str,
    reviewer: str,
    reviewed_at: str,
    note: str | None,
) -> dict[str, Any] | None:
    conn.execute(
        """
        UPDATE public_submissions
        SET status = ?, reviewer = ?, reviewed_at = ?, decision_note = ?
        WHERE id = ?
        """,
        (status, reviewer, reviewed_at, note, submission_id),
    )
    conn.commit()
    row = conn.execute(
        """
        SELECT id, task_id, response_text, contributor_name, self_rating, submitted_at,
               status, reviewer, reviewed_at, decision_note, exported
        FROM public_submissions WHERE id = ?
        """,
        (submission_id,),
    ).fetchone()
    return dict(row) if row else None


def mark_exported(conn: sqlite3.Connection, submission_id: int) -> None:
    conn.execute("UPDATE public_submissions SET exported = 1 WHERE id = ?", (submission_id,))
    conn.commit()


def db_stats(conn: sqlite3.Connection) -> dict[str, int]:
    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    submissions = conn.execute("SELECT COUNT(*) FROM public_submissions").fetchone()[0]
    pending = conn.execute(
        "SELECT COUNT(*) FROM public_submissions WHERE status = 'pending'"
    ).fetchone()[0]
    approved = conn.execute(
        "SELECT COUNT(*) FROM public_submissions WHERE status = 'approved'"
    ).fetchone()[0]
    rejected = conn.execute(
        "SELECT COUNT(*) FROM public_submissions WHERE status = 'rejected'"
    ).fetchone()[0]
    return {
        "users": users,
        "events": events,
        "public_submissions": submissions,
        "pending_submissions": pending,
        "approved_submissions": approved,
        "rejected_submissions": rejected,
    }
