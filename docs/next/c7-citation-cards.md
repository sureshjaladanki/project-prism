# C7 citation cards

Slice: **C7**. Citizen question: How do births, deaths, child survival, and nutrition stand in the official record?

Producers on these cards: Office of the Registrar General of India / ORGI (Vital Statistics Division) for the Sample Registration System (SRS); International Institute for Population Sciences (IIPS) under MoHFW stewardship for NFHS-6 fact sheets; Ministry of Health and Family Welfare (MoHFW), Statistics Division, for Rural Health Statistics (RHS), hosted on the MoHFW HMIS portal. These are **three records** (SRS vital rates; NFHS survey indicators; RHS facility counts). The page shows each as itself. It does **not** mix SRS rates with NFHS nutrition/IMR-style indicators into one number, and it does **not** invent a blended C2+C7 product.

**C2 overlap (People slice):** Cards 1–2 reuse the same ORGI SRS artifacts already cited for C2 (Bulletin 2024 and Statistical Report 2024). Same producer series and fetch URLs/ids; this slice asks a different citizen question (health and survival, not population stock). Do not merge C2 and C7 into one product. Stable ids from C2 remain valid: `srs-bulletin-2024` / `cite-c2-srs-bulletin-2024`; `srs-statistical-report-2024` / `cite-c2-srs-statistical-report-2024`. C7 citation ids below mirror them for this slice’s trail.

Latest SRS products on these cards: **SRS Bulletin Volume 59 No. 1** (reference year **2024**, published **May 2026**) and **SRS Statistical Report 2024** (same May 2026 vintage). Latest NFHS round on these cards: **NFHS-6 (2023-24)** India and State/UT Fact Sheets (**May 2026** release; PIB 29 May 2026). Latest RHS facility-count yearbook found fetchable on HMIS Publications: **Rural Health Statistics 2021-22** (as on **31 March 2022**; PDF CreationDate January 2023). Districts parked.

---

## Citation cards

### Card 1 — SRS Bulletin 2024, Volume 59 No. 1 (birth, death, infant mortality)

```text
producer:     Office of the Registrar General of India, Vital Statistics Division (ORGI)
series:       Sample Registration System (SRS) Bulletin — estimated Birth Rate, Death Rate, Natural Growth Rate and Infant Mortality Rate
id:           NADA catalog 47150; ID SRS_Bulletin_2024_Vol_59_No_1; file SRS_Bulletin_2024_Vol_59_No_1.pdf. Tables 1–6 as listed on page 1 (Table 1 is the four rates for India and States/UTs, Total / Rural / Urban). series_id srs-bulletin-2024; citation_id cite-c7-srs-bulletin-2024 (same artifact as cite-c2-srs-bulletin-2024)
vintage:      reference_period calendar year 2024; release_date May 2026 (cover: VOLUME 59 No.1 May, 2026). NADA date published 20 May 2026.
url:          https://censusindia.gov.in/nada/index.php/catalog/47150/download/51394/SRS_Bulletin_2024_Vol_59_No_1.pdf
geography:    India; Bigger States/Union Territories; Smaller States; Union Territories — labels as printed in Table 1 (including Telangana, Ladakh, and Dadra & Nagar Haveli and Daman & Diu as one UT). Not districts.
frequency:    this issue is annual for reference year 2024 (Vol. 59 No. 1)
licence:      Not stated on the PDF. ORGI / NADA all rights reserved; not stated as CC-BY.
next_release: unknown (no date on this bulletin for the 2025 reference year)
caveat:       Survey estimates, not a census and not NFHS. Bulletin does not publish TFR or under-five mortality detail — those live on Card 2. Do not blend with Card 3 NFHS indicators. Cell-mapped: no — PDF only. Same C2 Card 3 file (~539,058 bytes, 22 September 2026).
```

Fetch host is the producing office (ORGI NADA).

