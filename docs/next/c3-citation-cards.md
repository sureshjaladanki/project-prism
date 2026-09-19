# C3 citation cards

Slice: **C3**. Citizen question: What does the Union collect, and what does it spend it on?

Producers on these cards: Ministry of Finance, Budget Division (Union Budget documents on `indiabudget.gov.in`) for Budget Estimates (BE), Revised Estimates (RE) and the previous year’s Actuals as printed in Budget 2026-2027; Controller General of Accounts (CGA), Department of Expenditure, Ministry of Finance, for unaudited monthly Union accounts and for Union Finance Accounts 2024-2025. These are separate records. The page shows each as itself. It does not invent a blended “Union money” figure, a per-person number, or a Prism FRBM score.

Source class (re-carded **18 September 2026**): identify the data requirement; identify the producing office; fetch from official government agencies that can source that dependency (producing office first preference, not the only host); quote producer, series, date, **and fetch source**. A ministry site, `data.gov.in`, CAG as a host of Union Finance Accounts, NITI as a host of that table, or another `*.gov.in` is in when it supplies the **same** dependency. News, private polls, World Bank/IMF/credit-rating tables, and NITI **scorecards** are out. A companion xlsx on `indiabudget.gov.in` is in when it is the **same** Budget 2026-27 statement (same heads, same year columns). RBI Handbook / DBIE Union fiscal tables are allowed only if named as the table of record — not a silent substitute.

Extra-host search on **18 September 2026** (same eleven dependencies): `data.gov.in` HTML catalog/search listed Union Budget **catalogs through 2023-24** and Parliamentary-question extracts, not the 2026-27 statements of record; CAG hosts a **Financial Audit** report on Union accounts 2024-25, not Finance Accounts Statement No. 1 as a spreadsheet; DEA points at the Budget homepage, not a cell-mapped companion; `finmin.nic.in` / `www.mof.gov.in` did not resolve; NITI and MoSPI did not host these tables. **No extra-host file replaced a PDF/HTML card.** `data.gov.in` is not rejected for being a republisher — the hits failed as different series, year, or table.

Budget vintage on these cards: **Union Budget 2026-2027**, laid before Parliament **1 February 2026** (Annual Financial Statement cover). Columns on the Budget statements of record here are **Actuals 2024-2025**, **BE 2025-2026**, **RE 2025-2026**, **BE 2026-2027**, except where a named annex prints a longer run. Latest CGA monthly on these cards: **Union Government Accounts at a Glance as at the end of July 2026** (unaudited provisional), hosted from the CGA Monthly Accounts selector for month **07** / year **2026-2027**. Latest Union Finance Accounts on these cards: **2024-2025** (Actuals vs 2023-2024), CGA `FinanceReport` for that year.

Cell-mapped status after this search (xlsx/csv of the **same** series, any official government host): Cards **1, 2, 3, 5, 6 yes** (producing-office xlsx; fetch URL switched). Cards **4, 7, 8, 9, 10, 11 no** — fetch URLs unchanged (PDF or Word-exported HTML). Extra-host GETs did not supply a same-statement cell-mapped file for those six. Printed PDFs stay named as the book even where the fetch URL is the companion xlsx.

Stable ids (unchanged): `budget-2026-27-tax-revenue` / `cite-c3-budget-2026-27-tax-revenue`; `budget-2026-27-non-tax-revenue` / `cite-c3-budget-2026-27-non-tax-revenue`; `budget-2026-27-capital-receipts` / `cite-c3-budget-2026-27-capital-receipts`; `budget-2026-27-annex1-trends-receipts` / `cite-c3-budget-2026-27-annex1-trends-receipts`; `budget-2026-27-expenditure-stat1` / `cite-c3-budget-2026-27-expenditure-stat1`; `budget-2026-27-deficit-statistics` / `cite-c3-budget-2026-27-deficit-statistics`; `budget-2026-27-liabilities` / `cite-c3-budget-2026-27-liabilities`; `budget-2026-27-frbm-statements` / `cite-c3-budget-2026-27-frbm-statements`; `budget-2026-27-afs` / `cite-c3-budget-2026-27-afs`; `cga-monthly-glance-2026-07` / `cite-c3-cga-monthly-glance-2026-07`; `cga-finance-accounts-2024-25-stat1` / `cite-c3-cga-finance-accounts-2024-25-stat1`.

Geography is **Union / Government of India / Central Government** as the producer prints it — not states, not UTs as own governments, not districts. Do not use a Union total as if it were the country’s public money.

---

## Citation cards

### Card 1 — Receipt Budget: Tax Revenue

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Receipt Budget, 2026-2027 — I. Tax Revenue (major heads as published)
id:           Receipt Budget Part A; fetch file doc/rec/tr.xlsx sheet ReceiptReport123 (printed book doc/rec/tr.pdf). Major heads include 0020 Corporation Tax, 0021 Taxes on Income other than Corporation Tax, 0005 CGST, 0008 IGST, 0009 GST Compensation Cess, 0037 Customs, 0038 Union Excise Duties, and other tax heads as printed. series_id budget-2026-27-tax-revenue; citation_id cite-c3-budget-2026-27-tax-revenue
vintage:      reference_period Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027 (xlsx header row); printed PDF CreationDate 31 January 2026; Budget laid 1 February 2026
url:          https://www.indiabudget.gov.in/doc/rec/tr.xlsx
geography:    Government of India / Union as published. Not a state Finance Accounts table. Not districts.
frequency:    annual budget document
licence:      Not stated on the workbook. indiabudget.gov.in Terms of Use: content provided by Ministry of Finance; NIC hosts; disclaimer, not an open licence. Not stated as CC-BY.
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       BE / RE / Actuals are different vintages in the same table — do not collapse them. Gross tax is not Centre’s net tax (States’ share is netted in other statements). Cell-mapped: yes (xlsx).
```

Fetch host is the producing office (MoF Budget Division on `indiabudget.gov.in`). Printed book (same statement): `https://www.indiabudget.gov.in/doc/rec/tr.pdf` (200 PDF `%PDF-1.7`, 1,091,488 bytes). Xlsx 200 ZIP/XLSX (`PK 03 04`), 22,026 bytes; sheet `ReceiptReport123`; year columns Actuals 2024-2025 / Budget 2025-2026 / Revised 2025-2026 / Budget 2026-2027.

