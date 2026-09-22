# Architectural blueprint

The product and the machine it runs on. Schema: [data-contracts.md](data-contracts.md). Batch stages: [data-pipeline.md](data-pipeline.md). Languages, paths, and tools: [repo-conventions.md](repo-conventions.md). Citizen visual contract: [design-system.md](design-system.md) (UI/UX Developer). Routes, SEO, preview vs citizen HTTP: [web-design.md](web-design.md) (Front-end Architect). Citizen copy: [editorial-guidelines.md](editorial-guidelines.md). Who does the work: [team.md](team.md). What the country picture is for: [vision.md](vision.md).

## Product

A civic **CMS** for the portrait in [vision.md](vision.md). Not a folder of hand-built pages. Not a live scrape of ministry sites.

- **Template** — Content Editor’s copy and chart spec, with slots that only accept cited observations.
- **Data vintage** — an immutable snapshot of observations, citations, geography, and caveats after one pipeline run. That is **data-in-time**: the page is true as of that vintage.
- **Render** — `template + vintage → page`. Same inputs, same page.
- **Refresh** — when an official source updates, or an editor asks, Ingest lands the new artifact, Pipeline writes a **new** vintage, CMS re-renders, Platform publishes. Periodic or on-demand. Citizen-view moves only to a complete published desk.

The spine — ingest → immutable vintage → bind/render → atomic pointer — is a **choice**, not deference. Resonance is a voice, binding, and typography problem; nothing in it needs a server. The movement clause is a second observation from the same vintage; the thesis is a template sentence with slots. What the immutable vintage buys is checkable “no invented figures”: every figure on a page is traceable to one snapshot, and a page cannot silently change under a reader. Adding ISR or a request-time producer fetch would buy freshness we do not need and lose the property the trust argument rests on.

Do not hand-author a citizen page of numbers. Do not fetch a producer website at request time to fill a chart. Citizen-view is a pointer at a complete **published** desk. Preview is the same CMS in a second mode: the full desk, including slices that have not been published. No Next.js, no ISR, no request-time producer fetch, no API on the citizen path.

## System context

Prism sits between official statistical offices and a citizen (or editor) reading a page. It does not replace the producers. It does not decide what the numbers mean.

```text
Official statistical offices
  (MoSPI, RBI, Census, state DES, …)
        │  public files (PDF, CSV, SDMX, official export)
        ▼
┌──────────────────────────────────────────────────────────┐
│  Prism                                                   │
│  batch: ingest → vintage → render → publish              │
│  serve: static pages at a pointer                        │
└───────────────┬────────────────────────────┬─────────────┘
                │                            │
                ▼                            ▼
         Citizen-view                  Preview
         (cms_mode=citizen,            (cms_mode=preview,
          published slices only,        every bound slice,
          world-readable)               not world-readable)
                ▲                            ▲
                └──────── editors ───────────┘
                  templates in git,
                  on-demand refresh
```

**Outside the system:** producer websites, citation cards, geography frames, caveat notes, and templates. Those are inputs. The people who write them are in [team.md](team.md); they are not runtime components.

**Inside the system:** the batch CLI, the static site build, the stores, and the two serving pointers.

## Containers

What actually runs. Ownership of each box: [team.md](team.md). Frameworks: [repo-conventions.md](repo-conventions.md).

| Container | Job | Runs when |
|-----------|-----|-----------|
| **prism CLI** (`src/prism/`) | Ingest, write vintage, orchestrate render, flip pointers | Batch: schedule, source change, or on-demand |
| **CMS** (`src/cms/`) | Bind template slots to one vintage; emit static HTML and charts | Batch, as part of render |
| **DuckDB** | Read **exactly one** `vintage_id` during render | In-process at render. Not a server. Not on the citizen request path |
| **Stores** (`data/`, later object storage) | Artifacts, vintages, renders, CAS bytes, pointers | Every run and every serve |
| **CI** | Tests; later, scheduled refresh. Preview credentials cannot flip the citizen pointer | GitHub Actions |

Python is the batch machine, not the citizen API. FastAPI is not Wave 1 serving. The citizen request path is static files.

