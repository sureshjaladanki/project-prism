# Prism

A civic CMS that turns official Indian statistics into a checkable portrait of the country. It is not a newsroom, a partisan report card, or a live scrape of ministry sites.

Templates hold copy and charts. A **data vintage** is an immutable snapshot of observations, citations, geography, and caveats after one pipeline run. Render is `template + vintage → page`. When a source updates, ingest lands the new file, the pipeline writes a **new** vintage, the CMS re-renders, then a pointer flip publishes. Citizen view moves only to a complete published vintage.

Inspired by the *role* of [USAFacts](https://usafacts.org/): make government data usable, do not tell people what to think. Vision is in [`docs/vision.md`](docs/vision.md). Product and machine are in [`docs/architectural-blueprint.md`](docs/architectural-blueprint.md).

## Layout

| Path | Role |
|------|------|
| `src/prism/` | Python: schema, ingest, pipeline, pointers, render |
| `src/cms/` | Astro citizen site (templates, charts) |
| `tests/` | Contract tests (pytest) and page checks |
| `docs/` | Charters, conventions, blueprints |
| `data/` | Artifacts, vintages, renders, pointers (gitignored except `.gitkeep`) |

## Setup

Python 3.12 and [uv](https://docs.astral.sh/uv/). Node is needed to render the citizen site.

```bash
uv sync
cd src/cms && npm install
```

## Commands

```bash
uv run prism ingest
uv run prism vintage
uv run prism render --vintage-id <vintage_id> --set-preview
uv run prism preview
uv run pytest tests
```

`prism preview` serves the preview pointer with `noindex`. It does not flip the citizen pointer. Citizen publish waits for a Trust Auditor pass.

## Docs

- [`docs/architectural-blueprint.md`](docs/architectural-blueprint.md) — product and system
- [`docs/design-system.md`](docs/design-system.md) — citizen visual contract (not a USAFacts clone)
- [`docs/editorial-guidelines.md`](docs/editorial-guidelines.md) — how citizen pages read
- [`docs/data-contracts.md`](docs/data-contracts.md) — schema
- [`docs/data-pipeline.md`](docs/data-pipeline.md) — ingest and vintage writes
- [`docs/repo-conventions.md`](docs/repo-conventions.md) — layout and tooling
- [`docs/team.md`](docs/team.md) — who does the work