Abstract of all receipt families: `https://www.indiabudget.gov.in/doc/rec/ar.pdf`. Glance table of the same tax/non-tax/capital heads: Budget at a Glance *Receipts*, `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag5.pdf` (PDF 200; linked `bag5.xls` 404). Full Receipt Budget PDF: `https://www.indiabudget.gov.in/doc/rec/allrec.pdf`. Introductory Note: `https://www.indiabudget.gov.in/doc/rec/int.pdf`.

### Card 2 — Receipt Budget: Non-Tax Revenue

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Receipt Budget, 2026-2027 — II. Non-Tax Revenue
id:           Receipt Budget Part A; fetch file doc/rec/ntr.xlsx sheet ReceiptReport123 (printed book doc/rec/ntr.pdf). Heads as published include interest receipts, dividends and profits, other non-tax revenue, receipts of Union Territories. series_id budget-2026-27-non-tax-revenue; citation_id cite-c3-budget-2026-27-non-tax-revenue
vintage:      reference_period Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027 (xlsx header row); printed PDF CreationDate 31 January 2026; Budget laid 1 February 2026
url:          https://www.indiabudget.gov.in/doc/rec/ntr.xlsx
geography:    Government of India / Union as published. “Receipts of Union Territories” here is a Union budget head, not a UT Finance Accounts series.
frequency:    annual budget document
licence:      Same as Card 1 (not on the artifact; MoF content; not CC-BY)
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       Separate from tax revenue and from capital/debt receipts. Do not add Cards 1–3 into a Prism “collections” total that the producer did not print as one series. Sheet title is Non Tax Revenue; a leftover “Tax Revenue” label sits on the year-header row — use the Non-Tax heads (0049, 0050, …). Cell-mapped: yes (xlsx).
```

Fetch host is the producing office. Printed book: `https://www.indiabudget.gov.in/doc/rec/ntr.pdf` (200 PDF, 1,110,593 bytes). Xlsx 200 ZIP/XLSX, 27,087 bytes.

### Card 3 — Receipt Budget: Capital Receipts (non-debt and debt / borrowings as published)

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Receipt Budget, 2026-2027 — III. Capital Receipts (Non-Debt Receipts and Debt Receipts / Borrowings as printed)
id:           Receipt Budget Part A; fetch file doc/rec/ctr.xlsx sheet ReceiptReport123 (printed book doc/rec/cr.pdf). Workbook is ctr.xlsx, not cr.xlsx. Sections as printed: Non Debt Receipts (recoveries of loans and advances; miscellaneous capital receipts); Debt Receipts (Market Loans, Switching, Buyback, Short Term / Treasury Bills, External Loan, Securities against Small Savings, State Provident Fund, other receipts). series_id budget-2026-27-capital-receipts; citation_id cite-c3-budget-2026-27-capital-receipts
vintage:      reference_period Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027 (xlsx header row); printed PDF CreationDate 31 January 2026; Budget laid 1 February 2026
url:          https://www.indiabudget.gov.in/doc/rec/ctr.xlsx
geography:    Government of India / Union as published. Not state borrowings.
frequency:    annual budget document
licence:      Same as Card 1 (not on the artifact; MoF content; not CC-BY)
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       Debt receipts are printed net of repayments on many lines. Do not treat “Total Receipts” on the Abstract as if it excluded borrowings — the Abstract includes debt receipts. Market loans (net) is not the same as gross market borrowings. `cr.xlsx` is 404 — do not fetch it. Cell-mapped: yes (xlsx).
```

Fetch host is the producing office. Printed book: `https://www.indiabudget.gov.in/doc/rec/cr.pdf` (200 PDF, 1,115,051 bytes). Xlsx 200 ZIP/XLSX, 26,594 bytes.

### Card 4 — Receipt Budget Annex-1: Trends in Receipts (run of years)

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Receipt Budget, 2026-2027 — Annex-1 Trends in Receipts
id:           Annex-1; file doc/rec/annex1.pdf. Columns as printed: Actual 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25, RE 2025-26, BE 2026-27. Rows include Revenue Receipts, Tax Revenue (net of States’ share), Non-Tax Revenue, Capital Receipts (with market borrowings, external assistance, short-term, small savings, etc.), and printed deficit lines (Deficit on Revenue Account, Primary deficit, Fiscal deficit). series_id budget-2026-27-annex1-trends-receipts; citation_id cite-c3-budget-2026-27-annex1-trends-receipts
vintage:      reference_period financial years 2017-18 through 2026-27 as column labels in this annex; PDF CreationDate 31 January 2026
url:          https://www.indiabudget.gov.in/doc/rec/annex1.pdf
geography:    Government of India as published. Not states.
frequency:    annual annex (this file’s run is ten columns, not a longer historic series)
licence:      Same as Card 1
next_release: unknown — next Budget annex not dated here
caveat:       Name only the years in this file. Deficit rows sit in the same annex as receipts — they are the producer’s printed lines, not a Prism blend. Do not extend the run with RBI or IMF tables. Analysis of tax/non-tax inside the same run: Annex-2, https://www.indiabudget.gov.in/doc/rec/annex2.pdf. Cell-mapped: no — PDF only. Producing-office annex1.xlsx and annex1.xls returned 404 (18 September 2026). Extra-host search: no same-table xlsx/csv of Annex-1 2026-27 on data.gov.in, DEA, CAG, RBI, NITI, or MoSPI.
```

Fetch host is the producing office. There is **no** 2026-27 document titled “Receipts and Expenditure of Government of India” as a separate time-series book on the live Budget site (checked 18 September 2026). Annex-1 is the Budget’s own multi-year receipts table.

### Card 5 — Expenditure Profile Statement 1: Summary of Expenditure (budget’s own heads)

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Expenditure Profile 2026-2027 — Statement 1 Summary of Expenditure
id:           Expenditure Profile Statement 1; fetch file doc/eb/stat1.xlsx sheet Statement1 (printed book doc/eb/stat1.pdf). Heads as printed: Central Expenditure (Establishment; Central Sector Schemes; Other Central Expenditure); Transfers (Centrally Sponsored Schemes; Finance Commission Transfers; Other Transfers); Total Expenditure through Budget; Resources of Public Enterprises. series_id budget-2026-27-expenditure-stat1; citation_id cite-c3-budget-2026-27-expenditure-stat1
vintage:      reference_period Actuals 2024-2025, Budget Estimates 2025-2026, Revised Estimates 2025-2026, Budget Estimates 2026-2027, each split Revenue / Capital / Total (xlsx header rows 5–6; BE 2026-2027 Total is column 17); printed PDF CreationDate 31 January 2026
url:          https://www.indiabudget.gov.in/doc/eb/stat1.xlsx
geography:    Union budget heads. Transfers to States/UTs are Union outgo as printed — not state Finance Accounts.
frequency:    annual budget document
licence:      Same as Card 1
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       “Total Expenditure through Budget and Resources of Public Enterprises” is a different printed total from “Total Expenditure through Budget”. Do not use scheme MIS or Output-Outcome Framework as this series. BAG table *Expenditure of Government of India* uses the same I–VI heads: https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag6.pdf (linked bag6.xls 404). Cell-mapped: yes (xlsx).
```