```text
src/prism/  ──writes──►  data/raw|derived|lineage
            ──writes──►  data/vintages/{vintage_id}
            ──writes──►  data/desks/{desk_id}
            ──calls───►  src/cms/  ──writes──►  data/renders/{desk_id}
            ──writes──►  data/pointers/{citizen|preview}

Citizen HTTP  ──reads──►  files at citizen_pointer
Preview HTTP  ──reads──►  files at preview_pointer
```

`src/` holds application code. `tests/` holds tests. `data/` holds artifacts, vintages, and renders. `logs/` holds run output. Generated pages are outputs, not the source of truth. Do not add top-level folders for the pipeline or the CMS.

## Runtime views

### Refresh (batch)

The only way new official numbers reach a citizen.

```text
trigger:  schedule  |  source_change  |  on_demand
        │
        ▼
Ingest      lands / re-lands the artifact → data/     (pipeline Stage 1)
        │
        ▼
Pipeline    writes a **new** data vintage               (pipeline Stage 2)
        │
        ▼
CMS         render(template, vintage) → render store
        │
        ▼
Tests       eleven tests in this file
        │
        ▼
Platform    flip citizen_pointer (last) or keep the previous
```

Request-time scraping is not a trigger. Incremental regeneration of live citizen routes (ISR, per-path `revalidate`, stale-while-revalidate of production) is not a trigger and is not publish.

On fail at any step: do not move `citizen_pointer`. Do not mix observations from vintage A and vintage B on one citizen page.

How ingest and vintage mapping work: [data-pipeline.md](data-pipeline.md).

### Citizen request

No Python, no DuckDB, no producer fetch.

```text
HTTP GET citizen route
        │
        ▼
Read citizen_pointer → desk_id
        │
        ▼
Serve that desk’s completed **citizen** tree
```

A citizen route cannot read a non-published vintage. Unpublished slice URLs 404 on this prefix.

### Preview

Same bind and Astro build as citizen-view. `cms_mode=preview` includes every template on the preview desk (each **page** still one `vintage_id`). `cms_mode=citizen` includes only slices listed on the citizen desk. Isolation is a different prefix, `noindex`, signed URL (or later authenticated access). A different public URL is not isolation. Preview never aliases `citizen_pointer`.

### Retained vintages

Prior published `vintage_id`s stay addressable so someone can see what the page said then. Overwriting a published vintage in place is a bug.

## Stores

Logical stores Pipeline and CMS must use. Concrete paths: [repo-conventions.md](repo-conventions.md). Ingest tree: [data-pipeline.md](data-pipeline.md).

| Store | Writer | Reader | Rule |
|-------|--------|--------|------|
| **Artifact** | Ingest | Pipeline | Derived tables and lineage only. Pipeline does not fetch |
| **Vintage** | Pipeline | CMS (exactly one id per **page**) | One directory per `vintage_id`, immutable. Per-series Parquet + JSON; unchanged series hard-linked into CAS |
| **Render** | CMS | Serving, after pointer flip | One static tree per `desk_id`. Unchanged pages hard-linked. Citizen-view does not read it until the pointer flips |
| **Template** | Content Editor (git) | CMS | Slots bind to selectors, not typed numerals. Binding is not a template field |
| **Pointer** | Platform on publish | CMS on serve | `citizen_pointer` and `preview_pointer` name a `desk_id`, written atomically |
| **CAS** | Pipeline / CMS | Vintage and render directories | Write-once bytes. A second copy of an unchanged series or page is a bug |
| **Run log** | Pipeline | Operators, tests | `logs/{run_id}/report.json` — what ran, changed, failed. Not ingest `lineage.json` |

## Refresh contract

```text
vintage_id_rule:    "dv-" + run_date_utc (YYYYMMDD) + "-" + 12-hex of
                    manifest.json. Directory with that id is never overwritten.
desk_id_rule:       "desk-" + publish_date_utc (YYYYMMDD) + "-" + 12-hex of
                    desk.json. Directory with that id is never overwritten.
publish_unit:       a desk: one (template_id, vintage_id) per published slice.
                    Each page still binds exactly one vintage_id.
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline (data vintage) → cms render → publish pointer
atomic_publish:     yes   (citizen-view moves only when render of the new desk is complete)
on_fail:            keep previous published desk; do not serve a partial
retain_prior:       yes   (prior desks and prior vintages stay addressable)
```

