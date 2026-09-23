# C6 citation cards

Slice: **C6**. Citizen question: Who is in school, and what does the official record say about schools?

Producers on these cards: Department of School Education & Literacy (DoSEL), Ministry of Education, for **UDISE+** (Unified District Information System for Education Plus) — still named UDISE+ as of **22 September 2026**; no successor product renamed away from UDISE+ was found. Office of the Registrar General & Census Commissioner, India (ORGI) for Census 2011 literacy counts on a **separate** card. These are two records. Do not merge literacy into UDISE enrolment.

Latest UDISE+ vintage on these cards: academic year **2025-26**. Published annual booklets (NEP Structure and Existing Structure) carry PDF CreationDate **7 July 2026**. Live dashboard default year is **2025-26** (`yearId` **12**). Homepage aggregates on `udiseplus.gov.in` match that year (14.67 lakh schools, 24.72 crore students, 1.02 crore teachers). No UDISE+ 2026-27 annual report was found — next_release **unknown**.

Source of record for schools / enrolment / teachers / facilities: the **UDISE+ Report 2025-26** PDF booklets on the DoSEL dashboard host, not ASER, not board-exam portals, not NITI/PGI scorecards. Open-services JSON under `api.udiseplus.gov.in` returns the same yearId-12 aggregates and State/UT rows — cell-mapped companion for Ingest, not a different series.

---

## Citation cards

### Card 1 — UDISE+ Report 2025-26 (NEP Structure): schools, enrolments, teachers

```text
producer:     Department of School Education & Literacy (DoSEL), Ministry of Education — UDISE+
series:       UDISE+ Report 2025-26 — NEP Structure: schools, enrolments and teachers (India and State/UT)
id:           Dashboard label “UDISE+ Report 2025-26 NEP Structure(PDF)”; file UDISE+2025_26_Booklet_nep.94ceae1e8c2210549d21.pdf (175 pages). Tables of record: Table 1 National Highlights; Table 2.1 Distribution of Schools, Enrolments and Teachers by School Category; Table 2.2 State wise highlights — Schools, Enrolments and Teachers. Companion cell-mapped API (same vintage): POST https://api.udiseplus.gov.in/open-services/v1.1/schools-summarised-stats/public , teachers-summarised-stats/public , students-summarised-stats/public , and kpi/edu-highlights with body yearId "12", regionType 10 regionCode 99 (India) or regionType 21 (all State/UT rows in one response). Dashboard year map: 12=2025-26, 11=2024-25, 10=2023-24, 9=2022-23, 8=2021-22.
vintage:      reference_period academic year 2025-26; PDF CreationDate 7 July 2026 (D:20260707141152+05'30'); Author “Assistant Director”; Producer Microsoft Word 2016. Live dashboard showing 2025-26 as of 22 September 2026.
url:          https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_nep.94ceae1e8c2210549d21.pdf
geography:    India and States/UTs as labelled in Table 2.1 / 2.2 (36 State/UT names plus India). Not districts — district UDISE parked this iteration even where district tools exist.
frequency:    annual academic-year report
licence:      Not stated on the PDF title pages fetched. Portal footer: site belongs to DoSEL, Ministry of Education; designed/hosted by NIC. education.gov.in website-policies page is live (200 HTML) — reproduce accurately with source credit; not stated as CC-BY on the artifact.
next_release: unknown — no 2026-27 booklet or calendar date found on the dashboard Downloads list (years offered: 2025-26 through 2022-23).
caveat:       NEP Structure is the primary booklet for this slice (dashboard branded “Powered by NEP-2020”). Existing Structure PDF is the same year under the older category frame — do not stitch the two into one table without Methodologist. Table 6.x performance indicators (GER, NER, dropout) live in the same PDF but are derived rates; charter core is stocks (schools, enrolment, teachers). UDISE Table 6.6 title uses the acronym “ASER” for Age Specific Enrolment Rate — that is not Pratham ASER. Zero-enrolment and single-teacher school columns are producer caveats on Table 2.2.
```

Fetch host is the DoSEL UDISE+ dashboard (`dashboard.udiseplus.gov.in/report2026/...`). Locator (not the table): `https://dashboard.udiseplus.gov.in/` → UDISE+ Reports menu. Portal home: `https://udiseplus.gov.in/#/en/home`. Publications hub (SPA): `https://udiseplus.gov.in/#/en/page/publications`.

India totals printed on Table 2.2 (2025-26): **1,466,682** schools; **247,219,766** enrolments; **10,273,020** teachers. Same figures returned by open-services `edu-highlights` / summarised-stats for `yearId` 12.

