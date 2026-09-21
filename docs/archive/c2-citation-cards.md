# C2 citation cards

Slice: **C2**. Citizen question: How many people live in India, where, and how is that changing?

Producers on these cards: Office of the Registrar General & Census Commissioner, India (ORGI) for Census of India 2011 tables and the Sample Registration System (SRS); National Commission on Population, Ministry of Health and Family Welfare (MoHFW) for the 2011–2036 projection report. These are three records. The page shows each as itself. It does not pick a winner or invent a blended “India today” figure.

Source class (re-carded **18 September 2026**): identify the data requirement; identify the producing office; fetch from official government agencies that can source that dependency (producing office first preference, not the only host); quote producer, series, date, **and fetch source** if the host is not the producer. A ministry site, `data.gov.in`, NITI as a host of that table, or another `*.gov.in` is in when it supplies the **same** dependency. News, private polls, World Bank/UN/IMF/UNDP, and NITI **scorecards** are out. MoSPI is not the producer of Census/SRS; it (or `data.gov.in`) may host an ORGI file — then producer stays ORGI.

Census of record on these cards: **Census 2011** (reference date 00:00 hours, 1 March 2011). As of **18 September 2026** there is no published Census 2021 or Census 2027 headcount. Census 2027 houselisting is notified for 1 April 2026–30 September 2026; that is not a population total. Do not paper a 2011 count into a current headcount.

Latest SRS products on these cards: **SRS Bulletin Volume 59 No. 1** (reference year **2024**, published **May 2026**) and **SRS Statistical Report 2024** (same May 2026 vintage). Latest official projection on these cards: **Population Projections for India and States 2011–2036**, Report of the Technical Group, **November 2019** (NCP / MoHFW). Label it as a projection, not a census.

Cell-mapped status after this search (xlsx/csv of the **same** series, any official government host): Card 1 **yes** (producer xlsx). Cards 2–5 **no** — Card 2 remains OLE `.xls` plus companion PDF; Cards 3–5 remain PDF. Fetch URLs for all five cards are unchanged.

Stable ids (unchanged): `census-2011-pca-sd` / `cite-c2-census-2011-pca-sd`; `census-2011-a02-decadal` / `cite-c2-census-2011-a02-decadal`; `srs-bulletin-2024` / `cite-c2-srs-bulletin-2024`; `srs-statistical-report-2024` / `cite-c2-srs-statistical-report-2024`; `ncp-projections-2011-2036-table8` / `cite-c2-ncp-projections-2011-2036-table8`.

---

## Citation cards

### Card 1 — Census 2011 Primary Census Abstract (PCA SD), India and State/UT totals

```text
producer:     Office of the Registrar General & Census Commissioner, India (ORGI), Ministry of Home Affairs
series:       Census of India 2011 — Primary Census Abstract (PCA SD): population, households, and related PCA columns as published
id:           NADA catalog 6191; Reference ID PC11_PCA-SD; file DDW_PCA0000_2011_Indiastatedist.xlsx sheet Sheet1. Population of record: columns TOT_P, TOT_M, TOT_F for Level = India or STATE (not DISTRICT). TRU = Total / Rural / Urban as published. series_id census-2011-pca-sd; citation_id cite-c2-census-2011-pca-sd
vintage:      reference_period Census of India 2011 (00:00 hours, 1 March 2011); workbook has no printed release date; NADA catalog created/last modified 19 January 2021. Original paper PCA India release is not on this file — do not treat the NADA date as Census day.
url:          https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx
geography:    India and States/UTs as labelled in Name where Level = India or STATE (35 STATE labels plus India). TRU = Total / Rural / Urban. File also contains DISTRICT rows — parked this iteration; do not ingest them.
frequency:    decennial census (no later census totals published)
licence:      Not stated on the workbook. ORGI site footer: all rights reserved. NADA: © 2026, ORGI Digital Library, All Rights Reserved. Not stated as CC-BY.
next_release: unknown — delayed. Census 2021 population totals were not published. Census 2027 is notified (houselisting 1 April 2026–30 September 2026); no 2027 count on these cards.
caveat:       This is a 2011 count, about fifteen years behind 2026 — say so on the page. District rows are in the same file; stop at India / STATE. 2011 labels predate Telangana as a State row and Ladakh as a UT row. Sheets Sheet2 and Sheet3 are empty in this file. Cell-mapped: yes (xlsx).
```

