# Project Serendib v2 - Sovereign Sinhala Data Ecosystem

Project Serendib v2 builds a Sinhala-first, open, production-grade data ecosystem for local intelligence.

## Vision

- Build culturally grounded Sinhala datasets for education, economy, and society.
- Keep quality high through structured layers, validation, and contributor workflows.
- Enable student and teacher participation at national scale.

## Pillar Map (Visible + Actionable)

### 1) Education & Human Development | අධ්‍යාපන හා මානව සංවර්ධනය
Path: `pillar-education-human-development/`

- `teacher-empowerment/` - Classroom practice and teacher support. | පන්තිකාමර ක්‍රියාකාරීත්වය සහ ගුරු සහාය.
- `philosophy-psychology-personality/` - Mindset, ethics, wellbeing, and character. | මනෝභාවය, නීතිමය සිතුවිලි, සුවතාව හා චරිත වර්ධනය.
- `art-literature-culture/` - Sinhala arts, literature, and cultural continuity. | සිංහල කලා, සාහිත්‍ය හා සංස්කෘතික අඛණ්ඩතාව.

### 2) Economy & Enterprise | ආර්ථිකය හා ව්‍යවසාය
Path: `pillar-economy-enterprise/`

- `business-sme-bpm/` - SME growth, process quality, and operations. | කුඩා ව්‍යාපාර වර්ධනය, ක්‍රියාවලි ගුණාත්මකභාවය සහ මෙහෙයුම්.
- `finance-financial-literacy/` - Household finance and practical money literacy. | ගෘහ මූල්‍ය කළමනාකරණය සහ ප්‍රායෝගික මුදල් දැනුම.
- `political-economy/` - Policy, budgets, and public-economy behavior. | ප්‍රතිපත්ති, අයවැය සහ මහජන ආර්ථික හැසිරීම්.

### 3) Society & Environment | සමාජය හා පරිසරය
Path: `pillar-society-environment/`

- `sociology-social-dynamics/` - Community trust, inclusion, and social behavior. | ප්‍රජා විශ්වාසය, ඇතුළත්භාවය සහ සමාජ ගතිකතා.
- `sustainability-climate/` - Climate resilience and sustainability practices. | දේශගුණ තිරසාරභාවය සහ පරිසර හිතකාමී ක්‍රියාමාර්ග.

## Data Layers

- `layer0-raw` - Raw source material and base knowledge.
- `layer1-instruction` - Sinhala instruction-response records.
- `layer2-reasoning` - Reasoning traces and logic-heavy records.
- `layer3-structured` - Structured QA and domain schema data.
- `layer4-advanced` - Advanced future data types.

## Platform + Shared Ops

- `platform/app.py` - Bilingual landing page for pillar discovery and contribution entry.
- `shared/scripts/validate_datasets.py` - Enforces layer1 quality rules.
- `shared/argilla/config.yaml` - Argilla task templates for all sub-pillars.
- `future-pillars-template/` - Copy-ready scaffold for adding future pillars.

## How to Contribute (School Kids + Teachers)

### For school kids

1. Pick a sub-pillar you understand (example: `finance-financial-literacy`).
2. Read existing `layer1-instruction/records.v1.jsonl` samples.
3. Add a new Sinhala record with clear, useful, real-world content.
4. Keep `language` as `si` and avoid placeholders.
5. Ask your teacher to review before submission.

### For teachers

1. Assign each student group to one sub-pillar topic.
2. Review records for clarity, factual quality, and safe language.
3. Ensure schema format is correct and records are unique.
4. Run validation locally:

```bash
python shared/scripts/validate_datasets.py
```

5. Submit changes through your normal Git workflow.

## Validation + CI

- Local:

```bash
python shared/scripts/validate_datasets.py
```

- GitHub Actions: `.github/workflows/ci-validation.yml` runs validation on every push and pull request.

## Proposal Link

- Core blueprint: [PROPOSAL-v2.md](PROPOSAL-v2.md)

## Future Expansion

To add a 4th pillar later, use `future-pillars-template/README.md` and copy `pillar-name-template/`.