Same-year companion PDF (Existing Structure — alternate category frame, not the NEP primary for this card): `https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_existing.edd7cd16d934a10377ba.pdf` (189 pages; CreationDate 7 July 2026).

Prior-year NEP booklet (not the latest vintage): `https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2024_25_Booklet_nep.ea09e672a163f92d9cfe.pdf`.

### Card 2 — UDISE+ Report 2025-26 (NEP Structure): school facilities / infrastructure

```text
producer:     Department of School Education & Literacy (DoSEL), Ministry of Education — UDISE+
series:       UDISE+ Report 2025-26 — NEP Structure: school infrastructure and facilities (India and State/UT)
id:           Same NEP booklet as Card 1. Tables of record: Table 2.5 State wise highlights — Infrastructure (and continuation); Section 7 facility detail tables (toilets, drinking water, electricity, library, computers, internet, ramps, CWSN toilets, etc.). National facility percentages also in Key Results / Table 1. Cell-mapped companion: same schools-summarised-stats/public POST (yearId "12") fields totSchGToilet, totSchLibrary, totSchElectricity, totSchDrinkwater, totSchHandwash, totSchMedical, totSchRamp, etc.; edu-highlights percentages (elecPer, waterPer, toiletPer, …).
vintage:      reference_period academic year 2025-26; same PDF CreationDate 7 July 2026 as Card 1
url:          https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_nep.94ceae1e8c2210549d21.pdf
geography:    India and States/UTs as in Table 2.5 labels (same State/UT list as Card 1). Not districts.
frequency:    annual academic-year report
licence:      Same as Card 1 (not on the artifact; DoSEL/MoE portal; attribution required; not CC-BY)
next_release: unknown (same as Card 1)
caveat:       Counts of schools “having” a facility are not the same as functional-facility columns (Table 2.5 prints both). Do not invent a facilities index or rank states. Same NEP vs Existing Structure split as Card 1. District facility extracts parked.
```

National facility shares printed in Key Results (2025-26), for orientation only — cite Table 1 / 2.5 for the page: electricity 95.0%; drinking water 99.5%; toilet 99.1%; girls’ toilet 98.5%; boys’ toilet 97.2%; hand wash 96.9%; playground 81.9%; computer 69.9%; internet 67.4%; library/reading corner/book bank 90.5%.

### Card 3 — Census 2011 Primary Census Abstract: literacy counts (separate from UDISE)

```text
producer:     Office of the Registrar General & Census Commissioner, India (ORGI), Ministry of Home Affairs
series:       Census of India 2011 — Primary Census Abstract (PCA SD): literate and illiterate population counts as published
id:           NADA catalog 6191; Reference ID PC11_PCA-SD; file DDW_PCA0000_2011_Indiastatedist.xlsx sheet Sheet1. Literacy columns of record: P_LIT, M_LIT, F_LIT (and P_ILL, M_ILL, F_ILL). Population denominators on the same rows: TOT_P, TOT_M, TOT_F. Use Level = India or STATE only (not DISTRICT). TRU = Total / Rural / Urban as published. Same workbook as C2 Card 1 population — literacy fields only for this C6 card.
vintage:      reference_period Census of India 2011 (00:00 hours, 1 March 2011); workbook has no printed release date; NADA catalog created/last modified 19 January 2021
url:          https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx
geography:    India and States/UTs as labelled in Name where Level = India or STATE (35 STATE labels plus India on the 2011 frame). TRU = Total / Rural / Urban. File also contains DISTRICT rows — parked this iteration.
frequency:    decennial census (no later census literacy totals published)
licence:      Not stated on the workbook. ORGI / NADA: all rights reserved. Not stated as CC-BY.
next_release: unknown — delayed. Census 2021 population/literacy totals were not published. Census 2027 houselisting is operational, not a literacy release.
caveat:       This is a 2011 literacy count, about fifteen years behind 2026 and behind UDISE+ 2025-26 — say so on the page. Do not merge into UDISE enrolment or invent a “current literacy rate from schools.” Literacy rate for citizens is usually P_LIT / (TOT_P − age 0–6) per Census definition — Methodologist owns the exact rate formula; this card cites the published count columns. 2011 labels predate Telangana as a State row and Ladakh as a UT row.
```

Fetch host is the producing office (ORGI NADA). Catalog: `https://censusindia.gov.in/nada/index.php/catalog/6191`.

Opened India Total row (Sheet1): P_LIT **763,638,812**; P_ILL **447,216,165** (with TOT_P on the same row). Cell-mapped: yes (xlsx).

---

## Licence and calendar artifacts (not series)

