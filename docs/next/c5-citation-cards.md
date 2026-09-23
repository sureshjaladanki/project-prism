# C5 citation cards

Slice: **C5**. Citizen question: What do states and UTs collect and spend?

Producers on these cards: **Reserve Bank of India (RBI)** for the cross-state/UT budget compilation *State Finances: A Study of Budgets of 2025-26* (annual publication page on `rbi.org.in`, statement and appendix tables on `rbidocs.rbi.org.in`); **Comptroller and Auditor General of India (CAG)** for the audited *Combined Finance and Revenue Accounts* (CFRA) / *Union and State Finances at a Glance* (latest complete set on the live archive: **2020-21**). These are separate records. The page shows each as itself. It does not invent a blended “state money” figure, a fiscal-virtue rank, or treat Union grants as own tax.

**Boundary vs C3:** Union Budget (`indiabudget.gov.in`), CGA Union monthly accounts, and Union Finance Accounts stay on **C3**. Do not use a Union total as if it were state/UT finances. CGA’s live site (`cga.gov.in`) on this fetch publishes **Union** accounts releases — not a state/UT compilation of record for C5.

Vintage on the RBI cards: **State Finances: A Study of Budgets of 2025-26**, dated on the RBI Annual Publications listing **23 January 2026**. Columns / vintages inside the publication (as titled on the listing) include **2023-24 (Accounts)**, **2024-25 (Revised Estimates)**, and **2025-26 (Budget Estimates)** for financing statements; other statements use the producer’s year labels as printed. Vintage on the CAG CFRA card: **2020-21**, glance preface dated **6 September 2024**.

House rule: identify the data requirement; identify the producing office; fetch from official government agencies that can source that dependency (producing office first preference); quote producer, series, date, and fetch source. Prefer RBI’s own Study of Budgets release over a portal that republishes it. Deny World Bank, IMF, UNDP, CMIE, news, think tanks, and NITI fiscal scorecards as source of record.

---

## Citation cards

### Card 1 — RBI State Finances: major deficit / fiscal indicators

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Major Deficit Indicators / Major Fiscal Indicators (as published)
id:           Appendix Table 1: Major Deficit Indicators of State Governments (xlsx/pdf 01_APP…); companion Statements 1 Major Fiscal Indicators, 2 Revenue Deficit/Surplus, 3 Gross Fiscal Deficit/Surplus. Listing: Annual Publications “State Finances : A Study of Budgets” dated Jan 23, 2026. series_id rbi-sf-2025-26-deficit-indicators; citation_id cite-c5-rbi-sf-2025-26-deficit-indicators
vintage:      reference_period as labelled in the 2025-26 Study (BE / RE / Accounts columns as printed); release_date 23 January 2026 (RBI listing title date)
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    State Governments and UTs as labelled in the producer’s statements/appendices (Appendices I–IV title “States and Union Territories with Legislature”). Not districts. Not local bodies.
frequency:    annual publication
licence:      © Reserve Bank of India. All Rights Reserved (site footer on the listing). Not stated as CC-BY on the listing page.
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       BE, RE and Accounts are different vintages — do not collapse them. Deficit labels are the producer’s (RD, GFD, etc.), not a Prism “fiscal virtue” score. Full PDF book also linked on the same listing (0SF…PDF).
```

Fetch host is the producing office (RBI Annual Publications listing). Artifact files (same series): Appendix Table 1 XLSX `https://rbidocs.rbi.org.in/rdocs/Publications/DOCs/01_APP230120266318663B94AF422D8941472ECF135352.XLSX` and PDF twin under `/PDFs/`; Statements 1–3 under `/DOCs/` and `/PDFs/` with `01_ST`…`03_ST` hashes on the same listing. Whole-volume PDF: `https://rbidocs.rbi.org.in/rdocs/Publications/PDFs/0SF23012026877D47254C4F4B0793B2C38F05FB7EC5.PDF`. Explanatory Note on Data Sources and Methodology: `https://rbidocs.rbi.org.in/rdocs/Publications/PDFs/06EXPLANATORY24012608539CE016444F378E0A5AAB69B04CB8.PDF`.

What the table family contains: major deficit / fiscal indicators as RBI prints them for states/UTs (revenue deficit/surplus, gross fiscal deficit/surplus, and related indicator lines on Statements 1–3 / Appendix Table 1) — not Union Budget deficit statistics (C3).

