# Contributing to Project Serendib

Thanks for helping build **Project Serendib — Sovereign Sinhala Data Ecosystem** at University of Moratuwa (FOB-UOM).

This project is a **digital public good**. Please read `CODE_OF_CONDUCT.md` first.

## Student onboarding (fast path)

If you’re new, start with verification:

- **Step 1**: Join the Argilla verification queue in `argilla/`
- **Step 2**: **Verify 10 examples** (quality + safety + language + domain tags)
- **Reward**: earn your **first badge** + credits; opt-in to be listed in `CREDITS.md`

## Gamified roles (credits & badges)

Credits are awarded for validated work (typical ranges):

- **Verifier (1–3 credits)**: approve/reject, tag issues, mark PII/harm, domain/language
- **Curator (3–8 credits)**: fix issues, improve clarity, add provenance, ensure schema-valid
- **Evaluator (3–8 credits)**: add cultural benchmark prompts, run baselines, report regressions
- **Maintainer (8+ credits)**: review PRs, manage releases, evolve schemas and workflows

Badges (maintainers may award):

- **Bronze** (10 credits), **Silver** (25), **Gold** (50), **Platinum** (100)
- **Domain Specialist**, **Language Champion**, **Safety Steward**

## What you can contribute

- **Layer 0 (`corpus-raw/`)**: curated raw Sinhala text + provenance/metadata
- **Layer 1 (`instruction/`)**: multi-turn dialogues (HF-friendly JSONL)
- **Layer 2 (`reasoning/`)**: step-by-step explanations (structured artifacts)
- **Layer 3 (`structured/`)**: QA, summarization, entity extraction (esp. education/law)
- **Layer 4 (`advanced/`)**: templates for future advanced types
- **Tooling**: validators, OCR utilities, synthetic-gen scripts, CI
- **Evaluation**: Sri Lankan cultural benchmark prompts + harness improvements

## Repo layout (high level)

- `corpus-raw/` — Layer 0
- `instruction/` — Layer 1 (includes schema + validator)
- `reasoning/` — Layer 2
- `structured/` — Layer 3
- `advanced/` — Layer 4
- `ocr-pipeline/`, `synthetic-gen/`, `training/`, `argilla/`, `evaluation/`, `notebooks/`

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

## Contribution workflow (PRs)

1. **Pick an issue** (see `.github/ISSUE_TEMPLATE/`)
2. **Create a branch**: `git checkout -b student/<your-handle>/<short-topic>`
3. **Make small, reviewable changes** (data and/or code)
4. **Validate locally** (when adding instruction JSONL):

```bash
python instruction\validate_dataset.py --input <your-file>.jsonl
```

5. **Open a PR** with:
   - a short summary
   - what layer(s) you touched
   - a test plan (commands you ran)

## Credits (opt-in)

Add yourself to `CREDITS.md` in your PR (optional).