- **schedule** — a named cadence once operations exist; per series it follows the librarian’s `next_release`, not a hidden global clock.
- **source_change** — Ingest reports a checksum different from the last retrieve (`source_changed: yes`).
- **on_demand** — an editor asks for a run.

Refresh writes a new vintage, reuses unchanged series and pages (hard-link / CAS), re-renders only what changed, then moves the pointer.

The pointer write itself is atomic: local disk uses write-to-temp then rename; object storage uses a conditional PUT (`If-Match` / ETag) on a single current key and a publish lock so two publishers cannot interleave. Order: complete render for that `desk_id` → eleven tests pass → flip `citizen_pointer` last. A bare overwrite of a JSON file is not atomic publish.

## Serving rules

- Always the published pointer for citizen-view.
- Citizen HTTP injects `rel=canonical`, `og:url`, and absolute JSON-LD `url` / `item` from `data-prism-path` using `CITIZEN_ORIGIN`. Shared render HTML omits those tags. Preview does not inject them.
- Default order of states and UTs is alphabetical by official English name, or a documented geographic order. Ranking is not the default. A chart may measure-sort when **that chart’s own caption is a rank question** and the template declares it on the chart spec. Red–green, diverging performance scales, and podium palettes stay forbidden.
- Definition, unit, geography vintage, and data vintage appear in the same view as the number. A tooltip is not the only place they live.
- Charts and any observation API take citation cards with the number. Nothing serves a bare float.
- `unknown`, `not_comparable`, and `series_break` stay visible. Do not smooth them into a continuous line.

## Component boundaries

Each box is a write boundary, not a repo folder beyond `src/`.

| Component | Writes | Reads | Must not |
|-----------|--------|-------|----------|
| Ingest | raw artifact, derived table, lineage, `source_changed` | citation card | portrait schema, citizen pages |
| Pipeline | a **new** data vintage | derived table, lineage, caveat notes, geography vintage | fetch PDFs, edit an old vintage, publish |
| CMS | rendered preview and citizen desks | template store; one `vintage_id` per page | paste numbers, scrape at request time |
| Platform | schema, pointers, serving | vintages, renders | parsers, citizen copy |

## Tests that must fail

These are the acceptance tests the first citizen publish must encode. Tests 4–8 and 10–11 need a real render of C1–C3, not a Python-only stub.

1. An observation without `citation_id` cannot be written or rendered.
2. An observation without `caveat_id` cannot be written or rendered.
3. A geography code without `geography_vintage` cannot be written or rendered.
4. Publish does not move `citizen_pointer` if any slice in the desk failed to render. The pointer write is atomic (see Refresh contract). Unchanged pages may be hard-linked; missing required templates still fail.
5. A citizen route cannot read a non-published vintage. Preview is not world-readable.
6. One citizen page cannot bind slots from two `vintage_id`s.
7. An API or chart payload cannot include a number without its citation card.
8. Default ordering of states is not a rank or a red/green performance map. Gate this on the **chart** spec: no measure-sort on the state/UT axis unless **that chart’s own caption** is a rank question and the template declares it; never a red–green diverging colour scale. Trust checks that the declared caption really is a question about order — not that the page H1 was one.
9. A new vintage (and its render tree) must not duplicate bytes of a series or page whose payload checksum is unchanged. Reuse is a hard-link or the same content-addressed key; a second copy fails the test.
10. **Denomination integrity.** A rendered citizen figure whose canonical magnitude differs from the producer’s published magnitude fails the build. Worked fail: `0.35 Cr` for a `3526840` ₹ crore figure. The citizen string is produced from `value × denomination` via one formatter; peak-driven concept scaling is gone.
11. **Published zero is not a gap.** A published zero (`status: value`, `value: 0`) and a gap (`unknown` / `withheld`) are verbally and visually distinct. A gap is never plotted as numeric zero; the citizen phrase for a gap is **not published**.

Do not add a framework that serves a producer fetch at request time, or that regenerates live citizen routes in place.