Catalog: `https://censusindia.gov.in/nada/index.php/catalog/47150`. SRS listing on NADA: `https://censusindia.gov.in/nada/index.php/catalog/?tag=SRS&sort_by=year&sort_order=desc`.

### Card 2 — SRS Statistical Report 2024 (fertility, mortality including child / under-five as published)

```text
producer:     Office of the Registrar General & Census Commissioner, India (ORGI), Ministry of Home Affairs
series:       Sample Registration System (SRS) Statistical Report 2024 — fertility and mortality indicators as published (including Crude Birth Rate, Total Fertility Rate, Infant Mortality Rate, neonatal rates, and Under-five Mortality Rate)
id:           NADA catalog 47152; ID SRS_STAT_2024; file SRS_STAT_2024.pdf. Fertility: Chapter 3 and Detailed Table 3. Mortality: Chapter 4; Detailed Tables 8–11 (Table 9 “Child (Aged 0-4 years) and Infant Mortality Indicators, 2024”; Table 11 names Birth Rate, Death Rate, Infant Mortality Rate and Under-five Mortality Rate). Figures at a Glance, India — 2024. series_id srs-statistical-report-2024; citation_id cite-c7-srs-statistical-report-2024 (same artifact as cite-c2-srs-statistical-report-2024)
vintage:      reference_period calendar year 2024; PDF CreationDate 20 May 2026; NADA date published 20 May 2026.
url:          https://censusindia.gov.in/nada/index.php/catalog/47152/download/51396/SRS_STAT_2024.pdf
geography:    Preface: India and bigger States/UTs (population of 10 million and above), rural and urban, for the indicators in this report. Not a district file. NSS Natural Division maps/tables below the State/UT bar — parked.
frequency:    annual report
licence:      Not stated on the PDF. ORGI / NADA all rights reserved; not stated as CC-BY.
next_release: unknown (no date in the preface for the 2025 report)
caveat:       Same SRS family as Card 1, not NFHS. Under-five and neonatal rates are SRS definitions in this report — do not average them with Card 3 nutrition indicators. Bigger-State geography is narrower than Card 1’s full State/UT list. Cell-mapped: no — PDF only (~20,714,495 bytes).
```

Fetch host is the producing office (ORGI NADA).

Catalog: `https://censusindia.gov.in/nada/index.php/catalog/47152`.

### Card 3 — NFHS-6 (2023-24) India and State/UT Fact Sheets

```text
producer:     International Institute for Population Sciences (IIPS), Mumbai — nodal agency; survey under the stewardship of the Ministry of Health and Family Welfare (MoHFW). Suggested citation on the PDF: IIPS 2026.
series:       National Family Health Survey (NFHS-6), 2023-24 — India and State/UT Fact Sheets (101 key indicators on population, health, family planning, maternal and child health, nutrition, and related topics as printed)
id:           File “National Family Health Survey (NFHS-6) 2023-2024 Fact Sheets.pdf” (182 pages). National fact sheet: INDIA; State fact sheets for 27 States as listed in the TOC; UT fact sheets for 8 UTs as listed. series_id nfhs-6-factsheets-2023-24; citation_id cite-c7-nfhs-6-factsheets-2023-24
vintage:      reference_period survey fieldwork May 2023–December 2024 (NFHS-6); fact-sheet release May 2026 (title page); PDF CreationDate 14 May 2026 / ModDate 27 May 2026; India and States/UTs compendium released 29 May 2026 (IIPS release note; PIB PRID 2266600)
url:          https://www.nfhsiips.in/nfhsuser/assets/National%20Family%20Health%20Survey%20(NFHS-6)%202023-2024%20Fact%20Sheets.pdf
geography:    India and States/UTs as in the TOC (Andhra Pradesh through West Bengal; Andaman & Nicobar Islands; Chandigarh; Dadra & Nagar Haveli and Daman & Diu; Jammu & Kashmir; Ladakh; Lakshadweep; NCT of Delhi; Puducherry). Manipur is not in this India/State/UT fact-sheet set (producer release note: except Manipur). Urban / Rural / Total columns as published. Not districts.
frequency:    multi-year survey round (NFHS-6); this artifact is the May 2026 fact-sheet release
licence:      Not stated on the fact-sheet PDF. Government of India / IIPS survey product. Not stated as CC-BY.
next_release: unknown — no date for an NFHS-6 full national report or for NFHS-7 on the portal this run
caveat:       This is NFHS, not SRS — do not merge rates. The 101 fact-sheet indicators include child nutrition (e.g. stunting, wasting, underweight) and MCH/service measures; they do not print Neonatal / Infant / Under-five mortality rates as SRS does on Cards 1–2. Fact sheets compare NFHS-6 to NFHS-5 columns where printed — that is the producer’s own prior round, not a licence to invent a blended series. Cell-mapped: no — PDF only (~12,341,321 bytes).
```

