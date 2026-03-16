# Contributing to Project Serendib

Thanks for helping build Sri Lanka’s sovereign instruction dataset.

## Ground rules

- **Be respectful**: default to kind, constructive feedback.
- **No sensitive data**: do not submit personally identifiable information (PII), credentials, or private documents.
- **Provenance matters**: record sources and licenses for any externally-derived content.
- **Quality over quantity**: prefer fewer, well-verified examples over large noisy dumps.

## Ways to contribute

- **Student verification (recommended start)**: complete verification tasks in `argilla/` (label quality/safety, language, relevance).
- **Data curation**: propose new prompts/responses in the dataset JSONL format.
- **Tooling**: improve validation scripts, schema, conversions, or evaluation harness.
- **Evaluation**: add benchmarks and help run reproducible baselines.

## Repository structure

- `data/`: schema, templates, and release artifacts (large raw data is intentionally ignored by git)
- `scripts/`: CLI tools (validation, training stubs)
- `evaluation/`: evaluation harness scaffolding
- `argilla/`: verification task app (Space scaffold)
- `notebooks/`: exploration notebooks

## Development setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Run checks:

```bash
ruff check .
pytest -q
```

## Dataset contribution workflow

1. **Pick a task** in GitHub Issues (see “Student task” templates).
2. **Create a branch**: `git checkout -b student/<your-handle>/<short-topic>`
3. **Add or edit data** under `data/` (templates are in `data/hf_dataset_template/`).
4. **Validate locally**:

```bash
python scripts\validate_dataset.py --input <your-file>.jsonl
```

5. **Open a PR** with a clear description and test plan.

## Credits (opt-in)

If you’d like to be credited, add yourself to `CREDITS.md` in your PR.