Fetch host is the producing office. Printed book: `https://www.indiabudget.gov.in/doc/eb/stat1.pdf` (200 PDF, 889,536 bytes). Xlsx 200 ZIP/XLSX, 8,823 bytes.

Expenditure Budget (Full) ministry-wise demands exist at `https://www.indiabudget.gov.in/doc/eb/allsbe.pdf` (200 PDF) — that is the demand-by-demand book, not this summary statement. Do not ingest every Demand PDF for this slice unless a later card names one.

### Card 6 — Budget at a Glance: Deficit Statistics

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Budget at a Glance 2026-2027 — Deficit Statistics (Fiscal Deficit, Revenue Deficit, Effective Revenue Deficit, Primary Deficit, and Sources of Financing Fiscal Deficit)
id:           BAG table titled Deficit Statistics; fetch workbook doc/Budget_at_Glance/budget_at_a_glance.xlsx sheet “Deficit Statistics” (printed book doc/Budget_at_Glance/bag2.pdf). Parentheses are % of GDP as printed. series_id budget-2026-27-deficit-statistics; citation_id cite-c3-budget-2026-27-deficit-statistics
vintage:      reference_period Actuals 2024-2025, Budget Estimates 2025-2026, Revised Estimates 2025-2026, Budget Estimates 2026-2027 on the statistics table (xlsx rows 4–5); printed PDF CreationDate 1 February 2026
url:          https://www.indiabudget.gov.in/doc/Budget_at_Glance/budget_at_a_glance.xlsx
geography:    Government of India as published
frequency:    annual budget document
licence:      Same as Card 1
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       Use the producer’s labels (FD, RD, ERD, PD) — not a Prism score. GDP in BAG notes is NSO advance estimate as cited by the Budget, not a C3 population series. Ingest the sheet named “Deficit Statistics” — not BAAG, Receipts, Expenditure of GOI, or Transfer of Resources. Linked bag2.xls returned 404. Fiscal deficit in CGA monthly accounts is a different, intra-year unaudited figure (Card 10). Cell-mapped: yes (xlsx sheet Deficit Statistics).
```

Fetch host is the producing office. Printed book: `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag2.pdf` (200 PDF, 438,516 bytes). Workbook 200 ZIP/XLSX (`PK 03 04 14 00 06 00`), 28,188 bytes.

The combined BAG table (Revenue Receipts through Primary Deficit on one page) is `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag1.pdf` and xlsx sheet `BAAG`. That is the producer’s glance layout with separately numbered rows — not a licence to invent one “Union money” number.

### Card 7 — Receipt Budget: Statement of Liabilities of the Central Government (debt as published)

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Receipt Budget, 2026-2027 — Part B: 1 (i) Statement of Liabilities of the Central Government
id:           Annex 1(i); file doc/rec/annex91.pdf. Columns as printed: end of 1950-51; 2021-2022; 2022-2023; 2023-24; 2024-25; Revised 2025-26; Budget 2026-27. Heads: Public Debt (Internal Debt, External Debt*); Other Liabilities; Total / Net Liabilities of the Central Government. External debt footnote: book value / historical rate as printed. series_id budget-2026-27-liabilities; citation_id cite-c3-budget-2026-27-liabilities
vintage:      reference_period outstanding at year-end as labelled in the statement; PDF CreationDate 31 January 2026
url:          https://www.indiabudget.gov.in/doc/rec/annex91.pdf
geography:    Central Government / Government of India as published
frequency:    annual budget document
licence:      Same as Card 1
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       Two printed debt concepts sit nearby: this Statement of Liabilities, and “Debt as defined in the FRBM Act” on BAG deficit charts — do not merge them. Annex-9 narrative (https://www.indiabudget.gov.in/doc/rec/annex9.pdf) also quotes a different coverage note (current exchange rate, EBRs, cash-balance adjustment). Card this statement as itself. Cell-mapped: no — PDF only. Producing-office annex91.xlsx and annex91.xls returned 404 (18 September 2026). Extra-host: data.gov.in resource “Year-wise Details of Outstanding Debt on the Union Government from 2022-23 to 2026-27” is Rajya Sabha Session 270 Starred Question No. 190 (answered 10 March 2026; 189-byte file; Rs. lakh crore) — not Annex 1(i).
```

Fetch host is the producing office. Related Part B files (not this liabilities table): assets `annex92.pdf`; guarantees `annex93.pdf`; asset register `annex94.pdf`.

### Card 8 — Statements of Fiscal Policy under the FRBM Act, 2003

```text
producer:     Ministry of Finance, Budget Division, Government of India
series:       Statements of Fiscal Policy as required under the Fiscal Responsibility and Budget Management Act, 2003 (Budget 2026-2027)
id:           Combined PDF doc/frbm1.pdf (title page February 2026). Contents as printed: (1) Macro-Economic Framework Statement; (2) Medium-term Fiscal Policy cum Fiscal Policy Strategy Statement; plus a Statement of deviation under FRBM Act s.4 / s.7(3)(b) as described in the Preface. Homepage also lists a separate frbm2.pdf for statement (2) — that URL returned 404 on 18 September 2026; this combined file is the artifact that exists. series_id budget-2026-27-frbm-statements; citation_id cite-c3-budget-2026-27-frbm-statements
vintage:      reference_period Budget 2026-27 / RE 2025-26 as discussed in the Preface (Fiscal Deficit 4.4 per cent of GDP in RE 2025-26; 4.3 per cent projected in FY 2026-27 — producer text, not a Prism score); PDF CreationDate 31 January 2026; presented February 2026
url:          https://www.indiabudget.gov.in/doc/frbm1.pdf
geography:    Central Government as in the FRBM statements
frequency:    annual with the Union Budget
licence:      Same as Card 1
next_release: unknown — next FRBM budget statements not dated here
caveat:       Print FRBM labels as printed. Do not turn the 3% / 40% / 60% statutory wording into a Prism grade. Macro-economic prose in this PDF is not a statistical series for receipts or expenditure; Cards 1–7 remain the Budget tables of record for those heads. Cell-mapped: no — PDF only. Producing-office frbm1.xlsx and frbm.xlsx returned 404. Extra-host: data.gov.in “Category-wise Central Government Debt Position as per the Definition in the FRBM Act, 2003 during 2020-21 and 2021-22” is a different year; not this Budget 2026-27 FRBM PDF.
```

