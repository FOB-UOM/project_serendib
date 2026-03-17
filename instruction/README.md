# Layer 1 — Instruction Dataset (`instruction/`)

This layer contains **high-quality instruction / dialogue data** for Sinhala-local helpfulness and alignment.

Recommended formats:

- **JSONL** for multi-turn dialogues (Hugging Face dataset friendly)
- Small, reviewable dataset packs (one domain/slice per folder)

Start here:

- `instruction/hf_dataset_template/` — schema + sample JSONL
- `instruction/teachers_v0_1/` — initial dataset pack (pilot slice)
- `instruction/validate_dataset.py` — JSONL schema validator

# Data

This folder holds **schema + templates + releases** for `Lanka-Instruct-v1`.

## Recommended layout

- `hf_dataset_template/`: schema + example JSONL for contributors
- `releases/`: versioned releases (kept out of git by default; publish via GitHub Releases / Hugging Face Datasets)
- `raw/`: raw sources (ignored by git)
- `processed/`: intermediate artifacts (ignored by git)

## Canonical format

The canonical contribution format is **JSON Lines (`.jsonl`)** with one conversation per line.

See `data/hf_dataset_template/`.

