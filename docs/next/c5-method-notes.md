# C5 method notes

Persona: Methodologist. Sleeve: **Money**. Slice: **C5**.

Citizen question: What do states and UTs collect and spend?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`.

Locked inputs: [`c5-citation-cards.md`](c5-citation-cards.md), [`c5-geography-frame.md`](c5-geography-frame.md). Charter block: [`topic-charters.md`](topic-charters.md) § C5.

**RBI State Finances and CAG CFRA are two records.** Cards 1–6 are RBI *State Finances: A Study of Budgets of 2025-26* (listing 23 January 2026). Card 7 is CAG CFRA / *Union and State Finances at a Glance* **2020-21**. Do not pick a winner. Do not invent a blended “state money” figure or a fiscal-virtue rank.

**Budget estimates, revised estimates, and accounts are different series.** Never chart them as one continuous collect or spend. RBI prints Accounts / RE / BE as separate columns or statement titles — keep them separate.

**Release date is not the reference period.** Listing date 23 January 2026 is not FY 2025-26 Accounts. Glance preface 6 September 2024 is not FY 2020-21.

**Own tax is not Centre transfers.** Card 2 (and Card 7 glance) keep own tax / own non-tax / share of Union taxes / grants as distinct printed lines. Do not treat grants or devolution as own tax.

**This slice is not C3.** Union Budget, CGA Union monthly accounts, and Union Finance Accounts stay on C3. Frame A is states and UTs with legislature; UTs without legislature and districts are missing.

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| Deficit / fiscal indicators | Do not collapse BE/RE/Accounts; do not grade “fiscal virtue” | State/UT deficit lines as RBI prints them |
| Revenue receipts | Do not fold grants into own tax | Own tax, own non-tax, and Centre transfers kept separate |
| Expenditure | Do not issue waste/welfare verdicts; do not merge with C3 | State/UT expenditure heads as printed |
| Capital receipts | Do not treat debt receipts as own tax or as revenue | Capital receipts including borrowings as printed |
| GFD financing | Do not rank financing mixes | How GFD is decomposed and financed, by year-status |
| Liabilities / borrowings | Do not merge with Union liabilities (C3) | Outstanding liabilities and market borrowings as printed |
| CAG CFRA glance | Do not stitch onto RBI 2025-26; do not use Union CFRA lines as C3 | Audited 2020-21 Union-and-state compilation; lagged |

---

## Card 1 — RBI major deficit / fiscal indicators

Binds: citation Card 1. Geography: **Frame A**.

```text
concept:            Major deficit and fiscal indicators of state governments / UTs as RBI prints them (revenue deficit/surplus, gross fiscal deficit/surplus, and related indicator lines on Statements 1–3 / Appendix Table 1).
unit:               Rupees as labelled (and ratios if the producer prints them). Blank is not zero.
population:         State Governments and UTs on Frame A. Not Union deficit (C3). Not districts. Not local bodies.
reference_period:   Column / statement label: Accounts, RE, or BE as printed in the 2025-26 Study. Not 23 January 2026.
producer_definition: RBI State Finances: A Study of Budgets of 2025-26 — Major Deficit Indicators / Major Fiscal Indicators (Appendix Table 1; Statements 1–3). Explanatory Note on Data Sources and Methodology on the same listing.
comparable_from:    Within this Study’s labelled Accounts / RE / BE columns. Do not stitch to Card 7’s 2020-21 audited figures as one line.
breaks:             BE vs RE vs Accounts are different vintages. Do not recode Frame A labels onto Frame B.
lags:               Study listed 23 January 2026; next edition unknown. Accounts lag BE.
disagrees_with:     Card 7 CAG CFRA fiscal parameters for 2020-21 (audited, older). C3 Union BAG deficit statistics (different government).
do_not:             Do not collapse BE/RE/Accounts. Do not rank states by “fiscal virtue”. Do not present as Union deficit. Do not hide missing UTs-without-legislature or parked districts.
```

---

## Card 2 — RBI revenue receipts (own tax, own non-tax, Centre transfers)

Binds: citation Card 2. Geography: **Frame A**.

```text
concept:            Revenue receipts of states/UTs: tax revenue; non-tax revenue; devolution and transfer of resources from the Centre — as distinct RBI statements/appendices.
unit:               Rupees as labelled.
population:         States and UTs with Legislature (Appendix I title) / State Governments and UTs as on Statements 14/15/17/33.
reference_period:   As labelled in the 2025-26 Study (Accounts / RE / BE). Not 23 January 2026.
producer_definition: Statements 14 Tax Revenue, 15 Non-Tax Revenue, 17 Devolution and Transfer of Resources from the Centre, 33 Revenue Receipts; Appendix I; Appendix Table 2. Statement 16 Loans from the Centre is loans, not tax.
comparable_from:    Within this Study. Own-tax lines are not comparable to Union tax (C3 Card 1) as one “India tax” series.
breaks:             Own tax / own non-tax / Centre transfers stay separate. BE vs RE vs Accounts.
lags:               Same Study lag as Card 1.
disagrees_with:     Card 7 glance (SOTR vs share of Union taxes vs grants-in-aid for 2020-21). C3 Union tax/non-tax.
do_not:             Do not treat Union grants or tax devolution as own tax. Do not treat Statement 16 loans as tax. Do not merge with C3. Same missing-units and rank do-nots as Card 1.
```

---

## Card 3 — RBI expenditure

Binds: citation Card 3. Geography: **Frame A**.

```text
concept:            State/UT expenditure as published: revenue and capital appendices; development / non-development and social-sector appendix tables; Statement 34 revenue expenditure.
unit:               Rupees as labelled.
population:         Frame A units. Not Union expenditure profile (C3). Not local bodies.
reference_period:   As labelled in the 2025-26 Study.
producer_definition: Statement 34; Statements 11–12; Appendices II and IV; Appendix Tables 3–7. Sector detail Statements 26–32, 35–37 only when the page cites that statement.
comparable_from:    Within this Study’s labelled vintages.
breaks:             Development / non-development are RBI heads, not a welfare verdict. BE vs RE vs Accounts.
lags:               Same Study lag as Card 1.
disagrees_with:     Card 7 CFRA expenditure for 2020-21. C3 Expenditure Profile.
do_not:             Do not issue waste/welfare verdicts. Do not merge with Union spend. Do not rank “best spender”. Do not hide missing UTs-without-legislature.
```

---

## Card 4 — RBI capital receipts

Binds: citation Card 4. Geography: **Frame A**.

```text
concept:            Capital receipts of States and Union Territories with Legislature as RBI publishes them (Appendix III), including borrowings / Centre loans where that statement is used.
unit:               Rupees as labelled.
population:         Frame A (Appendix III title).
reference_period:   As labelled in the 2025-26 Study.
producer_definition: Appendix III Capital Receipts; related Statement 16 Loans from the Centre.
comparable_from:    Within this Study. Distinct from Card 2 revenue receipts.
breaks:             Debt receipts are not revenue and not own tax. BE vs RE vs Accounts.
lags:               Same Study lag as Card 1.
disagrees_with:     Card 6 outstanding liabilities (stock vs flow). C3 Union capital receipts.
do_not:             Do not treat debt receipts as own tax or as revenue. Do not merge with Card 2. Do not present as Union capital receipts.
```

---

## Card 5 — RBI GFD decomposition and financing

Binds: citation Card 5. Geography: **Frame A**.

```text
concept:            Decomposition and financing of gross fiscal deficit by state, as RBI prints for Accounts / RE / BE statement titles.
unit:               Rupees as labelled; per-cent-of-total companions as printed.
population:         State Governments as labelled on Appendix Tables 8–10 / Statements 4–10.
reference_period:   2023-24 (Accounts), 2024-25 (RE), 2025-26 (BE) as in Statement 5–10 titles — three vintages, not one year.
producer_definition: Appendix Tables 8–10; Statements 4–10 in the 2025-26 Study.
comparable_from:    Within each year-status table. Do not stitch the three financing statements into one continuous series.
breaks:             Accounts / RE / BE financing tables are separate. Do not recode onto Frame B.
lags:               Same Study lag as Card 1.
disagrees_with:     Card 1 deficit levels (related but different table family). C3 Union GFD financing.
do_not:             Do not rank financing mixes as virtue. Do not collapse the three year-status statements. Do not present as Union financing.
```

---

## Card 6 — RBI outstanding liabilities and market borrowings

Binds: citation Card 6. Geography: **Frame A**.

```text
concept:            Outstanding liabilities composition and totals (including % of GSDP where published); state government market borrowings / loans as RBI prints them. Guarantees (Statement 28) are optional detail — not the same as debt stock.
unit:               Rupees as labelled; per cent of GSDP / of total where printed.
population:         State Governments and UTs as in Appendix Tables 11–12 titles.
reference_period:   As labelled in the 2025-26 Study.
producer_definition: Appendix Tables 11–13; Statements 18–22 (and 23–25, 28 only if cited).
comparable_from:    Within this Study. Not Union Statement of Liabilities (C3).
breaks:             Liabilities stock ≠ market borrowings flow ≠ guarantees. BE vs RE vs Accounts where columns exist.
lags:               Same Study lag as Card 1.
disagrees_with:     Card 4 capital receipts (flow). Card 7 CFRA public debt for 2020-21. C3 Central outstanding liabilities.
do_not:             Do not merge with Union liabilities. Do not treat guarantees as outstanding debt stock. Do not rank “most indebted” as a verdict chart.
```

---

## Card 7 — CAG CFRA / Union and State Finances at a Glance 2020-21

Binds: citation Card 7. Geography: **Frame B**.

```text
concept:            Audited Combined Finance and Revenue Accounts overview and volumes for 2020-21: own tax vs share of Union taxes vs grants-in-aid, expenditure, deficit/fiscal parameters, and public debt/liabilities as CAG prints them for states/UTs (and Union lines in the same product).
unit:               Rupees as labelled in the glance / volumes.
population:         Frame B — Union and states/UTs with legislature as the glance states. For C5, use state/UT tables; Union CFRA lines are not a substitute for C3.
reference_period:   Financial year 2020-21 (Accounts). Not the 6 September 2024 preface date.
producer_definition: Union and State Finances at a Glance 2020-21; CFRA Volumes I–III 2020-21 (CAG combined-accounts archive).
comparable_from:    Within 2020-21 CFRA. Not a continuation of RBI Study 2025-26 columns.
breaks:             Several years behind Frame A. CFRA after 2020-21 is a named hole on the live archive. Own tax vs grants stay separate.
lags:               Audited compilation lagged; next CFRA year unknown on the live page (fetch date on citation card).
disagrees_with:     Cards 1–6 RBI Study (different producer, later budget vintages, different compilation). C3 Budget/CGA Union series.
do_not:             Do not stitch onto RBI 2025-26 as one line. Do not fold grants into own tax. Do not use Union CFRA lines as C3 Budget BE or as C5 state money. Do not pretend later CFRA years exist on the archive.
```

---

## Named holes (method)

- **UTs without legislature** on Frame A — missing from Appendices I–IV; say so beside any “All States and UTs” aggregate.
- **CAG CFRA after 2020-21** — not on the live archive as of the citation-card fetch.
- **No monthly comparable state-accounts compilation** verified for C5 (CGA live releases checked are Union).
- **rbidocs fetch path** — listing is of record; automated GET to statement files may hit WAF — Ingest must use an approved path; do not invent cells.

---

## Handoff

Next: Platform Architect (refresh contract) when this slice becomes a product; then Ingest. Geography Steward frame is locked. Do not start citizen template work from these notes alone.