### Card 2 — RBI State Finances: revenue receipts (own tax, own non-tax, Centre transfers)

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Revenue Receipts; Tax Revenue; Non-Tax Revenue; Devolution and Transfer of Resources from the Centre (as published)
id:           Statement 33 Revenue Receipts of State Governments and UTs; Statement 14 Tax Revenue; Statement 15 Non-Tax Revenue; Statement 17 Devolution and Transfer of Resources from the Centre; Appendix I Revenue Receipts of States and Union Territories with Legislature; Appendix Table 2 Devolution and Transfer of Resources from the Centre. series_id rbi-sf-2025-26-revenue-receipts; citation_id cite-c5-rbi-sf-2025-26-revenue-receipts
vintage:      reference_period as labelled in the 2025-26 Study; release_date 23 January 2026
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    States and Union Territories with Legislature as in Appendix I title; Statements 14/15/17/33 as labelled “State Governments and UTs”. Not districts.
frequency:    annual publication
licence:      Same as Card 1 (© RBI; not CC-BY on listing)
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       Keep own tax / own non-tax separate from devolution and grants from the Centre — the producer publishes them as distinct statements (14, 15, 17) and Appendix Table 2. Do not treat Union grants or tax devolution as own tax. Statement 16 (Loans from the Centre) is loans, not tax.
```

Fetch notes: Statement 14 XLSX `…/DOCs/14_ST230120264DFE56A61A0F424C823D5A84BE4C0294.XLSX`; Statement 15 `…/15_ST230120265C79C1E441C9480BBDE51CE41BE76B58.XLSX`; Statement 17 `…/17_ST2301202683B49BF6F4584A6985B2CCCAA41B020E.XLSX`; Statement 33 `…/33_ST23012026BCEB3D627A5F437FB20248AF4A6A7AD7.XLSX`; Appendix Table 2 `…/02_APP23012026B2830D87C491433F932392727168FB91.XLSX` (PDF twins under `/PDFs/`). Appendix I–IV files are the `1APPENDIX` / `2APPENDIX` / `3APPENDIX` / `4APPENDIX` family on the same listing. Notes to Appendices: `https://rbidocs.rbi.org.in/rdocs/Publications/PDFs/NOTES230120261772EAC66AA94026B3E4C074E6188FE9.PDF`.

What the table family contains: revenue receipts of states/UTs; tax revenue; non-tax revenue; devolution and transfers from the Centre (grants / share of Union taxes as RBI labels them) — the official split needed so grants are not mistaken for own tax.

### Card 3 — RBI State Finances: expenditure (revenue, capital, development)

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Revenue Expenditure; Capital Expenditure; Development and Non-Development Expenditure (as published)
id:           Statement 34 Revenue Expenditure of State Governments and UTs; Statements 11 Development Expenditure, 12 Non-Development Expenditure; Appendix II Revenue Expenditure and Appendix IV Capital Expenditure of States and Union Territories with Legislature; Appendix Tables 3–7 (Development and Non-Development Expenditure aggregate / major heads / social sector). series_id rbi-sf-2025-26-expenditure; citation_id cite-c5-rbi-sf-2025-26-expenditure
vintage:      reference_period as labelled in the 2025-26 Study; release_date 23 January 2026
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    States and UTs with Legislature / as labelled on Statements 11–12 and 34. Not districts. Not local-body accounts.
frequency:    annual publication
licence:      Same as Card 1
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       Development / non-development and social-sector cuts are RBI’s published heads — not a welfare verdict. Do not merge with Union Expenditure Profile (C3). Sector detail statements (education, health shares, subsidies, wages — Statements 26–32, 35–37) sit in the same publication; use them only when the page cites that statement.
```

Fetch notes: Statement 34 XLSX `…/34_ST23012026C857071F901744E5844154DF5079FCB4.XLSX`; Appendix Tables 3–7 are `03_APP`…`07_APP` on the listing. Companion Overview / Fiscal chapters PDFs (`1OVERVIEW…`, `2FISCAL…`) are narrative of the same Study — not a substitute series.

What the table family contains: state/UT expenditure as published (revenue and capital appendices; development / non-development and social-sector appendix tables).

### Card 4 — RBI State Finances: capital receipts

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Capital Receipts of States and Union Territories with Legislature
id:           Appendix III: Capital Receipts of States and Union Territories with Legislature (xlsx/pdf on listing under Appendices I to IV). Related: Statement 16 Loans from the Centre (not the full capital-receipts appendix). series_id rbi-sf-2025-26-capital-receipts; citation_id cite-c5-rbi-sf-2025-26-capital-receipts
vintage:      reference_period as labelled in the 2025-26 Study; release_date 23 January 2026
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    States and Union Territories with Legislature (Appendix III title). Not districts.
frequency:    annual publication
licence:      Same as Card 1
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       Capital receipts include borrowings as the producer prints them — do not treat debt receipts as “own tax” or as revenue. Distinct from Card 2 revenue receipts and from Union capital receipts (C3).
```

