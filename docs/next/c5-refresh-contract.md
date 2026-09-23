# C5 refresh and serving contract

Persona: Platform Architect. Slice: **C5**. Locked inputs: [`c5-citation-cards.md`](c5-citation-cards.md), [`c5-geography-frame.md`](c5-geography-frame.md), [`c5-method-notes.md`](c5-method-notes.md).

Same machine as C1. Do not mix with C3 Union series. A C5 vintage lists the seven series below only. Citizen pointer does not move until Charter after Trust.

**Catalog gate.** New catalog slice + parsers for RBI SF XLSX/PDF and CAG CFRA PDF. `rbidocs` may need an approved fetch client (WAF / TLS). Do not fetch until catalog validates.

---

## Refresh contract

```text
vintage_id_rule:    same as C1 (dv- + date + 12-hex InputManifest)
triggers:           schedule | source_change | on_demand
sequence:           ingest → pipeline → cms render → publish pointer
atomic_publish:     yes
on_fail:            keep previous published vintage
retain_prior:       yes
```

- **schedule** — all seven: **unknown** (next RBI Study / CFRA year not dated on cards). Do not invent an annual tick from 23 January 2026.
- **source_change** / **on_demand** — as C1.

---

## C5 series ids (stable)

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| 1 | `rbi-sf-2025-26-deficit-indicators` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 2 | `rbi-sf-2025-26-revenue-receipts` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 3 | `rbi-sf-2025-26-expenditure` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 4 | `rbi-sf-2025-26-capital-receipts` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 5 | `rbi-sf-2025-26-gfd-financing` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 6 | `rbi-sf-2025-26-liabilities` | `rbi` | `c5-frame-a` | `2025-26` | unknown | `2025-26-study` |
| 7 | `cag-cfra-2020-21-glance` | `cag` | `c5-frame-b` | `2020-21` | unknown | `2020-21` |

Citation ids from librarian cards (`cite-c5-…`); caveat ids `caveat-c5-…` matching Methodologist notes at catalog transcription.

Complete C5 vintage lists **all seven**. BE / RE / Accounts are `status` / `reference_period`, not geography. Own tax ≠ Centre transfers — separate measures or columns as mapped, never one blended “revenue”.

**Named hole (coverage, not completeness block):** UTs without legislature missing on Frame A; CFRA after 2020-21 absent — say so on the page; do not invent rows.

---

## Stores

```text
data/{raw,derived,lineage}/rbi/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/cag/{series_id}/{source_vintage}/…
```

`geography_code` = printed State/UT stub; `code_system: producer-specific`. Do not recode Frame A onto Frame B or onto C3. Do not treat “All States and UTs” as every UT in India.

---

## Publish / serving

Same as C1. Route: `/money/states` ([`web-design.md`](../web-design.md)).

Forbids: fiscal-virtue ranks; grants as own tax; Union Budget as state money; local-body accounts; district rows; stitching RBI 2025-26 onto CFRA 2020-21 as one line.

---

## Ingest Engineer — preconditions

Do not fetch until catalog + parsers exist. Prefer RBI listing XLSX; browser-capable path if `rbidocs` WAF blocks automated GET. CAG glance + volumes for Card 7. Stop rather than guess PDF grids.

---

## Wait

Ingest/Pipeline for RBI/CAG shapes; then Content / UI/UX / Trust. Do not move citizen pointer. Do not fold into C3.
