# C8 method notes

Persona: Methodologist. Sleeve: **Prices and production + Delivery**. Slice: **C8**.

Citizen question: What does the official record say about foodgrain, and what does the public food system deliver?

These notes are for Pipeline to attach (`caveat_id` on each series) and for Content Editor to explain a number without a verdict. They do not recode geography, rewrite citation cards, or land files in `data/`.

Locked inputs: [`c8-citation-cards.md`](c8-citation-cards.md), [`c8-geography-frame.md`](c8-geography-frame.md). Charter block: [`topic-charters.md`](topic-charters.md) § C8.

**Family A and Family B are two chart families.** Farm production / procurement (A) must not share a chart with PDS / NFSA delivery (B). Do not invent a single “food security” series.

**Advance Estimates ≠ Final Estimates.** Cards A1 and A2 are different production rounds. Do not stitch them as one undifferentiated line.

**Bulletin page 8 production is a reprint.** DES Cards A1–A3 are the production source of record. DFPD Foodgrains Bulletin production page cites DES — do not use it as Card A.

**Allocation ≠ offtake ≠ procurement ≠ stock ≠ farm output.** Five different concepts. Chart them only with their own cards.

**Release / upload date is not the reference period.** Bulletin upload 16 September 2026 is not “August offtake complete.” Stock “as on 01.09.2026” is not offtake. AE “as on 27.05.2026” is not Final.

**Fetch host ≠ producer** on Card A6 (FCI statement on DFPD). Quote both.

**Rule (once):** a citizen caveat says what the number is, never what a ministry should do. `citizen_note` is citizen. `do_not` is desk.

| Card | Desk (`do_not`) | Citizen (`citizen_note`) |
|------|-----------------|--------------------------|
| A1 3rd AE | Do not treat as Final; do not use bulletin page 8 as record | All-India foodgrain production, 2025-26 advance |
| A2 FE 2024-25 | Do not stitch onto A1 as one line | All-India foodgrain production, sealed 2024-25 |
| A3 State APY | Do not expand short forms by eye; do not invent Lakshadweep | State/UT area, production, yield as in the workbook |
| A4 ASAG | Do not prefer over A1–A3 for latest vintage | Older glance book tables as printed |
| A5 Procurement | Do not chart as farm output or as offtake | State-wise procurement into the public system |
| A6 Stocks | Do not chart as offtake or production | Central-pool rice/wheat stocks as on the statement date |
| B1 Allocation/offtake | Do not treat allocation as lifting or as household consumption | NFSA/PMGKAY allocation and offtake as printed |
| B2 Coverage / FPS | Do not treat as hunger index or as offtake tonnes | NFSA persons/families and fair-price shops |
| B3 RC dashboard | Do not treat as offtake; prefer B1/B2 for a file cite | Live ration-card administrative counts |
| B4 Annual Report | Do not prefer over monthly bulletin for offtake/procurement | Companion department narrative |

---

## Card A1 — Third Advance Estimates 2025-26 (All India)

Binds: citation Card A1. Geography: **Frame A**.

```text
concept:            All-India production of foodgrains (and crop/season lines as printed) under Third Advance Estimates for crop year 2025-26, with historical run on the same PDF.
unit:               Lakh tonnes as labelled.
population:         All-India crop production estimates (DES). Not State rows. Not PDS offtake.
reference_period:   Crop year 2025-26 (3rd AE column); as-on date 27 May 2026 is not the crop year.
producer_definition: Time-Series-3rd-AE-2025-26-English.pdf (DES / DA&FW). Summer symbols (@ / $) for earlier years when Summer was clubbed with Rabi.
comparable_from:    Within this AE round’s time-series columns. Not interchangeable with Card A2 Final without a break.
breaks:             Advance ≠ Final. Do not use DFPD bulletin page 8 as this series.
lags:               next_release unknown; watch advance-estimates locator.
disagrees_with:     Card A2 (different round/year). Card A4 ASAG (older book). Bulletin reprint of DES production.
do_not:             Do not present as Final. Do not invent State rows. Do not merge with Family B. Do not use as a hunger index.
```

---

## Card A2 — Final Estimates 2024-25 (All India)

Binds: citation Card A2. Geography: **Frame A**.

```text
concept:            All-India production of foodgrains under Final Estimates for crop year 2024-25.
unit:               Lakh tonnes as labelled.
population:         Same DES all-India production family as A1, sealed Final for 2024-25.
reference_period:   Crop year 2024-25 (Final); as-on 20 November 2025.
producer_definition: Time-Series-FE-2024-25-English.pdf (DES / DA&FW).
comparable_from:    Within Final Estimates runs. Name the round when comparing to A1’s 2025-26 AE.
breaks:             FE vs AE. No 2025-26 Final on these cards yet.
lags:               Final for 2025-26 not on these cards; next_release unknown.
disagrees_with:     Card A1 (live AE for a later year). Card A4.
do_not:             Do not stitch AE and FE as one undifferentiated series. Same Family B and hunger do-nots as A1.
```

