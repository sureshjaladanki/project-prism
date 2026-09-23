# C6 refresh and serving contract

Persona: Platform Architect. Slice: **C6**. Locked inputs: [`c6-citation-cards.md`](c6-citation-cards.md), [`c6-geography-frame.md`](c6-geography-frame.md), [`c6-method-notes.md`](c6-method-notes.md).

Same machine as C1. UDISE+ and Census literacy are separate series in one vintage — not one merged “school” measure. Citizen pointer unchanged until Charter after Trust.

**Catalog gate.** Parsers for UDISE+ PDF and/or open-services JSON (`yearId` 12); Census PCA literacy columns may reuse C2 PCA artifact family with a C6 citation/caveat bind. Do not fetch until catalog validates.

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

- **schedule** — all three: **unknown** (no 2026-27 UDISE booklet dated; Census literacy delayed). Do not invent an academic-year tick from 7 July 2026 PDF CreationDate.
- **source_change** / **on_demand** — as C1.

---

## C6 series ids (stable)

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| 1 | `udise-plus-2025-26-schools-enrolment-teachers` | `dosel-udise` | `c6-frame-a` | `2025-26` | unknown | `2025-26-nep` |
| 2 | `udise-plus-2025-26-facilities` | `dosel-udise` | `c6-frame-a` | `2025-26` | unknown | `2025-26-nep` |
| 3 | `census-2011-pca-literacy` | `orgi` | `c6-frame-b` | `2011` | unknown | `2011` |

Citation / caveat ids: `cite-c6-…` / `caveat-c6-…` at catalog transcription. Card 3 may share the C2 PCA raw artifact bytes (hard-link) but keeps **C6** citation/caveat and literacy-column mapping — not C2 population observations.

Complete C6 vintage lists **all three**. NEP Structure is primary; Existing Structure is not a silent substitute series.

---

## Stores

```text
data/{raw,derived,lineage}/dosel-udise/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/orgi/{series_id}/{source_vintage}/…
```

Frame A: PDF Table 2.2/2.5 stubs or API `regionName` as opened — do not silent-normalize. Frame B: Census 2011 codes as C2 Frame A. District UDISE parked.

---

## Publish / serving

Route: school path per [`web-design.md`](../web-design.md) (Front-end Architect). Forbids: ASER (Pratham) as record; UDISE “ASER” acronym as Pratham; board-exam portals; state rankings; merging literacy into enrolment; presenting 2011 literacy as current; district UDISE.

---

## Ingest Engineer — preconditions

Do not fetch until catalog validates. Prefer NEP PDF + open-services POST `yearId` `"12"`; PCA xlsx literacy columns, India/STATE only. Do not pull district microdata.

---

## Wait

Ingest/Pipeline; then Content / UI/UX / Trust. Do not move citizen pointer.