Fetch notes: Appendix III files are the `3APPENDIX23012026_…` XLSX/PDF set on the same Annual Publications listing. Statement 16 XLSX is linked beside “Loans from the Centre” on that page.

What the table family contains: capital receipts of states/UTs with legislature as RBI publishes them (including Centre loans where that statement is used).

### Card 5 — RBI State Finances: GFD decomposition and financing

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Decomposition and Financing of Gross Fiscal Deficit
id:           Appendix Tables 8–10 (Decomposition of GFD; Financing of GFD; Financing as per cent of Total); Statements 4–10 (Decomposition; Financing for 2023-24 Accounts, 2024-25 RE, 2025-26 BE, and per-cent-of-total companions). series_id rbi-sf-2025-26-gfd-financing; citation_id cite-c5-rbi-sf-2025-26-gfd-financing
vintage:      reference_period 2023-24 (Accounts), 2024-25 (RE), 2025-26 (BE) as in Statement 5–10 titles; release_date 23 January 2026
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    State Governments as labelled (Appendix Tables 8–10 titles). Not districts.
frequency:    annual publication
licence:      Same as Card 1
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       Financing tables are not a licence to rank “fiscal virtue”. Keep Accounts / RE / BE years separate. Distinct from Union BAG Deficit Statistics (C3 Card 6).
```

Fetch notes: Appendix Tables 8–10 are `08_APP`…`10_APP` on the listing; Statements 4–10 are `04_ST`…`10_ST`.

What the table family contains: how gross fiscal deficit is decomposed and financed, by state, for the three vintages named in the statement titles.

### Card 6 — RBI State Finances: outstanding liabilities and market borrowings

```text
producer:     Reserve Bank of India (RBI)
series:       State Finances: A Study of Budgets of 2025-26 — Outstanding Liabilities; Market Borrowings (as published)
id:           Appendix Tables 11–12 Composition of Outstanding Liabilities of State Governments and UTs (levels and as per cent of Total); Appendix Table 13 State Government Market Borrowings; Statements 18–22 (Composition; Total Outstanding Liabilities; as per cent of GSDP; Market Borrowings; Market Loans). Optional detail in same volume: Statements 23–25 maturity / T-bills; Statement 28 Outstanding Guarantees. series_id rbi-sf-2025-26-liabilities; citation_id cite-c5-rbi-sf-2025-26-liabilities
vintage:      reference_period as labelled in the 2025-26 Study; release_date 23 January 2026
url:          https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets
geography:    State Governments and UTs as in Appendix Tables 11–12 titles. Not districts.
frequency:    annual publication
licence:      Same as Card 1
next_release: unknown — next Study of Budgets edition not dated on these artifacts
caveat:       Outstanding liabilities and market borrowings are distinct printed concepts — do not merge with Union Statement of Liabilities (C3). Guarantees (Statement 28) are not the same as outstanding debt stock.
```

Fetch notes: Appendix Tables 11–13 are `11_APP`…`13_APP`; Statement 19 XLSX `…/19_ST23012026FBFD9DFE4C3F40E0B23C05BD508AB422.XLSX`. Companion **e-STATES Database** workbook on the same listing: `https://rbidocs.rbi.org.in/rdocs/Publications/DOCs/ESTATES23012026AB138FB463474EBFBCC03A8FC878C45A.XLSX` (producer-labelled companion file — not a separate citizen series unless Methodologist names it).

What the table family contains: outstanding liabilities composition and totals (including % of GSDP where published), and state government market borrowings / loans as RBI prints them.

### Card 7 — CAG Combined Finance and Revenue Accounts / Union and State Finances at a Glance (audited, lagged)

