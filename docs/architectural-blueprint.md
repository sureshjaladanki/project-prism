# Architectural blueprint

The machine the portrait runs on. Templates plus a data vintage in, a citizen page out. This is the contract and the data model. Languages and frameworks are in [repo-conventions.md](repo-conventions.md).

What the product is: [product.md](product.md). How official files land in `data/`: [ingestion-blueprint.md](ingestion-blueprint.md). This document does not specify parsers.

## What this is

A civic **CMS**. A page is `template + vintage → page`. Same inputs, same page. Citizen-view is a pointer at one complete published vintage.

It is not a folder of hand-built pages. It is not a live scrape of ministry sites. Request-time fetching of a producer website is not serving.

## Terms

- **Template** — Portrait copy and chart spec, with slots that only accept cited observations.
- **Observation** — one official figure (or an explicit hole) with its citation, geography, and caveat attached.
- **Data vintage** — an immutable snapshot of observations, citations, geography, and caveats after one pipeline run. The page is true as of that vintage.
- **Render** — bind a template to a vintage and write the page.
- **Publish** — move the citizen-view pointer to a vintage whose render finished.
- **Refresh** — ingest → new vintage (reuse unchanged series) → re-render what changed → publish. Old vintages stay as written.

## Components

Ownership follows [team.md](team.md). Each box is a boundary, not a repo folder beyond `src/` when a milestone needs code.

```text
citation card (Source Librarian)
geography frame (Geography Steward)
        │
        ▼
Ingest          lands the official artifact → data/  (see ingestion blueprint)
        │
        ▼
Methodologist   caveat note (definition, breaks, lags, disagreement)
        │
        ▼
Pipeline        maps derived tables → a new data vintage (immutable)
        │
        ▼
CMS             render(template, vintage) → preview | citizen page
        │
        ▼
Platform        store, pointers, atomic publish, serving
        │
        ▼
Trust Auditor   pass / block anything a citizen will see
```

| Component | Writes | Reads | Must not |
|-----------|--------|-------|----------|
| Ingest | raw artifact, derived table, lineage, `source_changed` | citation card | portrait schema, citizen pages |
| Pipeline | a **new** data vintage | derived table, lineage, caveat notes, geography vintage | fetch PDFs, edit an old vintage, publish |
| CMS | rendered pages, preview | template store, **one** vintage | paste numbers, scrape at request time |
| Platform | schema, pointers, serving | vintages, renders | parsers, citizen copy |

`src/` holds application code. `tests/` holds tests. `data/` holds artifacts, vintages, and renders. `logs/` holds run output, including the pipeline report. Generated pages are outputs, not the source of truth. Do not add top-level folders for the pipeline or the CMS. Paths: [repo-conventions.md](repo-conventions.md).

## Data model

Every number a citizen can see is an observation inside a data vintage. A float with no citation card is not stored and not served.

### Identity rules

- A **geography code without a geography vintage is a bug.** Store them as a pair.
- A **data vintage is immutable** once written. Refresh writes a new id.
- **Unchanged series are not recopied.** A new vintage directory lists every series; files whose payload checksum matches the previous vintage are hard-linked (or the same content-addressed key). Duplicating those bytes is a bug. `manifest.json` is always new.
- **Release date is not the reference period.** Both are stored; charts use the reference period.
- **Status is first-class.** Unknown, withheld, delayed, withdrawn, not comparable, and series break are stored as status, not missing columns that a chart skips.

### Series

The producer’s series, not a nickname.

```text
series_id:          (stable in this platform)
producer:           (office that publishes it)
name:               (name the producer uses)
frequency:
licence:            (from the citation card)
```

### Citation

Source Librarian’s card. Every observation points at one.

```text
citation_id:
producer:
series:
id:                 (round, statement, table, or dataset id)
reference_period:
release_date:
url:
geography_as_published:
frequency:
licence:
next_release:       (date or unknown)
caveat_one_line:
```

### Geography vintage

The map as of the series, not today’s map pasted onto an old table. Geography Steward owns the contents.

```text
geography_vintage:  (year / date the boundaries refer to)
code_system:        LGD | census | producer-specific | none
frame:              Union | state | UT | district | other
units_included:     (code + English name, each with geography_vintage)
units_missing:      (named, not implied)
breaks:             (splits, merges, renames that hit this frame)
crosswalk:          (path, or none — do not recode)
```

### Caveat note

Methodologist’s note. Every series in a vintage carries one.

```text
caveat_id:
concept:
unit:
population:
reference_period:
producer_definition:
comparable_from:
breaks:
lags:
disagrees_with:     (other official series, or none)
do_not:             (joins, ranks, or charts that would lie)
```

### Observation

```text
observation_id:
series_id:
citation_id:        (required)
caveat_id:          (required)
geography:          { code, geography_vintage, code_system }
reference_period:
value:              (number, or null)
unit:
status:             value | unknown | withheld | delayed | withdrawn
                    | not_comparable | series_break
lineage:            { raw_path, derived_path, checksum }
```

If `citation_id`, `caveat_id`, or `geography.geography_vintage` is missing, the write fails. Do not drop the field so a chart can render.

Two official series that disagree are two observations, each with its own citation and caveat. The model does not pick a winner.

### Data vintage

```text
vintage_id:         (see refresh contract; never reused)
created_at:
trigger:            schedule | source_change | on_demand
input_manifest:     written as manifest.json (human-readable) and hashed
                    into vintage_id. Per series: producer, series_id,
                    source_vintage, raw checksum, parser version,
                    lineage_ok, geography vintage, payload checksum,
                    reused: yes | no; plus caveat ids and mapper version.
                    The 12-hex is identity, not the audit trail.
observations:       one Parquet file per series_id; unchanged files are
                    hard-linked / CAS-reused, never byte-copied
citations:
geography_vintages:
caveat_notes:       per series, same reuse rule as observations
completeness:       complete | failed
```

