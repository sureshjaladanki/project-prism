# C4 citation cards

Slice: **C4**. Citizen question: How many people are working, seeking work, and what do they earn?

Producer for all cards below: National Statistics Office (NSO), Ministry of Statistics and Programme Implementation (MoSPI). Website product id **69** (`Periodic Labour Force Survey (PLFS)`). Publications/Reports category `cat_010` with subcategories Monthly (`sub_010_001`), Quarterly (`sub_010_002`), Yearly (`sub_010_003`).

PLFS is the charter’s only employment / unemployment / wages record. Usual status (ps+ss) and Current Weekly Status (CWS) are both published — keep them as separate published statuses, not a merge. Do not mix with CMIE or MGNREGA (C9).

Latest annual vintage on these cards: **PLFS Annual Report 2025** (survey period **January 2025 – December 2025**), press note **27 March 2026**, publications listing dated **2026-03-27**, PDF filename revision stamp **29052026**. Latest monthly: **August 2026** Monthly Bulletin (publications listing **2026-09-15**; companion press note **15 September 2026**). Latest quarterly: **April – June 2026** Quarterly Bulletin (publications listing **2026-08-10**).

From January 2025 the sample design and calendar-year survey period differ from earlier July–June annual reports. Methodologist owns comparability; these cards name the break, they do not stitch series across it.

---

## Citation cards

### Card 1 — PLFS Annual Report 2025: LFPR, WPR, UR (usual status and CWS), All India and States/UTs

```text
producer:     National Statistics Office (NSO), Ministry of Statistics and Programme Implementation (MoSPI)
series:       Periodic Labour Force Survey (PLFS) Annual Report — Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), Unemployment Rate (UR) in usual status (ps+ss) and in Current Weekly Status (CWS)
id:           MoSPI product_id 69; Publications/Reports cat_010 / sub_010_003 Yearly; publication id 2814 “Annual Report Periodic Labour Force Survey (PLFS 2025) (January - December 2025)”; latestRelease id 149 press note; Appendix A Tables (16.0)/(16.1)/(17.0)/(17.1)/(18.0)/(18.1) usual status LFPR/WPR/UR by State/UT; Tables (30)/(31)/(32) CWS LFPR/WPR/UR by State/UT. Cell-mapped family of record: uploads/documents/publicationsReports/APPENDIX-A/Table__*.xlsx (e.g. Table__16.0.xlsx, Table__30.xlsx). Companion narrative PDF PLFS_2025_F_REV_29052026.pdf.
vintage:      reference_period January 2025 – December 2025 (calendar year; mid-point of survey period as stated in the report); release_date 27 March 2026 (press note); publications listing published_year 2026-03-27; PDF revision filename stamp 29052026
url:          https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/Table__16.0.xlsx
geography:    all India and States/UTs as labelled in State/UT on Appendix A tables (producer labels; see Geography Steward). Rural / urban / rural+urban as published. Not districts.
frequency:    annual (calendar year from 2025)
licence:      Not stated on the workbook or press PDF. MoSPI Copyrights Policy: reproduce accurately, not in a derogatory or misleading context, source acknowledged. GSDD 2026 Category A (open access) gazette applies to MoSPI open data generally; PLFS is not named line-by-line in the Category A list excerpt checked. Not stated as CC-BY.
next_release: 25 March 2027 — Annual Report of PLFS for calendar year 2026 (Jan–Dec 2026), per ARC 2026-27 (updated till August 2026)
caveat:       Sample design and January–December survey period change from January 2025 — annual estimates for 2025 may not be strictly comparable with pre-2025 July–June annual reports or calendar-year figures derived from unit-level data for 2022–2024 (press note / report endnote). Usual status (ps+ss) and CWS are different statuses — do not blend. Chandigarh rural cells are blank where the frame has no rural area (Appendix A note). Smaller States/UTs: producer warns sample size may not support all characteristics. Design-based estimated worker counts are not for publishing headcounts of workers (Appendix A note 3). Districts parked.
```

