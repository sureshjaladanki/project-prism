# C2 refresh and serving contract

Persona: Platform Architect. Slice: **C2**. Locked inputs: [`c2-citation-cards.md`](c2-citation-cards.md), [`c2-geography-frame.md`](c2-geography-frame.md), [`c2-method-notes.md`](c2-method-notes.md).

Schema, pointers, and stores live in `src/prism/`. This note is the human contract. Pipeline, Ingest, and CMS must not invent fields around it. Vintage identity, triggers, atomic publish, and observation columns are the **same machine as C1** ([`c1-refresh-contract.md`](c1-refresh-contract.md)). C2 does not get a second web framework, ISR, or a request-time producer fetch.

Citizen C2 pages, ORGI/NHM fetches, and Content Editor copy wait until this contract is in git-shaped code (`src/prism/refresh.py`).

Do not mix C1 and C2 observations on one citizen page. A C1 vintage still lists the four CPI series only. A C2 vintage lists the five series below only. `data/pointers/citizen` stays on the published C1 vintage until Charter ships C2 (Trust + complete C2 render). Preview may point at a C2 vintage without moving citizen.

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

- **schedule** — GitHub Actions cron later; per series it follows `next_release`. **All five C2 series: unknown** (Census delayed; SRS 2025 date not on the 2024 products; no successor Technical Group report on the cards). There is no C2 calendar day on the clock until a librarian card names one. Do not invent a monthly tick from May 2026.
- **source_change** — Ingest `lineage.json` has `source_changed: yes` or `first_retrieve` (checksum of the raw artifact vs last retrieve). `source_changed: no` is not this trigger. Derived-table diffs are diagnostics, not the trigger.
- **on_demand** — an editor asks; same CLI later, not a request-time scrape.

Request-time producer fetch, Next.js ISR, and in-place regeneration of live citizen routes are not triggers and are not publish.

On fail at ingest, vintage write, render, or tests: do not move `data/pointers/citizen`. A failed vintage is retained for diagnosis and is never the citizen pointer. Unchanged series are hard-linked from `data/cas/{sha256}`; `manifest.json` is always new.

---

## C2 series ids (stable)

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| 1 | `census-2011-pca-sd` | `orgi` | `c2-frame-a` | `2011` | unknown | `2011` |
| 2 | `census-2011-a02-decadal` | `orgi` | `c2-frame-b` | `2011` | unknown | `2011` |
| 3 | `srs-bulletin-2024` | `orgi` | `c2-frame-c` | `2024` | unknown | `2024` |
| 4 | `srs-statistical-report-2024` | `orgi` | `c2-frame-d` | `2024` | unknown | `2024` |
| 5 | `ncp-projections-2011-2036-table8` | `ncp-mohfw` | `c2-frame-e` | `2019` | unknown | `2011-2036-table8` |

Locked citation / caveat ids (cards as of 18 September 2026):

| Card | `citation_id` | `caveat_id` |
|------|---------------|-------------|
| 1 | `cite-c2-census-2011-pca-sd` | `caveat-c2-census-2011-pca-sd` |
| 2 | `cite-c2-census-2011-a02-decadal` | `caveat-c2-census-2011-a02-decadal` |
| 3 | `cite-c2-srs-bulletin-2024` | `caveat-c2-srs-bulletin-2024` |
| 4 | `cite-c2-srs-statistical-report-2024` | `caveat-c2-srs-statistical-report-2024` |
| 5 | `cite-c2-ncp-projections-2011-2036-table8` | `caveat-c2-ncp-projections-2011-2036-table8` |

A later retrieve of the same census/SRS/projection file keeps `series_id`. A new Census headcount (when published) is a **new series or a new `citation_id` + `source_vintage`**, not a silent overwrite of `2011`. Do not borrow C1’s 14 September 2026 press date. Card 1–2 `release_date` on the citation is unknown where the librarian said the workbook has no printed release date — store `unknown`, not the NADA catalog date as Census day.

A complete **C2** vintage **lists all five series**. Unchanged series are reused (`reused: yes`) via cas hard-link, not omitted and not byte-copied. Do not require C1 series in a C2 vintage. Do not require C2 series in a C1 vintage.

