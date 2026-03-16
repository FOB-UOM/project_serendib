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

