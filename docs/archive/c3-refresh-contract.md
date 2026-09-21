# C3 refresh and serving contract

Persona: Platform Architect. Slice: **C3**. Locked inputs: [`c3-citation-cards.md`](c3-citation-cards.md), [`c3-geography-frame.md`](c3-geography-frame.md), [`c3-method-notes.md`](c3-method-notes.md).

Schema, pointers, and stores live in `src/prism/`. This note is the human contract. Pipeline, Ingest, and CMS must not invent fields around it. Vintage identity, triggers, atomic publish, and observation columns are the **same machine as C1** ([`c1-refresh-contract.md`](c1-refresh-contract.md)). C3 does not get a second web framework, ISR, or a request-time producer fetch.

Citizen C3 pages and Content Editor copy wait for a complete C3 vintage, CMS render, and Trust. Completeness no longer waits on an FRBM grid: Card 8 is a named hole. Ingest may land Cards 1–7 and 9–11 now.

Do not mix C1, C2, and C3 observations on one citizen page. A C3 vintage lists the eleven series below only. `data/pointers/citizen` stays on the published C1 vintage until Charter ships C3 (Trust + complete C3 render). Preview may point at a C3 vintage without moving citizen. Do not unblock C2 ingest from this file.

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

- **schedule** — GitHub Actions cron later; per series it follows `next_release`. **All eleven C3 series: unknown** (Budget 2027-28 not dated; CGA ARC HTML had no dated month list; Finance Accounts 2025-26 not on the dropdown). There is no C3 calendar day on the clock until a librarian card names one. Do not invent 1 February from the 2026 laying, and do not invent a CGA month from July 2026.
- **source_change** — Ingest `lineage.json` has `source_changed: yes` or `first_retrieve` (checksum of the raw artifact vs last retrieve). `source_changed: no` is not this trigger. Derived-table diffs are diagnostics, not the trigger.
- **on_demand** — an editor asks; same CLI later, not a request-time scrape.

Request-time producer fetch, Next.js ISR, and in-place regeneration of live citizen routes are not triggers and are not publish.

On fail at ingest, vintage write, render, or tests: do not move `data/pointers/citizen`. A failed vintage is retained for diagnosis and is never the citizen pointer. Unchanged series are hard-linked from `data/cas/{sha256}`; `manifest.json` is always new.

---

## C3 series ids (stable)

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| 1 | `budget-2026-27-tax-revenue` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 2 | `budget-2026-27-non-tax-revenue` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 3 | `budget-2026-27-capital-receipts` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 4 | `budget-2026-27-annex1-trends-receipts` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 5 | `budget-2026-27-expenditure-stat1` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 6 | `budget-2026-27-deficit-statistics` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 7 | `budget-2026-27-liabilities` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 8 | `budget-2026-27-frbm-statements` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 9 | `budget-2026-27-afs` | `mof-budget` | `c3-frame-a` | `2026` | unknown | `2026-27` |
| 10 | `cga-monthly-glance-2026-07` | `cga` | `c3-frame-b` | `2026` | unknown | `2026-07` |
| 11 | `cga-finance-accounts-2024-25-stat1` | `cga` | `c3-frame-c` | `2024` | unknown | `2024-25` |

Locked citation / caveat ids (cards as of 18 September 2026):

| Card | `citation_id` | `caveat_id` |
|------|---------------|-------------|
| 1 | `cite-c3-budget-2026-27-tax-revenue` | `caveat-c3-budget-2026-27-tax-revenue` |
| 2 | `cite-c3-budget-2026-27-non-tax-revenue` | `caveat-c3-budget-2026-27-non-tax-revenue` |
| 3 | `cite-c3-budget-2026-27-capital-receipts` | `caveat-c3-budget-2026-27-capital-receipts` |
| 4 | `cite-c3-budget-2026-27-annex1-trends-receipts` | `caveat-c3-budget-2026-27-annex1-trends-receipts` |
| 5 | `cite-c3-budget-2026-27-expenditure-stat1` | `caveat-c3-budget-2026-27-expenditure-stat1` |
| 6 | `cite-c3-budget-2026-27-deficit-statistics` | `caveat-c3-budget-2026-27-deficit-statistics` |
| 7 | `cite-c3-budget-2026-27-liabilities` | `caveat-c3-budget-2026-27-liabilities` |
| 8 | `cite-c3-budget-2026-27-frbm-statements` | `caveat-c3-budget-2026-27-frbm-statements` |
| 9 | `cite-c3-budget-2026-27-afs` | `caveat-c3-budget-2026-27-afs` |
| 10 | `cite-c3-cga-monthly-glance-2026-07` | `caveat-c3-cga-monthly-glance-2026-07` |
| 11 | `cite-c3-cga-finance-accounts-2024-25-stat1` | `caveat-c3-cga-finance-accounts-2024-25-stat1` |

A later retrieve of the same Budget 2026-27 PDF keeps `series_id`. Union Budget 2027-28 is a **new `source_vintage` / `citation_id`**, not an overwrite of `2026-27`. A later CGA month is a new `source_vintage` (not a silent overwrite of `2026-07`). Do not borrow C1’s 14 September 2026 press date.

A complete **C3** vintage **lists all eleven series**. Unchanged series are reused (`reused: yes`) via cas hard-link, not omitted and not byte-copied. Do not require C1 or C2 series in a C3 vintage.

