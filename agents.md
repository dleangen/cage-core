# AGENTS.md — dev.cageai.core

## What this repo is

`cage-core` is the protocol layer of the CAGE ecosystem. It has one job: define and distribute `artifacts/agents.md` — the canonical agent protocol that `cage-cli` seeds into new projects.

This repo is intentionally minimal. If you find yourself adding frameworks, dependencies, or abstractions, stop.

## Repo structure

```
dev.cageai.core/
├── agents.md                        ← you are here
├── artifacts/
│   └── agents.md                    ← the distributable protocol (the main deliverable)
├── management/
│   ├── backlog.yaml                 ← issue tracker (source of truth for active work)
│   └── scripts/
│       └── backlog.py               ← CLI to manage the backlog
```

## Before you do anything

Check the backlog for the active issue:

```bash
python management/scripts/backlog.py list --status=active
python management/scripts/backlog.py show CORE-XXXX
```

Only one issue may be active at a time. Work on that issue. If nothing is active, ask the user which backlog item to activate before proceeding.

## Backlog management

```bash
python management/scripts/backlog.py list
python management/scripts/backlog.py show <id>
python management/scripts/backlog.py activate <id>
python management/scripts/backlog.py done <id>
python management/scripts/backlog.py note <id> "progress note"
python management/scripts/backlog.py add
```

## Commit conventions

Light conventional commits. No tooling enforcement.

```
feat(cage-core): add agents.md v0.1.0
fix(cage-core): correct backlog ID generation
docs(cage-core): update README
chore(cage-core): bump version to 0.2.0
```

## Branch conventions

- One branch per issue: `core-XXXX` matching the issue ID.
- Branch from `main`. Merge back with `--no-ff`.

## Common files

`management/` is managed by `dev.cageai.bootstrap`. Do not edit those files directly here — make changes in bootstrap and run `sync.py`.

```bash
# From dev.cageai.bootstrap:
python scripts/sync.py core
```

## What NOT to do

- Do not add dependencies to this repo.
- Do not add a build system, framework, or CLI here — that belongs in `cage-cli`.
- Do not edit `management/` files directly — use bootstrap sync.
- Do not create Work Plans — just issues in `backlog.yaml`.
- Do not modify `artifacts/agents.md` unless it is the active issue.