Fetch host: official NFHS portal `nfhsiips.in` (IIPS / MoHFW). Locator (not the table): `https://www.nfhsiips.in/nfhsuser/index.php`. Companion release write-up (not the indicator tables): `https://www.nfhsiips.in/nfhsuser/assets/pdf/nfhs6%20fact%20sheet%20compendiums%20release%20writeup%20for%20website%20FINAL%2021aug26.pdf`. PIB press note (locator): `https://pib.gov.in/PressReleasePage.aspx?PRID=2266600` (29 May 2026).

TOC State list as printed: Andhra Pradesh; Arunachal Pradesh; Assam; Bihar; Chhattisgarh; Goa; Gujarat; Haryana; Himachal Pradesh; Jharkhand; Karnataka; Kerala; Madhya Pradesh; Maharashtra; Meghalaya; Mizoram; Nagaland; Odisha; Punjab; Rajasthan; Sikkim; Tamil Nadu; Telangana; Tripura; Uttar Pradesh; Uttarakhand; West Bengal. UTs: Andaman & Nicobar Islands; Chandigarh; Dadra & Nagar Haveli and Daman & Diu; Jammu & Kashmir; Ladakh; Lakshadweep; NCT of Delhi; Puducherry. **Missing from this artifact:** Manipur.

### Card 4 — Rural Health Statistics 2021-22 (facility counts)

```text
producer:     Ministry of Health and Family Welfare (MoHFW), Statistics Division
series:       Rural Health Statistics (RHS) — public health facility counts and related infrastructure / manpower statements as published (SCs, PHCs, CHCs and related tables)
id:           HMIS Publications download fileid=34; Content-Disposition filename “RHS 2021-22.pdf” (270 pages). Title page: Government of India, Ministry of Health and Family Welfare, Statistics Division, Rural Health Statistics 2021-22. State-wise facility tables begin Part 2 Section I (e.g. Statement 1 State-wise SCs, PHCs & CHCs functioning). series_id rhs-2021-22; citation_id cite-c7-rhs-2021-22
vintage:      reference_period as on 31 March 2022 (DDG preface); PDF CreationDate 2 January 2023 / ModDate 3 January 2023. Latest RHS yearbook listed on HMIS Publications menu this run (fileids 34=2021-22 down through 39=2016-17).
url:          https://hmis.mohfw.gov.in/downloadfile?fileid=34
geography:    India and States/UTs in the comparative / state-wise statements (Rural, and Urban / Tribal material as printed in the same yearbook). Section II is district-wise health-care infrastructure — parked this iteration; do not ingest district rows.
frequency:    annual yearbook (this issue: 2021-22)
licence:      Not stated on the PDF cover/preface pages opened. Government of India publication. Not stated as CC-BY.
next_release: unknown — delayed. No RHS 2022-23 or later PDF linked on the HMIS Publications menu as of 22 September 2026.
caveat:       Administrative facility counts from the MoHFW statistical system (RHS via HMIS), not SRS rates and not NFHS survey indicators. Do not use NITI Health Index, hospital star-ratings, or private insurance products as the facility record. Cell-mapped: no — PDF only (~30,074,457 bytes).
```

