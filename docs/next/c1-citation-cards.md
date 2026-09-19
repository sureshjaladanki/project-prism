# C1 citation cards

Slice: **C1**. Citizen question: How fast are retail prices rising in India, including food?

Producer for all cards below: National Statistics Office (NSO), Price Statistics Division, Ministry of Statistics and Programme Implementation (MoSPI). Website product id **9** (`Consumer Price Index (CPI)`). Rural, Urban and Combined are one published family — not a merge invented here.

Latest month on these cards: **August 2026 (Provisional)** and **July 2026 (Final)** in the same monthly workbook; press note dated **14 September 2026**. Comparable run on this base: **January 2025 onward** (Base 2024=100). Do not stitch the 2012=100 series onto these cards.

---

## Citation cards

### Card 1 — CPI General (Rural, Urban, Combined), Base 2024=100

```text
producer:     National Statistics Office, Price Statistics Division, Ministry of Statistics and Programme Implementation (MoSPI)
series:       Consumer Price Index (CPI) General — Rural, Urban and Combined (Base 2024=100)
id:           MoSPI product_id 9; latestRelease id 170 “Press release of CPI for the month of August 2026”; Documents id 315 “CPI Data - August 2026 Based on Base Year 2024” file Data_August_CPI_2026_14092026.xlsx sheet General; companion Annex.xlsx sheet Annexure-III (State/UT wise general). Time series of record for Jan 2025–Dec 2025: CPI_2024-Jan2025-Dec2025.xlsx sheet General; for Jan 2026: CPI_2024-Jan2026.xlsx sheet General.
vintage:      reference_period August 2026 (Provisional) and July 2026 (Final) in the monthly workbook; release_date 14 September 2026 (press note). Time-series files cover January 2025–December 2025 and January 2026.
url:          https://www.mospi.gov.in/uploads/documents/productChartTable/1789491098345-Data_August_CPI_2026_14092026.xlsx
geography:    All India and States/UTs as labelled in State Name (37 labels including All India); Sector = Rural / Urban / Combined as published. Not districts.
frequency:    monthly
licence:      Not stated on the workbook or press PDF. MoSPI Copyrights Policy: reproduce accurately, not in a derogatory or misleading context, source acknowledged. GSDD 2026 Category A (open access) lists Consumer Price Index (CPI). Not stated as CC-BY.
next_release: 12 October 2026 (CPI for September 2026), per the 14 September 2026 press note; ARC 2026-27 also lists 12th Oct All India CPI.
caveat:       Latest month is Provisional; Combined is a published sector, not a user merge. Chandigarh Rural is withheld (dash) in Annexure-III. Base-year break vs 2012=100. Districts are not in this file.
```

Latest-month source of record (same release): press PDF `https://www.mospi.gov.in/uploads/latestreleasesfiles/1789382372004-Press%20Release%20of%20CPI%20for%20August%202026.pdf` (title: *PRESS RELEASE OF CONSUMER PRICE INDEX ON BASE 2024=100 FOR AUGUST, 2026*). Duplicate copy: `https://www.mospi.gov.in/uploads/latestReleases/latest_release_1789381904344_6c792dcf-8a9f-4fca-93d3-99d833bdb358_Press_Release_of_CPI_for_August_2026.pdf`. Annex workbook: `https://www.mospi.gov.in/uploads/documents/productChartTable/1789491131821-Annex.xlsx`.

Time-series workbooks (same series, Base 2024=100):

- `https://www.mospi.gov.in/uploads/documents/CPI/CPI_2024-Jan2025-Dec2025.xlsx`
- `https://www.mospi.gov.in/uploads/documents/CPI/CPI_2024-Jan2026.xlsx`

Later months appear as further “CPI Data – {Month} Based on Base Year 2024” files on product 9 Documents. Columns on sheet General: Base Year, State Code, State Name, Sector, year, month, index, inflation (%), status (F/P).

### Card 2 — Consumer Food Price Index (CFPI) / CPI Group Food (01.1)

```text
producer:     National Statistics Office, Price Statistics Division, MoSPI
series:       Consumer Food Price Index (CFPI) — Rural, Urban and Combined; same values as CPI Group name “Food”, Group code 01.1 (Base 2024=100)
id:           Same monthly workbook as Card 1, sheet Group, Group Name = Food / Group code 01.1; press note Key Statistics table “CFPI”; Annex.xlsx sheet Annexure-II row 01.1 Food. Time series: CPI_2024-Jan2025-Dec2025.xlsx and CPI_2024-Jan2026.xlsx sheet Group.
vintage:      reference_period August 2026 (Provisional) and July 2026 (Final); release_date 14 September 2026
url:          https://www.mospi.gov.in/uploads/documents/productChartTable/1789491098345-Data_August_CPI_2026_14092026.xlsx
geography:    All India and States/UTs as in State Name; Sector = Rural / Urban / Combined. Not districts.
frequency:    monthly
licence:      Same as Card 1 (not on the artifact; GSDD 2026 Category A; attribution required; not CC-BY)
next_release: 12 October 2026 (same CPI release as Card 1)
caveat:       CFPI is not the same as Division “Food and beverages” (01), which also includes beverages and food-processing services. Use Group Food 01.1 / the press CFPI table for the named food index. Latest month Provisional.
```

