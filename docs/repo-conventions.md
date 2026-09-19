# Repo conventions

Layout, languages, and tooling. Product and serving: [architectural-blueprint.md](architectural-blueprint.md). Schema: [data-contracts.md](data-contracts.md). Ingest and vintage writes: [data-pipeline.md](data-pipeline.md).

One git repository. Do not split ingest, pipeline, CMS, or serving into separate repos — the schema and the nine contract tests would version-skew.

## Layout

| Path | Role |
|------|------|
| `src/prism/` | Python package: schema, ingest, pipeline, pointers, publish, render orchestration |
| `src/cms/` | Astro citizen site (templates, charts, static build). `package.json` lives here, not at repo root |
| `tests/` | pytest (contract) and Playwright (citizen page). Python tests may live here even when they drive `src/cms/` |
| `docs/` | Verdicts, charters, conventions (kebab-case filenames) |
| `docs/personas/` | Agent personas for the team in [team.md](team.md) |
| `data/` | Artifacts, vintages, renders, pointers (gitignored except `.gitkeep`). Ingest layout in [data-pipeline.md](data-pipeline.md) |
| `logs/` | Run output (gitignored except `.gitkeep`), including `logs/{run_id}/report.json` |
| `pyproject.toml` | Python project at repo root (`uv`) |

New docs go under `docs/` with kebab-case names. STOP memos and closed-programme summaries belong in `docs/archive/`; active next work in `docs/next/`.

Do not invent extra top-level folders (`apps/`, `packages/`, `web/`). Generated pages are outputs under `data/renders/`, not a source of truth.

```text
data/cas/{sha256}                   write-once bytes (observations, JSON, rendered pages)
data/vintages/{vintage_id}/         immutable directory: manifest.json plus
                                    series/{series_id}/ files hard-linked into cas
data/renders/{vintage_id}/          complete Astro tree; unchanged pages hard-linked
                                    into cas; not citizen-view until the pointer flips
data/pointers/citizen               vintage_id of the last complete published vintage
data/pointers/preview               vintage_id for unpublished preview (never an alias of citizen)
data/raw|derived|lineage/           ingest (see data pipeline)
logs/{run_id}/report.json           what ran, changed, failed — not lineage.json
```

## Languages

- **Python 3.12** — schema, ingest, pipeline, pointers, publish, contract tests. Package manager: `uv`.
- **TypeScript** — Astro templates and Vega-Lite chart specs under `src/cms/`.
- **SQL** — DuckDB at render time, reading one vintage directory. Not a second source of truth.

Python is the machine, not the citizen API. FastAPI is not Wave 1 serving.

Types for the page layer are generated from Pydantic (`model_json_schema()` → TypeScript). Do not hand-maintain a parallel schema.

## Schema and stores

- **Pydantic v2** — observations, citations, caveats, geography pair, vintage payload. Write fails if `citation_id`, `caveat_id`, or `geography.geography_vintage` is missing.
- **Vintage store** — one directory per `vintage_id`. Never overwrite. Observations are **one Parquet file per `series_id`** (`series/{series_id}/observations.parquet`) plus that series’ citation, caveat, and geography JSON.
- **No full copy.** If a series payload is unchanged (same checksum of observations + citation + caveat + geography as the previous vintage), do not write new bytes. Write once to `data/cas/{sha256}`; the new vintage **hard-links** those files (object storage: reuse the same content-addressed key). A byte-for-byte copy of an unchanged series is a bug. `manifest.json` is always new.
- **`manifest.json`** — human-readable input manifest (also hashed into `vintage_id`). Per series: producer, `series_id`, `source_vintage`, raw checksum, parser version, `lineage_ok`, geography vintage, **payload checksum**, **reused: yes | no**; plus caveat ids and mapper version. The 12-hex in `vintage_id` is identity, not the audit trail.
- **Pointer store** — `data/pointers/citizen` and `data/pointers/preview`. Local write: temp file, then atomic rename. Object storage: conditional PUT (`If-Match` / ETag) on a single current key, plus a publish lock so two publishers cannot interleave. The pointer flip is the last step, after a complete render and after the nine tests pass.
- **DuckDB** — read exactly one `vintage_id` at render. Do not query across vintages to build a citizen page.

## Ingest