Fetch host is the producing office. Key to the Budget Documents 2026-2027 (lists AFS, Demands, Finance Bill, the two FRBM statements, Expenditure Budget, Receipt Budget, Expenditure Profile, Budget at a Glance): `https://www.indiabudget.gov.in/doc/Key_to_Budget_Document_2026.pdf`.

### Card 9 — Annual Financial Statement of the Central Government, 2026-2027

```text
producer:     Ministry of Finance, Budget Division, Government of India (as laid before Parliament)
series:       Annual Financial Statement of the Central Government for 2026-2027
id:           Constitutional AFS; file doc/AFS/allafs.pdf (title page 1 February 2026). Statement I Consolidated Fund (Revenue Account Receipts / Disbursements; Capital Account Receipts / Disbursements); Statement IA Charged disbursements; Statement II Contingency Fund; Statement III Public Account. PDF columns on Statement I Revenue Receipts: Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. series_id budget-2026-27-afs; citation_id cite-c3-budget-2026-27-afs
vintage:      reference_period as in Statement I columns; release_date 1 February 2026 (cover: New Delhi, February 1, 2026); PDF CreationDate 31 January 2026
url:          https://www.indiabudget.gov.in/doc/AFS/allafs.pdf
geography:    Central Government / Consolidated Fund of India, Contingency Fund, Public Account. AFS also includes a statement of Receipts and Expenditure of Union Territories without Legislature — that is still Union accounts, not C5.
frequency:    annual (Article 112)
licence:      Same as Card 1
next_release: unknown — Union Budget 2027-28 is not dated on these artifacts
caveat:       Estimates are net of refunds and recoveries (Key to Budget Documents). Do not use the companion xlsx as this vintage: https://www.indiabudget.gov.in/doc/AFS/allafs.xlsx returned 200 ZIP/XLSX (101,398 bytes) on 18 September 2026 but Sheet1 headers still read Actuals 2022-2023 / Budget Estimates 2023-2024 / Revised Estimates 2023-2024 / Budget Estimates 2024-2025 — not the 2026-27 PDF. Cell-mapped: no — PDF of record; companion xlsx is a different year. Extra-host search found no AFS 2026-27 workbook with these Statement I columns.
```

Fetch host is the producing office.

### Card 10 — CGA Monthly Accounts: Union Government Accounts at a Glance (upto July 2026)

```text
producer:     Controller General of Accounts (CGA), Department of Expenditure, Ministry of Finance
series:       Union Government Accounts at a Glance as at the end of July 2026 (Monthly Accounts)
id:           CGA Monthly Accounts selector month=07, year=2026-2027; published page MonthlyReport/Published/7/2026-2027.aspx; artifact file writereaddata/MonthAccount/72026/DATA2627.htm (title: GOVERNMENT OF INDIA UNION GOVERNMENT ACCOUNTS AT A GLANCE). Detail HTMs in the same folder: DTL12627.htm, DTL22627.htm. Columns as printed: Budget Estimates 2026-2027; Actuals @ upto July 2026; % of Actuals to Budget Estimates (current and COPPY). series_id cga-monthly-glance-2026-07; citation_id cite-c3-cga-monthly-glance-2026-07
vintage:      reference_period April–July 2026 of FY 2026-2027 vs BE 2026-2027
url:          https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.htm
geography:    Government of India / Union Government as printed. Not states, not districts.
frequency:    monthly during the year
licence:      CGA site footer: website belongs to Controller General of Accounts, Ministry of Finance; © 2016, All rights reserved, National Informatics Centre Services Inc. Not stated as CC-BY.
next_release: unknown — Advance Release Calendar page (https://cga.gov.in/Page/Advance-Release-Calendar.aspx) did not expose a dated month table in the HTML fetched on 18 September 2026.
caveat:       Actuals are unaudited provisional (@). Fiscal deficit in the monthly file is not necessarily the year-end deficit (producer note on temporal mismatch). Do not substitute Budget Actuals 2024-25 or Finance Accounts 2024-25 for this intra-year file. Cell-mapped: no — Word-exported HTML (`xmlns:v`, `MsoNormalTable`); six `<table>` elements with `<td>` exist, but headers are split/colspan and are not a spreadsheet grid. Producing-office DATA2627.xlsx / .xls / .csv returned 404. No xlsx/csv export on the July 2026 Published page. Extra-host: data.gov.in “Accounts at a Glance July 2026” hits are stale Budget at a Glance years, MGNREGA, TNEB, and fisheries “at a glance” tables — not CGA monthly July 2026.
```

Fetch host is the producing office (`cga.gov.in`). Locator (not the table): `https://cga.gov.in/MonthlyReport/Published/7/2026-2027.aspx`. Prior months in the same FY on this host: `/MonthlyReport/Published/4/2026-2027.aspx`, `/5/`, `/6/`. `cga.nic.in` serves the same site (200). Use `https://cga.gov.in/` — not `www.cga.gov.in`.

### Card 11 — CGA Union Finance Accounts 2024-2025, Statement No. 1 Summary of Transactions

