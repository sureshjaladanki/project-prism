# C7 refresh and serving contract

Persona: Platform Architect. Slice: **C7**. Locked inputs: [`c7-citation-cards.md`](c7-citation-cards.md), [`c7-geography-frame.md`](c7-geography-frame.md), [`c7-method-notes.md`](c7-method-notes.md).

Same machine as C1. SRS, NFHS, and RHS are three records in one vintage — never one blended health number. Cards 1–2 reuse C2 SRS artifacts (same `series_id` family / raw bytes may hard-link); C7 keeps its own citation trail and citizen question. Do not invent a merged C2+C7 product vintage.

Citizen pointer unchanged until Charter after Trust.

**Catalog gate.** PDF parsers for SRS (may extend C2 SRS shapes), NFHS fact sheets, RHS yearbook. Do not fetch until catalog validates.

---

## Refresh contract

```text
vintage_id_rule:    same as C1
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline → cms render → publish pointer
atomic_publish:     yes
on_fail:            keep previous published vintage
retain_prior:       yes
```

- **schedule** — all four: **unknown** (SRS 2025 not dated; NFHS-7 / full NFHS-6 report not dated; RHS after 2021-22 not on HMIS menu).
- **source_change** / **on_demand** — as C1.

---

## C7 series ids (stable)

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| 1 | `srs-bulletin-2024` | `orgi` | `c7-frame-a` | `2024` | unknown | `2024` |
| 2 | `srs-statistical-report-2024` | `orgi` | `c7-frame-b` | `2024` | unknown | `2024` |
| 3 | `nfhs-6-factsheets-2023-24` | `iips-mohfw` | `c7-frame-c` | `2023-24` | unknown | `2023-24-factsheets` |
| 4 | `rhs-2021-22` | `mohfw-hmis` | `c7-frame-d` | `2021-22` | unknown | `2021-22` |

Cards 1–2 share series_ids with C2 where the artifact is the same; vintage membership is per-slice (a C7 vintage lists these four; a C2 vintage lists C2’s five). Citation ids: `cite-c7-srs-bulletin-2024` / `cite-c7-srs-statistical-report-2024` (librarian) alongside C2 cites for the shared files.

Complete C7 vintage lists **all four**.

**Named holes (page must say; do not invent):** NFHS-6 full report / IMR cells on fact sheets; Manipur absent on Frame C; RHS after 2021-22; districts parked.

---

## Stores

```text
data/{raw,derived,lineage}/orgi/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/iips-mohfw/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/mohfw-hmis/{series_id}/{source_vintage}/…
```

Do not recode Frames A–D onto each other. Do not ingest NFHS district fact sheets or RHS Section II.

---

## Publish / serving

Forbids: mixing SRS and NFHS into one number; NITI Health Index as record; hospital star-ratings; private insurance; filling Manipur from SRS; serving RHS as 2026 stock without the 31 March 2022 date.

---

## Ingest Engineer — preconditions

Do not fetch until catalog validates. Four named PDFs on the cards. Prefer hard-link shared SRS raw bytes with C2 when checksums match.

---

## Wait

Ingest/Pipeline; then Content / UI/UX / Trust. Do not move citizen pointer. Do not start Wave 3 (C9) from this file.
