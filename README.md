# cage-core

`cage-core` is the protocol layer of the CAGE ecosystem. It defines the canonical `agents.md` specification that governs how AI agents collaborate within a CAGE-enabled project.

## What this repo contains

- **`artifacts/agents.md`** — the distributable agent protocol, seeded into new projects by `cage-cli`.
- **`agents.md`** — this repo's own agent protocol (governs work on cage-core itself).
- **`management/backlog.yaml`** — flat issue tracker for cage-core development.
- **`management/scripts/backlog.py`** — CLI script to manage the backlog.

## Project structure

```
dev.cageai.core/
├── agents.md
├── artifacts/
│   └── agents.md
└── management/
    ├── backlog.yaml
    └── scripts/
        └── backlog.py
```

## Management

```bash
python management/scripts/backlog.py list
python management/scripts/backlog.py show CORE-0001
python management/scripts/backlog.py note CORE-0001 "Some progress note"
python management/scripts/backlog.py done CORE-0001
```

## Dependencies

- Python 3.10+
- `pyyaml`
