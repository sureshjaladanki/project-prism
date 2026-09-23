# C7 geography frame

Persona: Geography Steward. Slice: **C7** (How do births, deaths, child survival, and nutrition stand in the official record?).

Input locked: `docs/next/c7-citation-cards.md`. Charter geography: national and state/UT as published; districts parked (NFHS district fact sheets; RHS Section II; any district SRS).

Store a row on **the producer’s name as printed on that artifact**. Do not match on spelling alone. Do not join an SRS 2024 stub to an NFHS-6 fact-sheet title or an RHS 2021-22 row because the English looks similar. Do not merge SRS rates with NFHS indicators by geography either.

Residence (Total / Rural / Urban) on SRS and NFHS is **not** geography. Facility type (SC / PHC / CHC) on RHS is **not** geography.

**Districts:** parked. **Crosswalk between frames: none.** SRS Bulletin, SRS Statistical Report (bigger only), NFHS-6 fact sheets, and RHS 2021-22 are four maps. Cards 1–2 reuse the same ORGI artifacts as C2 Cards 3–4 — same maps as C2 Frames C–D ([`docs/archive/c2-geography-frame.md`](../archive/c2-geography-frame.md)); do not invent a second SRS geography for C7.

Four frames.

---

## Frame A — SRS Bulletin 2024, all Table 1 units (Card 1)

Binds: Card 1 — same artifact and map as C2 Frame C.

Artifact: `SRS_Bulletin_2024_Vol_59_No_1.pdf` (NADA catalog 47150). Groups as printed: **India**; **Bigger States/Union Territories**; **Smaller States**; **Union Territories**.

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
  districts and below (parked)
breaks:         Same post-reorganisation 2024 map as C2 Frame C. Manipur* is a
                sample footnote, not a second unit. Do not recode onto Frames B–D.
crosswalk:      none — do not recode (including onto C2 Census frames)
```

---

## Frame B — SRS Statistical Report 2024, bigger States/UTs (Card 2)

Binds: Card 2 — same artifact and map as C2 Frame D. NSS Natural Division tables parked.

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
  all Frame A Smaller States
  all Frame A Union Territories (including Ladakh and merged DNH–DD)
  districts; NSS Natural Division rows (parked)
breaks:         Narrower than Frame A. Do not fill smaller States/UTs from the
                Bulletin and call it the Statistical Report.
crosswalk:      none — do not recode
```

A national figure on this frame must still say smaller States, UTs, and districts are missing from the report’s main tables.

---

## Frame C — NFHS-6 (2023-24) India and State/UT Fact Sheets (Card 3)

Binds: Card 3 — Fact Sheets PDF TOC (India; 27 States; 8 UTs). Urban / Rural / Total columns are not geography.

```text
frame:          Union | state | UT
vintage:        2023-24 (fieldwork); fact-sheet release May 2026
code_system:    none
units_included:
  India
  States:
    Andhra Pradesh
    Arunachal Pradesh
    Assam
    Bihar
    Chhattisgarh
    Goa
    Gujarat
    Haryana
    Himachal Pradesh
    Jharkhand
    Karnataka
    Kerala
    Madhya Pradesh
    Maharashtra
    Meghalaya
    Mizoram
    Nagaland
    Odisha
    Punjab
    Rajasthan
    Sikkim
    Tamil Nadu
    Telangana
    Tripura
    Uttar Pradesh
    Uttarakhand
    West Bengal
  Union Territories:
    Andaman & Nicobar Islands
    Chandigarh
    Dadra & Nagar Haveli and Daman & Diu
    Jammu & Kashmir
    Ladakh
    Lakshadweep
    NCT of Delhi
    Puducherry
units_missing:
  Manipur (producer release note: except Manipur — not in this fact-sheet set)
  districts and below (district fact-sheet compendiums parked; login wall)
breaks:         NFHS-6 fact-sheet map. Manipur absence is a coverage hole, not a
                recode from Frame A. Do not fill Manipur from SRS or RHS.
crosswalk:      none — do not recode onto Frames A, B, or D
```

---

## Frame D — Rural Health Statistics 2021-22 (Card 4)

Binds: Card 4 — state-wise / comparative facility statements (Part 2 Section I). **Section II district-wise infrastructure parked** — do not ingest.

Artifact: `RHS 2021-22.pdf` via HMIS `downloadfile?fileid=34`. Reference period as on **31 March 2022**.

```text
frame:          Union | state | UT
vintage:        2021-22 (as on 31 March 2022)
code_system:    none
units_included:
  India and States/UTs as labelled in Part 2 Section I comparative / state-wise
  statements (Ingest stores stubs exactly as printed on Statement 1 and companions —
  confirm on open; expect post-reorganisation labels including Telangana, Ladakh,
  and merged Dadra & Nagar Haveli and Daman & Diu where the yearbook prints them)
units_missing:
  districts and below (Section II — parked)
  RHS years after 2021-22 (named hole on the citation card — not on this map)
breaks:         Facility stock map as of 31 March 2022 — several years behind SRS 2024
                and NFHS-6 fieldwork. Do not recode onto Frames A–C. Do not use
                district Section II to fake a state total.
crosswalk:      none — do not recode
```

---

## Handoff

Next persona: **Methodologist** (SRS vs NFHS disagreement; fact sheets lack NMR/IMR/U5MR; RHS lag; Manipur hole on NFHS). Do not ingest until Platform names the refresh contract for this slice. Keep SRS, NFHS, and RHS as separate series.
