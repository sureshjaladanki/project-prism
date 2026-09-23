# C8 geography frame

Persona: Geography Steward. Slice: **C8** (What does the official record say about foodgrain, and what does the public food system deliver?).

Input locked: `docs/next/c8-citation-cards.md`. Charter geography: national and state/UT as published; **districts parked**. Keep Family A (farm production / procurement) and Family B (PDS / NFSA delivery) as separate chart families — geography frames still must not silent-merge labels across producers.

Store a row on **the producer’s name as printed on that artifact**. Do not match on spelling alone (`J&K` ≠ `Jammu & Kashmir`; `DNH` ≠ `Dadra and Nagar Haveli and Daman and Diu`; `Telangna` ≠ `Telangana` if both appear). Do not join a DES APY row to a DFPD bulletin stub or an FCI stock region because the English looks similar.

Crop season (Kharif / Rabi / Summer), marketing season (KMS / RMS), and scheme (AAY / PHH / Tide Over) are **not** geography.

**Districts:** parked. **Crosswalk between frames: none.**

Six frames.

---

## Frame A — DES All-India foodgrain production time series (Cards A1–A2)

Binds: Card A1 (3rd AE 2025-26); Card A2 (Final Estimates 2024-25).

```text
frame:          Union
vintage:        A1: crop year 2025-26 (3rd AE, as on 27 May 2026); A2: crop year 2024-25 Final (as on 20 November 2025)
code_system:    none
units_included:
  All India (as printed on the Time-Series PDFs)
units_missing:
  all States and UTs as own rows (not in these artifacts)
  districts and below (parked)
breaks:         Advance Estimates vs Final Estimates are different production rounds —
                not geography. Do not invent State rows from Frame B and call them A1/A2.
crosswalk:      none — do not recode
```

A national production figure on this frame must still say States/UTs and districts are missing from **these** PDFs (State APY lives on Frame B).

---

## Frame B — DES Five-Years State/UT APY workbook (Card A3)

Binds: Card A3 — sheet `Total Foodgrains` (and crop sheets with the same State list). Labels observed on the citation card.

```text
frame:          Union | state | UT | other
vintage:        2021-22 to 2025-26 (2025-26 column = 3rd AE vintage aligned with Card A1)
code_system:    producer-specific
units_included:
  All India
  A&N Islands
  Andhra Pradesh
  Arunachal Pradesh
  Assam
  Bihar
  Chandigarh
  Chhattisgarh
  DNH
  Daman And Diu
  Delhi
  Goa
  Gujarat
  Haryana
  Himachal Pradesh
  J&K
  Jharkhand
  Karnataka
  Kerala
  Ladakh
  Madhya Pradesh
  Maharashtra
  Manipur
  Meghalaya
  Mizoram
  Nagaland
  Odisha
  Others
  Puducherry
  Punjab
  Rajasthan
  Sikkim
  Tamil Nadu
  Telangana
  Tripura
  Uttar Pradesh
  Uttarakhand
  West Bengal
units_missing:
  Lakshadweep (not in the observed Total Foodgrains State list on the citation card —
    confirm on open; do not invent a row)
  today’s merged UT string “Dadra and Nagar Haveli and Daman and Diu” as one row
    (this workbook prints DNH and Daman And Diu separately)
  districts and below (parked)
breaks:         Short forms (J&K, DNH, A&N Islands) are the store keys — do not
                silent-expand to Frame D/E/F spellings. Others is a residual bucket,
                not a State. Blank 2025-26 cells for some smaller geographies are
                data holes, not missing units. Do not recode onto Frames C–F.
crosswalk:      none — do not recode
```

---

## Frame C — ASAG 2024-25 foodgrain production tables (Card A4)

Binds: Card A4 — tables 2.2 / 2.3 (a)(b) and crop-wise companions as cited.