---

## Card A3 — State/UT Area, Production and Yield (Five-Years workbook)

Binds: citation Card A3. Geography: **Frame B**.

```text
concept:            Crop-wise and Total Foodgrains area, production, and yield by State/UT for 2021-22 through 2025-26 (2025-26 = 3rd AE vintage).
unit:               Area thousand ha; production thousand tonnes; yield kg/ha as labelled.
population:         DES State/UT crop statistics. Season = Kharif / Rabi / Summer as published.
reference_period:   Column year on the sheet; 2025-26 column is Advance, not Final.
producer_definition: Five-Years-2021-22-to-2025-263rd-AE.xlsx (DES / DA&FW).
comparable_from:    Within this workbook’s labelled years. Blank 2025-26 cells are holes, not zeros to fill.
breaks:             Short-form geography keys (J&K, DNH, Daman And Diu separate). Others is residual. Do not recode onto bulletin/FCI maps.
lags:               Aligned to 3rd AE package; next workbook with next AE/FE package.
disagrees_with:     Cards A1–A2 (all-India only PDFs). Frame D/E spellings.
do_not:             Do not expand short forms by eye. Do not invent Lakshadweep. Do not merge with procurement or offtake charts.
```

---

## Card A4 — ASAG 2024-25 foodgrain production tables

Binds: citation Card A4. Geography: **Frame C**.

```text
concept:            Foodgrain production tables in Agricultural Statistics at a Glance 2024-25 (season-wise and all-India / major-states panels as printed).
unit:               As labelled in each table.
population:         DES glance book; Major States panels are not a full UT set.
reference_period:   Years printed inside each table — not the November 2024 upload alone.
producer_definition: ASAG 2024-25 bilingual PDF (DES / DA&FW).
comparable_from:    Within ASAG tables. Prefer A1–A3 for latest AE/FE vintage.
breaks:             Chapter 3 procurement/stock reprints are not DES production — use A5/A6/B1 instead.
lags:               ASAG 2025-26 not on category page as of citation fetch.
disagrees_with:     Cards A1–A3 (newer production rounds).
do_not:             Do not prefer ASAG over A1–A3 for the live production question. Do not use ASAG procurement tables as primary.
```

---

## Card A5 — State-wise procurement (Foodgrains Bulletin)

Binds: citation Card A5. Geography: **Frame D**.

```text
concept:            State-wise procurement of rice, wheat, and coarsegrains into the public system (KMS / RMS marketing seasons as column headers).
unit:               LMT as labelled.
population:         Procurement by FCI and State agencies as the bulletin describes — not farm harvest (A1–A3) and not PDS offtake (B1).
reference_period:   Bulletin month August 2026; salient features cite procurement up to 31.08.2026 as printed.
producer_definition: DFPD Foodgrains Bulletin August 2026, procurement section (page 9 family).
comparable_from:    Within bulletin procurement tables / marketing seasons.
breaks:             Procurement ≠ production ≠ offtake. Spelling variants across pages stay as printed.
lags:               Monthly; next bulletin unknown (expect ~mid-month cadence).
disagrees_with:     Cards A1–A3 (output). Card B1 (lifting). Card A6 (stocks).
do_not:             Do not chart as farm output or as household delivery. Do not use bulletin page 8 production as DES of record.
```

---

## Card A6 — Central Pool stocks (FCI / DFPD host)

Binds: citation Card A6. Geography: **Frame E**.

```text
concept:            Total stocks of foodgrains in the Central Pool (FCI + State agencies) — rice and wheat by region/State as printed.
unit:               LMT as labelled.
population:         Central-pool inventory. Rice excludes unmilled paddy per producer footnotes. Buffer norms (w.e.f. 22.01.2015) are norms, not live stock.
reference_period:   As on 01.09.2026 (opening) on the standalone PDF; bulletin companion may use 31.08.2026 closing — name which.
producer_definition: FCI Coordination Division statement; fetch host DFPD. Quote both.
comparable_from:    Within stock statements / bulletin monthwise stock pages.
breaks:             Stock ≠ offtake ≠ procurement ≠ production. NE States aggregate ≠ a State. Stock-vs-norms companion PDF 404 — norms inside this PDF/bulletin only.
lags:               next_release unknown; watch DFPD Allocation “Current stock position” and next bulletin.
disagrees_with:     Card B1 offtake. Cards A1–A5.
do_not:             Do not present stock as delivery to households. Do not treat norms as current stock. Do not omit FCI as producer because DFPD hosts the file.
```