Source of record for State/UT rates: Appendix A Excel tables under `https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/` (hyperlinked from the Annual Report PDF). Companion Annual Report PDF (same publication): `https://www.mospi.gov.in/uploads/publications_reports/publications_reports1780040415321_0624fb13-fb47-40bc-b470-7c7e9635c3ef_PLFS_2025_F_REV_29052026.pdf`. Press note (same release): `https://www.mospi.gov.in/uploads/latestreleasesfiles/1774608774774-Press_note_AR_PLFS_2025_23032025_V2.1_26032026_final.pdf`.

Core charter tables in that Appendix A folder (same family; Ingest can fetch the folder or the named files):

- Usual status (ps+ss): `Table__16.0.xlsx` (LFPR), `Table__17.0.xlsx` (WPR), `Table__18.0.xlsx` (UR); principal-status companions `Table__16.1.xlsx`, `Table__17.1.xlsx`, `Table__18.1.xlsx`
- CWS: `Table__30.xlsx` (LFPR), `Table__31.xlsx` (WPR), `Table__32.xlsx` (UR)

Sample-design note (not the series): `https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_Changes-in-2025_rev.pdf` (also listed as `PLFS_changes_in_2025_Final.pdf` on the Yearly publications list).

### Card 2 — PLFS Annual Report 2025: wages and earnings (as published)

```text
producer:     National Statistics Office (NSO), MoSPI
series:       Periodic Labour Force Survey (PLFS) Annual Report — average wage/salary earnings from regular wage/salaried employment (CWS); average wage earnings per day from casual labour work other than public works; average gross earnings from self-employment (CWS)
id:           Same Annual Report publication id 2814 / product_id 69 as Card 1; Appendix A Tables (38), (39), (40) by State/UT; related Tables (51), (52) as published. Excel: Table__38.xlsx, Table__39.xlsx, Table__40.xlsx (and Table__51.xlsx / Table__52.xlsx / table__53.xlsx naming as on the APPENDIX-A path). Narrative: Annual Report Section Four “Earnings from employment”.
vintage:      reference_period January 2025 – December 2025; release_date 27 March 2026 (same Annual Report vintage as Card 1)
url:          https://www.mospi.gov.in/uploads/documents/publicationsReports/APPENDIX-A/Table__38.xlsx
geography:    all India and States/UTs as in State/UT on the earnings tables. Not districts. Not MGNREGA public works wages (C9).
frequency:    annual (calendar year from 2025)
licence:      Same as Card 1 (not on the artifact; MoSPI copyright acknowledgement; GSDD 2026 Category A gazette; not CC-BY)
next_release: 25 March 2027 (same Annual Report cadence as Card 1)
caveat:       Earnings concepts differ by status in employment (monthly regular wage/salary; per-day casual other than public works; last-30-days self-employment gross) — use the producer’s table titles, do not invent a single “wage”. Casual “other than public works” is not MGNREGA. Same 2025 design-break caveat as Card 1. Press note highlights are snapshots, not substitutes for the State/UT Excel tables.
```

Same Annual Report PDF and press note as Card 1. Press note also states nominal earnings growth for women in self-employed, regular wage/salaried, and casual labour — cite the Annual Report / Appendix A tables for the portrait number, not the press headline alone.

### Card 3 — PLFS Monthly Bulletin: LFPR, WPR, UR in CWS (all-India)