```text
producer:     Controller General of Accounts (CGA), Ministry of Finance. CAG certificate PDF is a companion on the same CGA FinanceReport page — CGA remains the accounts publisher here.
series:       Finance Accounts, Union Government, 2024-2025 — No. 1 Summary of Transactions (receipts and disbursements, Actuals)
id:           CGA FinanceReport year 2024-2025; Statement1 PDF Fin20242025Statement1.pdf. Title on the statement: FINANCE ACCOUNTS, UNION GOVERNMENT; No. 1—SUMMARY OF TRANSACTIONS. Columns: Actuals 2024-2025 and 2023-2024 (In crores of rupees), Consolidated Fund revenue receipt/disbursement heads as printed. series_id cga-finance-accounts-2024-25-stat1; citation_id cite-c3-cga-finance-accounts-2024-25-stat1
vintage:      reference_period financial year 2024-2025 (with 2023-2024 comparatives); PDF CreationDate 20 December 2025; CGA FinanceReport page https://cga.gov.in/FinanceReport/Published/2024-2025.aspx
url:          https://cga.gov.in/writereaddata/file/Fin20242025Statement1.pdf
geography:    Union Government as printed. Annexure to Statement 1 (page 26 in this PDF) shows proceeds assigned to States — that is Union tax assignment, not C5 state accounts.
frequency:    annual audited-year accounts (this file’s figures are Actuals)
licence:      Same CGA site reservation as Card 10 (all rights reserved; not CC-BY)
next_release: unknown — Finance Accounts 2025-2026 not on the CGA year dropdown as of 18 September 2026 (latest option 2024-2025)
caveat:       Annual Actuals, not BE/RE. Do not silent-substitute this file when monthly accounts are what the page needs, or vice versa. Gross vs net tax (proceeds assigned to States) is in the Statement 1 annexure. Introduction PDF: https://cga.gov.in/writereaddata/file/Fin20242025Introduction.pdf. CGA certificate: https://cga.gov.in/writereaddata/file/Fin20242025CGACert.pdf. CAG certificate companion on the same CGA page: https://cga.gov.in/writereaddata/file/Fin20242025CAGCert.pdf. Cell-mapped: no — PDF only. Producing-office Fin20242025Statement1.xlsx / .xls / .csv returned 404. Extra-host: CAG Report No. 6 of 2026 is a Financial Audit on Accounts of the Union Government 2024-25, not Statement No. 1 as cells. data.gov.in “Finance Accounts” catalogs are state/scheme finance files, not this Union statement.
```

