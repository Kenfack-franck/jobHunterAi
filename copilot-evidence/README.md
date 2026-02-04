# Copilot CLI Evidence (for judges)

This folder contains proof of usage of **GitHub Copilot CLI** during the project development, plus derived statistics.

## Contents
- `INDEX.md`: inventory of evidence files
- `STATISTICS.md`: Copilot CLI usage stats computed from local sessions
- `GIT_IMPACT.md`: git impact stats (commits/files/lines) since 2026-01-30
- `exports/`: human-readable conversation exports (Markdown)
- `scripts/`: scripts used to collect/export and generate statistics

## Privacy / raw logs
Raw Copilot session files (e.g. `events.jsonl`) and process logs are **not committed** because they can be very large and may contain sensitive information.
All included exports are meant to be shareable with judges.

## How to regenerate (local)
The scripts in `scripts/` can be run locally to regenerate exports and stats.