```text
producer:     National Statistics Office (NSO), MoSPI
series:       Periodic Labour Force Survey (PLFS) Monthly Bulletin — LFPR, WPR and UR in Current Weekly Status (CWS) for persons of age 15 years and above (and age groups as published), rural / urban / rural+urban, by gender
id:           MoSPI product_id 69; Publications/Reports cat_010 / sub_010_001 Monthly; latest publication id 2863 “Periodic Labour Force Survey (PLFS) Monthly Bulletin August 2026”; file Monthly_Bulletin_Aug_2026.pdf; Statements 1–3 (LFPR, WPR, UR) and Statement 5 (RSE). Companion latestRelease id 171 press note Monthly_Press_note_Aug_2026.pdf. Seventeenth monthly bulletin in the post-January-2025 series.
vintage:      reference_period August 2026 (CWS); publications listing published_year 2026-09-15; press note dated 15 September 2026
url:          https://www.mospi.gov.in/uploads/publications_reports/publications_reports1789465291404_ba9c7140-0b83-481b-a5fd-a7ac121c476f_Monthly_Bulletin_Aug_2026.pdf
geography:    all-India only (rural / urban / rural+urban). Not States/UTs. Not districts.
frequency:    monthly
licence:      Same as Card 1 (not on the PDF; MoSPI copyright acknowledgement; GSDD 2026 Category A gazette; not CC-BY)
next_release: 15 October 2026 — Monthly Bulletin of PLFS for September 2026, per ARC 2026-27 (updated till August 2026)
caveat:       CWS only — do not treat monthly rates as usual status (ps+ss). All-India only; State/UT rates are Cards 1 and 4. Upload path includes a content-hash prefix that changes each month — refresh via product 69 latestRelease / publications list cat_010 Monthly, not a frozen hash URL. No separate Excel annex on the August 2026 bulletin (statements are in the PDF).
```

Companion press note (same month): `https://www.mospi.gov.in/uploads/latestreleasesfiles/1789468732902-Monthly_Press_note_Aug_2026.pdf`.

Later months appear as further “PLFS Monthly Bulletin {Month Year}” files on publications cat_010 Monthly and as press notes on product 69 latestRelease.

### Card 4 — PLFS Quarterly Bulletin: LFPR, WPR, UR in CWS (all-India and selected States)

```text
producer:     National Statistics Office (NSO), MoSPI
series:       Periodic Labour Force Survey (PLFS) Quarterly Bulletin — LFPR, WPR and UR in Current Weekly Status (CWS), plus distribution of workers by broad status in employment and industry of work as published; all-India and selected States
id:           MoSPI product_id 69; Publications/Reports cat_010 / sub_010_002 Quarterly; publication id 2855 “Periodic Labour Force Survey (PLFS) Quarterly Bulletin April- June 2026”; file PLFS_QB_April_June_2026.pdf. Detailed Tables (2)/(3)/(5) LFPR/WPR/UR for selected States (Excel annexes hyperlinked from the PDF). From April–June 2025 the quarterly series covers rural and urban (not urban-only).
vintage:      reference_period April – June 2026; publications listing published_year 2026-08-10
url:          https://www.mospi.gov.in/uploads/publications_reports/publications_reports1786356638461_03375143-dcda-4a2e-89bf-036a8c7a87fc_PLFS_QB_April_June_2026.pdf
geography:    all-India (rural / urban / rural+urban) in the bulletin statements; selected States only in Appendix detailed tables (not the full State/UT roster of Card 1). Labels as printed (e.g. Delhi; Jammu & Kashmir). Not districts. Not all UTs.
frequency:    quarterly
licence:      Same as Card 1 (not on the PDF; MoSPI copyright acknowledgement; GSDD 2026 Category A gazette; not CC-BY)
next_release: 10 November 2026 — Quarterly Bulletin of PLFS for July – September 2026, per ARC 2026-27 (updated till August 2026)
caveat:       CWS only. “Selected States” is a producer subset — do not impute missing States/UTs from this bulletin. Excel annex URLs are under uploads/documents/documents/ with release-specific numeric prefixes (change each quarter); prefer PDF hyperlinks or the publications list for refresh. Pre-2025 quarterly bulletins were urban-only — do not stitch. No earnings tables in this quarterly product (earnings are Card 2 / Annual Report).
```

Cell-mapped selected-State tables for the April–June 2026 bulletin (same release; verify via PDF hyperlinks on refresh):

- `https://www.mospi.gov.in/uploads/documents/documents/1786355698953-Table_2.xlsx` (LFPR CWS, selected States)
- `https://www.mospi.gov.in/uploads/documents/documents/1786355710853-Table_3.xlsx` (WPR CWS)
- `https://www.mospi.gov.in/uploads/documents/documents/1786355731577-Table_5.xlsx` (UR CWS)