### Card 3 — CPI Division and Group indexes (COICOP 2018), including Food and beverages

```text
producer:     National Statistics Office, Price Statistics Division, MoSPI
series:       CPI Division indexes and CPI Group indexes, Rural / Urban / Combined (Base 2024=100), COICOP 2018 (12 Divisions, 43 Groups)
id:           Same monthly workbook as Card 1, sheets Division and Group; press Annexure-I (division) and Annexure-II (group); Documents id 314 Annex.xlsx. Time series: CPI_2024-Jan2025-Dec2025.xlsx and CPI_2024-Jan2026.xlsx sheets Division and Group.
vintage:      reference_period August 2026 (Provisional) and July 2026 (Final); release_date 14 September 2026
url:          https://www.mospi.gov.in/uploads/documents/productChartTable/1789491098345-Data_August_CPI_2026_14092026.xlsx
geography:    All India and States/UTs as in State Name; Sector = Rural / Urban / Combined. Not districts. Not city/centre rankings.
frequency:    monthly
licence:      Same as Card 1 (not on the artifact; GSDD 2026 Category A; attribution required; not CC-BY)
next_release: 12 October 2026 (same CPI release as Card 1)
caveat:       Division 01 is “Food and beverages”; food-only is Card 2. Item and Subclass sheets exist in the same workbook — do not use them to rank cities. Some item indices on eSankhyiki are thin-sample (press note warning); this slice uses Division/Group/General as published.
```

Division names as printed (August 2026 Annexure-I): Food and beverages; Paan, tobacco and intoxicants; Clothing and footwear; Housing, water, electricity, gas and other fuels; Furnishings, household equipment and routine household maintenance; Health; Transport; Information and communication; Recreation, sport and culture; Education services; Restaurants and accommodation services; Personal care, social protection and miscellaneous goods and services.

### Card 4 — CPI Back Series Index and Inflation (Base 2024=100, linked)

```text
producer:     National Statistics Office, Price Statistics Division, MoSPI
series:       CPI Back Series Index Inflation Based on Base Year 2024 (linked General only)
id:           Documents id 290; file CPI_2024-Back-Series-Index-Inflation.xlsx sheet Sheet1; columns Base Year, State code, State name, Sector, Year, Month, Group, Index, Inflation (%)
vintage:      reference_period January 2013 onward as rows in the file (All India General); this file’s own release date is not printed on the sheet — treat as the MoSPI product-9 Documents vintage, not the August 2026 monthly release
url:          https://www.mospi.gov.in/uploads/documents/CPI/CPI_2024-Back-Series-Index-Inflation.xlsx
geography:    All India only in the opened rows (State name = All India, State code 00); Sector = Rural / Urban / Combined; Group = General
frequency:    monthly
licence:      Same as Card 1 (not on the artifact; GSDD 2026 Category A; attribution required; not CC-BY)
next_release: unknown (not a monthly press product; no date on the file)
caveat:       Linked / back-cast onto 2024=100 — not independently compiled 2024-basket observations before the new series. Do not stitch this to the 2012=100 series as if they were one. All India only in this file; no State/UT rows in the previewed sheet. Inflation (%) is blank on early rows.
```

Use Cards 1–3 for the charter’s comparable run on the current series (from January 2025). Card 4 is only the producer’s own linked back series, with the break stated.

---

## Licence and calendar artifacts (not series)

