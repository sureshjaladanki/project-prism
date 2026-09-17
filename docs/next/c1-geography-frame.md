# C1 geography frame

Persona: Geography Steward. Slice: **C1** (How fast are retail prices rising in India, including food?). Series of record: MoSPI NSO CPI Base 2024=100.

Input locked: `docs/next/c1-citation-cards.md`. Charter geography: national (keep **All India** as printed); in: national, states, UTs as published; districts parked. Two maps: Cards 1–3 publish All India plus States/UTs; Card 4 publishes All India only.

Store a row on **producer `State Code` + `State Name` as printed**. Do not match on spelling alone (Odisha not Orissa; Puducherry not Pondicherry; NCT of Delhi not Delhi; Jammu And Kashmir not undivided Jammu & Kashmir).

Sector (`Rural` / `Urban` / `Combined`) is **not** geography. Combined is a published sector, not a missing UT.

**Districts:** parked for this iteration. Do not pull district files. Do not recode districts. **City / centre rankings:** charter-out; do not build a city frame (Item/Subclass sheets are still State/UT, not cities).

---

## Frame A — All India and States/UTs (Cards 1–3)

Binds:

- Card 1 — CPI General (Rural, Urban, Combined), Base 2024=100
- Card 2 — CFPI / CPI Group Food 01.1
- Card 3 — CPI Division and Group indexes (COICOP 2018)

Artifact of record: `https://www.mospi.gov.in/uploads/documents/productChartTable/1789491098345-Data_August_CPI_2026_14092026.xlsx` (sheets General, Group, Division; same 37 `State Code`/`State Name` pairs on Class, Subclass, Item). Companion: `https://www.mospi.gov.in/uploads/documents/productChartTable/1789491131821-Annex.xlsx` sheet Annexure-III (State/UT names; no code column). Same 37 pairs on time-series `CPI_2024-Jan2025-Dec2025.xlsx` and `CPI_2024-Jan2026.xlsx` sheet General.

Column names as printed: `State Code` + `State Name` on General / Division / Group / Class / Subclass; Item sheet uses `State code` + `state_name`. Codes are zero-padded two-digit strings (including `00`).

```text
frame:          Union | state | UT
vintage:        2024
code_system:    producer-specific
units_included:
  00 | All India
  01 | Jammu And Kashmir
  02 | Himachal Pradesh
  03 | Punjab
  04 | Chandigarh
  05 | Uttarakhand
  06 | Haryana
  07 | NCT of Delhi
  08 | Rajasthan
  09 | Uttar Pradesh
  10 | Bihar
  11 | Sikkim
  12 | Arunachal Pradesh
  13 | Nagaland
  14 | Manipur
  15 | Mizoram
  16 | Tripura
  17 | Meghalaya
  18 | Assam
  19 | West Bengal
  20 | Jharkhand
  21 | Odisha
  22 | Chhattisgarh
  23 | Madhya Pradesh
  24 | Gujarat
  25 | The Dadra And Nagar Haveli And Daman And Diu
  27 | Maharashtra
  28 | Andhra Pradesh
  29 | Karnataka
  30 | Goa
  31 | Lakshadweep
  32 | Kerala
  33 | Tamil Nadu
  34 | Puducherry
  35 | Andaman And Nicobar Islands
  36 | Telangana
  37 | Ladakh
units_missing:
  districts and below (not in these artifacts; parked — do not pull, do not recode)
  city / centre geographies (charter-out; not this frame)
  Chandigarh Rural: not a missing UT. Unit 04 Chandigarh is included.
    Workbook General: Urban and Combined rows only (no Rural row).
    Annexure-III prints Chandigarh* with Rural cells blank; footnote
    “*: No rural market in Chandigarh”. Combined equals Urban on that row.
    Do not recode; do not treat Combined as a missing unit.
  No current State or UT is absent from State Name (28 states + 8 UTs + All India = 37 labels).
  Code 26 is unused (see breaks); it is not a missing published unit.
breaks:         This Base 2024=100 map is post-reorganisation throughout the
                comparable run (January 2025 onward). Hits that already sit
                on the sheet as separate current units:
                - 2014: Telangana (36) and Andhra Pradesh (28) are distinct;
                  undivided Andhra Pradesh is not a unit here.
                - 2019: Jammu And Kashmir (01) and Ladakh (37) are distinct UTs;
                  undivided Jammu & Kashmir state is not a unit here.
                - 2020: Dadra and Nagar Haveli and Daman and Diu are one UT
                  (25); former separate UTs and census-style code 26 are not published.
                Do not recode 2012=100 (or earlier) geographies onto these rows.
                State/UT Combined is not comparable to a user average of
                districts: districts are not on the map.
crosswalk:      none — do not recode
```