```text
producer:     Comptroller and Auditor General of India (CAG)
series:       Combined Finance and Revenue Accounts (CFRA) of the Union and State Governments — Union and State Finances at a Glance 2020-21 (and CFRA Volumes I–III for 2020-21)
id:           Archive listing Combined Finance and Revenue Accounts-Union & State (?arch=1); files Union-and-State-finances-at-a-Glance-2020-21-final-….pdf; Volume-I / Volume-II / Volume-III 2020-21 PDFs under /uploads/combined_accounts/. Glance preface signed 6 September 2024. series_id cag-cfra-2020-21-glance; citation_id cite-c5-cag-cfra-2020-21-glance
vintage:      reference_period financial year 2020-21 (Accounts); glance release/preface date 6 September 2024; archive page last updated 22 September 2026 on this fetch
url:          https://cag.gov.in/en/combined-accounts?arch=1
geography:    Union and State Governments / Union Territories with Legislature as the glance states (preface). Glance revenue-receipt charts list states plus UT Jammu & Kashmir, NCT Delhi, UT Puducherry among others. Not districts. Not local bodies.
frequency:    annual when published; latest complete set on live archive as of this fetch is 2020-21 (no 2021-22+ CFRA volumes on the archive page)
licence:      Copyright © 2026 Comptroller and Auditor General of India. All Rights Reserved (site footer). Not stated as CC-BY on the archive page.
next_release: unknown — current (non-archive) combined-accounts page had no newer volume links on this fetch; next CFRA year not dated there
caveat:       Audited accounts compilation, several years behind RBI’s 2025-26 Study. Includes Union and states in one CFRA product — use state/UT tables for C5; do not substitute Union CFRA lines for C3 Budget/CGA cards. Glance explicitly separates States’/UTs Own Tax Revenue (SOTR), Non-Tax Revenue, Share of Union Taxes and Duties, and Grant-in-Aid — do not fold grants into own tax.
```

Fetch host is CAG. Glance PDF (verified `%PDF-1.6`, 200): `https://cag.gov.in/uploads/combined_accounts/Union-and-State-finances-at-a-Glance-2020-21-final-0671a1ecc965a37-34532341.pdf`. Volume I (verified `%PDF-1.7`, 200): `https://cag.gov.in/uploads/combined_accounts/Volume-I-0674d8193e331c4-72536869.pdf`. Volume II: `https://cag.gov.in/uploads/combined_accounts/Volume-II-0674d81876d98e9-45172153.pdf`. Volume III: `https://cag.gov.in/uploads/combined_accounts/Volume-III-0674d8176e27743-44131175.pdf`. Non-archive hub: `https://cag.gov.in/en/combined-accounts` (no newer year files linked on this fetch). Related CAG hubs (not this card’s table): State Accounts index `https://cag.gov.in/en/state-accounts-report`; Territories Accounts `https://cag.gov.in/en/state-accounts-report?show_ut_only=1`; State Finance Dashboard shell `https://cag.gov.in/en/page-statefinances24-25`.

What the table family contains: audited Union-and-state finances overview and detailed CFRA volumes for 2020-21, including own-tax vs share of Union taxes vs grants-in-aid, expenditure, deficit/fiscal parameters, and public debt/liabilities as CAG prints them.

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| Union Budget 2026-27 receipts/expenditure/deficit/debt (`indiabudget.gov.in`) | Union-only. That is **C3**. Charter out for C5. |
| CGA Union Government Accounts / Union Finance Accounts (`cga.gov.in` monthly and Finance Accounts releases) | Union accounts of record for C3. No state/UT compilation of record found on the live CGA site on this fetch. |
| Individual State/UT Budget documents (state finance department sites) | Not the cross-India comparable compilation the charter asks the librarian to name. Prefer RBI Study of Budgets (and CAG CFRA for audited lag). |
| Individual State Finance Accounts / Appropriation Accounts (CAG State Accounts index `cag.gov.in/en/state-accounts-report`) | Per-state audited accounts — underlying books, not the single cross-state compilation of record for this slice. Use only if a later card names one state artifact. |
| CAG State Finances Audit Reports (per-state “Report on State Finances” under audit-report) | Audit narrative/report cards by state, not the comparable multi-state table family named above. |
| CAG State Finance Dashboard page (`page-statefinances24-25`) / ORDS dashboards | Shell / dashboard hosts on this fetch — not a named CFRA/RBI statement file of record. |
| data.rbi.org.in (DBIE SPA) | Host responds 200 HTML app shell; no named state-finance statement artifact resolved on this fetch that replaces the Study of Budgets XLSX/PDF family. Do not silent-substitute. |
| MoSPI Statistical Year Book / MoSPI homepage | No MoSPI-produced state-finance compilation of record verified on this fetch as the comparable cross-state series. |
| NITI fiscal rankings / SDG or “best state” fiscal scorecards | Charter-out; house deny for scorecards. |
| World Bank, IMF, UNDP, CMIE, news, think-tank state-finance tables | Not the producing office. |
| Local-body accounts / CAG Local Bodies Audit Reports | Charter-out. |
| District finance tables | Not in RBI SF or CFRA glance geography. Districts parked. |
| Ranking states by “fiscal virtue” | Charter-out. Bound ranks of a published measure only if a later citizen question is a rank question — not this H1. |