Fetch host is the producing office (CGA). CAG was searched as a **host** of the same Statement No. 1: homepage `https://cag.gov.in/` (302 → `/en`, 200 HTML, 377,023 bytes) lists State Accounts, Combined Finance and Revenue Accounts–Union & State (`https://cag.gov.in/en/combined-accounts`, 200 — a different combined product), and State Finances 2024-25. Audit-report hit: [Report No. 6 of 2026](https://cag.gov.in/en/audit-report/details/125152) (200 HTML) — *Report of the CAG of India on Accounts of the Union Government for the year 2024-25* (Financial Audit); full PDF 200, 3,994,339 bytes. That is a CAG audit report, not CGA Statement No. 1. Do not switch Card 11. CAG remains the certificate companion on the CGA FinanceReport page.

---

## Licence and calendar artifacts (not series)

- Union Budget Terms of Use: `https://www.indiabudget.gov.in/termsofuse.php` (200 HTML). Content provided by Ministry of Finance; designed/developed/maintained by NIC; legal disclaimer; no CC-BY statement. `copyright.php` and `websitepolicies.php` returned 404. Disclaimer: `https://www.indiabudget.gov.in/disclaimer.php` (200). Privacy: `https://www.indiabudget.gov.in/privacypolicy.php` (200). Homepage footer: content managed and owned by Ministry of Finance; hosted by NIC.
- CGA Terms of Use: `https://cga.gov.in/Page/Terms-of-Use.aspx` (200). Site footer: © 2016, All rights reserved, NICSI.
- CGA Advance Release Calendar page exists (`https://cga.gov.in/Page/Advance-Release-Calendar.aspx`, 200) but the fetched HTML did not include a dated month list — do not invent a next monthly date from it.
- Key to Budget Documents 2026-2027: `https://www.indiabudget.gov.in/doc/Key_to_Budget_Document_2026.pdf` (200). Previous Union Budgets locator: `https://www.indiabudget.gov.in/previous_union_budget.php` (200).
- Named Budget PDF/XLSX URLs did not present a login wall (HTTP 200).

---

## Considered and rejected

| Series | Why rejected |
|--------|----------------|
| `doc/frbm2.pdf` (Macro-Economic Framework as a separate file) | Linked from the Budget homepage; **404** on 18 September 2026. Combined statements are Card 8. |
| `doc/frbm1.xlsx`, `doc/frbm.xlsx` | **404**. Card 8 stays `frbm1.pdf`. |
| `doc/rec/annex1.xlsx`, `annex1.xls` | **404**. Card 4 stays `annex1.pdf`. |
| `doc/rec/annex91.xlsx`, `annex91.xls`, `annex9.xlsx` | **404**. Card 7 stays `annex91.pdf`. |
| `doc/rec/cr.xlsx` | **404**. Capital Receipts workbook of record is `ctr.xlsx` (Card 3). |
| `doc/Budget_at_Glance/bag1.xls`, `bag2.xls`, `bag5.xls`, `bag6.xls` | Linked from the homepage; **404**. Use the PDFs and `budget_at_a_glance.xlsx` (Card 6 fetch is that xlsx, sheet Deficit Statistics). |
| `doc/AFS/allafs.xlsx` | 200 XLSX (101,398 bytes), but sheet headers are still Actuals **2022-2023** / BE **2024-2025**. Not the 2026-27 AFS PDF. Do not ingest as this vintage. |
| `MonthAccount/72026/DATA2627.xlsx` / `.xls` / `.csv` | **404**. Card 10 stays the HTM. |
| `file/Fin20242025Statement1.xlsx` / `.xls` / `.csv` | **404**. Card 11 stays the PDF. |
| Standalone “Receipts and Expenditure of Government of India” time-series book | Not on the 2026-27 document list. Use Card 4 Annex-1 for the years that file actually contains. |
| Economic Survey 2025-2026 (`economicsurvey/index.php`) | Charter-out narrative. Reprint tables only if the producing Budget/CGA series is cited — it is not the series. |
| Output Outcome Framework 2026-2027 (`doc/OutcomeBudgetE2026_2027.pdf`) | Scheme outputs, not Union receipts/expenditure/deficit/debt as accounts. |
| Implementation of Budget Announcements 2025-26; Budget Highlights; Budget Speech | Narrative / announcement tracking, not the accounts series. |
| Finance Bill / tax notifications | Law, not the receipts table of record (Card 1). |
| Expenditure Budget Full (`allsbe.pdf`) and each Demand for Grants | Ministry demand books; charter is the budget’s own summary heads (Card 5). Do not pull every DG. |
| BAG *Transfer of Resources to States and Union Territories with Legislature* (`bag3.pdf`); xlsx sheet “Transfer of Resources”; Receipt Budget Annex 4 / 4A / 4B state-wise devolution | Union transfers / tax assignment by State. Not C5 state finances; parked so C3 stays Union-only. |
| State / UT Finance Accounts; local-body accounts; district files | Charter-out (C5 / parked). |
| Scheme MIS, ministry “achievements”, NITI scorecards | Charter-out. |
| SEBI LODR; USAFacts “four missions”; a US 10-K frame | Charter-out. |
| World Bank, IMF, credit-rating agencies, news, think tanks | Not the producing office. |
| data.gov.in Union Budget **catalogs** 2018-19 / 2019-20 Interim / 2021-22 / 2022-23 / 2023-24 (DEA) | Official government host. **Wrong year** — latest Budget catalog on the portal this run is 2023-24, not Receipt/Expenditure/BAG/AFS/FRBM 2026-27. |
| data.gov.in “Year-wise Details of Outstanding Debt on the Union Government from 2022-23 to 2026-27” (`/resource/year-wise-details-outstanding-debt-union-government-2022-23-2026-27`, 200 HTML) | Rajya Sabha Session 270 Starred Question No. 190 (10 March 2026; 189-byte file). Not Receipt Budget Annex 1(i) (Card 7). |
| data.gov.in “Year-wise Deficit Statistics under Union Budget from 2021-22 to 2023-24”; “Deficit Statistics 2020-21 to 2022-23” | Official host of a **different year** than BAG Deficit Statistics 2026-27 (Card 6). |
| data.gov.in Budget at a Glance extracts (2016-17–2018-19; 2019-20 Interim; 2019-20–2021-22; 2020-21–2022-23; 2021-22–2023-24) | Stale BAG years. Not `budget_at_a_glance.xlsx` sheet Deficit Statistics for 2026-27. |
| data.gov.in scheme-wise Tax Revenue / Non-Tax Revenue 2021-22 to 2023-24; scheme-wise BE/RE/Actuals 2024-25 to 2026-27; cesses and surcharges 2022-23 to 2026-27; gender budget; tax slabs Budget 2025-26 | Different table (scheme-wise, PQ extract, or tax-rate) — not Cards 1–3 or 5 Statement 1. |
| data.gov.in “Category-wise Central Government Debt Position as per the Definition in the FRBM Act, 2003 during 2020-21 and 2021-22” | FRBM-labelled, **wrong years** vs Card 8 Budget 2026-27 statements. |
| data.gov.in catalog title search “Finance Accounts” | Hits are CPI Gujarat, Punjab SC loans, PMJDY, PM-KISAN, panchayat finance, Assam procurement — not Union Finance Accounts 2024-25 Statement No. 1. |
| data.gov.in search “Finance Accounts 2024-25 Statement 1”; “Accounts at a Glance July 2026”; “FRBM 2026-27”; “Receipt Budget Tax Revenue”; “Deficit Statistics 2026-27”; “Annual Financial Statement 2026-27” | HTML search ran. No same-table cell-mapped file of the named 2026-27 / July 2026 / FA 2024-25 Statement 1 series. |
| `dea.gov.in` Union Budget tile | 200 HTML; link is `https://www.indiabudget.gov.in/` (locator), not a cell-mapped statement file. Economic Survey tile is charter-out narrative. |
| `www.dea.gov.in` | SSL check failed (curl 60). Use `https://dea.gov.in/`. |
| `finmin.nic.in`, `www.finmin.nic.in`, `www.mof.gov.in` | Could not resolve host (curl 6) on 18 September 2026. |
| RBI Handbook of Statistics / DBIE Union fiscal tables | Allowed only if named as table of record. Budget and CGA files exist for this vintage — do not silent-substitute RBI. Handbook locator 200 HTML (423,208 bytes, 18 September 2026); not carded. |
| CAG Combined Finance and Revenue Accounts–Union & State (`cag.gov.in/en/combined-accounts`) | Different product (combined Union and State). Not Card 11 Statement No. 1. |
| CAG Report No. 6 of 2026 on Accounts of the Union Government 2024-25 (Financial Audit) | Same year as Card 11, **different table** (audit report PDF, 3,994,339 bytes). Keep CGA Statement 1 PDF. |
| CAG State Accounts / State Finances 2024-25 / UT finances | Charter-out (C5 / parked). |
| NITI homepage and SDG overview (`/competitive-federalism/overview-sustainable-development-goals`, 200) | Scorecards out. NITI did not host the named eleven tables this run. |
| MoSPI homepage (`www.mospi.gov.in`, 200 SPA shell, 2,657 bytes) | Host only; not the producer of Union Budget / CGA accounts. No named C3 table on this fetch. |
| CGA Accounts at a Glance **annual** dropdown (2024-2025 …) and GFSM Data | Different CGA products; this slice uses monthly Accounts at a Glance (Card 10) and Finance Accounts Statement 1 (Card 11). |
| `www.cga.gov.in` | SSL hostname mismatch (`SEC_E_WRONG_PRINCIPAL`); use `https://cga.gov.in/`. |

`data.gov.in` is **not** rejected merely for being a republishing host. Rows above that name `data.gov.in` failed because they are a different series, a different year, a different table, or a scorecard — not because NIC hosted them. CKAN `package_search` returned **500** this run; HTML catalog/search was used instead.

---

## Geography Steward

**Required: no re-run.** The eleven series and printed Union labels are unchanged versus `docs/next/c3-geography-frame.md`. Cards 1, 2, 3, 5, and 6 now fetch producing-office xlsx of the **same** Budget 2026-27 statements; Cards 4, 7, 8, 9 remain the same PDFs; Card 10 remains `DATA2627.htm`; Card 11 remains `Fin20242025Statement1.pdf`. No new printed names. Union-only frame unchanged.

**Missing / parked (name them):** all States; all Union Territories as own governments (including NCT of Delhi and Puducherry with legislatures, and UTs without legislature as separate finance accounts); all districts and below.

Do not recode labels here. Do not ingest Annex 4 state-wise rows or BAG transfers-to-States as if they were C5. AFS “Receipts and Expenditure of Union Territories without Legislature” stays inside Union accounts — it does not fill the missing State/UT finance units.

---

## Handoff

Next persona: **ingest-engineer**. Do not fetch in this librarian pass. `geography_frame` already exists (`docs/next/c3-geography-frame.md`); no Geography Steward re-run. Do not unblock C2. Do not start C4–C20. Do not move `citizen_pointer`.

Ingest fetches the **named card URLs** (xlsx for Cards 1, 2, 3, 5, 6; PDF/HTML for the rest). Current `parse_c3.py` still stops on PDF/HTML; xlsx parse is Ingest’s job. Do not write Budget/CGA files into `data/` in this librarian job. Do not fetch 404 paths (`frbm2.pdf`, `bag*.xls`, `annex1.xlsx`, `annex91.xlsx`, `DATA2627.xlsx`, `Fin20242025Statement1.xlsx`). Do not fetch `allafs.xlsx` for 2026-27. Do not pull state Finance Accounts, district files, Economic Survey prose, or RBI as a stand-in.

Keep three records: Budget 2026-27, CGA monthly (July 2026), Finance Accounts 2024-25 Statement No. 1.

---

## HTTP status (verified GET, 18 September 2026)

Browser User-Agent used (required for CGA). Magic / size from this run.

| URL | Status | Type |
|-----|--------|------|
| `https://www.indiabudget.gov.in/` | 200 | HTML (354,821 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/tr.pdf` | 200 | PDF `%PDF-1.7` (1,091,488 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/tr.xlsx` | 200 | XLSX (`PK 03 04`; 22,026 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/ntr.pdf` | 200 | PDF (1,110,593 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/ntr.xlsx` | 200 | XLSX (27,087 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/cr.pdf` | 200 | PDF (1,115,051 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/ctr.xlsx` | 200 | XLSX (26,594 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/cr.xlsx` | 404 | HTML stub (1,245 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/ar.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/rec/int.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/rec/allrec.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/rec/annex1.pdf` | 200 | PDF (711,987 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/annex1.xlsx` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/rec/annex1.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/rec/annex2.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/rec/annex9.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/rec/annex91.pdf` | 200 | PDF (649,624 bytes) |
| `https://www.indiabudget.gov.in/doc/rec/annex91.xlsx` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/rec/annex91.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/rec/annex9.xlsx` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/eb/stat1.pdf` | 200 | PDF (889,536 bytes) |
| `https://www.indiabudget.gov.in/doc/eb/stat1.xlsx` | 200 | XLSX (8,823 bytes) |
| `https://www.indiabudget.gov.in/doc/eb/allsbe.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag1.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag2.pdf` | 200 | PDF (438,516 bytes) |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag5.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag6.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/budget_at_a_glance.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/budget_at_a_glance.xlsx` | 200 | XLSX (`PK 03 04 14 00 06 00`; 28,188 bytes) |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag1.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag2.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag5.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag6.xls` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/frbm1.pdf` | 200 | PDF (1,623,802 bytes) |
| `https://www.indiabudget.gov.in/doc/frbm2.pdf` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/frbm1.xlsx` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/frbm.xlsx` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/doc/AFS/allafs.pdf` | 200 | PDF `%PDF-1.6` (934,171 bytes) |
| `https://www.indiabudget.gov.in/doc/AFS/allafs.xlsx` | 200 | XLSX (101,398 bytes; stale year headers — not Card 9) |
| `https://www.indiabudget.gov.in/doc/Key_to_Budget_Document_2026.pdf` | 200 | PDF |
| `https://www.indiabudget.gov.in/termsofuse.php` | 200 | HTML |
| `https://www.indiabudget.gov.in/disclaimer.php` | 200 | HTML |
| `https://www.indiabudget.gov.in/privacypolicy.php` | 200 | HTML |
| `https://www.indiabudget.gov.in/copyright.php` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/websitepolicies.php` | 404 | HTML stub |
| `https://www.indiabudget.gov.in/previous_union_budget.php` | 200 | HTML |
| `https://cga.gov.in/` | 200 | HTML (306,258 bytes; GET with browser UA) |
| `https://cga.gov.in/MonthlyReport/Published/7/2026-2027.aspx` | 200 | HTML (374,263 bytes) |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.htm` | 200 | HTML (`<html xmlns:v`; 130,160 bytes) |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DTL12627.htm` | 200 | HTML |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DTL22627.htm` | 200 | HTML |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.xlsx` | 404 | HTML stub |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.xls` | 404 | HTML stub |
| `https://cga.gov.in/writereaddata/MonthAccount/72026/DATA2627.csv` | 404 | HTML stub |
| `https://cga.gov.in/FinanceReport/Published/2024-2025.aspx` | 200 | HTML (105,007 bytes) |
| `https://cga.gov.in/writereaddata/file/Fin20242025Statement1.pdf` | 200 | PDF (1,133,367 bytes) |
| `https://cga.gov.in/writereaddata/file/Fin20242025Statement1.xlsx` | 404 | HTML stub |
| `https://cga.gov.in/writereaddata/file/Fin20242025Statement1.xls` | 404 | HTML stub |
| `https://cga.gov.in/writereaddata/file/Fin20242025Statement1.csv` | 404 | HTML stub |
| `https://cga.gov.in/writereaddata/file/Fin20242025Introduction.pdf` | 200 | PDF |
| `https://cga.gov.in/writereaddata/file/Fin20242025CGACert.pdf` | 200 | PDF |
| `https://cga.gov.in/writereaddata/file/Fin20242025CAGCert.pdf` | 200 | PDF |
| `https://cga.gov.in/Page/Advance-Release-Calendar.aspx` | 200 | HTML |
| `https://cga.gov.in/Page/Terms-of-Use.aspx` | 200 | HTML |
| `https://cga.nic.in/` | 200 | HTML (same app as cga.gov.in) |
| `https://cag.gov.in/` | 302 → `/en` | HTML |
| `https://cag.gov.in/en` | 200 | HTML (377,023 bytes) |
| `https://cag.gov.in/en/combined-accounts` | 200 | HTML (79,436 bytes; Combined Finance and Revenue Accounts–Union & State — not Card 11) |
| `https://cag.gov.in/en/state-accounts-report` | 200 | HTML |
| `https://cag.gov.in/en/audit-report` | 200 | HTML |
| `https://cag.gov.in/en/audit-report?title=Finance%20Accounts%20Union` | 200 | HTML (160,538 bytes) |
| `https://cag.gov.in/en/audit-report/details/125152` | 200 | HTML (84,496 bytes; Report No. 6 of 2026 Financial Audit) |
| `https://cag.gov.in/webroot/uploads/download_audit_report/2026/6of2026UGEng-069ce496f1158e0.22682438.pdf` | 200 | PDF (3,994,339 bytes; not Statement No. 1) |
| `https://cag.gov.in/uploads/PressRelease/PR-Press-Release-on-Report-no-6-of-2026-in-english-069ce58face4518-40869759.pdf` | 200 | PDF (564,261 bytes) |
| `https://cag.gov.in/en/search?keys=Union%20Finance%20Accounts%202024-25` | 404 | HTML |
| `https://cag.gov.in/en/search/node?keys=Union%20Finance%20Accounts` | 404 | HTML |
| `https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook%20of%20Statistics%20on%20Indian%20Economy` | 200 | HTML (423,208 bytes; rejected as substitute) |
| `https://www.data.gov.in/` | 200 | HTML (`text/html; charset=utf-8`) |
| `https://www.data.gov.in/catalogs` | 200 | HTML |
| `https://data.gov.in/api/3/action/package_search?q=union%20budget%202026-27&rows=3` | 302 then **500** | HTML error (387 bytes) |
| `https://www.data.gov.in/search?title=Union%20Budget%202026-27` | **500** via curl; **200** in browser HTML/JS | Catalogs through 2023-24 (wrong year) plus PQ extracts |
| `https://www.data.gov.in/catalogs?title=Union%20Budget%202026-27&sortby=_score` | **500** via curl; **200** in browser | Same catalog hits as above |
| `https://www.data.gov.in/catalog/union-budget` | 302 → `/not-found` then 200 | HTML stub page |
| `https://www.data.gov.in/catalog/finance-accounts` | **500** | HTML error |
| `https://www.data.gov.in/catalog/union-budget-2013-14-expenditure-budget` | **500** | HTML error |
| `https://www.data.gov.in/ministrydepartment/ministry-finance` | **500** | HTML error |
| `https://www.data.gov.in/resource/year-wise-details-outstanding-debt-union-government-2022-23-2026-27` | 200 | HTML (1,003,771 bytes; Rajya Sabha PQ — not Card 7) |
| `https://www.data.gov.in/catalogs?title=Finance%20Accounts` | 200 in browser | State/scheme finance catalogs — not Union Statement 1 |
| `https://www.data.gov.in/search?title=Finance%20Accounts%202024-25%20Statement%201` | 200 in browser | No same-table hit |
| `https://www.data.gov.in/search?title=Accounts%20at%20a%20Glance%20July%202026` | 200 in browser | Stale BAG / other “at a glance” — not Card 10 |
| `https://www.data.gov.in/search?title=FRBM%202026-27` | 200 in browser | FRBM debt 2020-21/2021-22 — wrong year |
| `https://www.data.gov.in/search?title=Receipt%20Budget%20Tax%20Revenue` | 200 in browser | Scheme-wise / stale-year tax tables — not Card 1 |
| `https://www.data.gov.in/search?title=Deficit%20Statistics%202026-27` | 200 in browser | Deficit Statistics 2020-23 / 2021-24 — wrong year |
| `https://dea.gov.in/` | 200 | HTML (92,798 bytes; Union Budget tile → indiabudget.gov.in locator) |
| `https://www.dea.gov.in/` | SSL fail (curl 60) | — |
| `https://finmin.nic.in/` | DNS fail (curl 6) | Could not resolve host |
| `https://www.finmin.nic.in/` | DNS fail (curl 6) | Could not resolve host |
| `https://www.mof.gov.in/` | DNS fail (curl 6) | Could not resolve host |
| `https://www.niti.gov.in/` | 200 | HTML (123,549 bytes) |
| `https://www.niti.gov.in/competitive-federalism/overview-sustainable-development-goals` | 200 | HTML (SDG scorecard family — not a named C3 table) |
| `https://www.mospi.gov.in/` | 200 | HTML SPA shell (2,657 bytes) |
| `https://www.cga.gov.in/` | SSL hostname mismatch (curl 60, `SEC_E_WRONG_PRINCIPAL`) | — |

---

## Return to parent

1. **Fetch URL changes (five cards):**
   - Card 1: `https://www.indiabudget.gov.in/doc/rec/tr.pdf` → `https://www.indiabudget.gov.in/doc/rec/tr.xlsx`
   - Card 2: `https://www.indiabudget.gov.in/doc/rec/ntr.pdf` → `https://www.indiabudget.gov.in/doc/rec/ntr.xlsx`
   - Card 3: `https://www.indiabudget.gov.in/doc/rec/cr.pdf` → `https://www.indiabudget.gov.in/doc/rec/ctr.xlsx`
   - Card 5: `https://www.indiabudget.gov.in/doc/eb/stat1.pdf` → `https://www.indiabudget.gov.in/doc/eb/stat1.xlsx`
   - Card 6: `https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag2.pdf` → `https://www.indiabudget.gov.in/doc/Budget_at_Glance/budget_at_a_glance.xlsx` (sheet **Deficit Statistics**)
   - Cards 4, 7, 8, 9, 10, 11: **unchanged**

2. **Cell-mapped:** 1 yes, 2 yes, 3 yes, 4 no, 5 yes, 6 yes, 7 no, 8 no, 9 no, 10 no, 11 no.

3. **Geography Steward re-run:** **no**.

4. **Searched and did not replace a PDF/HTML:** producing-office companions `annex1.xlsx`/`xls`, `annex91.xlsx`/`xls`, `frbm1.xlsx`/`frbm.xlsx` **404**; `allafs.xlsx` **200 but Actuals 2022-2023 / BE 2024-2025** (not Card 9); `bag*.xls` **404**; CGA `DATA2627.xlsx`/`xls`/`csv` and `Fin20242025Statement1.xlsx`/`xls`/`csv` **404**. Extra hosts: `data.gov.in` CKAN **500**; HTML search found Union Budget catalogs **through 2023-24**, Rajya Sabha outstanding-debt PQ, stale BAG/deficit years, scheme-wise extracts — **not** the eleven 2026-27 / July 2026 / FA Statement 1 files; CAG Combined Accounts and Report No. 6 of 2026 (Financial Audit) are **different products**; DEA is a Budget homepage locator; `finmin.nic.in` / `www.mof.gov.in` did not resolve; RBI Handbook **200** (rejected substitute); NITI SDG scorecards out; MoSPI SPA host only.
