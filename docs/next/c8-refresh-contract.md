# C8 refresh and serving contract

Persona: Platform Architect. Slice: **C8**. Locked inputs: [`c8-citation-cards.md`](c8-citation-cards.md), [`c8-geography-frame.md`](c8-geography-frame.md), [`c8-method-notes.md`](c8-method-notes.md).

Same machine as C1. **Family A** (production / procurement / stocks) and **Family B** (PDS / NFSA delivery) are separate chart families in one vintage — never one “food security” measure. Citizen pointer unchanged until Charter after Trust.

**Catalog gate.** Parsers for DES PDF/XLSX, DFPD Foodgrains Bulletin PDF, FCI stock PDF, NFSA dashboard (prefer bulletin tables B1/B2 over live HTML when a file cite is required). `desagri.gov.in` may need TLS-tolerant approved client. Do not fetch until catalog validates.

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

- **schedule** — AE/FE rounds **unknown** until librarian dates the next; Foodgrains Bulletin monthly cadence expected but next month **unknown** on cards; NFSA dashboard continuous. Do not invent ticks from upload dates alone.
- **source_change** / **on_demand** — as C1.

---

## C8 series ids (stable)

### Family A — farm production / procurement / stocks

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| A1 | `des-foodgrain-3rd-ae-2025-26` | `desagri` | `c8-frame-a` | `2025-26` | unknown | `2025-26-3rd-ae` |
| A2 | `des-foodgrain-fe-2024-25` | `desagri` | `c8-frame-a` | `2024-25` | unknown | `2024-25-fe` |
| A3 | `des-foodgrain-apy-state-3rd-ae` | `desagri` | `c8-frame-b` | `2025-26` | unknown | `2021-22-2025-26-3rd-ae` |
| A4 | `des-asag-2024-25-foodgrain` | `desagri` | `c8-frame-c` | `2024-25` | unknown | `asag-2024-25` |
| A5 | `dfpd-bulletin-procurement` | `dfpd` | `c8-frame-d` | `2026-08` | unknown | `2026-08` |
| A6 | `fci-central-pool-stocks` | `fci` | `c8-frame-e` | `2026-09-01` | unknown | `2026-09-01` |

### Family B — PDS / NFSA delivery

| Card | `series_id` | `producer_slug` | Frame | `geography_vintage` | `next_release` | Locked `source_vintage` |
|------|-------------|-----------------|-------|---------------------|----------------|-------------------------|
| B1 | `dfpd-bulletin-allocation-offtake` | `dfpd` | `c8-frame-d` | `2026-08` | unknown | `2026-08` |
| B2 | `dfpd-bulletin-nfsa-coverage-fps` | `dfpd` | `c8-frame-d` | `2026-08` | unknown | `2026-08` |
| B3 | `nfsa-ration-card-dashboard` | `nfsa` | `c8-frame-f` | live | continuous | capture UI date at fetch |
| B4 | `dfpd-annual-report-2025-26` | `dfpd` | companion | `2025-26` | unknown | `2025-26-ar` |

Complete C8 vintage lists **all ten**. A5/B1/B2 may share one bulletin raw artifact (hard-link) with three series parses. A6 producer is FCI; fetch host DFPD — lineage must name both.

**Named holes:** districts; Annavitran; data.desagri.gov.in APY web; stock-vs-norms PDF 404; FAO/MSP-as-income rejected (no series).

---

## Stores

```text
data/{raw,derived,lineage}/desagri/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/dfpd/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/fci/{series_id}/{source_vintage}/…
data/{raw,derived,lineage}/nfsa/{series_id}/{source_vintage}/…
```

Do not recode Frames A–F onto each other. AE ≠ FE (`status` / `source_vintage`). Allocation ≠ offtake.

---

## Publish / serving

Forbids: one food-security chart merging A and B; bulletin page 8 as DES production; hunger index; MSP as income verdict; treating allocation as offtake or stock as delivery; district crop/PDS files.

---

## Ingest Engineer — preconditions

Do not fetch until catalog validates. Card URLs on [`c8-citation-cards.md`](c8-citation-cards.md). Prefer B1/B2 file tables over B3 live HTML for citable monthly series. Approved client for `desagri.gov.in` TLS if needed.

---

## Wait

Ingest/Pipeline for DES/DFPD/FCI/NFSA shapes; then Content / UI/UX / Trust. Do not move citizen pointer. Do not start Wave 3 from this file.