---

## Geography Steward

**Required: yes.** Cards 1–6 are state/UT-shaped (RBI labels “State Governments and UTs” / “States and Union Territories with Legislature”). Card 7 (CAG CFRA glance) covers Union plus states/UTs with legislature and prints a state/UT list in revenue-receipt charts (including e.g. Andhra Pradesh … West Bengal, UT Jammu & Kashmir, NCT Delhi, UT Puducherry in the glance extract). Geography Steward must set the map from the producer’s labels before Ingest pulls. Do not recode labels here.

**Coverage note (as titled, not a full label dump from every XLSX):** RBI Appendices I–IV are explicitly **States and Union Territories with Legislature**. UTs without legislature may be absent or differently treated — Steward confirms against the opened statements. **Missing / parked:** districts and below; local bodies.

---

## Named holes

- **CAG CFRA after 2020-21:** Live non-archive combined-accounts page had no newer volume links on this fetch (22 September 2026). Archive tops at **2020-21**. No fetchable CFRA table of record for 2021-22+ on that page.
- **Intra-year / monthly comparable state accounts:** No CGA-style monthly “states at a glance” compilation of record verified for C5 (CGA live releases checked are Union).
- **UTs without legislature:** Not titled into RBI Appendices I–IV; may be a coverage hole relative to “all UTs” wording in the citizen question — Steward/Methodologist to confirm from Explanatory Note / opened files.
- **rbidocs WAF:** Statement/appendix file URLs are published on the RBI listing (200), but non-browser GETs to `rbidocs.rbi.org.in` returned a bot-challenge HTML page on this fetch — Ingest needs a browser-capable or approved fetch path; listing page alone is not the cell grid.
- **Cell-mapped DBIE twin of the same RBI statements:** Not verified as a stable named artifact on `data.rbi.org.in` on this fetch.

---

## Handoff

Next persona: **Geography Steward** (state/UT rows exist), then Methodologist. Do not ingest until citation cards exist (they do) and `geography_frame` exists for non–all-India rows.

Primary compilation of record for current comparable state/UT budgets: **RBI State Finances: A Study of Budgets of 2025-26** (Cards 1–6). Audited lagged companion: **CAG CFRA / Union and State Finances at a Glance 2020-21** (Card 7). Keep own tax / own non-tax / Centre transfers on separate lines as the producers print them.

---

## HTTP status (verified, 22 September 2026)

| URL | Status | Type |
|-----|--------|------|
| `https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=State%20Finances%20:%20A%20Study%20of%20Budgets` | 200 | HTML (listing; titles/links for 2025-26 Study dated Jan 23, 2026) |
| `https://rbidocs.rbi.org.in/rdocs/Publications/DOCs/01_APP…XLSX` (and sibling ST/APP/PDF URLs from listing) | 200 body was WAF/challenge HTML on automated GET | Linked from listing; open via browser/approved client |
| `https://cag.gov.in/en/combined-accounts` | 200 | HTML (no newer CFRA files linked) |
| `https://cag.gov.in/en/combined-accounts?arch=1` | 200 | HTML archive through 2020-21 |
| `…/Union-and-State-finances-at-a-Glance-2020-21-final-….pdf` | 200 | PDF `%PDF-1.6` (~10.2 MB) |
| `…/Volume-I-0674d8193e331c4-72536869.pdf` | 200 | PDF `%PDF-1.7` (~1.4 MB) |
| `https://cag.gov.in/en/state-accounts-report` | 200 | HTML (per-state accounts index) |
| `https://cag.gov.in/en/page-statefinances24-25` | 200 | HTML dashboard shell |
| `https://cga.gov.in/` | 200 | HTML (Union accounts orientation) |
| `https://data.rbi.org.in/` | 200 | HTML DBIE SPA shell |
| `https://www.mospi.gov.in/` | 200 | HTML |
