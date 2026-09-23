# C4 refresh and serving contract

Persona: Platform Architect. Slice: **C4**. Locked inputs: [`c4-citation-cards.md`](c4-citation-cards.md), [`c4-geography-frame.md`](c4-geography-frame.md), [`c4-method-notes.md`](c4-method-notes.md).

Same machine as C1 ([`c1-refresh-contract.md`](../archive/c1-refresh-contract.md)): vintage identity, triggers, atomic publish, observation columns. No second web framework, ISR, or request-time producer fetch.

Do not mix C4 observations with C1–C3 or with MGNREGA (C9). A C4 vintage lists the four series below only. `data/pointers/citizen` does not move for C4 until Charter ships after Trust. Preview may bind a C4 vintage without moving citizen.

**Catalog gate.** Add `src/prism/catalog/slices/c4.yaml` and card YAML only after Ingest/Pipeline register parsers/mappers for PLFS shapes (new table families — do not copy `pipeline/c3.py`). Do not fetch until this contract is the store and the catalog entry validates.

---

## Refresh contract

```text
vintage_id_rule:    "dv-" + run_date_utc (YYYYMMDD) + "-" + 12-hex of
                    InputManifest JSON (created_at, trigger, per-series
                    entries). Directory with that id is never overwritten.
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline (data vintage) → cms render → publish pointer
atomic_publish:     yes
on_fail:            keep previous published vintage; do not serve a partial
retain_prior:       yes
```

- **schedule** — per `next_release`: Monthly **2026-10-15**; Quarterly **2026-11-10**; Annual and earnings follow the next calendar-year annual (ARC). Re-resolve MoSPI hashed upload paths via product 69 on refresh.
- **source_change** — Ingest `lineage.json` `source_changed: yes` or `first_retrieve`.
- **on_demand** — editor asks; same CLI; not a request-time scrape.

---

## C4 series ids (stable)

Producer slug: `mospi`. Producer: NSO / MoSPI (PLFS product 69).

| Card | `series_id` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|---------------------|---------------------|----------------|-------------------------|
| 1 | `plfs-monthly-lfpr-wpr-ur-cws` | `c4-frame-a` | `2025` | 2026-10-15 | `2026-08` |
| 2 | `plfs-quarterly-lfpr-wpr-ur-cws` | `c4-frame-b` | `2025` | 2026-11-10 | `2026-Q2` |
| 3 | `plfs-annual-lfpr-wpr-ur-2025` | `c4-frame-c` | `2025` | unknown | `2025` |
| 4 | `plfs-annual-earnings-2025` | `c4-frame-c` | `2025` | unknown | `2025` |

Citation / caveat ids (lock at catalog transcription; mirror Methodologist caveat keys):

| Card | `citation_id` | `caveat_id` |
|------|---------------|-------------|
| 1 | `cite-c4-plfs-monthly-lfpr-wpr-ur-cws-2026-08` | `caveat-c4-plfs-monthly-lfpr-wpr-ur-cws` |
| 2 | `cite-c4-plfs-quarterly-lfpr-wpr-ur-cws-2026-q2` | `caveat-c4-plfs-quarterly-lfpr-wpr-ur-cws` |
| 3 | `cite-c4-plfs-annual-lfpr-wpr-ur-2025` | `caveat-c4-plfs-annual-lfpr-wpr-ur-2025` |
| 4 | `cite-c4-plfs-annual-earnings-2025` | `caveat-c4-plfs-annual-earnings-2025` |

A later monthly/quarterly retrieve gets a new `citation_id` / `source_vintage`; `series_id` does not change. A complete C4 vintage **lists all four series**. Usual status and CWS on Card 3 stay separate observations — do not merge in the store.

`geography_vintage` `2025` marks the post–January-2025 PLFS design map (Frames A–C), not Census 2011.

---

## Stores

Same layout as C1. Path segment: `data/{raw,derived,lineage}/mospi/{series_id}/{source_vintage}/…`.

`geography_code` = printed stub (All India / State/UT as on the opened table); `code_system: none` on Frames A–B; Frame C uses producer-specific printed `State/UT` strings. Sector rural/urban is **not** geography. Do not fill Frame B missing States from Frame C.

Parquet columns unchanged. `status` may carry usual vs CWS / earnings concept where Pipeline maps it — do not invent a second schema.

Licence: MoSPI / GSDD Category A for aggregate bulletins; not Category B unit-level. No login wall on named PDF/XLSX. Stop if terms or walls change.

---

## Publish / serving

Unchanged from C1 (desk pointer, `COMPLETE`, one `vintage_id` per page, `ServedObservation` only, no rank-sort default).

C4-specific forbids:

- Do not serve CMIE or MGNREGA as PLFS.
- Do not serve usual status and CWS as one rate.
- Do not serve pre-2025 PLFS as continuous with these four without a series_break.
- Do not serve Card 2 as “all States” — selected States only.
- Do not serve one “average wage” across Card 4’s three earnings tables.
- Do not pull district PLFS for this slice.

Route/slug: Front-end Architect already holds `/work/labour` in [`web-design.md`](../web-design.md). Do not invent a second path here.

---

## Ingest Engineer — preconditions

Cards, geography, method notes, and this contract exist. **Do not fetch** until `c4.yaml` + parsers/mappers register and `prism catalog validate` passes.

Fetch Card URLs (PDF + named Appendix XLSX). Re-resolve hashed MoSPI paths via product 69. Card 1 is PDF-only this release. Do not fetch unit-level microdata. Do not fetch Selected Districts snapshot.

---

## Wait

**Ingest Engineer** + **Pipeline Engineer**: PLFS parser/mapper families and catalog transcription. **Content Editor** / **UI/UX** / **Trust** after a complete C4 vintage. Do not move `citizen_pointer` for C4 in this pass. Do not start Wave 3 from this file.
