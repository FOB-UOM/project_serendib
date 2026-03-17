# Layer 0 — Raw Pre-Training Corpus (`corpus-raw/`)

This folder is for **clean Sinhala text suitable for continued pre-training** and factual grounding.

What belongs here:

- Public-domain classics (digitized)
- Historical documents / manuscripts (where legally permissible)
- Newspapers (license permitting)
- Laws / gazettes (license permitting)

Recommended formats:

- Plain text: `.txt` (UTF-8)
- One-document-per-file, with a small sidecar metadata file (see `corpus-raw/templates/`)

Notes:

- Do **not** commit large raw dumps to git; keep templates and small samples only.
- Track provenance and licensing for every source.

