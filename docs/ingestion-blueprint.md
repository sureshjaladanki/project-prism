# Ingestion blueprint

How an official artifact becomes files another agent can replay. The pull is scripted, the raw bytes are kept, the lineage is written down. Mapping those tables into a data vintage is Pipeline Engineer, specified in [architectural-blueprint.md](architectural-blueprint.md).

This is not how citizen pages are written. Templates and copy are not ingested from ministry sites. This is not a live scrape at request time.

## What ingest is for

Turn a **citation card** into:

1. the producer’s file, stored as retrieved
2. a tidy table that still means what the producer meant
3. a lineage record another run can check
4. a `source_changed` signal the refresh contract can use

Stop at the producer’s table.

## Preconditions

Do not fetch until all of these exist:

```text
citation_card:      Source Librarian card (producer, series, id, url, licence)
source_class:       Charter Editor allow (surveys, censuses, administrative
                    series, budget figures — official statistical systems)
geography_frame:    Geography Steward, if the artifact is not all-India
                    with no sub-national rows
```

No citation card → no retrieve. A news write-up, portal republish, NITI scorecard, private poll, or international secondary database is not a card Ingest may honour even if it quotes government figures.

If the URL requires a login wall, stop. If the producer’s terms forbid the pull, stop.

## What may be retrieved

The producing office’s own release: PDF, spreadsheet, CSV, SDMX, or an official bulk/export the office publishes.

Dashboards are allowed only as a **scripted retrieve of a durable official export**, with the same lineage as a file. They are not a way to fill a chart when a citizen opens a page.

Economic Survey narrative, press releases, and ministry “achievements” pages are not artifacts. If they reprint a table, the librarian must cite the producing series; Ingest fetches that series.

## Layout under `data/`

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

## Retrieve

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

## Derived table

Tidy, still the producer’s definitions. No new concept, unit, or total that is not in the artifact.

- Every derived column maps to a cell, table, or field in the artifact.
- Blanks, withheld cells, and footnotes that say “not available” stay null / flagged. Do not impute, smooth, or carry forward.
- Do not recode geography. Store the producer’s names and codes as published. Geography Steward’s frame is applied later by Pipeline.
- If the PDF is ambiguous (unit, footnote, scanned page, pagination, totals that do not add up), **stop**. Flag Methodologist. Do not guess.

Budget estimates, revised estimates, and actuals stay distinct columns or rows — never collapsed. Survey vs census vs administrative stay distinct.

## Lineage record

Written to `lineage.json`. This is the ingest output the next persona consumes.

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

`lineage_ok: no` means Pipeline must not build a vintage from this retrieve. Keep the previous good derived table in place. Do not “fix up” a changed file so the old parse still matches.

A pipeline run report (what ran, changed, failed) is not this file. That belongs at `logs/{run_id}/report.json`.

## `source_changed`

Refresh trigger consumed by Platform’s contract.

| Result | Meaning |
|--------|---------|
| `first_retrieve` | no prior checksum |
| `yes` | raw checksum differs from last retrieve |
| `no` | same bytes |

A later retrieve of the same URL that returns different bytes is a change, even if the filename did not. Do not rewrite the new file to match the old parse.

Checksum of the raw artifact is the signal. Derived-table diffs are diagnostics, not the trigger.

## Parser version

The parser is part of lineage. Changing how a table is read is a new `parser` version. Re-run retrieve or re-parse from **kept raw**; do not edit derived cells by hand.

If a parser change would alter numbers without a source change, Pipeline still writes a **new data vintage**. Ingest reports the new parser on the lineage record.

## Explicit non-goals

Ingest does not:

- choose which series is better
- fill holes or last-year stand-ins
- drop raw once derived exists
- map rows into the portrait observation schema
- attach Methodologist caveats (it only preserves producer footnotes as flags/nulls)
- recode districts across boundary changes
- serve a citizen page from `data/`
- scrape at request time for a chart

## Handoff

```text
Methodologist     opens derived_path; trusts it is the producer’s table
Pipeline          reads derived_path + checksum; sees source_changed
Platform          uses source_changed as a refresh trigger
```

If `flags` include ambiguity, Methodologist goes next — not Pipeline guessing a unit.

## Done when

A second retrieve of the same card is the same script, a new `{retrieved_at}`, a comparable checksum, and a lineage record Pipeline can trust without opening the PDF to see what happened.
