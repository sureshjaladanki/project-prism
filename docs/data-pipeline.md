# Data pipeline

How official bytes become an immutable **data vintage**. Two stages, one batch machine, two owners.

Ingest Engineer lands the producer’s table. Pipeline Engineer maps that table into the portrait schema. They must not be collapsed into one job: ingest does not write observations; pipeline does not fetch.

This is not citizen serving ([architectural-blueprint.md](architectural-blueprint.md)). Field lists: [data-contracts.md](data-contracts.md). Paths and tools: [repo-conventions.md](repo-conventions.md).

## Why two stages, one document

Ingest talks to producer websites and parsers. Vintage mapping talks to the schema, caveats, and geography frame. Different failure modes, different “must not” lists. One document so the handoff is visible; two personas so neither job absorbs the other.

```text
citation card + geography frame
        │
        ▼
Stage 1  Ingest     raw artifact → derived table → lineage + source_changed
        │           stop at the producer’s table
        ▼
        Methodologist caveat note (not a pipeline step; a required input)
        │
        ▼
Stage 2  Vintage    derived + lineage + caveat + geography → new data vintage
        │
        ▼
        CMS render + Platform publish   (architecture, not this file)
```

## Stage 1 — Ingest

Turn a **citation card** into:

1. the producer’s file, stored as retrieved
2. a tidy table that still means what the producer meant
3. a lineage record another run can check
4. a `source_changed` signal the refresh contract can use

Stop at the producer’s table. Templates and copy are not ingested from ministry sites. This is not a live scrape at request time.

### Preconditions

Do not fetch until all of these exist:

```text
citation_card:      Source Librarian card (producer, series, id, url, licence)
source_class:       Charter Editor allow (surveys, censuses, administrative
                    series, budget figures — official statistical systems)
geography_frame:    Geography Steward, if the artifact is not all-India
                    with no sub-national rows
```

No citation card → no retrieve. A news write-up, NITI scorecard, private poll, or international secondary database is not a card Ingest may honour even if it quotes government figures. An official government host of the named dependency (`data.gov.in`, a line ministry, NITI as a host of that table) is in when the citation card names the producing office; producing office first preference.

If the URL requires a login wall, stop. If the producer’s terms forbid the pull, stop.

### What may be retrieved

The named data dependency, from official government agencies that can source it: PDF, spreadsheet, CSV, SDMX, or an official bulk/export. Prefer the producing office’s own release. Another government office is allowed when it supplies that dependency.

Dashboards are allowed only as a **scripted retrieve of a durable official export**, with the same lineage as a file. They are not a way to fill a chart when a citizen opens a page.

Economic Survey narrative, press releases, and ministry “achievements” pages are not artifacts. If they reprint a table, the librarian must cite the producing series; Ingest fetches that series.

### Layout under `data/`

Names include producer, series id, and the producer’s vintage (the reference period / release the librarian named). Paths use `/`. `data/` is gitignored except `.gitkeep`.

```text
data/
  raw/{producer}/{series_id}/{source_vintage}/{retrieved_at}/
      artifact          original bytes (keep the producer’s filename / suffix)
      headers.json      URL, HTTP status, content-type, as retrieved
  derived/{producer}/{series_id}/{source_vintage}/
      table.csv         tidy table (producer meaning; CSV until a named format change)
  lineage/{producer}/{series_id}/{source_vintage}/
      lineage.json      latest retrieve + checksum + parser + flags
```

- **Raw is kept.** A derived CSV does not replace the PDF.
- A new retrieve writes a **new** `{retrieved_at}` directory. Previous raw directories stay.
- `derived/` holds the current successful parse for that `source_vintage`. Previous derived bytes belong in lineage history if the parse must be compared; do not silently overwrite without a checksum note in `lineage.json`.
- Do not invent other top-level folders for ingest.

`{retrieved_at}` is UTC, `YYYYMMDDThhmmssZ`. `{source_vintage}` is the librarian’s reference period, then release date if needed to disambiguate — not the retrieve clock.

### Retrieve

Same script every time. New retrieve date. No hand downloads as the source of record.

```text
1. Read the citation card (url, producer, series, id).
2. Fetch the bytes. Store under data/raw/.../{retrieved_at}/.
3. Checksum the raw artifact.
4. Compare to the last retrieve for that producer/series/source_vintage.
5. Parse to derived only from those bytes. Do not mix files from two retrieves.
6. Write lineage.json. Emit source_changed.
```

Delayed stays delayed. Withdrawn stays withdrawn. Do not substitute last year’s file to keep the job green.

### Derived table

Tidy, still the producer’s definitions. No new concept, unit, or total that is not in the artifact.