- UDISE+ portal footer (`udiseplus.gov.in`): belongs to Department of School Education & Literacy, Ministry of Education; designed, developed, maintained and hosted by NIC.
- DoSEL site: `https://www.dsel-education.gov.in/` (200 HTML); `dsel.education.gov.in` redirects here.
- Ministry site policies locator: `https://www.education.gov.in/website-policies` (200 HTML).
- UDISE+ open-services API base used by the public dashboard: `https://api.udiseplus.gov.in/open-services/v1.1/` (POST JSON; Origin/Referer from dashboard accepted this run). Not a login wall for the named public endpoints.
- No Advance Release Calendar date for UDISE+ 2026-27 found on the dashboard Downloads year list (stops at 2025-26 as latest).
- Archive / microdata portals (`data.udiseplus.gov.in/archive`, `microdata.udiseplus.gov.in`) are live HTML — district/unit microdata and historical tools; **parked** for this iteration (district bar).

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| ASER (Pratham / ASER Centre) as source of record | Charter-out. NGO learning assessment, not DoSEL UDISE+. `asercentre.org` 200 HTML — not cited. |
| UDISE Table 6.6 “Age Specific Enrolment Rate (ASER)” misread as Pratham ASER | Same PDF acronym collision only. If used later, Methodologist must name it as UDISE ASER (enrolment rate), not Pratham. Not a separate card here. |
| Board-exam result portals (CBSE/state boards, DigiLocker results) | Charter-out. `results.digilocker.gov.in` returned 403 this run — irrelevant; not UDISE. |
| “Learning crisis” verdicts; state rankings; PGI / District PGI / State PGI | Scorecards and verdicts are out. Dashboard links to State PGI / District PGI exist — not the series. |
| District UDISE files / Know Your School / GIS / microdata unit records | Geography bar: districts parked. Stop at State/UT even though district tools exist. |
| UDISE+ Report Existing Structure as primary instead of NEP | Same year, different school-category frame. Companion only; NEP booklet is Card 1–2 of record for the NEP-powered dashboard. |
| Older UDISE / UDISE+ booklets (2024-25 and earlier) as “latest” | Superseded by 2025-26. Keep only as history if a later refresh needs a break. |
| “Flash Statistics” as a separate live product name for 2025-26 | Current published annual product on the dashboard is titled **UDISE+ Report** booklet. No separate 2025-26 “Flash Statistics” PDF URL verified this run. |
| Performance / GER / NER / dropout as the charter core series | In the same PDF (Section 6); not the enrolment/teachers/facilities stocks named in the charter. Methodologist may bind later — not Cards 1–2. |
| Table 2.6 Aadhaar-linked enrolment | In the report; not the citizen school-stock question; privacy-adjacent — do not lead the page with it. |
| NSS / NSO education rounds as literacy of record (e.g. historical Report paths) | No clear **current** official NSS literacy-rate series verified this run as a live MoSPI product URL. Guessed path `Report_585_75th_round_Education...pdf` → 404. Older `nss_rep_575.pdf` (200 PDF, last-modified 2016) is not cited as C6 literacy of record — Census 2011 PCA remains the named literacy card. Do not merge NSS attendance into UDISE. |
| World Bank, UNESCO, UNICEF, news, think tanks, NITI SDG scorecards | Not the producing office / not the record. |
| `data.gov.in` UDISE republishes | Catalog search endpoint 500 this run; even when healthy, host only if the **same** DoSEL table — prefer dashboard PDF/API. |
| SDMS / login modules (`sdms.udiseplus.gov.in`) | School data-entry system, not the published statistics artifact. |

---

## Geography Steward

**Required: yes.** Cards 1–2 publish India plus States and Union Territories under the producer’s Table 2.1 / 2.2 / 2.5 labels (36 State/UT names plus India). Open-services `regionType` 21 returns the same 36 units with ALL-CAPS `regionName` strings that do not always match the PDF title case. Card 3 uses the Census 2011 PCA STATE frame (no Telangana / Ladakh STATE rows). Geography Steward must set the map **before** Ingest pulls. Do not recode labels here.

**UDISE+ 2025-26 State/UT labels as printed on Table 2.2 / 2.5:** India; Andaman & Nicobar Islands; Andhra Pradesh; Arunachal Pradesh; Assam; Bihar; Chandigarh; Chhattisgarh; Daman & Diu and Dadra & Nagar Haveli; Delhi; Goa; Gujarat; Haryana; Himachal Pradesh; Jammu & Kashmir; Jharkhand; Karnataka; Kerala; Ladakh; Lakshadweep; Madhya Pradesh; Maharashtra; Manipur; Meghalaya; Mizoram; Nagaland; Odisha; Puducherry; Punjab; Rajasthan; Sikkim; Tamil Nadu; Telangana; Tripura; Uttar Pradesh; Uttarakhand; West Bengal.

