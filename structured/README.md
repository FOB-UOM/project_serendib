# Layer 3 — Domain-Specific Structured Data (`structured/`)

This layer holds **structured datasets** for Sri Lankan domains, especially:

- Education (O/L & A/L)
- Laws and regulations (SME, labor, tax, etc.)

Typical tasks:

- QA pairs (grounded)
- Summarization targets
- Entity extraction / normalization

Recommended formats:

- JSONL (one record per line) with explicit `source` + `provenance`
- CSV for small, clearly versioned tables (avoid for large corpora)

