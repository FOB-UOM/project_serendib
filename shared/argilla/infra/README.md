# Argilla + App Contributor Infra

This folder contains lightweight infrastructure for contributor accounts, contribution events, and gamification badges used by the Streamlit platform.

## Files

- `state.json` — persistent local state for users and events.

## Model

- **Accounts**: lightweight contributor identities (`username`, `display_name`, `joined_at`) for project participation tracking.
- **Events**: contribution actions recorded from app/admin tools.
- **Badges**: assigned automatically from contribution points.

## Security and ownership

- This layer intentionally does **not** store passwords or secrets.
- Authentication and RBAC for production should be handled by Argilla workspace auth and/or institution SSO.
- API keys/tokens must be provided through environment variables, not committed files.

## Operational flow

1. Register contributor accounts.
2. Record contribution events (verify, curate, evaluate, maintain).
3. Recompute points and badges automatically.
4. Use leaderboard in app and exports for faculty visibility.