`uv`, **httpx**, **pandas** + **openpyxl** + **xlrd** (OLE `.xls`; stop if the workbook cannot be read as cells), **pdfplumber** (stop if scanned or ambiguous; do not guess), **sdmx1** when a producer publishes SDMX. Keep raw bytes. Derived table stays tidy producer CSV under `data/derived/`.

## Pipeline and refresh

**Typer** CLI: ingest → vintage → render → publish. Refresh triggers are only `schedule` | `source_change` | `on_demand` ([architectural-blueprint.md](architectural-blueprint.md)). Batch stages: [data-pipeline.md](data-pipeline.md).

- **schedule** — GitHub Actions cron, following each series’ `next_release`, not a hidden global clock.
- **source_change** — ingest checksum compare. No extra bus.
- **on_demand** — same CLI, manual dispatch.

`pytest` encodes the nine tests in the blueprint. A pipeline run writes `logs/{run_id}/report.json`. That is not `lineage.json`. The report must say, per series, reused or rewritten.

## CMS and serving

Templates in git under `src/cms/`: Markdown copy + YAML slots (selector → series / geography / period). Content Editor never types a numeral into the page.

**Astro SSG:** `template + one vintage → static HTML`. Same inputs, same page. Publish points the citizen prefix at a finished `data/renders/{vintage_id}/`. Preview is a **different, non-public** prefix: private bucket (or equivalent), `noindex`, signed URL. A second public URL is not isolation. Routes, titles, SEO, preview headers: [web-design.md](web-design.md) (Front-end Architect owns the contract; UI/UX Developer implements).

Unchanged pages (every bound slot’s series payload checksum unchanged) are hard-linked from cas / the prior render. Re-render only templates whose inputs changed. Do not rebuild and recopy the whole tree because one series moved.

**Vega-Lite** for charts. Breaks, unknown, and not-comparable stay encodings. Default state/UT order is alphabetical by official English name, or a documented geographic order. Colour, type, and chart chrome: [design-system.md](design-system.md) (UI/UX Developer) — USAFacts is a reading reference, not a look to copy.

**Forbidden as publish or refresh:** incremental regeneration of live citizen routes (Next.js ISR, `revalidate`, `revalidatePath`, stale-while-revalidate of production). Mutating live paths in place is not publish. Do not add Next.js, SSR, or request-time `fetch` of a producer site. Do not recopy unchanged series or pages.

UTC in stores. Display release dates in `Asia/Kolkata`.

## Tests

The nine tests in the architecture blueprint are required. Tests 4–8 need a real Astro render of C1; do not ship Python-only and defer them. Test 9 runs as soon as a second vintage exists: unchanged series and pages must not gain a second copy.

Test 8 is a static check of generated Vega-Lite JSON, not only a screenshot: `sort` on the state/UT axis is never by a measure field; `color.scale` is never a red–green diverging scheme.

**Playwright:** a number on a citizen page shows producer, series, date, geography vintage, and caveat in the same view.

## Quality and CI

- Python: **Ruff** + **mypy** (CI-blocking on schema and contract code). `ty` is advisory until a stable release.
- TypeScript: **Biome**.
- GitHub Actions: separate preview and citizen environments so a preview job cannot flip `citizen_pointer`. Pointer-write credentials exist only on the post-test publish job.
- `data/` is gitignored. CI caches or artifacts `data/raw` and `data/derived` by producer / series / `source_vintage`. Do not re-fetch a producer site as the default CI path.

## Do not add

Mongo, a schemaless lake, or a warehouse as the portrait store. Airflow, Dagster, or Spark at Wave 1–2 scale. WordPress, Strapi, Wagtail. Next.js (including ISR). Jupyter as a product surface. Kubernetes. A mobile app. A client-side engagement, heatmap, or A/B SDK. A hand-maintained second TypeScript schema. Rank or red–green chart defaults. A full-snapshot copy of unchanged series into a new vintage.

## Later, on a named event

Not by wave number.

| Add | When |
|-----|------|
| Object storage + CDN | First citizen page served to real users |
| FastAPI | First public observation API, or preview auth beyond a signed URL |
| Postgres | First observation API that needs transactional writes |
| Job runner | About 15–20 independently scheduled series, or a backfill Actions cannot express |
| Product analytics | CDN access-log aggregates only. No per-user identifiers. Never a most-viewed-states ranking. |