Fetch host: MoHFW HMIS portal (`hmis.mohfw.gov.in`) — official host for the Statistics Division RHS yearbook downloads. Portal locator: `https://hmis.mohfw.gov.in/` (Publications → RHS 2021-22).

---

## Licence and calendar artifacts (not series)

- ORGI / NADA: same house as C2 — NADA download URLs returned HTTP 200 with `Content-Disposition: attachment`; site/NADA footers all rights reserved; not CC-BY on these PDFs.
- NFHS portal `nfhsiips.in`: MoHFW / IIPS official NFHS site. Fact-sheet PDF has no printed CC-BY licence line. District fact-sheet compendiums are announced on the same portal but require guest login for download — not used on these cards.
- PIB PRID 2266600 (29 May 2026): release announcement for NFHS-6; locator only, not the indicator tables.
- HMIS RHS downloads: no login wall on `downloadfile?fileid=34` this run (HTTP 200 PDF attachment).
- CBHI National Health Profile 2023 PDF is fetchable but is a different product family (compilation) — not substituted for RHS facility counts (see rejected).
- `rchiips.org` (legacy NFHS host linked from older IIPS pages): HTTP 404 this run — do not use.
- `nfhsindia.org`: “Under construction” placeholder — do not use.

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| Blended “child survival” from SRS IMR/U5MR + NFHS stunting/IMR-style cells | Charter-out. Separate cards only. |
| NITI Aayog Health Index / SDG league tables / other NITI scorecards | Scorecards are not the record (`https://www.niti.gov.in/` 200 HTML — not used as series). |
| Hospital star-ratings; private insurance product tables | Charter-out. |
| NFHS-6 District Fact Sheet Compendiums (35 States/UTs; released Aug 2026) | District geography parked; portal requires guest login for download. |
| NFHS-6 full national report (mortality-rate chapters) | Not found as an open fetchable PDF on `nfhsiips.in` this run — fact sheets only for India/State/UT. Named hole. |
| NFHS-5 India Report (DHS Program FR375, `dhsprogram.com` 200 PDF) | Fetchable, but host is the international DHS Program, not an Indian government producer/host. Reject as source of record. |
| NFHS-5 factsheets / India report on `rchiips.org` | Legacy URLs return 404; site dead this run. |
| `nfhsindia.org` | Under-construction placeholder (200 HTML), not a statistical release. |
| IIPS `National_Dissemination.pdf` (Phase-2 key findings link on iipsindia.ac.in) | HTTP 404 this run. |
| CBHI National Health Profile 2023 (`cbhidghs.mohfw.gov.in` …/NHP-2023-Last-Final.pdf 200 PDF) | Official CBHI compilation; not the RHS facility-count yearbook named for this charter. Keep Card 4 = RHS. |
| HMIS live dashboards / facility master as the statistical yearbook | Portal UI only; source of record for printed counts is RHS PDF Card 4. |
| RHS years older than 2021-22 (HMIS fileids 35–39) | Superseded by 2021-22 for latest facility stock on that menu. |
| SRS Abridged Life Tables; SRS Cause of Death; Maternal Mortality special bulletin | Related ORGI products; C7 vital rates of record are Cards 1–2. |
| Civil Registration System (CRS) | Registration completeness series — not SRS Bulletin/Statistical Report. |
| World Bank, UNICEF, WHO, UNDP, news, think-tank republishes of NFHS/SRS | Secondary; not the producing office. |
| data.gov.in NFHS/RHS extracts | CKAN API returned HTML/not usable this run; no substitute open artifact verified that replaces Cards 3–4. |

---

## Geography Steward

**Required: yes.** Cards 1–4 are not all-India-only: SRS Bulletin Table 1 and NFHS-6 fact sheets publish India plus States/UTs; SRS Statistical Report uses bigger States/UTs; RHS has state-wise facility statements. Geography Steward must set the map before Ingest pulls. Do not recode labels here.

