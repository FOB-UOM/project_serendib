# Contributing to Project Serendib v2

Thank you for contributing to this long-term faculty public-good project.

## Contribution Model (3 Pillars + Shared Layer)

Work should be organized under one of the three main pillars:

1. `pillar-education-human-development/`
2. `pillar-economy-enterprise/`
3. `pillar-society-environment/`

Each pillar contains visible sub-pillars. Contribute inside the most specific sub-pillar possible.

Shared and cross-pillar work belongs in:
- `shared/ocr-pipeline/`
- `shared/argilla/`
- `shared/argilla/infra/`
- `shared/scripts/`
- `platform/`

## How Students Should Contribute

- Keep changes small and well-scoped.
- Preserve old content and add new content incrementally.
- Use clear filenames and concise commit messages.
- Add references/sources for factual or policy content.
- Do not include private or sensitive personal data.

## Adding a New Pillar (Future Expansion)

Project Serendib v2 is designed to grow.

1. Copy `future-pillars-template/pillar-name-template/`.
2. Rename it to `pillar-<domain-name>/`.
3. Create/rename sub-pillars to clearly represent scope.
4. Add a pillar-level `README.md` and sub-pillar `README.md` files.
5. Update links and navigation in:
   - root `README.md`
   - `platform/app.py`
   - relevant workflow/config docs if needed

## Quality Expectations

- Follow repository lint/test checks before opening a PR.
- Keep folder names descriptive and stable.
- Keep reusable automation in `shared/scripts/`.
- Keep OCR-related enhancements inside `shared/ocr-pipeline/`.
- For contributor operations, use the gamification tooling in `shared/scripts/gamification_cli.py`.
- For dataset contributions, follow each sub-pillar `record.schema.json` contract.
- Public submissions must pass moderation before canonical export.

## Code of Conduct

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
