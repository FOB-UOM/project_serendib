# Future Pillars Template

Use this folder when you want to add a 4th pillar (or any new pillar) without breaking existing structure.

## What to copy

1. Copy `pillar-name-template/`.
2. Rename it to `pillar-<your-domain>/`.
3. Inside it, copy `sub-pillar-template/` for each new sub-pillar.
4. Rename each copied folder (example: `agri-food-systems/`).

## Required files per sub-pillar

- `LAYERS.md`
- `record.schema.json`
- `dataset.manifest.json`
- `seed.sample.jsonl`
- `dataset.v1.jsonl`
- `layer0-raw/records.v1.jsonl`
- `layer1-instruction/records.v1.jsonl`
- `layer2-reasoning/records.v1.jsonl`
- `layer3-structured/records.v1.jsonl`
- `layer4-advanced/records.v1.jsonl`

## After adding the new pillar

1. Add the pillar and sub-pillars to `README.md`.
2. Add the pillar cards/sub-pillars in `platform/app.py`.
3. Add sub-pillar entries in `shared/argilla/config.yaml`.
4. Run validation:

```bash
python shared/scripts/validate_datasets.py
```

## Goal

Keep every new pillar compatible with the same validation, curation, and contribution workflows used in Project Serendib v2.