Frames to expect:

- **Card 1 (SRS Bulletin 2024):** India; Bigger States/UTs; Smaller States; UTs as printed (includes Telangana, Ladakh, merged DNH&DD). Same frame family as C2 Card 3.
- **Card 2 (SRS Statistical Report 2024):** India and bigger States/UTs only (population ≥10 million). Same frame family as C2 Card 4.
- **Card 3 (NFHS-6 fact sheets):** India + 27 States + 8 UTs as in TOC; **Manipur absent**. Urban/Rural/Total.
- **Card 4 (RHS 2021-22):** State/UT-wise statements for facilities; district Section II parked.

**Parked this iteration:** NFHS district fact sheets; RHS Section II district tables; any district SRS file.

Crosswalk between SRS bigger-State vs full State/UT vs NFHS (no Manipur) vs RHS labels: none invented here — Geography Steward owns it.

---

## Handoff

Next persona: **Geography Steward** (state/UT-shaped artifacts on all four cards). Then Methodologist (SRS vs NFHS disagreement; NFHS fact sheets lack IMR/U5MR cells; RHS lag). **Ingest Engineer must not fetch until** these citation cards exist (they do) **and** `geography_frame` exists for C7.

Ingest fetches the four named PDFs on the cards. Keep SRS and NFHS as separate series. Do not pull district NFHS/RHS sections. Do not write files into the git tree until that ingest job. Do not use NITI Health Index or DHS FR375 as the record.

---

## HTTP status (verified GET, 22 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `.../catalog/47150/download/51394/SRS_Bulletin_2024_Vol_59_No_1.pdf` | 200 | PDF `%PDF` (539,058 bytes; `Content-Disposition` attachment) |
| `.../catalog/47152/download/51396/SRS_STAT_2024.pdf` | 200 | PDF `%PDF` (20,714,495 bytes; attachment) |
| `https://censusindia.gov.in/nada/index.php/catalog/47150` | 200 | HTML (catalog locator) |
| `https://censusindia.gov.in/nada/index.php/catalog/47152` | 200 | HTML (catalog locator) |
| `https://www.nfhsiips.in/nfhsuser/assets/National%20Family%20Health%20Survey%20(NFHS-6)%202023-2024%20Fact%20Sheets.pdf` | 200 | PDF `%PDF` (12,341,321 bytes) |
| `https://www.nfhsiips.in/nfhsuser/assets/pdf/nfhs6%20fact%20sheet%20compendiums%20release%20writeup%20for%20website%20FINAL%2021aug26.pdf` | 200 | PDF `%PDF` (93,560 bytes; release note, not the tables) |
| `https://www.nfhsiips.in/nfhsuser/index.php` | 200 | HTML (portal locator) |
| `https://hmis.mohfw.gov.in/downloadfile?fileid=34` | 200 | PDF `%PDF` (30,074,457 bytes; `Content-Disposition` filename `RHS 2021-22.pdf`) |
| `https://hmis.mohfw.gov.in/` | 200 | HTML (portal; Publications lists RHS years) |
| `https://pib.gov.in/PressReleasePage.aspx?PRID=2266600` | 200 | HTML (PIB locator, 29 May 2026) |
| `https://cbhidghs.mohfw.gov.in/sites/default/files/NHP/NHP-2023-Last-Final.pdf` | 200 | PDF (NHP — rejected as RHS substitute) |
| `https://rchiips.org/nfhs/` | 404 | HTML |
| `https://dhsprogram.com/pubs/pdf/FR375/FR375.pdf` | 200 | PDF (DHS host — rejected as source of record) |
| `https://nfhsindia.org/` | 200 | HTML (“Under construction”) |
| `https://www.iipsindia.ac.in/content/nfhs-project` | 200 | HTML (links; several legacy PDF targets 404) |
| `https://www.niti.gov.in/` | 200 | HTML (not used as series) |
