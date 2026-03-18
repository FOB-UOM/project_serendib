---
title: Project Serendib Verification
emoji: "\U0001F52C"
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
---

# Project Serendib — Student Verification Space

This Space is a thin UI for **student verification tasks** backed by Argilla.

## Setup

1. Create an Argilla workspace and API key.
2. Set Space secrets/environment variables:

- `ARGILLA_API_URL`
- `ARGILLA_API_KEY`
- `ARGILLA_WORKSPACE` (optional; defaults to `admin`)

## Automated Space creation (Hugging Face)

You can create or update the free Space via the repo script:

```bash
python shared/scripts/create_argilla_space.py
```

Required environment variables:

- `HF_TOKEN`
- `HF_USERNAME`
- `HF_SPACE_NAME` (optional; defaults to `project-serendib-verification`)
- `HF_SPACE_VISIBILITY` (optional; `public` or `private`)

## What this app does

- Connects to Argilla
- Lists available datasets for verification
- Provides a minimal “pull a record → label → submit” flow (starter scaffold)
