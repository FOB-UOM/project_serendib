# Project Serendib — Sovereign Sinhala Data Ecosystem

Truly Local at Heart. Multi-Type Open Corpus for Deep Local Intelligence & Adaptive AI.

## Core thesis

Global models lack epistemic depth in Sinhala contexts. We solve this by creating a full multi-type open data foundation:

- Rich raw knowledge corpus for factual grounding and continued pre-training
- High-quality instruction data for helpful, culturally aligned behavior
- Bridging layers (reasoning/CoT, structured QA, etc.) for advanced intelligence
- Student-powered curation flywheel that turns data work into education

Building on the original instruction-focused vision, we now expand to a full multi-type ecosystem for deeper intelligence. This work is **complementary to SinLLM lineage**, not competitive.

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

## Supporting infrastructure

- `ocr-pipeline/` — Tesseract + TrOCR Sinhala OCR starters
- `synthetic-gen/` — Bonito / LLaMA-Factory style synthetic generation (human verification required)
- `training/` — Unsloth QLoRA scripts for instruction + continued-pretrain (mixed training later)
- `argilla/` — gamified student verification tasks + leaderboard scaffolding
- `evaluation/` — Sri Lankan cultural benchmark + custom eval set scaffolding
- `notebooks/` — Colab-friendly examples

## Phased deliverables

- **v0.1 Pilot (1–3 months)**: Layer 1 (instruction) + small `Lanka-Instruct-v1` on Qwen2.5-7B or SinLLM base (Lean-AI via LoRA/PEFT)
- **v1.0 Depth (3–9 months)**: Add Layer 0 raw corpus + mixed training
- **v2.0 Holistic Ecosystem (9–24 months)**: All layers live with 100+ student contributors

## Quick-start (students & researchers)

### Install (recommended: venv)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Validate an instruction JSONL file

```bash
python instruction\validate_dataset.py --input instruction\hf_dataset_template\lanka_instruct_v1.sample.jsonl
```

### Train (baseline) with Unsloth QLoRA (instruction)

```bash
python training\train_unsloth_qlora.py --dataset instruction\hf_dataset_template\lanka_instruct_v1.sample.jsonl
```

## Student contribution guide (Argilla gamification)

Start here: `CONTRIBUTING.md`.

Fast onboarding:

- **Verify 10 examples → earn badge + credit** (Argilla verification queue)
- **Fix 5 flagged issues → earn curator credit** (formatting/provenance/safety)
- **Add 10 eval prompts → earn evaluator credit** (cultural benchmark growth)

Credits (typical):

- **Verifier (1–3 credits)**: label quality, safety, language, relevance in Argilla
- **Curator (3–8 credits)**: improve records, add metadata/provenance, fix schema
- **Evaluator (3–8 credits)**: add evaluation prompts, run baselines, report regressions
- **Maintainer (8+ credits)**: review PRs, manage releases, update schema/process

Badges (maintainers may award):

- **Bronze** (10 credits), **Silver** (25), **Gold** (50), **Platinum** (100)
- **Domain Specialist** (education, SME regs, history, etc.)
- **Language Champion** (Sinhala/Tamil/English)
- **Safety Steward** (PII/safety triage excellence)

Opt-in credit roll: `CREDITS.md`.

## Tech stack (2026)

- **Cursor** for contributor productivity and reviews
- **Unsloth** for fast QLoRA/PEFT fine-tuning
- **Argilla** for student labeling/verification + leaderboards
- **Bonito / LLaMA-Factory style pipelines** for synthetic candidate generation
- **Tesseract (Sinhala) + TrOCR** for OCR ingestion

## Original proposal and continuity

- **Original proposal (OCR transcription)**: `PROPOSAL.md`  
- **OCR outputs**: `proposal_ocr.txt`, `proposal_extracted.md`  

If you have the original proposal PDF, add it to the repo root as `PROPOSAL.pdf` and link it from this section.

## License and public good commitment

- **License**: MIT (`LICENSE`)
- **Code of conduct**: this project is a **national digital public good** for education and enterprise; contributors must follow `CODE_OF_CONDUCT.md` and avoid harmful content and PII.