- MoSPI Copyrights Policy (site API text): reproduce following GSDD 2026; source must be prominently acknowledged.
- GSDD 2026 Gazette PDF: `https://www.mospi.gov.in/uploads/acts_and_policies/acts_and_policies1778231030122_a1a3ee77-e36d-4895-8da5-b294751cbb1a_272304_(1).pdf` — Category A (open access) explicitly lists Consumer Price Index (CPI).
- Advance Release Calendar 2026-27 (updated till August 2026): `https://www.mospi.gov.in/uploads/documents/releaseCalender/1788266096813-ARC%202026-27%20updated%20till%20August%202026.pdf`
- National Metadata Structure PDF on the site still describes the older grouping (NSS 68th round weights / six groups). Live 2024=100 releases use COICOP 2018 (product-9 metadata and August 2026 annexes). Methodologist owns that disagreement.

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| Wholesale Price Index (WPI), Office of the Economic Adviser / DPIIT (`eaindustry.nic.in` 200) | Wholesale, not MoSPI CPI retail. Charter named CPI. |
| CPI-IW (Labour Bureau) (`labourbureau.gov.in` 200) | Industrial workers; different producer, population and basket. |
| CPI-AL / CPI-RL (Labour Bureau) | Agricultural / rural labour; not NSO CPI Combined. |
| Retail petrol / diesel pump prices (PPAC `ppac.gov.in` 200) | Not the CPI series. CPI includes selected fuel items in the basket (press note: petrol, diesel and LPG price reference is the 15th of the month). |
| City / centre rankings | Charter-out. Collection uses 1407 urban markets and 1465 villages; that is not a city-ranking series. Press “top five States” tables are not a series to ingest for ranking. |
| District files | None on product 9. Prices are collected covering States/UTs; published files stop at State/UT. Districts parked. |
| CPI UNME (product-9 “more data”) | Discontinued urban non-manual employees series; not current CPI Combined. |
| CPI Base 2012=100 (including `State-wise group indices December 2025` PDF, still printed Base 2012=100) | Previous series. Base-year break. Do not stitch onto 2024=100. |
| CPI Base 2010=100 | Older still; product metadata remnant only. |
| World Bank, IMF, UNDP, CMIE, news, think tanks, NITI scorecards, data.gov.in republishes | Not the producing office. |
| eSankhyiki HTML (`https://esankhyiki.mospi.gov.in/macroindicators?product=cpi` 200 HTML) | MoSPI portal, not a named PDF/XLSX. Press points here for state/item download; Ingest can use the workbooks on Cards 1–3 instead. |
| `https://cpi.mospi.gov.in/` (CPI warehouse) | Connection timed out (no HTTP status). Do not use. |

---

## Geography Steward

**Required: yes.** Cards 1–3 are not all-India-only: sheet General / Division / Group and Annexure-III publish All India plus States and Union Territories under the producer’s `State Name` labels (36 State/UT names plus All India). Geography Steward must set the map before Ingest pulls. Do not recode labels here.

Units on the files: All India; Andaman And Nicobar Islands; Andhra Pradesh; Arunachal Pradesh; Assam; Bihar; Chandigarh; Chhattisgarh; Goa; Gujarat; Haryana; Himachal Pradesh; Jammu And Kashmir; Jharkhand; Karnataka; Kerala; Ladakh; Lakshadweep; Madhya Pradesh; Maharashtra; Manipur; Meghalaya; Mizoram; NCT of Delhi; Nagaland; Odisha; Puducherry; Punjab; Rajasthan; Sikkim; Tamil Nadu; Telangana; The Dadra And Nagar Haveli And Daman And Diu; Tripura; Uttar Pradesh; Uttarakhand; West Bengal. Sectors Rural / Urban / Combined. **Missing / parked:** districts and below (not in these artifacts). Some Rural cells are withheld (Chandigarh Rural = “-” in Annexure-III). Card 4 is All India only.

---

## Handoff

Next persona: **Geography Steward** (state/UT rows exist). Then Methodologist. **Ingest Engineer must not fetch until** this citation card exists (it does) **and** `geography_frame` exists — the artifacts are not all-India with no sub-national rows (`docs/data-pipeline.md` Stage 1 preconditions).

No login wall on the named PDF/XLSX URLs. Terms (GSDD 2026 Category A plus copyright acknowledgement) do not forbid the pull; they require accurate reproduction and source credit. Ingest fetches the workbooks/PDFs on the cards, not the React homepage and not eSankhyiki HTML.

---

## HTTP status (verified GET, 16 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `.../1789491098345-Data_August_CPI_2026_14092026.xlsx` | 200 | XLSX (magic `PK`) |
| `.../1789491131821-Annex.xlsx` | 200 | XLSX |
| `.../1789382372004-Press Release of CPI for August 2026.pdf` | 200 | PDF `%PDF-1.7` |
| `.../latest_release_1789381904344_..._Press_Release_of_CPI_for_August_2026.pdf` | 200 | PDF |
| `.../CPI/CPI_2024-Jan2025-Dec2025.xlsx` | 200 | XLSX |
| `.../CPI/CPI_2024-Jan2026.xlsx` | 200 | XLSX |
| `.../CPI/CPI_2024-Back-Series-Index-Inflation.xlsx` | 200 | XLSX |
| `.../ARC 2026-27 updated till August 2026.pdf` | 200 | PDF |
| `.../272304_(1).pdf` (GSDD 2026) | 200 | PDF |
| `.../1787833429671-National_Metadata_Structure_for_CPI.pdf` | 200 | PDF |
| `https://www.mospi.gov.in/api/product/get-product-data` POST `{product_id:9, lang:en}` | 200 | JSON (locator only, not the series artifact) |
| `https://cpi.mospi.gov.in/` | no response (timeout) | — |
