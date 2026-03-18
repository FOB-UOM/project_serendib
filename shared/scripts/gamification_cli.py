"""CLI for contributor account and badge operations."""

from __future__ import annotations

import argparse
from pathlib import Path

from gamification import leaderboard, load_state, record_event, register_user, save_state

DEFAULT_STATE_PATH = Path("shared/argilla/infra/state.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project Serendib gamification operations")
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH), help="Path to state.json")

    subparsers = parser.add_subparsers(dest="command", required=True)

    register_cmd = subparsers.add_parser("register", help="Register a contributor account")
    register_cmd.add_argument("username")
    register_cmd.add_argument("--display-name", default=None)

    event_cmd = subparsers.add_parser("event", help="Record a contribution event")
    event_cmd.add_argument("username")
    event_cmd.add_argument("event_type", choices=["verify", "curate", "evaluate", "maintain"])
    event_cmd.add_argument("--units", type=int, default=1)

    leaderboard_cmd = subparsers.add_parser("leaderboard", help="Print leaderboard")
    leaderboard_cmd.add_argument("--top", type=int, default=20)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    state_path = Path(args.state)
    state = load_state(state_path)

    if args.command == "register":
        user = register_user(state, args.username, args.display_name)
        save_state(state_path, state)
        print(f"Registered user: {user['username']}")
        return

    if args.command == "event":
        event = record_event(state, args.username, args.event_type, args.units)
        save_state(state_path, state)
        print(
            f"Recorded event: {event['event_type']} x{event['units']} "
            f"(+{event['points_gained']} points)"
        )
        return

    if args.command == "leaderboard":
        for rank, user in enumerate(leaderboard(state, args.top), start=1):
            badges = ", ".join(user.get("badges", [])) or "-"
            print(f"{rank}. {user['username']} ({user['points']} pts) badges: {badges}")


if __name__ == "__main__":
    main()
