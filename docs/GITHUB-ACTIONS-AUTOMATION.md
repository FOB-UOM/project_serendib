# GitHub Actions Automation: What is Feasible for Serendib

## Yes, feasible right now

### 1) Data validation and quality gates
- Validate all sub-pillar datasets against `record.schema.json` contracts.
- Fail PRs if contract or quality checks fail.

### 2) Scheduled dataset iteration jobs
- Run scheduled workflows to regenerate quality reports.
- Rebuild moderation queue artifacts from latest submissions/state.
- Publish reports as workflow artifacts.

### 3) OCR batch pre-processing
- Process incoming committed OCR files with confidence routing.
- Emit uncertain-item queue artifacts for review.

### 4) Snapshot/release packaging
- Build periodic release reports (`v0.x`) from current data files.
- Upload structured release artifacts for faculty review.

## Feasible with additional setup

### 5) Argilla integration with real remote workspace
- Pull/push tasks with API keys from GitHub Secrets.
- Requires secure secret management and environment hardening.

### 6) Auto moderation assist
- Run model-assisted pre-score and triage in Actions.
- Requires policy decisions to keep final human moderation authority.

## Not ideal (or limited) on Actions runners

- Long-running interactive curation sessions (better in app/Argilla UI).
- Stateful services relying on local runner disk persistence across runs.
- Workflows requiring secret exposure without proper environment protections.

## Practical next automation steps (recommended)

1. Keep `dataset-iteration.yml` scheduled + manual.
2. Add environment-scoped secrets for Argilla sync.
3. Add a PR bot summary comment with key metrics:
   - new records per pillar
   - pending/approved moderation counts
   - quality score trend
