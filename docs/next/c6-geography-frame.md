# C6 geography frame

Persona: Geography Steward. Slice: **C6** (Who is in school, and what does the official record say about schools?).

Input locked: `docs/next/c6-citation-cards.md`. Charter geography: national and state/UT as published; **district UDISE parked** even where district tools exist. Literacy (Card 3) is Census 2011 — separate map from UDISE+.

Store a row on **the producer’s name as printed on that artifact**. Do not match on spelling alone. Do not join a UDISE+ 2025-26 State/UT row to a Census 2011 STATE row because the English looks similar. Do not merge PDF title case with API ALL-CAPS `regionName` into one invented spelling.

School category (NEP Structure vs Existing Structure), TRU on Census PCA, and facility “having” vs “functional” columns are **not** geography.

**Districts:** parked (UDISE district reports, Know Your School, GIS, microdata; PCA DISTRICT literacy rows). **Crosswalk between frames: none** — UDISE+ 2025-26 and Census 2011 are two maps. PDF booklet labels and open-services `regionName` strings for the same year are two printed forms of Frame A — store the form from the artifact Ingest opened; do not silent-normalize.

Two frames for this slice (Card 3 reuses the C2 Census 2011 PCA STATE map).

---

## Frame A — UDISE+ Report 2025-26 NEP Structure (Cards 1–2)

Binds: Card 1 (schools, enrolments, teachers); Card 2 (infrastructure / facilities). Same booklet geography.

Artifact of record for names: Table 2.2 / 2.5 State-wise highlights in  
`https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_nep.94ceae1e8c2210549d21.pdf`  
(CreationDate 7 July 2026). Companion cell map: open-services `regionType` 21 / India `regionType` 10 for `yearId` `"12"` — same units, different `regionName` strings (see note below).

```text
frame:          Union | state | UT
vintage:        2025-26 (academic year; not the 7 July 2026 PDF CreationDate)
code_system:    producer-specific
units_included:
  India
  Andaman & Nicobar Islands
  Andhra Pradesh
  Arunachal Pradesh
  Assam
  Bihar
  Chandigarh
  Chhattisgarh
  Daman & Diu and Dadra & Nagar Haveli
  Delhi
  Goa
  Gujarat
  Haryana
  Himachal Pradesh
  Jammu & Kashmir
  Jharkhand
  Karnataka
  Kerala
  Ladakh
  Lakshadweep
  Madhya Pradesh
  Maharashtra
  Manipur
  Meghalaya
  Mizoram
  Nagaland
  Odisha
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
  districts and below (parked — district UDISE tools exist; do not pull)
breaks:         2025-26 UDISE+ map as printed. Telangana and Ladakh are titled units.
                Merged UT label is “Daman & Diu and Dadra & Nagar Haveli” on the PDF
                (API may print “DADRA & NAGAR HAVELI AND DAMAN & DIU” — same unit,
                two strings; store the opened artifact’s string).
                Do not recode onto Frame B (Census 2011).
crosswalk:      none — do not recode onto Census 2011 or invent an LGD join
```

**PDF vs API strings:** Ingest that opens the PDF stores Table 2.2 / 2.5 labels. Ingest that opens open-services stores `regionName` / national label as returned (`ALL INDIA` / `India` with `regionCode` 100 on highlights). Do not merge the two spellings in the store because casing or word order differs. Pipeline may later document a name map; Geography Steward does not author a silent recode here.

**India** on this frame is the published national total for UDISE+ 2025-26, not a roll-up Ingest invents from State/UT rows, and not “literacy India 2011”.

---

## Frame B — Census 2011 PCA India and STATE (Card 3 literacy)

Binds: Card 3 — PCA SD literacy columns (`P_LIT` / `M_LIT` / `F_LIT` and illiterate companions) on `Level` in {`India`, `STATE`} only. Same workbook and **same map** as C2 Frame A ([`docs/archive/c2-geography-frame.md`](../archive/c2-geography-frame.md) Frame A). TRU (`Total` / `Rural` / `Urban`) is not geography.

```text
frame:          Union | state | UT
vintage:        2011
code_system:    census
units_included:
  00 | India
  01 | JAMMU & KASHMIR
  02 | HIMACHAL PRADESH
  03 | PUNJAB
  04 | CHANDIGARH
  05 | UTTARAKHAND
  06 | HARYANA
  07 | NCT OF DELHI
  08 | RAJASTHAN
  09 | UTTAR PRADESH
  10 | BIHAR
  11 | SIKKIM
  12 | ARUNACHAL PRADESH
  13 | NAGALAND
  14 | MANIPUR
  15 | MIZORAM
  16 | TRIPURA
  17 | MEGHALAYA
  18 | ASSAM
  19 | WEST BENGAL
  20 | JHARKHAND
  21 | ODISHA
  22 | CHHATTISGARH
  23 | MADHYA PRADESH
  24 | GUJARAT
  25 | DAMAN & DIU
  26 | DADRA & NAGAR HAVELI
  27 | MAHARASHTRA
  28 | ANDHRA PRADESH
  29 | KARNATAKA
  30 | GOA
  31 | LAKSHADWEEP
  32 | KERALA
  33 | TAMIL NADU
  34 | PUDUCHERRY
  35 | ANDAMAN & NICOBAR ISLANDS
units_missing:
  Telangana as a STATE row (2014 split is after this vintage)
  Ladakh as a UT row (not a STATE/UT label on this sheet)
  today’s merged UT “Dadra and Nagar Haveli and Daman and Diu” as one row (25 and 26 are separate)
  districts and below (DISTRICT rows in the same workbook — parked)
breaks:         2011 Census map. Do not recode onto Frame A (UDISE+ 2025-26).
                Do not present 2011 literacy as current school enrolment.
crosswalk:      none — do not recode onto Frame A (same rule as C2 Frame A → later maps)
```

Key: `State` (zero-padded two-digit) + `Name` as printed + `Level`. Literacy columns only for C6; population stock remains C2’s series.

---

## Handoff

Next persona: **Methodologist**. Do not ingest until Platform names the refresh contract for this slice. Prefer NEP PDF and/or open-services `yearId` `"12"` for Cards 1–2; PCA xlsx literacy columns for Card 3 (India/STATE only).