**Named hole — Card 8** (`budget-2026-27-frbm-statements`): the FRBM statutory packet is not a reconstructable receipts/expenditure/deficit/debt grid. A complete C3 vintage **may** have Card 8 `lineage_ok: no`. It stays listed. Observations are `status: unknown`, value null, still cited — not a fake table, not omitted. Cards 1–7 and 9–11 (`C3_LINEAGE_REQUIRED_SERIES_IDS`) must be `lineage_ok: yes`. Omitting Card 8, or `lineage_ok: no` on an H1 series, cannot be `completeness: complete`. If Card 8 later becomes a table, `lineage_ok: yes` is still complete.

Constants: `src/prism/refresh.py` (`C3_NAMED_HOLE_SERIES_IDS`, `C3_LINEAGE_REQUIRED_SERIES_IDS`).

---

## Stores

Same layout as C1. Producer path segments for C3:

```text
data/raw/mof-budget/{series_id}/{source_vintage}/{retrieved_at}/
data/derived/mof-budget/{series_id}/{source_vintage}/table.csv
data/lineage/mof-budget/{series_id}/{source_vintage}/lineage.json

data/raw/cga/{series_id}/{source_vintage}/{retrieved_at}/
data/derived/cga/{series_id}/{source_vintage}/table.csv
data/lineage/cga/{series_id}/{source_vintage}/lineage.json
```

`retrieved_at` is UTC `YYYYMMDDThhmmssZ`. Stop at the producer’s table. Do not write observations, vintages, or pointers in Ingest.

`lineage.json` must validate as `prism.schema.LineageRecord`, including `source_changed: yes | no | first_retrieve` and `lineage_ok: yes | no`. Refresh treats `yes` and `first_retrieve` as `source_change`. `lineage_ok: no` means Pipeline must not map that retrieve into value observations. Card 8 is the C3 named hole: `lineage_ok: no` does not fail vintage completeness. Any other C3 series with `lineage_ok: no` does.

Parquet columns stay the C1 schema. BE / RE / Actuals / monthly “upto” uses the existing `status` (and `reference_period`) fields — they are not geography.

`geography_code` + `geography_vintage` are a pair. Frames A–C have `code_system: none` — store the printed Union label as `geography_code` (stable slug from the printed string, not an LGD join) with vintages `2026` / `2024` as in the table above. Do not recode Frame A onto Frame B or C. Do not recode Union transfers onto C5.

Licence: MoF Budget site terms (not CC-BY); CGA all rights reserved, not CC-BY. Named HTTP 200 downloads on the cards did not present a login wall on 18 September 2026. If a later retrieve hits a login wall or terms forbid, Ingest **stops**. Do not fetch `www.cga.gov.in` (SSL mismatch). Do not fetch `frbm2.pdf`, `bag*.xls`, or `allafs.xlsx` as this vintage.

---

## Publish / serving

Unchanged from C1: temp+rename pointers; `COMPLETE` marker; nine tests; DuckDB reads **exactly one** `vintage_id`; `ServedObservation` only; no rank-sort default; definition, unit, geography vintage, and data vintage in the same view as the number.

C3-specific serving rules Platform forbids (UI/UX / Content Editor implement; tests fail a bare float either way):

- Do not serve a Union total without naming missing states, UTs, and districts.
- Do not serve BE, RE, and Actuals as one observation.
- Do not serve a number that blends Budget, CGA monthly, and Finance Accounts into one “Union money”.
- `unknown` / `not_comparable` / `series_break` stay first-class. Do not hide FRBM as a grade. Do not serve Card 8 as a receipts/expenditure/deficit/debt table while it is the named hole.

A C3 template bind is a later CMS job. Tests 4–8 need a real Astro render of C3 and stay skipped until UI/UX Developer renders C3. Tests 1–3 (write) and test 9 (series cas / hard-link) apply to a C3 vintage the same way as C1, with `required_series_ids=C3_SERIES_IDS`.

---

## Ingest Engineer — remaining Platform preconditions

`citation_card`, `source_class: allow`, `geography_frame`, method notes, and this contract (including named-hole completeness) exist. This is the store Ingest lands into.

Fetch the **card URL**: xlsx for Cards 1, 2, 3, 5, 6 (`tr.xlsx`, `ntr.xlsx`, `ctr.xlsx`, `stat1.xlsx`, `budget_at_a_glance.xlsx` sheet **Deficit Statistics**); PDF or `DATA2627.htm` for Cards 4, 7, 8, 9, 10, 11. Card 6 must not read other BAG sheets. Do not ingest `allafs.xlsx`. Do not pull Annex 4 state-wise rows, BAG transfers-to-States, state Finance Accounts, or district files.

If PDF/HTML tables cannot be read as cells without guessing, **stop** (`lineage_ok: no`) and flag Methodologist — do not OCR Budget books and do not reconstruct CGA monthly tables from layout guesses. Card 8 is the locked named hole (`frbm1.pdf` prose flag); keep retrieving it. Do not invent an FRBM grid. A complete C3 vintage requires Cards 1–7 and 9–11 `lineage_ok: yes`; Card 8 may stay `lineage_ok: no`.

---

## Wait

**Content Editor** writes the collect/spend explainer on the reconstructable cards (1–7, 9–11) and names Card 8 as unknown / not a table. **UI/UX Developer** renders that template at the C3 vintage; tests 4–8 stay skipped until that render. **Trust Auditor** still runs before anything a citizen sees.

Do not move `citizen_pointer` in this pass. Do not unblock C2. Do not start C4–C20.
