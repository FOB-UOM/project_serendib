from __future__ import annotations

import os
from dataclasses import dataclass

import gradio as gr


@dataclass(frozen=True)
class ArgillaConfig:
    api_url: str
    api_key: str
    workspace: str


def load_config() -> ArgillaConfig:
    api_url = os.environ.get("ARGILLA_API_URL", "").strip()
    api_key = os.environ.get("ARGILLA_API_KEY", "").strip()
    workspace = os.environ.get("ARGILLA_WORKSPACE", "admin").strip() or "admin"
    return ArgillaConfig(api_url=api_url, api_key=api_key, workspace=workspace)


def connect_status() -> str:
    cfg = load_config()
    if not cfg.api_url or not cfg.api_key:
        return (
            "Missing configuration. Set `ARGILLA_API_URL` and `ARGILLA_API_KEY` "
            "(and optionally `ARGILLA_WORKSPACE`)."
        )

    try:
        import argilla as rg

        rg.init(api_url=cfg.api_url, api_key=cfg.api_key, workspace=cfg.workspace)
        # Lightweight call to confirm connectivity
        _ = rg.Workspace.from_name(cfg.workspace)
        return f"Connected to Argilla workspace: {cfg.workspace}"
    except Exception as e:  # noqa: BLE001
        return f"Failed to connect to Argilla: {type(e).__name__}: {e}"


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Project Serendib Verification") as demo:
        gr.Markdown(
            """
## Project Serendib — Student Verification

This is a starter UI scaffold. In a full implementation, this app would:

- pull unlabeled records from an Argilla dataset
- show the multi-turn conversation
- capture labels (quality/safety/domain/language)
- submit annotations back to Argilla
"""
        )
        status = gr.Textbox(label="Connection status", value=connect_status(), interactive=False)
        refresh = gr.Button("Refresh status")
        refresh.click(fn=connect_status, outputs=status)

    return demo


if __name__ == "__main__":
    build_app().launch()

