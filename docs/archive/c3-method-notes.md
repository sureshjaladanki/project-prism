# C3 method notes

Persona: Methodologist. Sleeve: **Money**. Slice: **C3**.

Citizen question: What does the Union collect, and what does it spend it on?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`. Schema for caveats already exists in [`docs/data-contracts.md`](../data-contracts.md) (`caveat_id`, `concept`, `unit`, `population`, `reference_period`, `producer_definition`, `comparable_from`, `breaks`, `lags`, `disagrees_with`, `do_not`). This pass writes the notes, not the store. When the slice becomes a product, Platform Architect still owns CMS and the refresh contract.

Locked inputs: [`c3-citation-cards.md`](c3-citation-cards.md), [`c3-geography-frame.md`](c3-geography-frame.md). Charter: [`c3-charter.md`](c3-charter.md).

**Budget statements, CGA monthly accounts, and Finance Accounts are three records.** Cards 1–9 are Union Budget 2026-27 (laid 1 February 2026): BE, RE, and printed Actuals as labelled. Card 10 is CGA unaudited monthly accounts to end-July 2026. Card 11 is CGA Finance Accounts 2024-25 Actuals. Do not pick a winner. Do not invent a blended “Union money” figure or a per-person number.

**Budget estimates, revised estimates, and actuals are different series.** Never chart them as one continuous collect or spend. A column labelled Actuals 2024-25 in the Budget book is still the Budget’s printed Actuals — not Card 11.

**Release date is not the reference period.** Budget laid 1 February 2026; PDF CreationDate late January 2026; CGA news 1 September 2026. Financial years and “upto July 2026” on the row are the reference periods.

**Union is not the country’s public money.** Frames A–C are Union-only. States, UTs as own governments, and districts are missing (C5 / parked). Transfers and tax assignment printed on Union statements are Union outgo, not C5.

**FRBM labels as printed — not a Prism score.** Two nearby debt concepts stay two concepts (Card 7 liabilities vs FRBM-defined debt on BAG charts).

**How the cited table was built (print on the page methodology).** When a cited table was reconstructed from PDF or HTML — not from a spreadsheet cell map — the methodology section must say so, name the parser class, and say ingest **stopped rather than guessed** if a number could sit in two columns.

- **Spreadsheet cell map (openpyxl):** Cards **1, 2, 3, 5, 6**. Producing-office xlsx of the same Budget 2026-27 statement. Do not describe these as PDF scrapes.
- **PDF word-to-column:** Cards **4, 7, 9, 11**. pdfplumber words assigned to a unique nearest year-column. Ingest flag: `pdfplumber words; assigned=…; ambiguous=0`. Repo lock is pdfplumber (stop if scanned or ambiguous), not Camelot. `ambiguous=0` is the accuracy analogue.
- **HTML table expand:** Card **10**. stdlib html.parser; table 0; colspan/rowspan expanded. Ingest flag: `html table 0; colspan/rowspan expanded`.
- **Not a table:** Card **8**. Statutory FRBM prose packet. Do not print a reconstructed receipts/expenditure/deficit/debt grid. Do not ingest page 9 “Economic Performance at a Glance” as this card.

Reconstruction with `ambiguous=0` is a named method. It is not a substitute for the producer’s spreadsheet when one exists. This note does not rewrite Platform’s [`c3-refresh-contract.md`](c3-refresh-contract.md) as a ship.

Integrity the methodology must name (not hide): amounts rest on a unique column map, so the grid is usable; PDF **line labels** can wrap or truncate (`(Details in Annexure 2)` instead of Tax Revenue; `Market Loans ( Annex.`); AFS/FA labels can include CID/Hindi font leftovers, with English head names still present; Finance Accounts can emit a column-number header row (`1, 2, 3`) — ingest drops 1–2 digit index rows and must not treat them as crores; Card 8 cannot be reconstructed as this card’s collect/spend/deficit/debt grid (deficit/debt figures remain on Cards 6–7; the missing piece is the FRBM statutory packet).

---

## Card 1 — Receipt Budget: Tax Revenue

Binds: citation Card 1. Geography: **Frame A**.

```text
concept:            Union tax revenue by major heads as printed in Receipt Budget 2026-27 Part A (I. Tax Revenue): corporation tax, taxes on income other than corporation tax, CGST, IGST, GST Compensation Cess, customs, Union excise, and other tax heads on the statement. Gross tax is not Centre’s net tax.
unit:               Rupees as labelled on the statement (typically crore). Blank / dotted cells are not zero.
population:         Government of India / Union tax receipts as published. Not state tax. Not districts. Not a per-person tax.
reference_period:   Column label on the cell: Actuals 2024-2025, BE 2025-2026, RE 2025-2026, or BE 2026-2027. Not the 1 February 2026 laying date.
producer_definition: Receipt Budget, 2026-2027 — I. Tax Revenue; major heads include 0020 Corporation Tax, 0021 Taxes on Income other than Corporation Tax, 0005 CGST, 0008 IGST, 0009 GST Compensation Cess, 0037 Customs, 0038 Union Excise Duties (MoF Budget Division, fetch tr.xlsx sheet ReceiptReport123; printed book tr.pdf). Tidy table: openpyxl cells of that sheet (ingest flag `sheet=ReceiptReport123`) — not reconstructed from tr.pdf. States’ share is netted in other statements — this card is the tax-revenue statement as printed.
comparable_from:    The four columns in this file. A longer run of receipts lives on Card 4 (Annex-1), which uses net-of-States’-share tax — not this gross-head table.
breaks:             BE vs RE vs Actuals in the same table: four vintages, not one line. GST Compensation Cess BE 2026-27 printed blank/dots in BAG Receipts — a hole, not 0. Do not recode onto Frame B or C. Spreadsheet cell map of the same Budget statement — not a PDF scrape.
lags:               Budget laid 1 February 2026. next_release unknown (Budget 2027-28 not dated on these artifacts).
disagrees_with:     Card 4 tax revenue net of States’ share (same Budget family, different concept). Card 9 AFS revenue receipts (constitutional statement). Card 10 monthly actuals vs BE. Card 11 Finance Accounts Actuals 2024-25. Fetch tr.xlsx is the same statement as printed tr.pdf — not a second series.
do_not:             Do not collapse BE/RE/Actuals. Do not treat gross tax as Centre’s net tax. Do not add Cards 1–3 into a Prism “collections” total the producer did not print as one series. Do not chart blank cess as 0. Do not use Finance Bill slabs as this series. Do not present Union tax as all-India public receipts. Do not rank, forecast, or per-person. Do not present this card as reconstructed from PDF or HTML.
```

---

## Card 2 — Receipt Budget: Non-Tax Revenue

Binds: citation Card 2. Geography: **Frame A**.

```text
concept:            Union non-tax revenue as printed (II. Non-Tax Revenue): interest receipts, dividends and profits, other non-tax revenue, receipts of Union Territories, and other heads on the statement.
unit:               Rupees as labelled. Blank is not zero.
population:         Government of India / Union. “Receipts of Union Territories” here is a Union budget head, not UT Finance Accounts (C5).
reference_period:   Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027 as column labels. Not 1 February 2026.
producer_definition: Receipt Budget, 2026-2027 — II. Non-Tax Revenue (MoF Budget Division, fetch ntr.xlsx sheet ReceiptReport123; printed book ntr.pdf). Tidy table: openpyxl cells of that sheet (ingest flag `sheet=ReceiptReport123`) — not reconstructed from ntr.pdf. Separate from tax revenue and from capital/debt receipts. A leftover “Tax Revenue” label sits on the year-header row — use the Non-Tax heads.
comparable_from:    The four columns in this file. Card 4 Annex-1 has a Non-Tax Revenue row in its own run — still a different table.
breaks:             BE vs RE vs Actuals. Do not add to Card 1 as one “revenue” unless the producer prints that total on Abstract of Receipts — and then cite the Abstract as the producer’s printed total, not a user sum of Cards 1–2. Spreadsheet cell map of the same Budget statement — not a PDF scrape.
lags:               Same Budget 2026-27 lag as Card 1. next_release unknown.
disagrees_with:     Card 1 (tax). Card 3 (capital/debt). Card 4 multi-year non-tax row. Cards 9–11.
do_not:             Do not treat UT receipts on this statement as C5. Do not merge tax and non-tax. Same Union-missing-units, rank, forecast, and BE/RE/Actuals do-nots as Card 1. Do not present this card as reconstructed from PDF or HTML.
```

---

## Card 3 — Receipt Budget: Capital Receipts (non-debt and debt)

Binds: citation Card 3. Geography: **Frame A**.

```text
concept:            Union capital receipts as printed: Non-Debt Receipts (recoveries of loans and advances; miscellaneous capital receipts) and Debt Receipts / borrowings (market loans, switching, buyback, short-term / treasury bills, external loan, securities against small savings, State Provident Fund, other receipts as printed).
unit:               Rupees as labelled. Many debt lines are printed net of repayments.
population:         Government of India / Union. Not state borrowings.
reference_period:   Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. Not 1 February 2026.
producer_definition: Receipt Budget, 2026-2027 — III. Capital Receipts; Non Debt Receipts and Debt Receipts as printed (MoF Budget Division, fetch ctr.xlsx sheet ReceiptReport123; printed book cr.pdf). Tidy table: openpyxl cells of that sheet (ingest flag `sheet=ReceiptReport123`) — not reconstructed from cr.pdf. Workbook is ctr.xlsx, not cr.xlsx (404).
comparable_from:    The four columns in this file. Card 4 Annex-1 capital-receipt rows are a multi-year layout of related printed lines — still that annex, not this statement.
breaks:             BE vs RE vs Actuals. Net vs gross market borrowings: market loans (net) is not gross market borrowings. Abstract “Total Receipts” includes debt receipts — do not read it as revenue-only. Spreadsheet cell map of the same Budget statement — not a PDF scrape.
lags:               Same Budget 2026-27 lag. next_release unknown.
disagrees_with:     Card 7 outstanding liabilities (stock, not a year’s net debt receipts). Card 6 deficit (financing, not this receipt statement). Cards 10–11.
do_not:             Do not treat net debt receipts as gross borrowings. Do not drop debt receipts to invent a “collections without borrowing” total unless the producer prints that line. Do not use this card as the debt stock (Card 7). Do not chart as C5 state debt. Do not present this card as reconstructed from PDF or HTML.
```

---

## Card 4 — Annex-1 Trends in Receipts (run of years)

Binds: citation Card 4. Geography: **Frame A**.

```text
concept:            Multi-year Union receipts table as printed in Receipt Budget Annex-1, including revenue receipts, tax revenue net of States’ share, non-tax revenue, capital receipts (market borrowings and other printed lines), and printed deficit lines that sit in the same annex.
unit:               Rupees as labelled. Deficit lines are the producer’s printed lines, not a Prism blend.
population:         Government of India as published. Not states.
reference_period:   Financial-year column on the cell: Actual 2017-18 through 2024-25, RE 2025-26, BE 2026-27 as labelled. Name only the years in this file.
producer_definition: Receipt Budget, 2026-2027 — Annex-1 Trends in Receipts (MoF Budget Division, annex1.pdf). Tidy table reconstructed from PDF by PDF word-to-column (pdfplumber words → unique nearest year-column). Ingest flag: `pdfplumber words; assigned=…; ambiguous=0`. Producing-office annex1.xlsx / annex1.xls returned 404. There is no 2026-27 “Receipts and Expenditure of Government of India” book on the live Budget site (checked 18 September 2026); this annex is the Budget’s own multi-year receipts table.
comparable_from:    Columns the producer prints. Do not extend with RBI Handbook or IMF. Last two columns are RE and BE, not Actuals.
breaks:             Reconstructed from PDF, not a spreadsheet cell map — say so on the page methodology. Amounts are usable because each amount token mapped uniquely (`ambiguous=0`); ingest stopped rather than guessed. Line labels may wrap or truncate (e.g. `(Details in Annexure 2)` instead of the Tax Revenue head). Actual vs RE vs BE in one row: show the status, never one continuous Actuals line through 2026-27. Tax revenue here is net of States’ share — break vs Card 1 major-head (gross) tax. Deficit rows in this annex are not Card 6’s BAG deficit table.
lags:               Same Budget laying. next_release unknown. Reconstruction is not a later release.
disagrees_with:     Card 1 (gross tax heads). Card 6 BAG Deficit Statistics (same Budget, different table). Card 11 Actuals 2024-25. RBI compilations (rejected as silent substitute).
do_not:             Do not hide PDF reconstruction. Do not OCR. Do not guess an ambiguous amount into a year column. Do not treat a truncated label as a different series. Do not name years the file does not contain. Do not stitch RBI/IMF onto the right of the table. Do not chart RE/BE as Actuals. Do not treat printed deficit lines as a user-calculated residual. Do not use Annex-2 as this card (related analysis, different file).
```

---

## Card 5 — Expenditure Profile Statement 1

Binds: citation Card 5. Geography: **Frame A**.

```text
concept:            Union expenditure summary as printed: Central Expenditure (Establishment; Central Sector Schemes; Other Central Expenditure); Transfers (Centrally Sponsored Schemes; Finance Commission Transfers; Other Transfers); Total Expenditure through Budget; Resources of Public Enterprises — each split Revenue / Capital / Total where printed.
unit:               Rupees as labelled.
population:         Union budget heads. Transfers to States/UTs are Union outgo as printed — not state Finance Accounts.
reference_period:   Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. Not 1 February 2026.
producer_definition: Expenditure Profile 2026-2027 — Statement 1 Summary of Expenditure (MoF Budget Division, fetch stat1.xlsx sheet Statement1; printed book stat1.pdf). Tidy table: openpyxl cells of that sheet (ingest flag `sheet=Statement1`) — not reconstructed from stat1.pdf. BE 2026-27 Total sits one empty column after Capital in the workbook; that is the spreadsheet layout. “Total Expenditure through Budget and Resources of Public Enterprises” is a different printed total from “Total Expenditure through Budget”.
comparable_from:    The four year-status columns in this statement. BAG Expenditure of Government of India uses the same I–VI heads (bag6.pdf) — glance layout, not a licence to drop Statement 1.
breaks:             BE vs RE vs Actuals. Two printed totals (with / without public-enterprise resources): do not swap labels. Demand-by-demand Expenditure Budget Full is not this summary. Spreadsheet cell map of the same Budget statement — not a PDF scrape.
lags:               Same Budget 2026-27 lag. next_release unknown.
disagrees_with:     Card 9 AFS disbursements. Card 10 monthly expenditure vs BE. Card 11 Finance Accounts. Output-Outcome Framework (rejected; scheme outputs, not this statement).
do_not:             Do not use scheme MIS or Output-Outcome as this series. Do not ingest every Demand for Grants. Do not treat Transfers as C5. Do not chart the two printed totals as one. Do not issue waste/welfare verdicts. Do not present this card as reconstructed from PDF or HTML.
```

---

## Card 6 — Budget at a Glance: Deficit Statistics

Binds: citation Card 6. Geography: **Frame A**.

```text
concept:            Union deficit statistics as printed: Fiscal Deficit, Revenue Deficit, Effective Revenue Deficit, Primary Deficit, and Sources of Financing Fiscal Deficit. Parentheses are % of GDP as printed.
unit:               Rupees as labelled, and percent of GDP where the producer prints parentheses. GDP in BAG notes is the NSO advance estimate as cited by the Budget — not a C3 population series and not Card 11.
population:         Government of India as published.
reference_period:   Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027 on the statistics table. Chart years on page 2 run 2017-18 through 2026-27 BE — still BAG, and still BE/RE where labelled.
producer_definition: Budget at a Glance 2026-2027 — Deficit Statistics (MoF Budget Division, fetch budget_at_a_glance.xlsx sheet “Deficit Statistics”; printed book bag2.pdf). Tidy table: openpyxl cells of that sheet, including bilingual Actuals/BE/RE cells (ingest flag `sheet=Deficit Statistics`) — not reconstructed from bag2.pdf. Use the producer’s labels (FD, RD, ERD, PD) — not a Prism score. Do not ingest BAAG, Receipts, Expenditure of GOI, or Transfer of Resources from the same workbook. Linked bag2.xls returned 404 (18 September 2026).
comparable_from:    Columns on this table. Card 4 annex deficit lines are a different printed table. Card 10 monthly fiscal deficit is intra-year unaudited.
breaks:             BE vs RE vs Actuals. % of GDP uses the Budget’s cited GDP, which can differ from later NSO releases — show the BAG note, do not replace the denominator. Combined BAG page (bag1.pdf) is glance layout with numbered rows — not one “Union money” number. Spreadsheet cell map of the same Budget statement — not a PDF scrape.
lags:               PDF CreationDate 1 February 2026. next_release unknown.
disagrees_with:     Card 4 printed deficit lines. Card 8 FRBM prose percentages. Card 10 monthly fiscal deficit (producer note on temporal mismatch). Card 11 year-end Actuals.
do_not:             Do not grade FRBM targets from this table. Do not swap in a later GDP to “correct” the %. Do not blend monthly Card 10 into this year-status table. Do not chart bag1 rows as a homemade residual. Do not present this card as reconstructed from PDF or HTML.
```

---

## Card 7 — Statement of Liabilities of the Central Government

Binds: citation Card 7. Geography: **Frame A**.

```text
concept:            Outstanding liabilities of the Central Government as printed: Public Debt (Internal Debt, External Debt*); Other Liabilities; Total / Net Liabilities. Stock at year-end, not a year’s deficit.
unit:               Rupees as labelled. External debt footnote: book value / historical rate as printed.
population:         Central Government / Government of India. Not state debt.
reference_period:   Outstanding at year-end as labelled: end of 1950-51; 2021-2022 through 2024-25; Revised 2025-26; Budget 2026-27.
producer_definition: Receipt Budget, 2026-2027 — Part B: 1 (i) Statement of Liabilities of the Central Government (MoF Budget Division, annex91.pdf). Tidy table reconstructed from PDF by PDF word-to-column (pdfplumber words → unique nearest year-column). Ingest flag: `pdfplumber words; assigned=…; ambiguous=0`. Producing-office annex91.xlsx / annex91.xls returned 404. Nearby “Debt as defined in the FRBM Act” on BAG deficit charts is a different printed concept. Annex-9 narrative quotes other coverage notes (current exchange rate, EBRs, cash-balance adjustment) — not this statement’s merge.
comparable_from:    Columns on this statement. 1950-51 is a printed historical column, not a continuous market-debt series to splice into 2021–27 without the producer’s own notes.
breaks:             Reconstructed from PDF, not a spreadsheet cell map — say so on the page methodology. Amounts are usable because each amount token mapped uniquely (`ambiguous=0`); ingest stopped rather than guessed. Line labels may wrap or truncate (e.g. `Market Loans ( Annex.`). Two debt concepts: this Statement of Liabilities vs FRBM-defined debt. Revised vs Budget vs year-end Actuals columns. External debt valuation as footnoted — do not convert silently to current exchange rate.
lags:               Same Budget 2026-27 document. next_release unknown. Reconstruction is not a later release.
disagrees_with:     Card 6 / BAG FRBM debt charts. Card 8 FRBM statements. Card 3 net debt receipts (flow vs stock). Annex-9 narrative coverage.
do_not:             Do not hide PDF reconstruction. Do not OCR. Do not guess an ambiguous amount into a year column. Do not treat a truncated label as a different series. Do not merge FRBM-defined debt into this stock. Do not use assets/guarantees annexes (annex92–94) as this table. Do not rank or per-person. Do not present Union liabilities as general government including states.
```

---

## Card 8 — FRBM fiscal-policy statements

Binds: citation Card 8. Geography: **Frame A**.

```text
concept:            Statements of Fiscal Policy required under the FRBM Act, 2003, as bound for Budget 2026-27: Macro-Economic Framework Statement; Medium-term Fiscal Policy cum Fiscal Policy Strategy Statement; deviation statement as described in the Preface. This is the statutory packet, not the receipts/expenditure table of record.
unit:               Percent of GDP and other figures as printed in those statements. Not a Prism grade against 3% / 40% / 60% wording.
population:         Central Government as in the FRBM statements.
reference_period:   Budget 2026-27 / RE 2025-26 as discussed in the Preface (producer text includes Fiscal Deficit 4.4 per cent of GDP in RE 2025-26 and 4.3 per cent projected in FY 2026-27 — quote as producer text, not a score).
producer_definition: Combined PDF frbm1.pdf (title page February 2026). Homepage frbm2.pdf returned 404 on 18 September 2026; this combined file is the artifact that exists. This card is the statutory FRBM prose packet — Macro-Economic Framework Statement; Medium-term Fiscal Policy cum Fiscal Policy Strategy Statement; deviation statement as described in the Preface — not a reconstructable receipts/expenditure/deficit/debt grid. Ingest flag: `frbm1.pdf is statutory FRBM prose, not a reconstructable receipts/expenditure/deficit/debt grid; do not ingest page 9 Economic Performance at a Glance as this card`. `lineage_ok: no`. Do not print a reconstructed FRBM table.
comparable_from:    This Budget’s FRBM packet. Do not time-series FRBM prose against later NSO GDP without saying the statement’s own vintage.
breaks:             Not a table: cannot be reconstructed as this card’s collect/spend/deficit/debt grid. Cards 6–7 remain the Budget tables of record for deficit statistics and outstanding liabilities. What is missing is the FRBM statutory packet (macro framework, medium-term strategy, deviation statement, FRBM labels as printed) — not the collect/spend figures. Missing separate frbm2.pdf is a hole in the homepage links, not a second series. FRBM statutory wording vs printed RE/BE ratios: show both as printed; do not compute a pass/fail.
lags:               Presented February 2026 with the Budget. next_release unknown.
disagrees_with:     Card 6 BAG deficit statistics (tables vs policy statements). Card 7 liabilities vs FRBM-defined debt. Later CGA actuals (Cards 10–11).
do_not:             Do not tell Content Editor to print a fake FRBM receipts/expenditure/deficit/debt table. Do not ingest page 9 “Economic Performance at a Glance” as this card. Do not treat reconstruction of Cards 4, 7, 9, 10, 11 as a licence to grid this packet. Do not turn 3% / 40% / 60% into a Prism grade. Do not use this PDF as the receipts or expenditure series. Do not substitute Economic Survey narrative. Do not forecast from the medium-term statement as fact.
```

---

## Card 9 — Annual Financial Statement 2026-27

Binds: citation Card 9. Geography: **Frame A**.

```text
concept:            Annual Financial Statement of the Central Government for 2026-2027 as laid: Statement I Consolidated Fund (Revenue Account Receipts / Disbursements; Capital Account Receipts / Disbursements); Statement IA Charged disbursements; Statement II Contingency Fund; Statement III Public Account.
unit:               Rupees as labelled. Estimates are net of refunds and recoveries (Key to Budget Documents).
population:         Central Government / Consolidated Fund of India, Contingency Fund, Public Account. AFS “Receipts and Expenditure of Union Territories without Legislature” is still Union accounts, not C5.
reference_period:   Statement I columns: Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. Cover date 1 February 2026 is the laying date, not the financial year.
producer_definition: Annual Financial Statement of the Central Government for 2026-2027 (MoF Budget Division, allafs.pdf). Tidy table reconstructed from PDF by PDF word-to-column (pdfplumber words → unique nearest year-column). Two printed `2025-2026` columns are consumed left-to-right as BE then RE. Ingest flag: `pdfplumber words; assigned=…; ambiguous=0`. Companion allafs.xlsx returned 200 but Sheet1 headers still read Actuals 2022-2023 / BE 2024-2025 — not this vintage. Do not use the stale xlsx. Labels may include CID/Hindi font leftovers; English head names remain.
comparable_from:    PDF columns only. Do not use the stale xlsx.
breaks:             Reconstructed from PDF, not a spreadsheet cell map — say so on the page methodology. Amounts are usable because each amount token mapped uniquely (`ambiguous=0`); ingest stopped rather than guessed. Two `2025-2026` year tokens are BE then RE left-to-right, not two copies of one column. Font leftovers in labels are not a second series. BE vs RE vs Actuals. PDF vs xlsx disagreement: the xlsx is the wrong year — a named hole, not a second 2026-27 AFS.
lags:               Laid 1 February 2026. next_release unknown. Reconstruction is not a later release.
disagrees_with:     Cards 1–5 (Receipt Budget / Expenditure Profile vs constitutional AFS). Card 11 Finance Accounts Actuals. Stale allafs.xlsx.
do_not:             Do not hide PDF reconstruction. Do not OCR. Do not guess an ambiguous amount into a year column. Do not ingest allafs.xlsx as 2026-27. Do not treat UT-without-legislature AFS lines as C5. Do not blend Consolidated Fund with Public Account into one homemade total unless the producer prints it.
```

---

## Card 10 — CGA Monthly Accounts at a Glance (end July 2026)

Binds: citation Card 10. Geography: **Frame B**.

```text
concept:            Union Government Accounts at a Glance as at the end of July 2026: intra-year unaudited provisional actuals versus Budget Estimates 2026-2027, with % of Actuals to Budget Estimates (current and COPPY) as printed.
unit:               Rupees as labelled, and percent of BE where printed. @ marks unaudited provisional.
population:         Government of India / Union Government as printed. Not states, not districts.
reference_period:   April–July 2026 of FY 2026-2027 vs BE 2026-2027. Not the CGA news date 1 September 2026. DATA2627.htm LastSaved 29 July 2026 is file metadata — not the release date.
producer_definition: GOVERNMENT OF INDIA UNION GOVERNMENT ACCOUNTS AT A GLANCE AS AT THE END OF JULY 2026 (CGA, DATA2627.htm). Tidy table reconstructed from HTML by HTML table expand: stdlib html.parser; table 0; colspan/rowspan expanded. Ingest flag: `html table 0; colspan/rowspan expanded`. Not a spreadsheet cell map. Actuals are unaudited provisional (@). Fiscal deficit in the monthly file is not necessarily the year-end deficit (producer note on temporal mismatch).
comparable_from:    This month’s file. Prior months in FY 2026-27 exist as other retrieves — each month is its own snapshot, not a revision of July. Do not substitute Budget Actuals 2024-25 or Finance Accounts 2024-25 for this intra-year file.
breaks:             Reconstructed from Word-exported HTML, not a spreadsheet — say so on the page methodology. Monthly vs Budget year-status (Cards 1–7). Monthly vs Finance Accounts year-end (Card 11). August 2026 was on the month dropdown but was not the default latest snapshot on 18 September 2026 — do not silently take August.
lags:               News dated 1 September 2026 for upto July 2026. next_release unknown (ARC HTML had no dated month list). CGA GET without a browser-like UA may 404 — that is a retrieve hole, not a substitute file. Reconstruction is not a later release.
disagrees_with:     Card 6 year-status fiscal deficit. Card 11 2024-25 Actuals. Budget BE 2026-27 (the comparator, not the same observation).
do_not:             Do not hide HTML reconstruction. Do not guess merged cells. Do not annualise April–July as a year-end actual. Do not replace @ actuals with Budget Actuals. Do not use www.cga.gov.in (SSL mismatch). Do not invent next_release from an empty ARC page.
```

---

## Card 11 — Finance Accounts 2024-25 Statement No. 1

Binds: citation Card 11. Geography: **Frame C**.

```text
concept:            Union Finance Accounts 2024-2025 No. 1 Summary of Transactions: receipts and disbursements, Actuals, Consolidated Fund revenue receipt/disbursement heads as printed, with 2023-2024 comparatives.
unit:               Crores of rupees as printed.
population:         Union Government as printed. Annexure to Statement 1 (proceeds assigned to States) is Union tax assignment, not C5.
reference_period:   Financial year 2024-2025 (and 2023-2024 comparatives). PDF CreationDate 20 December 2025 is not FY 2025-26.
producer_definition: FINANCE ACCOUNTS, UNION GOVERNMENT; No. 1—SUMMARY OF TRANSACTIONS (CGA, Fin20242025Statement1.pdf). Tidy table reconstructed from PDF by PDF word-to-column (pdfplumber words, stream — not a ruled lattice). Ingest flag: `pdfplumber words; assigned=…; ambiguous=0`. Column-number header rows (`1, 2, 3`) are dropped; they are not crore amounts. Labels may include CID/Hindi font leftovers; English head names remain. CGA remains the accounts publisher; CAG certificate is a companion on the same CGA page.
comparable_from:    The two Actuals years on this statement. 2025-26 Finance Accounts were not on the CGA dropdown as of 18 September 2026.
breaks:             Reconstructed from PDF, not a spreadsheet cell map — say so on the page methodology. Amounts are usable because each amount token mapped uniquely (`ambiguous=0`); ingest stopped rather than guessed. Index rows are not values. Font leftovers in labels are not a second series. Annual Actuals vs Budget Actuals 2024-25 (Card 9 / Receipt Budget). vs monthly Card 10. Gross vs net tax (proceeds assigned to States in the annexure).
lags:               Accounts for 2024-25; next_release unknown (2025-26 FA not on dropdown). Reconstruction is not a later release.
disagrees_with:     Budget printed Actuals 2024-25 (Cards 1–9). Card 10 intra-year 2026. CAG site stub (rejected as table of record).
do_not:             Do not hide PDF reconstruction. Do not OCR. Do not guess an ambiguous amount into a year column. Do not treat 1–2 digit column-index rows as crores. Do not silent-substitute this file for monthly accounts or Budget BE. Do not recode the States annexure into C5. Do not treat CAG certificate as the transaction table.
```

---

## Do not chart (Content Editor)

A chart that does any of the following is a lie for this slice:

1. **BE, RE, and Actuals as one continuous collect or spend.**
2. **One “Union money” number** blending Cards 1–11.
3. **Gross tax as Centre’s net tax** (Card 1 vs Card 4 net of States’ share).
4. **Net debt receipts as gross borrowings** (Card 3).
5. **Card 5 two printed expenditure totals swapped.**
6. **Union as the country’s public money** (states, UTs, districts missing).
7. **Transfers / tax assignment / UT receipts heads as C5.**
8. **Statement of Liabilities merged with FRBM-defined debt.**
9. **FRBM 3% / 40% / 60% as a pass/fail grade.**
10. **Card 10 April–July annualised as year-end.**
11. **Card 11 Actuals 2024-25 drawn as Budget 2026-27.**
12. **Stale allafs.xlsx as AFS 2026-27.**
13. **Blank / dotted cells as zero** (including GST Compensation Cess BE 2026-27 where dotted).
14. **Per-person ranks; waste/welfare verdicts; scheme report cards; Economic Survey prose.**
15. **RBI / IMF / ratings as a longer run.**
16. **Forecasts from FRBM medium-term text as fact.**
17. **A PDF/HTML reconstruction presented as a spreadsheet cell map** — or Cards 1, 2, 3, 5, 6 presented as PDF scrapes.
18. **A reconstructed FRBM receipts/expenditure/deficit/debt grid from Card 8.**
19. **An ambiguous PDF amount guessed into a year column.**
20. **Finance Accounts column-index rows (`1, 2, 3`) drawn as crore amounts.**

Content Editor may show receipts, expenditure, deficit, and debt as the producer’s own heads; BE / RE / Actuals as separate status; Budget vs CGA monthly vs Finance Accounts as three records; Union beside named missing states, UTs, and districts. Content Editor must print the PDF/HTML reconstruction house rule in Methodology for Cards 4, 7, 9, 10, 11. Content Editor must not invent a Card 8 table.

---

## Holes (Trust Auditor)

Named holes. None require Charter Editor to shrink C3: the charter already parks states (C5), districts, scheme report cards, verdicts, Economic Survey prose, and per-person ranks.

| Hole | Where | What to show |
|------|--------|----------------|
| States, UTs, districts missing | Frames A–C | Union-only; not the country’s public money |
| BE vs RE vs Actuals | Cards 1–9 | Four (or labelled) vintages; never one line |
| Gross vs net tax | Cards 1 vs 4 / 11 annexure | Two concepts |
| Two expenditure totals | Card 5 | Print both labels |
| Two debt concepts | Cards 7 vs FRBM/BAG | Do not merge |
| frbm2.pdf 404 | Card 8 | Combined frbm1.pdf exists; do not invent the missing file |
| bag*.xls 404 | Cards 1, 5, 6 | Use named xlsx fetch / printed PDFs |
| PDF/HTML reconstruction vs spreadsheet | Cards 4, 7, 9, 11 PDF word-to-column; Card 10 HTML table expand; Cards 1–3, 5, 6 openpyxl | Page methodology must name PDF/HTML reconstruction and the parser class. `ambiguous=0` is a named method, not a substitute for the producer’s spreadsheet when one exists. Not a rewrite of Platform’s refresh contract as a ship |
| Unique amounts vs wrapped labels | Cards 4, 7, 9, 11 | Amounts uniquely mapped; labels may wrap/truncate (`(Details in Annexure 2)`; `Market Loans ( Annex.`) or carry CID/Hindi leftovers — name both |
| FA index rows | Card 11 | Drop `1, 2, 3` header rows; they are not crores |
| Card 8 not a reconstructable grid | Card 8 | `lineage_ok: no`. Do not print a fake FRBM table. Deficit/debt figures remain on Cards 6–7. Missing: statutory packet (macro framework, medium-term strategy, deviation statement, FRBM labels as printed) |
| allafs.xlsx wrong years | Card 9 | PDF reconstruction only; do not switch to the stale workbook |
| No Receipts-and-Expenditure book | Card 4 | Annex-1 years only |
| GST cess BE blank/dots | Card 1 / BAG | Hole, not 0 |
| Monthly ≠ year-end deficit | Cards 10 vs 6 / 11 | Temporal mismatch |
| next_release unknown | All cards | Do not invent Budget day or CGA month |
| CGA UA / www.cga.gov.in | Card 10 | prism-ingest UA may 404; SSL host is wrong |
| August 2026 on dropdown, July default | Card 10 | Cards lock July 2026 |
| FA 2025-26 not published | Card 11 | 2024-25 is the latest on the dropdown |
| RBI not used | Rejected | Budget/CGA exist; no silent substitute |

No stretch of definition was used to make a chart work. Caveat fields fit the existing schema; nothing to hand to Platform for a missing field.

---

## Handoff

Method notes updated 18 September 2026 for PDF/HTML transparency: Cards **1, 2, 3, 5, 6** are openpyxl cells of the producing-office xlsx. Cards **4, 7, 9, 11** are PDF word-to-column (`pdfplumber words; assigned=…; ambiguous=0`). Card **10** is HTML table expand (`html table 0; colspan/rowspan expanded`). Card **8** is still not a reconstructable grid (`lineage_ok: no`). Reconstruction with `ambiguous=0` is a named method, not a substitute for the producer’s spreadsheet when one exists, and not a Platform ship.

Next: **Content Editor** for the methodology block when a C3 page exists (quote the house rule; do not invent a Card 8 table). **Ingest Engineer** only if a retrieve is missing those lineage flags. Not Methodologist. Do not write a C3 vintage, start a citizen page, or move `citizen_pointer` / `preview` in this pass.
