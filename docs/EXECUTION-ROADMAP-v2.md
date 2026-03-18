# Project Serendib v2 — Execution Roadmap (Architect View)

## 1) What is already done (foundation complete)

- Repository restructured into 3 clear pillars with visible sub-pillars.
- Shared layer established with OCR router and CLI scaffolding.
- Platform app upgraded to a full Streamlit multi-section interface.
- Contributor account + gamification infra added (`shared/argilla/infra/` + scripts).
- Core workflow stubs added for CI, OCR batch, HF sync, Argilla generation, quality gate.
- Future pillar template added for long-term extensibility.

## 2) What must be built next (to make this real)

### A. Data Operations (critical)
1. Define strict per-pillar data schemas (JSON Schema + metadata contract).
2. Add provenance requirements (source, license, collection method, reviewer).
3. Add dataset release snapshots (`v0.1`, `v0.2`, etc.) and changelog policy.

### B. OCR Productionization
1. Extend OCR CLI from routing demo to batch pipeline outputs.
2. Add confidence scoring + uncertain sample routing to Argilla queues.
3. Automate OCR result packaging in `ocr-batch.yml`.

### C. Argilla Integration (real workflow)
1. Create Argilla dataset/task templates for each pillar sub-domain.
2. Build script to ingest approved Argilla records into correct pillar paths.
3. Convert approved records to gamification events automatically.

### D. Contributor Program + Governance
1. Define student role matrix (Verifier, Curator, Evaluator, Maintainer).
2. Publish contribution SLAs (review windows and quality expectations).
3. Publish monthly leaderboard + recognition cycle.

### E. Quality + Security Gates
1. Add schema validation for every contributed record in CI.
2. Add PII/safety lint checks on new content.
3. Keep CodeQL and PR review gates mandatory before merge.

## 3) 90-day delivery plan

### Sprint 1 (Weeks 1–3)
- Finalize schemas and directory-level READMEs per sub-pillar.
- Implement Argilla task templates + import/export scripts.
- Upgrade OCR CLI to batch mode with output artifacts.

### Sprint 2 (Weeks 4–7)
- Activate OCR-to-Argilla uncertain sample loop.
- Implement event ingestion from Argilla actions to gamification state.
- Add release packaging for first faculty demo dataset.

### Sprint 3 (Weeks 8–12)
- Publish v0.1 data release with quality report.
- Run pilot with student contributors and teacher reviewers.
- Iterate badge rules and contribution UX based on usage.

## 4) Architectural guardrails

- Keep pillars independent; shared logic goes only under `shared/`.
- Avoid monolithic scripts; prefer composable reusable modules.
- Preserve all legacy content; layer v2 additions without destructive changes.
- No secrets in repo. Use environment variables for all integration credentials.

## 5) Definition of success

- Active contributors can onboard and contribute without GitHub expertise.
- OCR corrections flow into reusable, quality-controlled datasets.
- Pillar datasets grow continuously with provenance and quality metadata.
- Faculty can track progress via app dashboard + reproducible releases.
