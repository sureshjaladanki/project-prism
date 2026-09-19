# C2 geography frame

Persona: Geography Steward. Slice: **C2** (How many people live in India, where, and how is that changing?).

Input locked: `docs/next/c2-citation-cards.md`. Charter geography: national (keep the producer’s **India** / **INDIA** label); in: national, states, UTs as published; districts parked even if Census publishes them.

Store a row on **the producer’s code + name as printed on that artifact**. Do not match on spelling alone (ODISHA not Orissa; PUDUCHERRY not Pondicherry; NCT OF DELHI / NCT of Delhi / NCT OF Delhi are three printed strings, not one unit to merge). Do not join a 2011 row to a 2024 row because the English looks similar.

TRU (`Total` / `Rural` / `Urban`) on Census PCA is **not** geography. Residence on SRS tables is **not** geography.

**Districts:** parked. Card 1 contains DISTRICT rows — do not ingest them. Do not recode 2011 districts to 2024 districts. **Crosswalk between frames: none.** Census stock, SRS rates, and the 2011–2036 projection are three maps.

Four frames (Card 2 shares the 2011 Census map with Card 1, with its own printed names).

---

## Frame A — Census 2011 India and STATE (Card 1)

Binds: Card 1 — PCA SD, `Level` in {`India`, `STATE`}, all `TRU` as published.

Artifact: `https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx` sheet Sheet1. Columns as printed: `State`, `District`, `Level`, `Name`, `TRU`. Inspected 18 September 2026: 3 India rows, 105 STATE rows (35 names × 3 TRU), **1,920 DISTRICT rows (parked)**.

Key: `State` (zero-padded two-digit) + `Name` as printed + `Level`. On these rows `District` is `000`. That is a Census 2011 state/UT code, not an LGD join licence.

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
  Telangana as a STATE row (not on this file; 2014 split is after this vintage)
  Ladakh as a UT row (not on this file; Leh(Ladakh) and Kargil are DISTRICT under 01 — parked)
  districts and below (1,920 DISTRICT rows in the same workbook — parked; do not pull, do not recode)
  today’s merged UT “Dadra and Nagar Haveli and Daman and Diu” as one row (25 and 26 are separate)
breaks:         2011 Census map. Later hits that are **not** units here:
                - 2014: Telangana is not split out; 28 ANDHRA PRADESH is the 2011 state
                  (includes the area later called Telangana).
                - 2019: 01 JAMMU & KASHMIR is the 2011 state (includes the area later
                  called Ladakh UT). Ladakh is not a STATE/UT label on this sheet.
                - 2020: 25 DAMAN & DIU and 26 DADRA & NAGAR HAVELI remain two UTs.
                Do not recode these rows onto Frame C or Frame E labels.
crosswalk:      none — do not recode
```

**India (`00`)** is the published Census 2011 national total, not a roll-up Ingest should compute from STATE rows, and not “India in 2026”. A national figure on this frame must still say:

- districts (and below) are in the file and **parked**;
- Telangana and Ladakh are **not** STATE/UT labels on this map;
- this is a **2011** count.

---

## Frame B — Census 2011 A-02 India and State/UT (Card 2)

Binds: Card 2 — Table A-02 decadal variation 1901–2011.

Artifact of record for names: companion PDF `https://censusindia.gov.in/nada/index.php/catalog/43333/download/47002/00%20A%202-India.pdf` (same NADA catalog as the `.xls`). Columns as printed: State Code, District Code (`000` on these rows), India/State/Union Territory, Census Year.

Same **2011** code list as Frame A (`00`–`35`). **Printed names are not the same strings as PCA.** Store A-02 names as printed (footnote marks stay on the name until Methodologist owns the footnotes).

```text
frame:          Union | state | UT
vintage:        2011
code_system:    census
units_included:
  00 | INDIA
  01 | Jammu & Kashmir
  02 | Himachal Pradesh
  03 | Punjab
  04 | Chandigarh
  05 | Uttarakhand
  06 | Haryana
  07 | NCT OF Delhi
  08 | Rajasthan
  09 | Uttar Pradesh
  10 | Bihar
  11 | Sikkim
  12 | Arunachal Pradesh *
  13 | Nagaland   ^
  14 | Manipur
  15 | Mizoram
  16 | Tripura
  17 | Meghalaya
  18 | Assam
  19 | West Bengal
  20 | Jharkhand
  21 | Odisha
  22 | Chhattisgarh
  23 | Madhya Pradesh   $$
  24 | Gujarat
  25 | Daman & Diu
  26 | Dadra & Nagar Haveli
  27 | Maharashtra  ##
  28 | Andhra Pradesh @@
  29 | Karnataka
  30 | Goa
  31 | Lakshadweep
  32 | Kerala
  33 | Tamil Nadu
  34 | Puducherry
  35 | Andaman & Nicobar Islands
units_missing:
  Telangana; Ladakh as its own UT; merged DNH–DD (same 2011 holes as Frame A)
  districts (this India artifact is District Code 000 only)
  some early census years are N.A. on included units (e.g. Arunachal Pradesh before 1961)
    — missing observations on an included unit, not a dropped State
breaks:         Same 2011 map as Frame A. Producer footnote marks (*, ^, $$, ##, @@, $, @, #, +)
                on names or years are breaks — Methodologist. Do not strip marks to “fix”
                a join to Frame A. Do not recode onto Frame C.
crosswalk:      none — do not recode (not even to Frame A Name)
```

