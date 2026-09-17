# C1 refresh and serving contract

Persona: Platform Engineer. Slice: **C1**. Locked inputs: [`c1-citation-cards.md`](c1-citation-cards.md), [`c1-geography-frame.md`](c1-geography-frame.md), [`c1-method-notes.md`](c1-method-notes.md).

Schema, pointers, and stores live in `src/prism/`. This note is the human contract. Pipeline, Ingest, and CMS must not invent fields around it.

Citizen pages, MoSPI fetches, and Portrait copy wait until this contract is in git-shaped code.

---

## Refresh contract

```text
vintage_id_rule:    "dv-" + run_date_utc (YYYYMMDD) + "-" + 12-hex of
                    InputManifest JSON (created_at, trigger, per-series
                    entries). Directory with that id is never overwritten.
                    vintage_id is assigned from the input manifest, then
                    written into manifest.json; the 12-hex is identity,
                    not the audit trail.
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline (data vintage) → cms render → publish pointer
atomic_publish:     yes   (citizen-view moves only when render of the new vintage is complete)
on_fail:            keep previous published vintage; do not serve a partial
retain_prior:       yes   (prior vintages stay addressable)
```

- **schedule** — GitHub Actions cron later; per series it follows `next_release`, not a hidden global clock. C1 Cards 1–3: **12 October 2026**. Card 4: **unknown** (not on the schedule).
- **source_change** — Ingest `lineage.json` has `source_changed: yes` or `first_retrieve` (checksum of the raw artifact vs last retrieve). `source_changed: no` is not this trigger. Derived-table diffs are diagnostics, not the trigger.
- **on_demand** — an editor asks; same CLI later, not a request-time scrape.

Request-time producer fetch, Next.js ISR, and in-place regeneration of live citizen routes are not triggers and are not publish.

On fail at ingest, vintage write, render, or tests: do not move `data/pointers/citizen`. A failed vintage is retained for diagnosis and is never the citizen pointer. Unchanged series are hard-linked from `data/cas/{sha256}`; `manifest.json` is always new.

---

## C1 series ids (stable)

Producer slug in `data/` paths: `mospi`. Producer name on the series: National Statistics Office, Price Statistics Division, MoSPI.

| Card | `series_id` | Frame | `next_release` | Locked `source_vintage` |
|------|-------------|-------|----------------|-------------------------|
| 1 | `cpi-general-base-2024` | `c1-frame-a` | 2026-10-12 | `2026-08` |
| 2 | `cpi-cfpi-base-2024` | `c1-frame-a` | 2026-10-12 | `2026-08` |
| 3 | `cpi-division-group-base-2024` | `c1-frame-a` | 2026-10-12 | `2026-08` |
| 4 | `cpi-back-series-linked-base-2024` | `c1-frame-b` | unknown | `2013-2024-linked` |

Locked citation / caveat ids (August 2026 monthly cards; Card 4 is the linked file, not that press date):

| Card | `citation_id` | `caveat_id` |
|------|---------------|-------------|
| 1 | `cite-c1-cpi-general-base-2024-2026-08` | `caveat-c1-cpi-general-base-2024` |
| 2 | `cite-c1-cpi-cfpi-base-2024-2026-08` | `caveat-c1-cpi-cfpi-base-2024` |
| 3 | `cite-c1-cpi-division-group-base-2024-2026-08` | `caveat-c1-cpi-division-group-base-2024` |
| 4 | `cite-c1-cpi-back-series-linked-base-2024` | `caveat-c1-cpi-back-series-linked-base-2024` |

A later monthly retrieve gets a new `citation_id` (new `reference_period` / `release_date`). `series_id` does not change. Card 4 `release_date` is `unknown` — do not borrow 14 September 2026.

A complete C1 vintage **lists all four series**. Unchanged series are reused (`reused: yes`) via cas hard-link, not omitted and not byte-copied.

Constants: `src/prism/refresh.py`.

---

## Stores