Selected State/UT labels in Table 2 for April–June 2026: Andhra Pradesh; Assam; Bihar; Chhattisgarh; Delhi; Gujarat; Haryana; Himachal Pradesh; Jharkhand; Karnataka; Kerala; Madhya Pradesh; Maharashtra; Odisha; Punjab; Rajasthan; Tamil Nadu; Telangana; Uttarakhand; Uttar Pradesh; West Bengal; Jammu & Kashmir; plus all-India.

---

## Licence and calendar artifacts (not series)

- MoSPI Copyrights Policy (site): reproduce following GSDD 2026; source must be prominently acknowledged.
- GSDD 2026 Gazette PDF: `https://www.mospi.gov.in/uploads/acts_and_policies/acts_and_policies1778231030122_a1a3ee77-e36d-4895-8da5-b294751cbb1a_272304_(1).pdf` — Category A (open access). PLFS is not called out by name in the Category A list text checked on 22 September 2026; still treat MoSPI attribution rules as binding.
- Advance Release Calendar 2026-27 (updated till August 2026): `https://www.mospi.gov.in/uploads/documents/releaseCalender/1788266096813-ARC%202026-27%20updated%20till%20August%202026.pdf` — monthly PLFS about the 15th; quarterly about the 10th; Annual Report CY 2026 listed 25 March 2027.
- PLFS: Changes in 2025 (sample design): `https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_Changes-in-2025_rev.pdf` (duplicate listing: `PLFS_changes_in_2025_Final.pdf`).
- Product locator (not the series artifact): `https://www.mospi.gov.in/api/product/get-product-data` POST `{product_id:69, lang:en}`.
- Publications list locator: `https://www.mospi.gov.in/api/publications-reports/get-web-publications-report-list` POST with `category_id: cat_010` and optional `sub_category_id` Monthly/Quarterly/Yearly.

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| CMIE Consumer Pyramids / unemployment series | Charter-out. Private. Not MoSPI/NSO PLFS. |
| MGNREGA employment / wages (any ministry MIS) | Charter-out for C4; belongs to C9. Do not mix with PLFS UR. |
| Labour Market Snapshot of Selected Districts (PLFS 2025) (`publications_reports1789723407069_..._Labour_Market_Snapshot_of_Selected_Districts-PLFS_2025.pdf`, 200) | Districts parked this iteration. |
| Labour Market Dynamics in Million-plus Cities (`Million_plus_city_F.pdf`, 200) | City geography; not national / States/UTs charter geography. |
| PLFS unit-level microdata (NADA catalog 284 CY 2025; 291 monthly; 292 quarterly) | Producer microdata for re-estimation. Prefer published Annual Report / Bulletin tables and Appendix Excel. Login/registration wall for microdata download. Do not recommend district files shipped with microdata layouts. |
| Key Employment Unemployment Indicators PLFS 2024 (`Key_employment_unemployment_indicators_PLFS_2024_final.pdf`) | Prior calendar-year key-indicators product. Current annual family of record is Annual Report 2025 (Card 1). |
| Pre-2025 July–June Annual Reports / urban-only Quarterly Bulletins as one continuous series with 2025+ | Design and coverage break. May be cited as prior vintages with the break stated; do not stitch onto Cards 1–4 as one series. |
| World Bank, IMF, UNDP, news, think tanks, NITI scorecards, data.gov.in republishes of PLFS | Not the producing office as source of record. |
| eSankhyiki HTML (`https://esankhyiki.mospi.gov.in/macroindicators?product=plfs` 200 SPA shell) | MoSPI portal locator, not a named PDF/XLSX. Use Cards 1–4 artifacts. |
| Flourish / Power BI embeds on product 69 | Visualisation hosts, not the table of record. |
| “Jobless growth” or other verdict series | Charter-out (verdicts). |

---

## Geography Steward

**Required: yes.** Cards 1–2 publish All India plus States and Union Territories under the producer’s `State/UT` labels. Card 4 publishes a **selected States** subset plus all-India. Geography Steward must set the map before Ingest pulls State/UT rows. Do not recode labels here. Card 3 is all-India only (still note rural/urban sectors).