`code_system` is **producer-specific**: the files label the column `State Code` / `State code`; they do not name LGD or Census, and they publish `00` for All India. The two-digit strings coincide with the familiar Census/LGD state numbering plus Telangana `36`, Ladakh `37`, and the merged UT on `25`. That resemblance is not a licence to join LGD or Census lists. No producer code list URL is printed on the workbook or Annex.xlsx.

**All India (`00`)** is a published national unit, not a roll-up Ingest should compute from State/UT Combined. A national figure on this frame must still say:

- districts (and below) are missing from the artifact and parked for this iteration;
- Chandigarh has no rural market, so Chandigarh Rural is withheld (dash / omitted row), not hidden inside a complete “every UT Rural” reading;
- All India is the producer’s All India, not “every district in India”.

Annexure-III lists the 36 State/UT **names** (alphabetical; Chandigarh*). All India for general/division/group lives on other annex sheets and on the data workbook’s `00` rows — not as a 37th Annexure-III line.

---

## Frame B — All India only (Card 4)

Binds: Card 4 — CPI Back Series Index and Inflation (Base 2024=100, linked).

Artifact: `https://www.mospi.gov.in/uploads/documents/CPI/CPI_2024-Back-Series-Index-Inflation.xlsx` sheet Sheet1. Columns include `State code`, `State name`. Opened rows: `State name` = All India, `State code` = `00` only. No State/UT rows. Trailing empty rows are not units. Sector is still Rural / Urban / Combined (not geography). Group = General.

```text
frame:          Union
vintage:        2024
code_system:    producer-specific
units_included:
  00 | All India
units_missing:
  all 36 States and Union Territories published on Frame A
    (Jammu And Kashmir through Ladakh / The Dadra And Nagar Haveli
    And Daman And Diu — none appear as rows in this file)
  districts and below (parked)
  city / centre geographies (charter-out; not this frame)
breaks:         File does not carry a State/UT map, so Telangana, J&K
                reorganisation, Ladakh, and the DNH–DD merger do not appear
                as changing units here. Linked national All India only;
                do not treat this as a state-level historical map.
                Do not recode Frame A State/UT rows onto Card 4.
crosswalk:      none — do not recode
```

Card 4 All India is still not “the whole country at every administrative level”: States, UTs, and districts are missing from this file.

---

## Ingest / Pipeline keys

| Field | Store as |
|-------|----------|
| Geography key | `State Code` (or `State code`) + `State Name` (or `state_name`) exactly as printed |
| Frame | A for Cards 1–3 workbooks; B for Card 4 |
| Sector | separate dimension; not a geography unit |
| Chandigarh Rural | missing observation on included unit `04`, not a dropped UT |
| Districts | out of frame |
| Cities | out of frame |

Do not invent English names. Do not hide missing districts inside All India. Do not rank jurisdictions.

---

## Handoff

Geography Steward done for C1: Ingest can store a row without guessing which Kerala (`32`) or which Delhi (`07` NCT of Delhi) the producer meant.

Next persona: **Methodologist** (first crew). Ingest is unblocked on geography for this slice; **do not fetch in this pass**.
