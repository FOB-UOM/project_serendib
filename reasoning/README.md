# Layer 2 — Reasoning & Chain-of-Thought (`reasoning/`)

This layer contains **step-by-step explanations / reasoning traces** to improve deep competence in local tasks.

Important:

- Store **structured reasoning artifacts** (e.g., explanation steps) rather than dumping hidden chain-of-thought.
- Where needed, prefer *annotated rationale summaries* and *verifiable intermediate steps*.

Recommended formats:

- JSONL with fields like `question`, `answer`, `steps` (see `reasoning/templates/`)

