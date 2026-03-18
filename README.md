# Project Serendib v2

**Sovereign Sinhala Data Ecosystem**  
**Truly Local at Heart.**

Project Serendib v2 is a modular, long-horizon faculty initiative organized around three visible pillars and a shared infrastructure layer for OCR, curation, and automation.

This is a quiet, long-term faculty seed project.

## Pillar Architecture

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

## Shared Platform Layers

- `shared/ocr-pipeline/` — hybrid OCR routing and improvement roadmap
- `shared/argilla/` — shared curation touchpoint
- `shared/scripts/` — shared automation scripts
- `shared/argilla/infra/` — contributor accounts, events, and badge state
- `shared/argilla/infra/public_tasks.json` — standalone public task catalog
- `shared/argilla/infra/public_submissions.json` — layperson submissions store
- `platform/app.py` — full Streamlit platform app (overview, explorer, OCR, public tasks, accounts/badges, roadmap)
- `platform/api.py` — production-baseline API for accounts/events/leaderboard

## How to Add a New Pillar in the Future

1. Copy `future-pillars-template/pillar-name-template/`.
2. Rename the copied folder to `pillar-<new-domain>/`.
3. Rename subfolders to meaningful sub-pillars.
4. Add a short `README.md` inside each new sub-pillar describing scope and contribution format.
5. Add links to the new pillar in:
   - this root `README.md`
   - `CONTRIBUTING.md`
   - `platform/app.py`
6. Keep `shared/` reusable and pillar-agnostic.

## Proposal v2

See the full v2 proposal in [PROPOSAL-v2.md](PROPOSAL-v2.md).

## Execution Roadmap

Architectural progress, remaining work, and the 90-day plan are tracked in
[docs/EXECUTION-ROADMAP-v2.md](docs/EXECUTION-ROADMAP-v2.md).

Production readiness audit and hardening gaps are tracked in
[docs/PRODUCTION-AUDIT.md](docs/PRODUCTION-AUDIT.md).

## Continuity Note

Existing repository assets from earlier phases are intentionally preserved to ensure continuity while this architecture evolves.