- Every derived column maps to a cell, table, or field in the artifact.
- Blanks, withheld cells, and footnotes that say “not available” stay null / flagged. Do not impute, smooth, or carry forward.
- Do not recode geography. Store the producer’s names and codes as published. Geography Steward’s frame is applied later by Pipeline.
- If the PDF is ambiguous (unit, footnote, scanned page, pagination, totals that do not add up), **stop**. Flag Methodologist. Do not guess.

Budget estimates, revised estimates, and actuals stay distinct columns or rows — never collapsed. Survey vs census vs administrative stay distinct.

### Lineage record

Written to `lineage.json`. This is the ingest output Stage 2 consumes.

```text
raw_path:
derived_path:
checksum:           (of the raw artifact)
retrieved_at:
parser:             (name + version)
citation_id:        (librarian card this retrieve bound)
row_count:
nulls:              (where the source had blanks / withheld)
source_changed:     yes | no | first_retrieve
lineage_ok:         yes | no
flags:              (pagination errors, scanned pages, mismatched totals,
                     terms/login stop, ambiguous unit)
```

`lineage_ok: no` means Pipeline must not map that retrieve into value observations. Keep the previous good derived table in place. Do not “fix up” a changed file so the old parse still matches. A **named hole** on the slice refresh contract is the exception for vintage completeness: the series stays listed as unknown / not a table (`lineage_ok: no`); it does not fail the vintage. Any other `lineage_ok: no` fails that series and completeness.

A pipeline run report (what ran, changed, failed) is not this file. That belongs at `logs/{run_id}/report.json`.

### `source_changed`

Refresh trigger consumed by Platform’s contract.

| Result | Meaning |
|--------|---------|
| `first_retrieve` | no prior checksum |
| `yes` | raw checksum differs from last retrieve |
| `no` | same bytes |

A later retrieve of the same URL that returns different bytes is a change, even if the filename did not. Do not rewrite the new file to match the old parse.

Checksum of the raw artifact is the signal. Derived-table diffs are diagnostics, not the trigger.

### Parser version

The parser is part of lineage. Changing how a table is read is a new `parser` version. Re-run retrieve or re-parse from **kept raw**; do not edit derived cells by hand.

If a parser change would alter numbers without a source change, Pipeline still writes a **new data vintage**. Ingest reports the new parser on the lineage record.

### Ingest must not

- choose which series is better
- fill holes or last-year stand-ins
- drop raw once derived exists
- map rows into the portrait observation schema
- attach Methodologist caveats (it only preserves producer footnotes as flags/nulls)
- recode districts across boundary changes
- serve a citizen page from `data/`
- scrape at request time for a chart

## Stage 2 — Data vintage

Map landed tables into a new **data vintage**: observations, citations, geography, and caveats as of one run. Schema: [data-contracts.md](data-contracts.md).

Pipeline reads derived tables and lineage. It does not fetch PDFs, edit an old vintage, or publish.

```text
1. Read derived_path + checksum + lineage_ok for each series in the run.
2. If lineage_ok is no: do not write value observations. A named hole still
   lists the series (unknown / not a table) and does not fail completeness.
   Any other lineage_ok: no fails that series and vintage completeness.
3. Bind citation, caveat note, and geography vintage (code + geography_vintage).
4. Write observations. Fail the series (and the vintage completeness) if
   citation_id, caveat_id, or geography.geography_vintage is missing.
5. Payload-checksum each series. If it matches the previous vintage, hard-link
   (or reuse the CAS key). Do not copy bytes.
6. Always write a new manifest.json. Assign vintage_id. Never overwrite
   an existing vintage directory.
7. Write logs/{run_id}/report.json: what ran, changed, failed, reused.
```

- A vintage is immutable once written. Refresh means a **new** id.
- Unchanged series are not recopied. Record `reused: yes | no` per series in `manifest.json` and in the run report.
- Two official series that disagree stay two observations. Do not pick a winner.
- Delayed or withdrawn stays delayed or withdrawn. Do not backfill from last year.
- Idempotent replay: same inputs, same vintage payload.
- A failed vintage is retained for diagnosis. It is never the citizen pointer.

`vintage_id` rule, triggers, and when the citizen pointer may move: [architectural-blueprint.md](architectural-blueprint.md).

## Handoff

```text
Methodologist     opens derived_path; trusts it is the producer’s table
Pipeline          reads derived_path + checksum; sees source_changed
Platform          uses source_changed as a refresh trigger
CMS               reads exactly one complete vintage_id; never this pipeline’s
                  derived CSV
```

If `flags` include ambiguity, Methodologist goes next — not Pipeline guessing a unit.

## Done when

A second retrieve of the same card is the same script, a new `{retrieved_at}`, a comparable checksum, and a lineage record Pipeline can trust without opening the PDF. A later vintage run can rebuild from `data/` without guessing, and CMS can render against that vintage.