Do not treat Frame A `JAMMU & KASHMIR` and Frame B `Jammu & Kashmir` as a spelling merge. They are the same 2011 unit **only** via Census code `01` on these two Census tables — still two printed names. Pipeline may key Census 2011 on `State`/`State Code` `01`; it must keep the printed name from the artifact that produced the observation.

---

## Frame C — SRS Bulletin 2024, all Table 1 units (Card 3)

Binds: Card 3 — SRS Bulletin Vol. 59 No. 1, Table 1 (and the other Tables 2–6 that use the same India / Bigger / Smaller / UT list).

Artifact: `https://censusindia.gov.in/nada/index.php/catalog/47150/download/51394/SRS_Bulletin_2024_Vol_59_No_1.pdf`. No state-code column. Groups as printed: **India**; **Bigger States/Union Territories** (population more than 10 million as per Census 2011); **Smaller States**; **Union Territories**.

```text
frame:          Union | state | UT
vintage:        2024
code_system:    none
units_included:
  India
  Bigger States/Union Territories:
    Andhra Pradesh
    Assam
    Bihar
    Chhattisgarh
    NCT of Delhi
    Gujarat
    Haryana
    Jammu & Kashmir
    Jharkhand
    Karnataka
    Kerala
    Madhya Pradesh
    Maharashtra
    Odisha
    Punjab
    Rajasthan
    Tamil Nadu
    Telangana
    Uttar Pradesh
    Uttarakhand
    West Bengal
  Smaller States:
    Arunachal Pradesh
    Goa
    Himachal Pradesh
    Manipur*
    Meghalaya
    Mizoram
    Nagaland
    Sikkim
    Tripura
  Union Territories:
    Andaman & Nicobar Islands
    Chandigarh
    Dadra & Nagar Haveli and Daman & Diu
    Ladakh
    Lakshadweep
    Puducherry
units_missing:
  districts and below (not in this bulletin; parked)
  2011-only labels: undivided Andhra Pradesh; undivided Jammu & Kashmir state;
    separate Daman & Diu; separate Dadra & Nagar Haveli
  no current State or UT is absent from Table 1 (21 bigger + 9 smaller + 6 UTs + India)
breaks:         Post-reorganisation map for reference year 2024:
                - Telangana and Andhra Pradesh are distinct bigger units.
                - Jammu & Kashmir and Ladakh are distinct (J&K in Bigger; Ladakh in UTs).
                - Dadra & Nagar Haveli and Daman & Diu is one UT row (printed across two lines).
                Manipur* is the Manipur unit; the asterisk is a producer sample footnote
                (130 SRS units), not a second geography.
                Do not recode Frame A/B `01` / `28` / `25`+`26` onto these rows.
crosswalk:      none — do not recode
```

**India** on this frame is the SRS all-India estimate for 2024, not Census 2011 `00 | India`, and not “every district”. Smaller-States/UTs IMR by sex and residence uses a three-year period on other tables — that is Methodologist, not a missing UT.

---

## Frame D — SRS Statistical Report 2024, bigger States/UTs (Card 4)

Binds: Card 4 — fertility (including TFR) and the report’s India / bigger States/UTs tables. NSS Natural Division maps/tables in the same PDF are **below** the charter bar — parked.

Preface (citation card): India and bigger States/UTs (population of 10 million and above), rural and urban. That is the **Bigger States/Union Territories** list on Frame C, plus India — **not** Frame C’s Smaller States or Union Territories list.

