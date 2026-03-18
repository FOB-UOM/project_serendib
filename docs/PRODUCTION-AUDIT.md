# Project Serendib v2 — Production Readiness Audit

## Current maturity snapshot

The repository now has a strong architecture baseline, a full Streamlit platform shell, and account/gamification infrastructure.

However, as a full production system, the project is still in **early maturity** and requires additional hardening.

## What is done (implemented)

- 3-pillar modular architecture with extensibility template
- Shared OCR layer + CLI/router foundation
- Streamlit full app skeleton (overview, explorer, OCR, accounts, roadmap)
- Contributor account/event/badge infrastructure
- API baseline (`platform/api.py`) for account/event/leaderboard operations
- CI/workflow stubs and quality checks

## Major gaps to reach production

1. **Identity & Access**
   - Missing full auth (SSO/OAuth), session management, role-based authorization
2. **Data Contracts**
   - Missing strict per-pillar schemas and ingestion validators for all record types
3. **Observability**
   - Missing structured logs, metrics, traces, SLO dashboards, alerting
4. **Reliability**
   - Missing queue-based processing, retries, idempotency, backup/restore automation
5. **Security**
   - Missing secret rotation policy, threat model, dependency security gate enforcement at release time
6. **Release Engineering**
   - Missing containerization, environment promotion (dev/stage/prod), rollback playbooks

## Production track (recommended)

### Track A — Platform core
- Introduce managed identity + RBAC
- Move from JSON state to DB-backed transactional store
- Add audit logs and immutable event history

### Track B — Data quality
- Enforce schema + provenance checks in CI for every contributed artifact
- Add safety/PII detectors and review workflows

### Track C — Operations
- Add deployment pipelines, health probes, and operational runbooks
- Add periodic release snapshots with quality scorecards

## Execution principle

Deliver in small, verified increments and avoid monolithic rewrites. Keep the v2 architecture stable while progressively hardening each layer.
