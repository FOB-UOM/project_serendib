from __future__ import annotations

import argparse
import os


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create the Project Serendib Argilla verification dataset (fields + questions)."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="serendib_verification_v0_1",
        help="Argilla dataset name to create/update.",
    )
    args = parser.parse_args()

    api_url = _require_env("ARGILLA_API_URL")
    api_key = _require_env("ARGILLA_API_KEY")
    workspace = os.environ.get("ARGILLA_WORKSPACE", "admin").strip() or "admin"

    try:
        import argilla as rg  # type: ignore[import]
    except ImportError as err:
        raise SystemExit(
            "Argilla is not installed. Install extras with: pip install argilla gradio"
        ) from err

    rg.init(api_url=api_url, api_key=api_key, workspace=workspace)

    # Argilla v2 dataset settings API. This is intentionally minimal but usable.
    settings = rg.Settings(
        guidelines=(
            "Student verification for Project Serendib.\n\n"
            "Goal: verify safety + quality + localization of candidate records before release.\n"
            "- Reject if PII, harmful content, or obvious nonsense.\n"
            "- Tag language/domain and add notes for curators.\n"
        ),
        fields=[
            rg.TextField(name="id", title="Record ID", required=True),
            rg.TextField(name="domain", title="Domain tag", required=False),
            rg.TextField(name="language", title="Language tag (si/ta/en/mixed)", required=False),
            rg.TextField(
                name="source_type",
                title="Source (human/synthetic/mixed)",
                required=False,
            ),
            rg.TextField(name="conversation", title="Conversation (rendered)", required=True),
            rg.TextField(name="provenance", title="Provenance/notes", required=False),
        ],
        questions=[
            rg.RatingQuestion(
                name="quality",
                title="Overall quality",
                values=[1, 2, 3, 4, 5],
                required=True,
                description="1=bad, 3=ok, 5=excellent",
            ),
            rg.LabelQuestion(
                name="safety",
                title="Safety",
                labels=["safe", "needs_review", "harmful"],
                required=True,
                description="Mark harmful if unsafe instructions, hate, harassment, etc.",
            ),
            rg.MultiLabelQuestion(
                name="issues",
                title="Issues found (multi-select)",
                labels=[
                    "pii",
                    "copyright_or_license",
                    "hallucination_or_unfounded_claims",
                    "poor_sinhala",
                    "formatting",
                    "off_topic",
                    "other",
                ],
                required=False,
            ),
            rg.TextQuestion(
                name="review_notes",
                title="Reviewer notes",
                required=False,
                description="Explain what to fix, or why you rejected/flagged this record.",
            ),
        ],
    )

    dataset = rg.Dataset(name=args.name, settings=settings)
    dataset.create()

    print(f"Created Argilla dataset: {dataset.name} (workspace={workspace})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