**API `regionName` variants seen for yearId 12 (not a recode — Steward owns the crosswalk):** ANDAMAN & NICOBAR ISLANDS; ANDHRA PRADESH; …; DADRA & NAGAR HAVELI AND DAMAN & DIU; DELHI; …; JAMMU & KASHMIR; LADAKH; …; WEST BENGAL (36 rows; national row is ALL INDIA / India with regionCode 100 on highlights).

**Parked this iteration:** district UDISE (any district report, Know Your School unit pages, GIS school points, microdata); PCA DISTRICT literacy rows.

---

## Handoff

Next persona: **Geography Steward** (State/UT rows exist on Cards 1–2; Card 3 needs the 2011 PCA frame already used on C2, plus an explicit literacy-column bind). Then Methodologist. **Ingest Engineer must not fetch until** this citation card exists (it does) **and** `geography_frame` exists for the UDISE 2025-26 State/UT labels (`docs/data-pipeline.md` Stage 1 preconditions).

Ingest fetches the NEP PDF on Cards 1–2 and/or the open-services POST endpoints with `yearId` `"12"` (cell-mapped). Prefer producer dashboard PDF + open-services — not the React homepage alone, not ASER, not board portals, not district microdata. Card 3 reuses the NADA PCA xlsx (literacy columns only; India/STATE rows only). Do not write UDISE or Census files into the git tree until that ingest job.

No login wall on the named PDF URLs (HTTP 200, `application/pdf`). Open-services public POSTs succeeded without OAuth this run when `Content-Type: application/json` and dashboard Origin/Referer were sent; empty/`{}` bodies fail with invalid_year_id.

---

## HTTP status (verified GET/POST, 22 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_nep.94ceae1e8c2210549d21.pdf` | 200 | PDF `%PDF-1.5` (11,233,346 bytes; CreationDate 7 Jul 2026) |
| `https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2025_26_Booklet_existing.edd7cd16d934a10377ba.pdf` | 200 | PDF `%PDF-1.5` (12,470,602 bytes; CreationDate 7 Jul 2026) |
| `https://dashboard.udiseplus.gov.in/report2026/static/media/UDISE+2024_25_Booklet_nep.ea09e672a163f92d9cfe.pdf` | 200 | PDF `%PDF-1.7` (10,469,304 bytes) |
| `https://dashboard.udiseplus.gov.in/` | 200 | HTML shell → `/report2026/` SPA |
| `https://udiseplus.gov.in/` | 200 | HTML (`last-modified` 18 Sep 2026 on this run) |
| `https://www.education.gov.in/` | 200 | HTML |
| `https://www.dsel-education.gov.in/` | 200 | HTML |
| `https://www.education.gov.in/website-policies` | 200 | HTML |
| `https://data.udiseplus.gov.in/archive` | 200 | HTML |
| `https://microdata.udiseplus.gov.in/` | 200 | HTML |
| `https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx` | 200 | XLSX (magic `PK 03 04`; 1,376,414 bytes) |
| POST `.../open-services/v1.1/kpi/edu-highlights` `{"yearId":"12","regionCode":99,"regionType":10,"valueType":1}` | 200 | JSON (`status`: true; India totSch 1466682) |
| POST `.../open-services/v1.1/schools-summarised-stats/public` yearId 12 regionType 21 | 200 | JSON (36 State/UT rows) |
| POST `.../open-services/v1.1/teachers-summarised-stats/public` yearId 12 regionType 21 | 200 | JSON (36 State/UT rows) |
| POST `.../open-services/v1.1/students-summarised-stats/public` yearId 12 regionType 21 | 200 | JSON (36 State/UT rows) |
| GET `.../schools-summarised-stats/public` (no body) | 405 | JSON Method Not Allowed |
| `https://asercentre.org/` | 200 | HTML (rejected as source of record) |
| `https://results.digilocker.gov.in/` | 403 | HTML (board-results class; rejected) |
| `https://www.mospi.gov.in/sites/default/files/publication_reports/Report_585_75th_round_Education_final_15072020.pdf` | 404 | — (NSS path not verified) |
| `https://mospi.gov.in/sites/default/files/publication_reports/nss_rep_575.pdf` | 200 | PDF (historical NSS education report; not C6 literacy of record) |
| `https://www.data.gov.in/catalogs?query=udise` | 500 | HTML (portal error this run) |
