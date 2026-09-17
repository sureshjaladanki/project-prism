# Coding Conventions

How to write and review code. Layout, languages, and tooling live in [repo-conventions.md](repo-conventions.md). This file does not repeat them.

One git repository. Python under `src/prism/`, TypeScript under `src/cms/`, tests under `tests/`. DuckDB SQL at render, reading one vintage. Do not invent extra top-level folders.

## Clean, simple, readable

Prefer clarity over cleverness. A reader should understand intent without reconstructing hidden control flow.

- Keep functions focused on one job.
- Prefer straight-line logic and small helpers over nested conditionals.
- Comment *why* when the reason is not obvious; do not narrate *what* the code already says.

## Immutable workflows — prefer functional style

Ingest, vintage, render, and publish are transforms: inputs in, new artifacts out. Old vintages stay as written. Repeat a step and the result must not change beyond the first successful run, when that is natural for the language and domain.

- Prefer pure functions (`frame in → frame out`, `vintage_id in → render tree out`).
- Do not mutate a caller’s object, a written vintage, or a live citizen path in place.
- File and pipeline steps must be safe to re-run (overwrite or skip completed work deliberately, not accidentally append or duplicate).
- Avoid hidden mutable globals; make side effects explicit.

## Contracts and instances — prefer objects

Schema, observations, citations, caveats, geography pair, and vintage payload are types with invariants, not loose dicts.

- Python: Pydantic models. Construction fails if `citation_id`, `caveat_id`, or `geography.geography_vintage` is missing.
- TypeScript: types generated from those models (`model_json_schema()`). Do not hand-maintain a parallel schema.
- Behaviour that belongs to the contract lives on the type. Ad-hoc records are for local plumbing only.

## Minimal branching

Keep control flow shallow.

- Avoid unnecessary `if` / `else` and defensive nesting.
- Do **not** add null / `None` / `undefined` checks “just in case.” Trust typed contracts and fail fast at the boundary when invariants break.
- Prefer early returns only when they flatten real complexity — not as a habit.

## Modular

Split by responsibility so modules stay small and composable.

- One module ≈ one concern (ingest, vintage, pointer, render).
- Public APIs accept and return the contract types above; keep helpers private in the language’s usual way (Python `_helper`, TypeScript unexported).
- Share utilities instead of copy-pasting near-identical logic.

## Do not over-engineer

Solve the problem in front of you.

- No abstractions, frameworks, or config layers until a second concrete use demands them.
- No speculative generality (“might need later”).
- Prefer the simplest correct implementation that matches existing patterns in the repo.

## Clear nomenclature

Names encode role and meaning. Use the blueprint’s vocabulary (observation, citation, caveat, series, vintage, geography, template, render, publish, pointer) — not parallel synonyms.

Follow the language of the file. Do not force Python names into TypeScript or the reverse.

### Python (`src/prism/`, `tests/`)

| Kind | Convention | Examples |
|------|------------|----------|
| Modules / files | `snake_case` | `vintage_store.py`, `citation_card.py` |
| Functions | verb + object, `snake_case` | `write_vintage`, `load_observations` |
| Variables | `snake_case`, domain terms | `vintage_id`, `series_id`, `geography_vintage` |
| Constants | `SCREAMING_SNAKE_CASE` | `CITIZEN_POINTER`, `PREVIEW_POINTER` |
| Classes / models | `PascalCase` | `Observation`, `VintageManifest` |
| Private helpers | leading `_` | `_payload_checksum`, `_atomic_rename` |
| Parquet / frame columns | stable `snake_case`, schema field names | `series_id`, `knowledge_date`, `reference_period` |

### TypeScript (`src/cms/`)

| Kind | Convention | Examples |
|------|------------|----------|
| Components | `PascalCase` files | `CitationCard.astro`, `StateChart.tsx` |
| Other modules | `kebab-case` files | `bind-slots.ts`, `vega-lite-spec.ts` |
| Functions / variables | `camelCase` | `bindSlots`, `vintageId` |
| Types | `PascalCase`, generated when they are schema | `Observation`, `VintageManifest` |
| Constants | `SCREAMING_SNAKE_CASE` | `CITIZEN_POINTER` |
| Schema fields | keep the generated names | do not camelCase `series_id` by hand |

Astro routes follow the file-based router (`index.astro`, `[vintageId].astro`), not the tables above.

### SQL (DuckDB)

Identifiers match the vintage schema (`snake_case`). Query exactly one `vintage_id`. SQL is not a second source of truth.

## Respect repository conventions

Paths, languages, package managers, linters, and forbidden stacks: [repo-conventions.md](repo-conventions.md).

Match the surrounding code before introducing a new style.

- Python lives in `src/prism/`; the citizen site lives in `src/cms/` (`package.json` stays there). Tests live in `tests/`.
- Prefer libraries already named in repo conventions (Pydantic, pandas, httpx, Astro, Vega-Lite). Do not add a second schema stack.
- When editing a file, mirror its naming, import style, and structure rather than reformatting unrelated code.
- New docs under `docs/` use kebab-case filenames.

When in doubt: **read a nearby module and do the same thing, only simpler.**
