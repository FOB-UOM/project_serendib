# Deployment Hardening Checklist

## Security
- Configure `SERENDIB_STAFF_API_KEY` and `SERENDIB_MAINTAINER_API_KEY` via secrets manager.
- Restrict API endpoints by role and enforce HTTPS only.
- Rotate API keys on a fixed schedule.

## Reliability
- Persist SQLite DB on durable volume or migrate to managed Postgres.
- Add scheduled backups and restore drills.
- Add health checks for Streamlit and API services.

## Accessibility & UX
- Maintain bilingual labels (English + Sinhala) for user-facing pages.
- Keep high-contrast mode available.
- Ensure form labels and controls remain keyboard navigable.

## Operations
- Add structured logging and metrics export.
- Define SLOs: uptime, moderation latency, and data approval throughput.
- Create incident response runbook for failed ingestion/moderation/export jobs.