Constants: `src/prism/refresh.py`.

---

## Stores

Same layout as C1. Producer path segments for C2:

```text
data/raw/orgi/{series_id}/{source_vintage}/{retrieved_at}/
data/derived/orgi/{series_id}/{source_vintage}/table.csv
data/lineage/orgi/{series_id}/{source_vintage}/lineage.json

data/raw/ncp-mohfw/{series_id}/{source_vintage}/{retrieved_at}/
data/derived/ncp-mohfw/{series_id}/{source_vintage}/table.csv
data/lineage/ncp-mohfw/{series_id}/{source_vintage}/lineage.json
```

`retrieved_at` is UTC `YYYYMMDDThhmmssZ`. Stop at the producer’s table. Do not write observations, vintages, or pointers in Ingest.

`lineage.json` must validate as `prism.schema.LineageRecord`, including `source_changed: yes | no | first_retrieve` and `lineage_ok: yes | no`. Refresh treats `yes` and `first_retrieve` as `source_change`. `lineage_ok: no` means Pipeline must not build a vintage from that retrieve.

Parquet columns stay the C1 schema. **Residence / TRU** (`Total` / `Rural` / `Urban`) uses the existing `sector` field — it is not geography. Frame E Table 8 has no TRU; store `sector` as the producer’s printed sex/total classifier if Pipeline maps one, not a fake Combined.

`geography_code` + `geography_vintage` are a pair. Frame A/B use Census `State` codes (`00`–`35`) with vintage `2011`. Frames C–E have `code_system: none` — store the printed stub as `geography_code` (stable slug from the printed name, not an LGD join) with vintages `2024` / `2019` as in the table above. Do not recode Frame A `01` onto Frame C `Jammu & Kashmir`.

Licence: ORGI / NADA all rights reserved, not CC-BY (Cards 1–4). Card 5: Government of India report; not stated as CC-BY. Terms on the named HTTP 200 downloads did not present a login wall on the citation-card check. If a later retrieve hits a login wall or a terms forbid, Ingest **stops**.

---

## Publish / serving

Unchanged from C1: temp+rename pointers; `COMPLETE` marker; nine tests; DuckDB reads **exactly one** `vintage_id`; `ServedObservation` only; no rank-sort default; definition, unit, geography vintage, and data vintage in the same view as the number.

C2-specific serving rules Platform forbids (UI/UX / Content Editor implement; tests fail a bare float either way):

- Do not serve Census 2011 `TOT_P` without the 1 March 2011 reference period and the delayed-census status.
- Do not serve a number that blends Cards 1–2, 3–4, and 5 into one “India today”.
- `unknown` / `delayed` / `not_comparable` / `series_break` stay first-class. Do not hide the Census hole.

A C2 template bind is a later CMS job. Tests 4–8 need a real Astro render of C2 and stay skipped until UI/UX Developer renders C2. Tests 1–3 (write) and test 9 (series cas / hard-link) apply to a C2 vintage the same way as C1, with `required_series_ids=C2_SERIES_IDS`.

---

## Ingest Engineer — remaining Platform preconditions

`citation_card`, `source_class: allow`, `geography_frame`, method notes, and this contract exist. Do not fetch until this contract is the store Ingest lands into.

Keep Card 1 at `Level` in {`India`, `STATE`} only. Do not pull DISTRICT PCA, A-01, NPR, or electoral rolls. Card 4 PDF is the Statistical Report; do not parse parked NSS Natural Division tables into the derived table. Card 5 is TABLE-8 only — not Table 11, not Appendix 1.

If Card 5 pages are image-only and the producer’s Table 8 cells cannot be read without guessing, **stop** (`lineage_ok: no`) and flag Methodologist — do not OCR a blended stock.

---

## Wait

**Ingest** may fetch after this contract is in git. **Pipeline** writes a C2 vintage with these types and must not invent fields or recode geography. **Content Editor** and **UI/UX Developer** wait for a C2 vintage and this serving contract; do not scaffold a C2 Astro template in this pass. **Trust Auditor** waits until a citizen can see a C2 page.

Do not move `citizen_pointer` in this pass. Do not start C3–C20.
