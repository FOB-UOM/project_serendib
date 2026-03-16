# Teachers v0.1 verification rubric

This rubric is designed for student verifiers working on teacher-assistant dialogues.

## Required checks

- **PII**: no real student names, phone numbers, addresses, ID numbers, etc.
- **Safety**: avoid harmful disciplinary advice; prefer supportive, evidence-aligned strategies.
- **Usefulness**: output should be directly usable (steps, scripts, templates).
- **Clarity**: teacher can follow without guessing missing details.
- **Local fit**: respects Sri Lankan classroom constraints (class size, limited resources).

## Suggested labels

- **Language**
  - `en`: clean English
  - `mixed`: Singlish / code-mix in Latin script

- **Domain**
  - `teachers_classroom_mgmt`
  - `teachers_low_resource`
  - `teachers_exam_prep`
  - `teachers_remediation`

- **Decision**
  - `approve`: good as-is
  - `needs_edit`: fixable (add steps, remove PII, clarify)
  - `reject`: fundamentally wrong/harmful/unfixable

## Scoring guidance (1–5)

- **Usefulness**
  - 1: vague encouragement only
  - 3: some steps, but missing key constraints
  - 5: ready-to-use plan/script/template

- **Clarity**
  - 1: confusing or contradictory
  - 3: understandable but needs simplification
  - 5: structured, crisp, easy to follow