```text
frame:          Union | state
vintage:        Agricultural Statistics at a Glance 2024-25 (tables carry their own reference years)
code_system:    producer-specific
units_included:
  All India and Major States as labelled in each table (not every table is a full
  36-UT panel — Ingest stores stubs exactly as printed on that table)
units_missing:
  States/UTs omitted from a given “Major States” table
  districts (parked)
breaks:         Prefer Frames A–B for the latest AE/FE production vintage. ASAG is an
                older book map — do not stitch onto Card A1’s 3rd AE column.
crosswalk:      none — do not recode onto Frame B
```

---

## Frame D — DFPD Foodgrains Bulletin State/UT tables (Cards A5, B1, B2)

Binds: Card A5 (procurement); Card B1 (allocation & offtake); Card B2 (NFSA coverage / FPS). Same August 2026 bulletin PDF; store each table’s stub as printed (short forms and spelling variants allowed).

```text
frame:          Union | state | UT
vintage:        August 2026 bulletin (upload 16 September 2026; table footnotes may use upto 31.08.2026 / July 2026)
code_system:    producer-specific
units_included:
  States/UTs (and All India / national totals) as labelled on each bulletin table —
  examples on Card A5 include Andhra Pradesh, Telangana, Assam, Bihar, Chandigarh,
  Chhattisgarh, Delhi, Gujarat, Haryana, Himachal Pradesh, Jharkhand, J&K, Karnataka,
  Kerala, Madhya Pradesh, Maharashtra, … (full stub list confirmed on open)
units_missing:
  districts and below (parked)
  units absent from a given table (do not fill from Frame B)
breaks:         Spelling variants across bulletin pages (e.g. Telangna/Telangana,
                Chhatisgarh/Chhattisgarh) are separate printed strings until Ingest
                opens the page — store as printed; do not merge by eye.
                Do not recode onto Frame B DES short forms or Frame E FCI regions.
crosswalk:      none — do not recode
```

---

## Frame E — FCI central-pool stocks by region/State (Card A6)

Binds: Card A6 — DFPD-hosted FCI stock PDF (and bulletin companion pages 11–13).

```text
frame:          Union | state | region
vintage:        stocks as on 01.09.2026 (opening) on the standalone PDF; bulletin companion may use 31.08.2026 closing
code_system:    producer-specific
units_included:
  Regions/States as labelled (Bihar, Jharkhand, Odisha, West Bengal, Assam, NE States,
  Delhi, Haryana, Himachal Pradesh, J&K, Punjab, Rajasthan, Uttar Pradesh, Uttarakhand,
  Andhra Pradesh, Karnataka, Kerala, Tamil Nadu, Telangana, Gujarat, Maharashtra,
  Madhya Pradesh, Chhattisgarh, plus zonal and All India totals — confirm on open)
units_missing:
  States/UTs not printed on the stock sheet (may be rolled into NE States or omitted)
  districts (parked)
breaks:         NE States is an aggregate region, not a State. Producer FCI; fetch host
                DFPD — geography keys still come from the printed stubs.
                Do not recode onto Frame D bulletin stubs or Frame B.
crosswalk:      none — do not recode
```

---

## Frame F — NFSA Public Ration Card Dashboard (Card B3)

Binds: Card B3 — interactive administrative dashboard.

```text
frame:          Union | state | UT
vintage:        live; capture “Data Availability Date” shown in UI at fetch time
code_system:    producer-specific
units_included:
  Central + State/UT filter list as on the portal footer (36 States/UTs including
  Ladakh and merged Dadra and Nagar Haveli and Daman and Diu — confirm strings on open)
units_missing:
  districts (parked this iteration even if related portals show them)
  Annavitran distribution dashboard (named hole — unreachable on citation-card fetch)
breaks:         Live dashboard map may differ from Frame B’s separate DNH / Daman And Diu
                rows. Do not recode. Prefer Frames D bulletin tables when a citable
                static file is required.
crosswalk:      none — do not recode
```

Card B4 (DFPD Annual Report) is national companion narrative; State figures only where a specific annex table prints them — treat each annex as its own printed stub list, not a new standing frame until Ingest names one.

---

## Handoff

Next persona: **Methodologist**. Do not ingest until Platform names the refresh contract. Keep Family A and Family B on separate charts. DES TLS may need an approved client path (`curl -k` / browser UA) as noted on the citation cards.
