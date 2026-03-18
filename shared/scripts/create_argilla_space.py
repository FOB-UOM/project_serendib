"""Create or update the public Argilla verification Space on Hugging Face."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    try:
        from huggingface_hub import HfApi, create_repo
    except ImportError:
        print("Missing dependency: huggingface_hub")
        print("Install with: python -m pip install huggingface_hub")
        return 1

    token = os.environ.get("HF_TOKEN")
    username = os.environ.get("HF_USERNAME")
    space_name = os.environ.get("HF_SPACE_NAME", "project-serendib-verification")
    visibility = os.environ.get("HF_SPACE_VISIBILITY", "public")

    if not token:
        print("HF_TOKEN is required to create or update a Space.")
        return 1
    if not username:
        print("HF_USERNAME is required to create or update a Space.")
        return 1

    repo_id = f"{username}/{space_name}"
    space_path = Path(__file__).resolve().parents[2] / "argilla" / "space"

    if not space_path.exists():
        print(f"Space source folder not found: {space_path}")
        return 1

    api = HfApi(token=token)
    create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
        private=(visibility.lower() == "private"),
        exist_ok=True,
        token=token,
    )

    api.upload_folder(
        repo_id=repo_id,
        repo_type="space",
        folder_path=str(space_path),
        commit_message="Update Project Serendib verification space",
    )

    print(f"Space ready: https://huggingface.co/spaces/{repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
