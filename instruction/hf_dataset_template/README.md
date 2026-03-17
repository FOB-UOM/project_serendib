# Lanka-Instruct-v1 (template)

This folder contains:

- `schema.json`: JSON Schema for validating dataset lines
- `lanka_instruct_v1.sample.jsonl`: a small, well-formed sample file

## JSONL record shape (high level)

Each line is a JSON object:

- `id`: unique string
- `language`: `si` | `ta` | `en` | `mixed`
- `domain`: topical tag (e.g., `public_services`, `education`, `agriculture`)
- `source`: `human` | `synthetic` | `mixed` (and provenance fields)
- `conversations`: list of messages with `role` and `content`

Run validation:

```bash
python scripts\validate_dataset.py --input data/hf_dataset_template/lanka_instruct_v1.sample.jsonl
```