Fetch host is the producing office (ORGI NADA).

Catalog page (locator, not the table): `https://censusindia.gov.in/nada/index.php/catalog/6191`. Listing among Census tables: `https://censusindia.gov.in/census.website/data/census-tables` (filter Primary Census Abstract).

Same PCA family, other official host (not the fetch URL): `data.gov.in` catalog [Primary Census Abstract 2011 - India and States](https://www.data.gov.in/catalog/primary-census-abstract-2011-india-and-states-0) names ORGI as contributor (NDSAP). Resource [Primary Census Abstract 2011 - India](https://www.data.gov.in/resource/primary-census-abstract-2011-india) is “Download (Through URL)” to `https://censusindia.gov.in/datagov/PCA0000_2011_MDDS.xls` (OLE `.xls`, 110,592 bytes, 18 September 2026) — a different filename and format from the NADA xlsx. Keep the NADA xlsx: it is the producing-office file Ingest can read as cells. Do not switch Card 1 to the MDDS `.xls`.

Sheet1 columns used for the charter’s headcount: State, District, Level, Name, TRU, No_HH, TOT_P, TOT_M, TOT_F (plus other PCA columns on the same rows). Ingest keeps `Level` in {`India`, `STATE`} only.

### Card 2 — Census 2011 A-02 decadal variation in population since 1901 (India and State/UT)

```text
producer:     Office of the Registrar General & Census Commissioner, India (ORGI)
series:       Census of India 2011 — Table A-02: Decadal variation in population since 1901
id:           NADA catalog 43333 (title: A-02: Decadal variation in population 1901-2011, India); files 00 A 2-India.pdf and 00 A 2-India.xls. Table A-2 as printed: India/State/Union Territory by Census Year, Persons, variation since the preceding census (absolute and percentage), Males, Females. State rows use District Code 000. series_id census-2011-a02-decadal; citation_id cite-c2-census-2011-a02-decadal
vintage:      reference_period Census years 1901–2011 as rows (2011 is the last year in the table); NADA catalog created/last modified 1 June 2022. No separate press date on the PDF.
url:          https://censusindia.gov.in/nada/index.php/catalog/43333/download/47001/00%20A%202-India.xls
geography:    INDIA and States/UTs as labelled in the India/State/Union Territory column (District Code 000). Not a district table in this India artifact. Some early years N.A. (e.g. Arunachal Pradesh before 1961).
frequency:    decennial (last year in the table: 2011)
licence:      Same as Card 1 (not on the artifact; ORGI / NADA all rights reserved; not CC-BY)
next_release: unknown — delayed (same Census hole as Card 1)
caveat:       Historical census counts, not an SRS rate and not a 2026 headcount. Footnotes in the table (*, $, @, #, +) are producer breaks — Methodologist owns them. Do not stitch to Card 5 projections. Cell-mapped: no — table of record is OLE .xls (magic D0 CF 11 E0); companion PDF is not a substitute if a spreadsheet exists. 18 September 2026 search found no official xlsx/csv of this same A-02 India table on NADA, data.gov.in, mospi.gov.in, mohfw.gov.in, nhm.gov.in, niti.gov.in, or censusindia.gov.in/datagov. Keep the .xls of record.
```

Fetch host is the producing office (ORGI NADA).

Companion PDF (same catalog, not the table of record): `https://censusindia.gov.in/nada/index.php/catalog/43333/download/47002/00%20A%202-India.pdf`. Catalog: `https://censusindia.gov.in/nada/index.php/catalog/43333`. NADA catalog 43333 lists only those two files.

### Card 3 — SRS Bulletin 2024, Volume 59 No. 1 (birth, death, infant mortality)

```text
producer:     Office of the Registrar General of India, Vital Statistics Division (ORGI)
series:       Sample Registration System (SRS) Bulletin — estimated Birth Rate, Death Rate, Natural Growth Rate and Infant Mortality Rate
id:           NADA catalog 47150; ID SRS_Bulletin_2024_Vol_59_No_1; file SRS_Bulletin_2024_Vol_59_No_1.pdf. Tables 1–6 as listed on page 1 (Table 1 is the four rates for India and States/UTs, Total / Rural / Urban). series_id srs-bulletin-2024; citation_id cite-c2-srs-bulletin-2024
vintage:      reference_period calendar year 2024; release_date May 2026 (cover: VOLUME 59 No.1 May, 2026). NADA date published 20 May 2026.
url:          https://censusindia.gov.in/nada/index.php/catalog/47150/download/51394/SRS_Bulletin_2024_Vol_59_No_1.pdf
geography:    India; Bigger States/Union Territories; Smaller States; Union Territories — labels as printed in Table 1 (including Telangana, Ladakh, and Dadra & Nagar Haveli and Daman & Diu as one UT). Not districts.
frequency:    this issue is annual for reference year 2024 (Vol. 59 No. 1)
licence:      Same as Card 1 (not on the PDF; ORGI / NADA all rights reserved; not CC-BY)
next_release: unknown (no date on this bulletin for the 2025 reference year)
caveat:       Survey estimates, not a census count. Bulletin does not publish TFR — that is Card 4. “Bigger States/UTs” means population more than 10 million as per Census 2011. Manipur estimates based on 130 SRS units (producer footnote). Smaller States/UTs IMR by sex and residence uses three-year period 2022–24 (Table 5 note). Do not add Card 1 population to these rates to invent a 2024 headcount. Cell-mapped: no — PDF only on NADA. 18 September 2026 search found no official xlsx/csv of this 2024 bulletin. data.gov.in SRS files found are other years (e.g. 2016 key indicators, 2020 IMR, MMR 2018–20) or state SHB reprints — not this product.
```

Fetch host is the producing office (ORGI NADA).

Catalog: `https://censusindia.gov.in/nada/index.php/catalog/47150`. SRS listing on NADA: `https://censusindia.gov.in/nada/index.php/catalog/?tag=SRS&sort_by=year&sort_order=desc`.

### Card 4 — SRS Statistical Report 2024 (fertility including TFR, and mortality as published)

```text
producer:     Office of the Registrar General & Census Commissioner, India (ORGI), Ministry of Home Affairs
series:       Sample Registration System (SRS) Statistical Report 2024 — fertility and mortality indicators as published (including Crude Birth Rate and Total Fertility Rate)
id:           NADA catalog 47152; ID SRS_STAT_2024; file SRS_STAT_2024.pdf (363 pages). Fertility: Chapter 3 and Detailed Table 3 “Fertility Indicators, 2024” (contents: pages 228–234). Mortality: Chapter 4 and Detailed Tables 8–11. Figures at a Glance, India — 2024 in the front matter. series_id srs-statistical-report-2024; citation_id cite-c2-srs-statistical-report-2024
vintage:      reference_period calendar year 2024; PDF CreationDate 20 May 2026; NADA date published 20 May 2026.
url:          https://censusindia.gov.in/nada/index.php/catalog/47152/download/51396/SRS_STAT_2024.pdf
geography:    Preface: India and bigger States/UTs (population of 10 million and above), rural and urban, for the indicators in this report. Not a district file. NSS Natural Division maps/tables in this PDF are below the charter’s State/UT bar — parked this iteration.
frequency:    annual report
licence:      Same as Card 1 (not on the PDF; ORGI / NADA all rights reserved; not CC-BY)
next_release: unknown (no date in the preface for the 2025 report)
caveat:       Same SRS family as Card 3, not a substitute census. TFR and other fertility measures live here, not in the Bulletin. Bigger-State geography is narrower than Card 3’s full State/UT list. Do not blend with Card 1 or Card 5. Cell-mapped: no — PDF only (~20,714,495 bytes). 18 September 2026 search found no official xlsx/csv of this 2024 statistical report.
```

Fetch host is the producing office (ORGI NADA).

Catalog: `https://censusindia.gov.in/nada/index.php/catalog/47152`.

### Card 5 — Official population projections 2011–2036 (Technical Group / NCP)

```text
producer:     National Commission on Population, Ministry of Health & Family Welfare (Technical Group on Population Projections)
series:       Census of India 2011 — Population Projections for India and States 2011–2036 (projections, not a census)
id:           Report of the Technical Group on Population Projections, November 2019. Population-of-record table: TABLE-8 “Projected Total Population by Sex as on 1st March - 2011 - 2036 : India, States and Union Territories* ('000)”. Companion in the same PDF: TABLE-11 (1st July) — same report, different reference day; do not merge the two into one series. series_id ncp-projections-2011-2036-table8; citation_id cite-c2-ncp-projections-2011-2036-table8
vintage:      reference_period projected years 2011–2036 as on 1st March in Table 8 (Table 11 as on 1st July); report dated November 2019; PDF CreationDate 21 November 2019. Base is Census 2011 (smoothed), not a 2019 count.
url:          https://nhm.gov.in/New_Updates_2018/Report_Population_Projection_2019.pdf
geography:    India, States and Union Territories as labelled in Table 8 (including Jammu & Kashmir*(UT) and Telangana). Some appendix tables exclude Goa; detailed tables combine North-East States excluding Assam. Not districts.
frequency:    one-off report (not an annual census)
licence:      Not stated on the title pages fetched. Government of India report. Not stated as CC-BY.
next_release: unknown — no successor Technical Group report found on censusindia.gov.in NADA (search 18 September 2026) or at this NHM path’s siblings.
caveat:       Projections, in thousands ('000), not Census 2011 PCA and not SRS. A Table-8 figure for a year after 2011 is not a census. Do not present it as “India has X people” without naming Table 8 and the 1st March reference. Not found as a NADA catalog hit under “Population Projections for India and States 2011”. Cell-mapped: no — PDF only. Do not OCR Table 8. 18 September 2026 search found no official xlsx/csv of Table 8.
```

Fetch source vs producer: file is fetched from **nhm.gov.in** (National Health Mission). Producer is **NCP / MoHFW**, not ORGI and not NHM as statistical office.

Same report, Table 8 continues across following pages. Input tables in Appendix 1 are assumptions — not the published projected stock.

Related `data.gov.in` file (not this card): [Projected population characteristics as on November, 2019 during 2011–2036](https://www.data.gov.in/resource/projected-population-characteristics-november-2019-during-2011-2036) is a 2.3 KB XLS in the MoHFW catalog *Health and Family Welfare Statistics 2019–20* (fields Sl.No., Category, Indicators, 2011, 2016) — national indicator characteristics, not Table 8 State/UT stock. Allowed as a government host of a **different** table from the same report family; do not substitute it for Table 8.

---

## Licence and calendar artifacts (not series)

- ORGI website footer (censusindia.gov.in, last updated 17-08-2026 on the homepage): site developed and maintained by the Office of the Registrar General & Census Commissioner, India; ©2025 all rights reserved.
- NADA / ORGI Digital Library footer: © 2026, ORGI Digital Library, All Rights Reserved.
- Named NADA download URLs did not present a login wall (HTTP 200, `Content-Disposition: attachment`).
- `data.gov.in` catalog pages: NDSAP / Government Open Data License - India for **hosted** resources. Remote “Download (Through URL)” PCA still lands on an ORGI `.xls`. GODL on the portal does not re-licence the NADA xlsx/pdfs on these cards.
- Census 2027 gazette notices (houselisting period, questionnaires, PE dates) are operational notices, not population totals — not cards. Example catalog: `https://censusindia.gov.in/nada/index.php/catalog/47084` (HLO period 1 April 2026–30 September 2026).
- Dedicated terms/website-policy paths under `/census.website/terms-and-conditions` and `/census.website/website-policy` returned 404 on 18 September 2026.
- MoSPI is not the producer of Census or SRS on these cards. GSDD 2026 was not used to re-licence ORGI files. `https://www.mospi.gov.in/` is 200 HTML — searched as a possible host, not used as producer.

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| Census 2021 population totals | NADA tag Census-2021 is circulars, schedules, gazette, citizenship/NPR rules — not a published headcount. |
| Census 2027 population totals | Notified and in houselisting; no count published. |
| A-01 Number of villages, towns, households, population and area (catalog 42526, file `A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx`) | Producer mixes India, State/UT, **district and sub-district**. Charter parks district files this iteration. Use Card 1 for State/UT population. |
| PCA district / UA / SC / ST / religion / female-headed / houseless files | Below the geography bar, or not the all-population PCA. |
| `censusindia.gov.in/datagov/PCA0000_2011_MDDS.xls` (data.gov.in “Download Through URL” for PCA 2011 India) | Same producer, **different file** (OLE MDDS `.xls`, 110,592 bytes) than Card 1’s NADA xlsx. Not a cell-mapped upgrade. Keep Card 1. |
| Rural Urban Distribution of Population PPT/PDF (catalog 42617) | Presentation of 2011 distribution; source of record for counts is Card 1. |
| Population Finder (village / sub-district / district) | District and below; parked. |
| NPR, NRC, citizenship registers, SECC as a population count | Charter-out. |
| Electoral rolls; data.gov.in 2024 electors/voters files | Not a census; charter-out. Not SRS. |
| SRS Abridged Life Tables; Cause of Death; Maternal Mortality special bulletin (NADA 47151) | Related SRS products; charter named births, deaths, infant mortality, fertility as published — Cards 3–4. |
| data.gov.in SRS extracts for **other years** (2016 key indicators; 2020 IMR; MMR 2016–18 / 2018–20; Tamil Nadu SHB 2009/2012/2015/2018) | Official government hosts, but **not** SRS Bulletin 2024 or Statistical Report 2024. |
| Civil Registration System (CRS) | Different series (registration completeness), not SRS and not Census PCA. |
| UIDAI / Aadhaar enrolment; NFHS household counts; NITI composites | Not a Census 2011/2021 headcount. |
| World Bank, UN, IMF, UNDP, news, think tanks | International secondary or not a government source of the dependency. |
| NITI scorecards / SDG league tables | Scorecards are not the record. NITI as a **host of the named table** would be in; no such Table 8 / A-02 / SRS 2024 file found on niti.gov.in this run. |
| data.gov.in “Human Population from 1901 to 2011” | Animal Husbandry Survey 2015 catalog; India-only Year/Population/growth columns (~509 bytes). Not Table A-02 State/UT. |
| data.gov.in “Projected population characteristics … 2011–2036” (HFW Statistics 2019–20, 2.3 KB XLS) | Same Technical Group **report family**, different table (national indicators 2011/2016), not TABLE-8 stock. |
| data.gov.in “State/UT-wise … Population Growth Rate … Technical Group … 2021 to 2025” | Growth rates 2021–2025, not Table 8 projected population 2011–2036. |
| MoSPI as SRS/Census **producer** | SRS Statistical Report and Bulletin are ORGI Vital Statistics / Census Commissioner. MoSPI may host; it did not supply these five files this run. |
| `https://census.gov.in/` (200 HTML) | Self-enumeration / Census 2027 portal, not the 2011 PCA or SRS PDFs. `www.census.gov.in` did not resolve. |
| Population Projections for India and States 1996–2016 (catalog 32987) and 1981–2001 (catalog 31298) | Superseded vintages; not the 2011–2036 Technical Group report. |
| UN / World Population Prospects as “India today” | International secondary; charter-out. |

`data.gov.in` is **not** rejected merely for being a republishing host. Rows above that name `data.gov.in` failed because they are a different series, a different year, a different table, or a scorecard — not because NIC hosted them.

---

## Geography Steward

**Required: no re-run.** The five fetch files and printed State/UT labels are unchanged versus `docs/archive/c2-geography-frame.md` (same NADA xlsx / xls / PDFs and the same NHM projection PDF). No new printed names.

Frames already on that note still apply: Card 1 PCA 2011 labels (no Telangana / Ladakh STATE rows; DISTRICT parked); Card 3 Table 1 includes Telangana, Ladakh, and merged DNH&DD; Card 4 bigger States/UTs only; Card 5 Table 8 has Jammu & Kashmir*(UT) and Telangana. Crosswalk between frames: none. Do not recode here.

**Parked this iteration:** Census PCA district tables; A-01 district and sub-district rows; Population Finder village/sub-district; any district file.

---

## Handoff

Next persona: **ingest-engineer**. Do not fetch in this librarian pass. `geography_frame` already exists (`docs/archive/c2-geography-frame.md`); no Geography Steward re-run.

Ingest fetches the named files on the cards (same five URLs). Keep Card 1 rows at India and STATE only. Card 2 remains OLE `.xls` until a parser exists — do not substitute the companion PDF. Cards 3–5 remain PDF (not cell-mapped). Do not pull A-01, district PCA, NPR, or electoral rolls. Do not write Census/SRS files into the git tree until that ingest job. Cards 1, 3, 4, and 5 remain three families: census stock, SRS rates, projections.

---

## HTTP status (verified GET, 18 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `https://censusindia.gov.in/census.website/` | 200 | HTML (`text/html; charset=UTF-8`) |
| `https://censusindia.gov.in/census.website/data/census-tables` | 200 | HTML |
| `https://censusindia.gov.in/nada/index.php/catalog/6191` | 200 | HTML |
| `.../catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx` | 200 | XLSX (magic `PK 03 04`; `Content-Disposition` filename as above; 1,376,414 bytes; `Content-Type: application/octet-stream`) |
| `https://censusindia.gov.in/nada/index.php/catalog/43333` | 200 | HTML |
| `.../catalog/43333/download/47001/00 A 2-India.xls` | 200 | OLE XLS (magic `D0 CF 11 E0 A1 B1 1A E1`; 100,352 bytes) |
| `.../catalog/43333/download/47002/00 A 2-India.pdf` | 200 | PDF `%PDF-1.5` (66,049 bytes) |
| `https://censusindia.gov.in/nada/index.php/catalog/47150` | 200 | HTML |
| `.../catalog/47150/download/51394/SRS_Bulletin_2024_Vol_59_No_1.pdf` | 200 | PDF `%PDF-1.7` (539,058 bytes) |
| `https://censusindia.gov.in/nada/index.php/catalog/47152` | 200 | HTML |
| `.../catalog/47152/download/51396/SRS_STAT_2024.pdf` | 200 | PDF `%PDF-1.7` (20,714,495 bytes) |
| `https://censusindia.gov.in/nada/index.php/catalog/?tag=SRS` | 200 | HTML |
| `https://nhm.gov.in/New_Updates_2018/Report_Population_Projection_2019.pdf` | 200 | PDF (`Content-Type: application/pdf`; `%PDF-1.5`; 11,543,351 bytes) |
| `https://mohfw.gov.in/sites/default/files/Population Projection Report 2011-2036 - upload_compressed_0.pdf` | 404 | HTML after 302 to www.mohfw.gov.in |
| `https://www.mohfw.gov.in/sites/default/files/Population Projection Report 2011-2036.pdf` | 404 | HTML |
| `https://nhm.gov.in/images/pdf/publication/Report_Population_Projection_2019.pdf` | 302 then 200 | NHM 404 page HTML (not the report) |
| `https://censusindia.gov.in/datagov/` | 200 | HTML body `403 Forbidden` (directory listing denied) |
| `https://censusindia.gov.in/datagov/PCA0000_2011_MDDS.xls` | 200 | OLE XLS (`application/vnd.ms-excel`; magic `D0 CF 11 E0`; 110,592 bytes) |
| `https://censusindia.gov.in/datagov/A-2.xls` | 404 | HTML |
| `https://censusindia.gov.in/datagov/00A2.xlsx` | 404 | HTML |
| `https://censusindia.gov.in/datagov/A02.xlsx` | 404 | HTML |
| `https://www.data.gov.in/catalog/primary-census-abstract-2011-india-and-states-0` | 200 | HTML |
| `https://www.data.gov.in/resource/primary-census-abstract-2011-india` | 200 | HTML |
| `https://www.data.gov.in/resource/projected-population-characteristics-november-2019-during-2011-2036` | 200 | HTML |
| `https://www.data.gov.in/resource/human-population-1901-2011` | 200 | HTML |
| `https://www.data.gov.in/catalog/health-and-family-welfare-statistics-2019-20` | 200 | HTML |
| `https://www.data.gov.in/api/3/action/package_search?...` | 500 | HTML (CKAN search API down this run; HTML search used instead) |
| `https://census.gov.in/` | 200 | HTML (not the statistical library) |
| `https://www.census.gov.in/` | no response (could not resolve host) | — |
| `https://www.mospi.gov.in/` | 200 | HTML (not used as SRS/Census producer) |
| `https://www.mohfw.gov.in/` | 200 | HTML |
| `https://www.niti.gov.in/` | 200 | HTML |
| `https://censusindia.gov.in/census.website/terms-and-conditions` | 404 | HTML |
| `https://censusindia.gov.in/census.website/website-policy` | 404 | HTML |
