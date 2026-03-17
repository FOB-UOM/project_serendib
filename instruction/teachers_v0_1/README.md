# Teachers v0.1 (Sri Lanka) — dataset pack

This is the first focused slice of `Lanka-Instruct-v1`, targeting **Sri Lanka school teachers** and their daily workflows.

## Scope

- **Audience**: mixed (Primary, O/L, A/L)
- **Language**: English (`en`) + Singlish (`mixed`)
- **Persona**: Sri Lanka Teacher Assistant (practical, safe, avoids PII)

## Domains

Use one of these `domain` values:

- `teachers_classroom_mgmt`
- `teachers_low_resource`
- `teachers_exam_prep`
- `teachers_remediation`

## Files

- `teachers_v0_1.sample.jsonl`: small, schema-valid examples
- `rubric.md`: how reviewers should label/verify records

## Validate

```bash
python scripts/validate_dataset.py --input data/teachers_v0_1/teachers_v0_1.sample.jsonl
```

