"""CLI wrapper for Argilla moderation/export pipeline."""

from __future__ import annotations

import argparse

from argilla_pipeline import build_moderation_queue, export_approved_to_pillar, moderate_item


def main() -> None:
    parser = argparse.ArgumentParser(description="Argilla moderation/export pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("build-queue")

    moderate = sub.add_parser("moderate")
    moderate.add_argument("submission_id")
    moderate.add_argument("decision", choices=["approved", "rejected"])
    moderate.add_argument("--reviewer", required=True)
    moderate.add_argument("--note", default=None)

    sub.add_parser("export-approved")

    args = parser.parse_args()
    if args.command == "build-queue":
        queue = build_moderation_queue()
        print(f"Queue size: {len(queue)}")
    elif args.command == "moderate":
        item = moderate_item(args.submission_id, args.decision, args.reviewer, args.note)
        print(f"Updated {item['submission_id']} -> {item['status']}")
    elif args.command == "export-approved":
        count = export_approved_to_pillar()
        print(f"Exported approved records: {count}")


if __name__ == "__main__":
    main()
