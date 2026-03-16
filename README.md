# Project Serendib

Sri Lanka’s open **sovereign instruction dataset** initiative — building `Lanka-Instruct-v1` with transparent governance, student participation, and reproducible training/evaluation workflows.

## What this repo contains

- **`data/`**: Dataset schema, templates, and (optionally) curated/validated releases.
- **`scripts/`**: Data validation, conversion, and training utilities.
- **`notebooks/`**: Exploration/QA notebooks (kept lightweight, reproducible).
- **`evaluation/`**: Benchmarks, prompts, and evaluation harness stubs.
- **`argilla/`**: Student verification workflows (Hugging Face Space-ready scaffold).
- **`PROPOSAL.md`**: OCR transcription of the proposal for easy reference.

## Current focus: Teacher workflows (v0.1)

We are starting with a teacher-assistant slice aimed at helping Sri Lanka school teachers with day-to-day work:

- Classroom management + pedagogy
- Low-resource teaching aids
- Exam prep
- Remediation / differentiation

See `data/teachers_v0_1/`.

## Executive summary (to be derived from the proposal)

The proposal PDF for Project Serendib is **image-based**. We OCR’d it into `proposal_ocr.txt` (repo file) to extract the content below.

- **Mandate**: Move beyond “simple translation” to capture Sri Lanka’s **epistemic context** (local reasoning, regulatory dynamics, cultural context). The proposal argues global models are “context-blind” for Sri Lankan needs.
- **Solution**: Build a high-quality **Instruction Dataset** as the primary asset, plus a **Reference AI Model** (`Lanka-Instruct-v1`) as proof of utility.
- **Method**: Apply a **Lean-AI** approach that prioritizes curation over raw compute; use **student participation** to solve the “data scarcity” bottleneck and convert data work into education (credits/badges).
- **Outcome**: Enable the university to lead **sovereign AI development**, building on and complementing local efforts like **SinLLM**.

## Objectives (to be derived from the proposal)

- **Primary objective (the asset)**: a rigorously curated **Sri Lankan Open Instruction Dataset** (multi-turn dialogue).
- **Secondary objective (the proof)**: `Lanka-Instruct-v1` pilot / reference model to demonstrate the dataset’s practical utility.
- **Focus domains (initial)**: O/L & A/L education, SME business regulations, and local history.
- **Strategic continuity**: extend (not compete with) **SinLLM**, specifically improving instruction-following via an adaptation layer on global base architectures (Llama/Mistral, etc.).

## Methodology (to be derived from the proposal)

- **Phase I — Participatory data curation**: human-in-the-loop verification/cleaning using the student body; treat data engineering as skill acquisition with a **gamified flywheel** (credits, badges, experience).
- **Phase II — Lean-AI technical layer**: **transfer learning** with **LoRA/PEFT** adapters on a frozen pre-trained base model; update a small fraction of parameters to bridge global models with local instruction data (resource efficient; standard hardware).
- **Phase III — Evaluation & deployment**: define success via **cultural relevance** rather than only global benchmarks; create a “Sri Lankan Cultural Evaluation Set” and aim for lightweight deployments accessible to local researchers/developers.

## Quickstart

### Install (recommended: venv)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Validate a JSONL dataset file

```bash
python scripts\validate_dataset.py --input data\hf_dataset_template\lanka_instruct_v1.sample.jsonl
```

### Train (stub) with Unsloth QLoRA

```bash
python scripts\train_unsloth_qlora_7b.py --dataset data\hf_dataset_template\lanka_instruct_v1.sample.jsonl
```

## Dataset format (HF-friendly)

Each record is a single JSON object (JSON Lines / `.jsonl`) representing one conversation with metadata. See:

- `data/hf_dataset_template/schema.json` (JSON Schema)
- `data/hf_dataset_template/lanka_instruct_v1.sample.jsonl` (sample)

## Contributing

Start here: `CONTRIBUTING.md`.

### Student gamification (credits & badges)

We track contributions by **credits** awarded for validated work:

- **Verifier (1–3 credits)**: label quality, safety, and relevance in Argilla tasks
- **Curator (3–8 credits)**: improve prompts/responses, add metadata, fix formatting
- **Evaluator (3–8 credits)**: add evaluation prompts, run baselines, report regressions
- **Maintainer (8+ credits)**: review PRs, manage releases, update schema/process

Badges (maintainers may award):

- **Bronze** (10 credits), **Silver** (25), **Gold** (50), **Platinum** (100)
- **Domain Specialist** (e.g., Health, Agriculture, Public Services)
- **Language Champion** (Sinhala/Tamil/English)
- **Safety Steward** (PII/safety triage excellence)

Your name/handle can be added to `CREDITS.md` (opt-in).

## License

Code is MIT (see `LICENSE`). Dataset licensing depends on sources and will be documented per-release in `data/` (dataset card + provenance).