Units as printed on Annual Report Appendix A Table (1) / Table (16.0) (producer spelling): all India; Andhra Pradesh; Arunachal Pradesh; Assam; Bihar; Chhattisgarh; Delhi; Goa; Gujarat; Haryana; Himachal Pradesh; Jharkhand; Karnataka; Kerala; Madhya Pradesh; Maharashtra; Manipur; Meghalaya; Mizoram; Nagaland; Odisha; Punjab; Rajasthan; Sikkim; Tamil Nadu; Telangana; Tripura; Uttarakhand; Uttar Pradesh; West Bengal; Andaman & N. Island; Chandigarh; Dadra & Nagar Haveli & Daman & Diu; Jammu & Kashmir; Ladakh; Lakshadweep; Puducherry. Sectors rural / urban / rural+urban as published.

**Missing / parked:** districts and below (charter-out; reject district snapshot). Chandigarh rural is blank / absent where noted. Card 4 omits many States/UTs that appear on Cards 1–2 — that is a producer “selected States” cut, not a Prism geography frame.

State/UT code companion on NADA (layout aid, not the rates series): `https://microdata.gov.in/NADA/index.php/catalog/284/download/5921` (`Indian_States_and_UTs_CodeName.xlsx`, 200).

---

## Handoff

Next persona: **Geography Steward** (State/UT rows on Cards 1–2 and selected States on Card 4). Then Methodologist (usual vs CWS; 2025 design break; earnings concepts). **Ingest Engineer must not fetch until** this citation card exists (it does) **and** `geography_frame` exists for any State/UT ingest (`docs/data-pipeline.md` Stage 1 preconditions).

No login wall on the named PDF/XLSX URLs on Cards 1–4. Terms require accurate reproduction and source credit. Ingest fetches the Appendix A Excel / bulletin PDFs on the cards, not the React homepage, not eSankhyiki HTML, and not NADA unit-level unless Methodologist later opens that path.

---

## HTTP status (verified HEAD/GET, 22 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `.../APPENDIX-A/Table__16.0.xlsx` | 200 | XLSX |
| `.../APPENDIX-A/Table__30.xlsx` | 200 | XLSX |
| `.../APPENDIX-A/Table__38.xlsx` | 200 | XLSX |
| `.../APPENDIX-A/Table__39.xlsx` | 200 | XLSX |
| `.../APPENDIX-A/Table__40.xlsx` | 200 | XLSX |
| `.../PLFS_2025_F_REV_29052026.pdf` (Annual Report) | 200 | PDF |
| `.../Monthly_Bulletin_Aug_2026.pdf` | 200 | PDF |
| `.../PLFS_QB_April_June_2026.pdf` | 200 | PDF |
| `.../1786355698953-Table_2.xlsx` (QB LFPR selected States) | 200 | XLSX |
| `.../Monthly_Press_note_Aug_2026.pdf` | 200 | PDF |
| `.../Press_note_AR_PLFS_2025_...pdf` | 200 | PDF |
| `.../PLFS_Changes-in-2025_rev.pdf` | 200 | PDF |
| `.../PLFS_changes_in_2025_Final.pdf` | 200 | PDF |
| `.../ARC 2026-27 updated till August 2026.pdf` | 200 | PDF |
| `.../272304_(1).pdf` (GSDD 2026) | 200 | PDF |
| `https://www.mospi.gov.in/api/product/get-product-data` POST `{product_id:69, lang:en}` | 200 | JSON (locator only) |
| `https://www.mospi.gov.in/api/publications-reports/get-web-publications-report-list` POST `category_id: cat_010` | 200 | JSON (locator only) |
| NADA `catalog/284/download/5921` (States/UTs code xlsx) | 200 | octet-stream |
| PIB press pages linked from ARC (timeout in this session) | no response | — use MoSPI uploads instead |
| Monthly/Quarterly bulletin PDF paths with content-hash prefixes | 200 now | **unstable across releases** — refresh via publications list / PDF hyperlinks |