---

## Card B1 — Allocation and offtake (NFSA / PMGKAY)

Binds: citation Card B1. Geography: **Frame D**.

```text
concept:            Allocation and offtake of foodgrains under NFSA/PMGKAY and related scheme tables as printed in the Foodgrains Bulletin.
unit:               LMT as labelled.
population:         Central-pool allocation to States/schemes and lifting (offtake). Not household consumption from a survey.
reference_period:   Bulletin August 2026; footnotes for offtake upto July/August 2026 as printed.
producer_definition: Same August 2026 Foodgrains Bulletin, allocation & offtake section.
comparable_from:    Within allocation vs offtake columns for the same scheme/period. Do not equate them.
breaks:             Allocation ≠ offtake. Keep separate from Family A charts.
lags:               Monthly bulletin cadence; next_release unknown.
disagrees_with:     Card A5 procurement. Card A6 stocks. Card B2 coverage counts (persons, not tonnes).
do_not:             Do not treat allocation as lifting. Do not treat offtake as household consumption. Do not merge with production charts. Do not use as a hunger index.
```

---

## Card B2 — NFSA coverage and FPS counts

Binds: citation Card B2. Geography: **Frame D**.

```text
concept:            State-wise persons/families covered under NFSA; State-wise Fair Price Shops under TPDS.
unit:               Persons / families / shop counts as labelled.
population:         Administrative NFSA / TPDS coverage — not undernourishment and not offtake tonnes.
reference_period:   August 2026 bulletin tables.
producer_definition: Same Foodgrains Bulletin statements named on Card B2.
comparable_from:    Within these bulletin coverage/FPS tables.
breaks:             Coverage ≠ offtake. Portability transaction pages in the same bulletin are operational metrics — use only if the page cites them explicitly.
lags:               Same monthly bulletin as B1.
disagrees_with:     Card B1 (tonnes). FAO/UN hunger indices (rejected).
do_not:             Do not present as a hunger index. Do not convert coverage into offtake tonnes. Do not pull districts.
```

---

## Card B3 — NFSA Ration Card dashboard

Binds: citation Card B3. Geography: **Frame F**.

```text
concept:            Administrative ration-card and beneficiary activity counts on the National Food Security Portal public dashboard.
unit:               Counts as shown in UI (RC issued/deleted/transferred; beneficiary added/deleted/transferred).
population:         Ration-card administrative system. Not offtake tonnes. Not farm production.
reference_period:   “Data Availability Date” in the UI at fetch time — capture it; not a static PDF vintage.
producer_definition: nfsa.gov.in PublicRCDashboard.aspx (DFPD content; NIC host).
comparable_from:    Weak for time series without a captured dated export. Prefer B1/B2 bulletin tables for a citable file.
breaks:             Live HTML, no verified cell-mapped workbook on citation fetch. Annavitran distribution dashboard unreachable (named hole).
lags:               Continuous; no ARC date.
disagrees_with:     Cards B1–B2 (bulletin file series).
do_not:             Do not treat as offtake. Do not lead the page with an undated screenshot. Do not pull district views this iteration.
```

---

## Card B4 — DFPD Annual Report 2025-26

Binds: citation Card B4. Geography: national companion (annex stubs only if cited).

```text
concept:            Department annual report narrative and annex tables for 2025-26.
unit:               As labelled in each annex table used.
population:         DFPD programme reporting — companion, not the monthly series of record.
reference_period:   Annual Report 2025-26 (upload 26 February 2026 on Reports list).
producer_definition: Food AR 2025-26 English.pdf (DFPD).
comparable_from:    Prefer Cards A5 and B1 for procurement/offtake time series.
breaks:             Not a substitute monthly bulletin.
lags:               Annual Report 2026-27 not listed; next_release unknown.
disagrees_with:     Monthly bulletin cards where figures differ by vintage.
do_not:             Do not prefer over A5/B1 for the citizen offtake/procurement question.
```

---

## Named holes (method)

- **Districts** — parked.
- **Annavitran** — unreachable on citation fetch.
- **data.desagri.gov.in APY web** — unreachable; Frame B xlsx covers State APY.
- **FAO/UN hunger index / MSP-as-income** — charter rejects; no substitute cards.
- **Stock-vs-norms linked PDF** — 404; norms inside A6 / bulletin only.
- **desagri.gov.in TLS** — some clients fail certificate trust; Ingest needs an approved path.

---

## Handoff

Next: Platform Architect (refresh contract) when this slice becomes a product; then Ingest. Geography frames locked. Keep Family A and Family B on separate charts.