```text
data/cas/{sha256}                          write-once bytes
data/vintages/{vintage_id}/manifest.json   always new
data/vintages/{vintage_id}/series/{series_id}/
    observations.parquet
    citation.json
    caveat.json
    geography.json
data/renders/{vintage_id}/                 CMS write; not citizen-view until the pointer flips
data/renders/{vintage_id}/COMPLETE         render-complete marker Platform publish requires
data/pointers/citizen                      vintage_id; atomic temp+rename
data/pointers/preview                      vintage_id; never an alias of citizen
data/raw|derived|lineage/                  ingest (see ingestion blueprint)
logs/{run_id}/report.json                  pipeline report; not lineage.json
```

Payload checksum (series reuse key): SHA-256 of the SHA-256 of observations bytes, citation JSON, caveat JSON, geography JSON, in that order.

Parquet columns (Pipeline writes; names are schema fields, flattened): `observation_id`, `series_id`, `citation_id`, `caveat_id`, `geography_code`, `geography_vintage`, `geography_code_system`, `sector`, `reference_period`, `value`, `unit`, `status`, `lineage_raw_path`, `lineage_derived_path`, `lineage_checksum`.

Sector is a published producer dimension (`Rural` / `Urban` / `Combined` on C1), not geography. `00` All India is a published unit. Geography vintage is `2024` on both C1 frames. `frame_id` distinguishes Frame A from Frame B.

UTC in stores. Display release dates in `Asia/Kolkata` (`prism.refresh.STORE_TIMEZONE`, `DISPLAY_TIMEZONE`). Do not store Kolkata wall time as naive UTC.

---

## Publish / serving

- Pointer write: temp file in `data/pointers/`, then `os.replace`. Publish lock is `data/pointers/.publish.lock` (mkdir). Object-storage If-Match comes later.
- Order: complete render for that `vintage_id` (`COMPLETE` marker) → nine tests pass → flip `citizen_pointer` last.
- `publish_citizen(..., render_complete=True, contract_tests_passed=True)` is the only citizen flip. Either flag false, or `completeness: failed`, keeps the previous citizen pointer.
- Preview is a different file. A citizen route reads only `citizen`. Preview is unpublished: private prefix, `noindex`, signed URL later. A second public URL is not isolation.
- DuckDB at render reads **exactly one** `vintage_id`. Do not join two vintages onto one page.
- Templates bind `SlotSelector` (series + geography pair + sector + reference period + unit + status) to a `ServedObservation` (observation + citation card + caveat). If nothing matches: unknown / not published — not a remembered figure.
- Charts and any observation API take `ServedObservation`. Nothing serves a bare float.
- Default State/UT order: alphabetical by official English `State Name` as published. No rank sort. No red–green diverging default (CMS Engineer gates Vega-Lite).
- Definition, unit, geography vintage, and data vintage belong in the same view as the number (CMS / Portrait). Platform only forbids serving a number without its cards.

Tests 4–8 in the architectural blueprint need a real Astro render of C1. They are skipped until CMS Engineer renders. Tests 1–3 (write) and test 9 (series cas / hard-link) are encoded now.

---

## Ingest Engineer — remaining Platform preconditions

`citation_card`, `source_class: allow`, and `geography_frame` already exist. Do not fetch until this contract is the store Ingest lands into.

Use these path segments (POSIX):

```text
data/raw/mospi/{series_id}/{source_vintage}/{retrieved_at}/
data/derived/mospi/{series_id}/{source_vintage}/table.csv
data/lineage/mospi/{series_id}/{source_vintage}/lineage.json
```

`retrieved_at` is UTC `YYYYMMDDThhmmssZ`. Stop at the producer’s table. Do not write observations, vintages, or pointers.

`lineage.json` must validate as `prism.schema.LineageRecord`, including `source_changed: yes | no | first_retrieve` and `lineage_ok: yes | no`. Refresh treats `yes` and `first_retrieve` as `source_change`. `lineage_ok: no` means Pipeline must not build a vintage from that retrieve.

Licence: GSDD 2026 Category A + MoSPI copyright (attribution; not CC-BY). Terms do not forbid the pull.

---

## Wait

**Ingest** may fetch after this contract is in git. **Pipeline** writes vintages with these types and must not invent fields. **Portrait** and **CMS Engineer** wait for a vintage and this serving contract; do not scaffold Astro or write citizen copy in this pass. **Trust Auditor** waits until a citizen can see a page.

Do not start C2–C20.