A failed vintage is retained for diagnosis. It is never the citizen pointer. Do not recopy the audit trail into `lineage.json`; ingest lineage stays per retrieve. The pipeline’s “what ran, changed, failed” record is `logs/{run_id}/report.json`. Do not write a full-portrait snapshot that duplicates unchanged series.

### Template

Portrait Editor authors copy and chart spec. Slots bind to selectors (series + geography + reference period), not to numerals typed into the page.

```text
template_id:
slots:              (each: selector → observation in the bound vintage)
copy:
chart_spec:         (breaks stay breaks; no default rank sort)
```

If the vintage has no matching observation, the slot renders as unknown / not published — not as a remembered figure.

### Pointers

```text
citizen_pointer:    vintage_id of the last complete published vintage
preview_pointer:    vintage_id for unpublished preview (never an alias of citizen)
retained_vintages:  prior published vintage_ids stay addressable
```

Preview and citizen-view are different pointers. A citizen route reads only `citizen_pointer`.

The pointer write itself is atomic: local disk uses write-to-temp then rename; object storage uses a conditional PUT (`If-Match` / ETag) on a single current key and a publish lock so two publishers cannot interleave. Order: complete render for that `vintage_id` → nine tests pass → flip `citizen_pointer` last. A bare overwrite of a JSON file is not atomic publish.

## Refresh contract

```text
vintage_id_rule:    "dv-" + run_date_utc (YYYYMMDD) + "-" + 12-hex of
                    manifest.json. Directory with that id is never overwritten.
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline (data vintage) → cms render → publish pointer
atomic_publish:     yes   (citizen-view moves only when render of the new vintage is complete)
on_fail:            keep previous published vintage; do not serve a partial
retain_prior:       yes   (prior vintages stay addressable)
```

- **schedule** — a named cadence once operations exist; per series it follows the librarian’s `next_release`, not a hidden global clock.
- **source_change** — Ingest reports a checksum different from the last retrieve (`source_changed: yes`).
- **on_demand** — an editor asks for a run.

Request-time scraping is not a trigger. Incremental regeneration of live citizen routes (ISR, per-path `revalidate`, stale-while-revalidate of production) is not a trigger and is not publish. Refresh writes a new vintage, reuses unchanged series and pages (hard-link / CAS), re-renders only what changed, then moves the pointer.

On fail at any step: do not move `citizen_pointer`. Do not mix observations from vintage A and vintage B on one citizen page. A torn mix is a bug.

## Serving

Logical routes and stores. Frameworks: [repo-conventions.md](repo-conventions.md).

**Stores Pipeline and CMS must use**

- **Artifact store** — `data/` as laid out in the ingestion blueprint. Pipeline reads derived tables and lineage; it does not fetch.
- **Vintage store** — one directory per `vintage_id`, immutable. Per-series Parquet + JSON; unchanged series hard-linked into `data/cas/{sha256}` (object storage: same key). Pipeline writes; CMS reads exactly one id per render. A full copy of an unchanged series is a bug.
- **Render store** — one static tree per `vintage_id`. Unchanged pages hard-linked; only templates whose slot inputs changed are rebuilt. Citizen-view does not read it until the pointer flips.
- **Template store** — templates and slot bindings in git. CMS reads; Portrait writes.
- **Pointer store** — `citizen_pointer` and `preview_pointer`, written atomically as above. Platform writes on publish; CMS reads on serve.

**Citizen-view**

- Always the published pointer.
- Default order of states and UTs is alphabetical by official English name, or a documented geographic order. Ranking is not the default.
- Definition, unit, geography vintage, and data vintage appear in the same view as the number. A tooltip is not the only place they live.
- Charts and any observation API take citation cards with the number. Nothing serves a bare float.
- `unknown`, `not_comparable`, and `series_break` stay visible. Do not smooth them into a continuous line.

**Preview**

- Unpublished. Never aliases `citizen_pointer`.
- Same render function as citizen-view. Only the pointer differs.
- Not world-readable. Private prefix (or equivalent), `noindex`, signed URL (or later authenticated access). A different public URL is not isolation.

**Retained vintages**

- Addressable when someone needs to see what the page said as of an older published vintage.
- Overwriting a published vintage in place is a bug.

## Tests that must fail

These are the acceptance tests the first citizen publish must encode. Tests 4–8 need a real render of C1, not a Python-only stub.

1. An observation without `citation_id` cannot be written or rendered.
2. An observation without `caveat_id` cannot be written or rendered.
3. A geography code without `geography_vintage` cannot be written or rendered.
4. Publish does not move `citizen_pointer` if any required template failed to render for that vintage. The pointer write is atomic (see Pointers). Unchanged pages may be hard-linked; missing required templates still fail.
5. A citizen route cannot read a non-published vintage. Preview is not world-readable.
6. One citizen page cannot bind slots from two `vintage_id`s.
7. An API or chart payload cannot include a number without its citation card.
8. Default ordering of states is not a rank or a red/green performance map. Gate this on the chart spec (no measure-sort on the state/UT axis; no red–green diverging colour scale), not only a screenshot.
9. A new vintage (and its render tree) must not duplicate bytes of a series or page whose payload checksum is unchanged. Reuse is a hard-link or the same content-addressed key; a second copy fails the test.

Tooling that implements this contract is in [repo-conventions.md](repo-conventions.md). Code goes under `src/` and `tests/`. Do not add a framework that serves a producer fetch at request time, or that regenerates live citizen routes in place.