```text
frame:          Union | state | UT
vintage:        2024
code_system:    none
units_included:
  India
  Andhra Pradesh
  Assam
  Bihar
  Chhattisgarh
  NCT of Delhi
  Gujarat
  Haryana
  Jammu & Kashmir
  Jharkhand
  Karnataka
  Kerala
  Madhya Pradesh
  Maharashtra
  Odisha
  Punjab
  Rajasthan
  Tamil Nadu
  Telangana
  Uttar Pradesh
  Uttarakhand
  West Bengal
units_missing:
  all Frame C Smaller States (Arunachal Pradesh through Tripura)
  all Frame C Union Territories (Andaman & Nicobar Islands through Puducherry,
    including Ladakh and the merged DNH–DD UT)
  districts; NSS Natural Division rows (parked)
breaks:         Same 2024 bigger-state map as Frame C’s bigger block. Narrower
                coverage than Card 3. Do not fill missing smaller States/UTs from
                the Bulletin and call it the Statistical Report.
crosswalk:      none — do not recode
```

A national TFR (or other Card 4 India figure) must still say smaller States, UTs, and districts are missing from this report’s main tables.

---

## Frame E — Population projections Table 8 (Card 5)

Binds: Card 5 — Technical Group / NCP / MoHFW, November 2019, **TABLE-8** only (projected total population by sex as on 1st March, 2011–2036, India, States and Union Territories*, in thousands). TABLE-11 (1st July) is a different reference day in the same PDF — not this frame’s merge.

Artifact: `https://nhm.gov.in/New_Updates_2018/Report_Population_Projection_2019.pdf`. The PDF is largely image pages; row labels are **as printed on Table 8**, not as OCR’d here. Librarian (and title page): India, States and UTs including **Jammu & Kashmir*(UT)** and **Telangana**. Some **other** tables in the same report exclude Goa or combine North-East States excluding Assam — those tables are not Table 8.

```text
frame:          Union | state | UT
vintage:        2019
code_system:    none
units_included:
  India, States and Union Territories as labelled on TABLE-8
  (including Jammu & Kashmir*(UT) and Telangana as printed)
units_missing:
  districts (not in Table 8)
  any unit that Table 8 does not print — do not copy Frame C’s list onto Table 8
  Goa / North-East exclusions that apply to other tables in this PDF are not
    assumed for Table 8; if a Table 8 row is absent, it is missing on this frame
breaks:         Projection map as of the November 2019 report, on a Census 2011 base.
                Not a 2011 PCA row and not a 2024 SRS row.
                Jammu & Kashmir*(UT) is the printed Table 8 unit — not Frame A `01`
                and not Frame C’s pair (Jammu & Kashmir + Ladakh) unless Table 8
                itself prints Ladakh.
                Do not recode thousands ('000) or 1st March vs 1st July into another frame.
crosswalk:      none — do not recode
```

Ingest stores Table 8 stub labels **exactly as printed**. Do not invent English names from Frame C.

---

## Do not recode (standing)

| From | To | Why not |
|------|----|---------|
| Frame A/B `01` JAMMU & KASHMIR / Jammu & Kashmir | Frame C `Jammu & Kashmir` + `Ladakh` | 2019 split; 2011 row includes the later Ladakh area |
| Frame A/B `28` ANDHRA PRADESH | Frame C `Andhra Pradesh` + `Telangana` | 2014 split |
| Frame A/B `25` + `26` | Frame C `Dadra & Nagar Haveli and Daman & Diu` | 2020 merger |
| Frame A `India` 2011 | Frame C `India` 2024 or Frame E Table 8 | Three records |
| Frame C smaller/UT units | Frame D | Card 4 does not publish them on the main tables |
| Any of the above | LGD “current” India | Not this vintage |

---

## Ingest / Pipeline keys

| Field | Store as |
|-------|----------|
| Frame A geography key | `State` + `Name` + `Level` (`India` or `STATE` only) |
| Frame B geography key | State Code + District Code `000` + India/State/Union Territory as printed |
| Frame C/D geography key | Table stub name as printed (no code column) |
| Frame E geography key | TABLE-8 row label as printed |
| TRU / residence | separate dimension; not a geography unit |
| Districts | out of frame on every card |
| Frame | A Card 1; B Card 2; C Card 3; D Card 4; E Card 5 |

Do not invent English names. Do not hide missing districts, Telangana, Ladakh, or smaller States/UTs inside a national figure. Do not rank jurisdictions.

---

## Handoff

Geography Steward done for C2: Ingest can store a row without guessing which Kerala or which Delhi the producer meant **on that artifact**, and without treating 2011 `JAMMU & KASHMIR` as 2024 `Jammu & Kashmir` + `Ladakh`.

Next persona: **Methodologist** (first crew). Ingest is unblocked on geography for this slice; **do not fetch into `data/` in this pass**.
