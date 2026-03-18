# Project Serendib v2 — Sovereign Sinhala Data Ecosystem

Truly Local at Heart. Multi-Type Open Corpus for Deep Local Intelligence & Adaptive AI.

## Core thesis

Global models lack epistemic depth in Sinhala contexts. We solve this by creating a full multi-type open data foundation while organizing project work into clear faculty pillars.

- Rich raw knowledge corpus for factual grounding and continued pre-training
- High-quality instruction data for helpful, culturally aligned behavior
- Bridging layers (reasoning/CoT, structured QA, etc.) for advanced intelligence
- Student-powered curation flywheel that turns data work into education

This is a quiet, long-term faculty seed project.

## Pillar architecture (v2 overlay)

### 1) Education & Human Development
Path: `pillar-education-human-development/`

Sub-pillars:
- `teacher-empowerment/`
- `philosophy-psychology-personality/`
- `art-literature-culture/`

### 2) Economy & Enterprise
Path: `pillar-economy-enterprise/`

Sub-pillars:
- `business-sme-bpm/`
- `finance-financial-literacy/`
- `political-economy/`

### 3) Society & Environment
Path: `pillar-society-environment/`

Sub-pillars:
- `sociology-social-dynamics/`
- `sustainability-climate/`

## Multi-type data layers

- **Layer 0 — Raw Pre-Training Corpus** (`corpus-raw/`)  
  Deepest driver of local factual grounding: books, historical documents, laws, newspapers, manuscripts (with provenance + licensing).

- **Layer 1 — Instruction Dataset** (`instruction/`)  
  Multi-turn dialogues in focus domains (deliverable-first).

- **Layer 2 — Reasoning & “Chain-of-Thought”** (`reasoning/`)  
  Step-by-step explanations and reasoning traces (stored as structured artifacts; see layer README).

- **Layer 3 — Domain-Specific Structured Data** (`structured/`)  
  QA pairs, summarization, entity extraction, especially for laws & education.

- **Layer 4 — Advanced Types (future stubs)** (`advanced/`)  
  Parallel Sinhala–English, preference data, tool-use traces, etc.

## Shared platform layers

- `shared/ocr-pipeline/` — hybrid OCR routing, batch confidence loop, improvement roadmap
- `shared/argilla/` — shared curation touchpoint
- `shared/argilla/infra/` — accounts/events/moderation/public-task stores
- `shared/scripts/` — validation, release, and pipeline automation
- `platform/app.py` — full Streamlit platform app
- `platform/api.py` — production-baseline API with auth/RBAC and moderation flows
- `platform/persistence.py` — SQLite persistence layer

## Data contracts and seed datasets

Each sub-pillar includes:
- `record.schema.json` (contract with provenance + license fields)
- `seed.sample.jsonl` and `dataset.v1.jsonl`
- Multi-type seed files:
  - `layer0.raw.jsonl`
  - `layer1.instruction.jsonl`
  - `layer2.reasoning.jsonl`
  - `layer3.structured.jsonl`
  - `layer4.advanced.jsonl`

Validate all sub-pillar datasets:

```bash
python shared/scripts/validate_pillar_records.py --root .
```

## Supporting infrastructure

- `ocr-pipeline/` — original OCR starters
- `synthetic-gen/` — synthetic generation support
- `training/` — Unsloth QLoRA training scripts
- `argilla/` — labeling/verification task tooling
- `evaluation/` — benchmark and evaluation scaffolding
- `notebooks/` — Colab-friendly examples

## Phased deliverables

- **v0.1 Pilot (1–3 months)**: seed datasets + moderation loop + validation baseline
- **v1.0 Depth (3–9 months)**: stronger raw corpus and curation throughput
- **v2.0 Holistic Ecosystem (9–24 months)**: all layers active with community flywheel

## Quick-start

### Install

```bash
python -m pip install -r requirements.txt
```

### Validate instruction dataset sample

```bash
python instruction/validate_dataset.py --input instruction/hf_dataset_template/lanka_instruct_v1.sample.jsonl
```

### Validate pillar contracts and data files

```bash
python shared/scripts/validate_pillar_records.py --root .
```

### Run tests

```bash
python -m pytest -q
```

## GitHub Actions automation (dataset iteration)

We can automate dataset progression and reporting via Actions:
- contract validation
- moderation queue artifact generation
- release quality report generation

See:
- [docs/GITHUB-ACTIONS-AUTOMATION.md](docs/GITHUB-ACTIONS-AUTOMATION.md)
- `.github/workflows/dataset-iteration.yml`

## Proposal and continuity

- Full v2 proposal: [PROPOSAL-v2.md](PROPOSAL-v2.md)
- Prior proposal artifacts remain preserved (`PROPOSAL.md`, OCR extracts)

## Execution references

- [docs/EXECUTION-ROADMAP-v2.md](docs/EXECUTION-ROADMAP-v2.md)
- [docs/PRODUCTION-AUDIT.md](docs/PRODUCTION-AUDIT.md)
- [docs/PILOT-PROGRAMS.md](docs/PILOT-PROGRAMS.md)
- [docs/DEPLOYMENT-HARDENING.md](docs/DEPLOYMENT-HARDENING.md)

## How to add a new pillar in the future

1. Copy `future-pillars-template/pillar-name-template/`.
2. Rename to `pillar-<new-domain>/`.
3. Add visible sub-pillars and sub-pillar READMEs.
4. Update links in this README, `CONTRIBUTING.md`, and `platform/app.py`.

## License and public-good commitment

- **License**: MIT (`LICENSE`)
- **Code of Conduct**: see `CODE_OF_CONDUCT.md`
